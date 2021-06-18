import kfp.dsl as dsl
import json
import kfp.components as comp
import time

SPARK_RUNNING_STATE = "RUNNING"
SPARK_COMPLETED_STATE = "COMPLETED"
SPARK_APPLICATION_KIND = "sparkapplications"
NAMESPACE = "kubeflow"


def print_op(msg):
    """Print a message."""
    return dsl.ContainerOp(
        name='Print',
        image='alpine:3.6',
        command=['echo', msg],
    )


@dsl.graph_component
def graph_component_spark_app_status(input_from_op):
    k8s_get_op = comp.load_component_from_file("spark_get_component.yaml")
    check_spark_application_status_op = k8s_get_op(
        name=input_from_op,
        kind=SPARK_APPLICATION_KIND,
        namespace=NAMESPACE
    )
    check_spark_application_status_op.execution_options.caching_strategy.max_cache_staleness = "P0D"
    time.sleep(5)
    with dsl.Condition(check_spark_application_status_op.outputs["applicationstate"] == SPARK_RUNNING_STATE):
        graph_component_spark_app_status(check_spark_application_status_op.outputs["name"])


@dsl.pipeline(
    name='Submit Spark job pipeline',
    description='Submit Spark job pipeline'
)
def submit_spark_job_pipeline():
    k8s_apply_op = comp.load_component_from_file("component.yaml")

    with open("spark-job.json", "rb") as f:
        json_object = json.load(f)

    spark_job_op = k8s_apply_op(object=json.dumps(json_object))
    name = spark_job_op.outputs["name"]
    kind = spark_job_op.outputs["kind"]
    object_spark_apply = spark_job_op.outputs["object"]
    namespace = "kubeflow"

    spark_job_op.execution_options.caching_strategy.max_cache_staleness = "P0D"
    print_op(spark_job_op.outputs["object"]).after(spark_job_op)

    graph_spark_app_status_op = graph_component_spark_app_status(spark_job_op.outputs["name"])
    graph_spark_app_status_op.after(spark_job_op)
    # graph_spark_app_status_op.execution_options.caching_strategy.max_cache_staleness = "P0D"


if __name__ == "__main__":
    #Compile the pipeline
    import kfp.compiler as compiler
    pipeline_func = submit_spark_job_pipeline
    pipeline_filename = pipeline_func.__name__ + '.yaml'
    compiler.Compiler().compile(pipeline_func, pipeline_filename)
