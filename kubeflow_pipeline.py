import json
import time
import yaml

import kfp.components as comp
import kfp.dsl as dsl

SPARK_RUNNING_STATE = "RUNNING"
SPARK_COMPLETED_STATE = "COMPLETED"
SPARK_APPLICATION_KIND = "sparkapplications"


def get_spark_job_definition():
    """
    Read Spark Operator job manifest file and return the corresponding dictionary and
    add some randomness in the job name
    :return: dictionary defining the spark job
    """
    # Read manifest file
    with open("spark-job.yaml", "r") as stream:
        spark_job_manifest = yaml.safe_load(stream)

    # Add epoch time in the job name
    epoch = int(time.time())
    spark_job_manifest["metadata"]["name"] = spark_job_manifest["metadata"]["name"].format(epoch=epoch)

    return spark_job_manifest


def print_op(msg):
    """
    Op to print a message.
    """
    return dsl.ContainerOp(
        name="Print message.",
        image="alpine:3.6",
        command=["echo", msg],
    )


@dsl.graph_component  # Graph component decorator is used to annotate recursive functions
def graph_component_spark_app_status(input_from_op):
    k8s_get_op = comp.load_component_from_file("spark-get-component.yaml")
    check_spark_application_status_op = k8s_get_op(
        name=input_from_op,
        kind=SPARK_APPLICATION_KIND
    )
    # Remove cache
    check_spark_application_status_op.execution_options.caching_strategy.max_cache_staleness = "P0D"

    time.sleep(5)
    with dsl.Condition(check_spark_application_status_op.outputs["applicationstate"] != SPARK_COMPLETED_STATE):
        graph_component_spark_app_status(check_spark_application_status_op.outputs["name"])


@dsl.pipeline(
    name="Spark Operator job pipeline",
    description="Spark Operator job pipeline"
)
def spark_job_pipeline():
    spark_job_definition = get_spark_job_definition()

    k8s_apply_op = comp.load_component_from_file("spark-apply-component.yaml")
    spark_job_op = k8s_apply_op(object=json.dumps(spark_job_definition))
    name = spark_job_op.outputs["name"]

    # Remove cache for the apply operator
    spark_job_op.execution_options.caching_strategy.max_cache_staleness = "P0D"

    spark_application_status_op = graph_component_spark_app_status(spark_job_op.outputs["name"])
    spark_application_status_op.after(spark_job_op)

    print_message = print_op(name)
    print_message.after(spark_application_status_op)
    print_message.execution_options.caching_strategy.max_cache_staleness = "P0D"


if __name__ == "__main__":
    # Compile the pipeline
    import kfp.compiler as compiler
    pipeline_func = spark_job_pipeline
    pipeline_filename = pipeline_func.__name__ + ".yaml"
    compiler.Compiler().compile(pipeline_func, pipeline_filename)
