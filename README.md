# Kubeflow Spark
Orchestrate Spark Jobs using Kubeflow, a modern Machine Learning orchestration framework.

## Requirements
1. Kubernetes cluster (1.17+)
2. Kubeflow pipelines (1.6.0+)
3. Spark Operator (1.1.0+)
4. Python (3.6+)
5. kubectl
6. helm3

## Getting started
1. Start your local cluster
```
./scripts/start-minikube.sh
```

2. Install Kubeflow Pipelines
```
./scripts/install-kubeflow.sh
```

3. Install Spark Operator
```
./scripts/install-spark-operator.sh
```

4. Create Spark Service Account and add permissions
```
./scripts/add-spark-rbac.sh
```

5. Make Kubeflow UI reachable

* a. (Optional) Add Kubeflow UI Ingress
```
./scripts/add-kubeflow-ui-ingress.sh
``` 
* b. (Optional) Forward service port, e.g:
```
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8005:80
```

6. Create Kubeflow pipeline definition file
```
python kubeflow_pipeline.py
```

7. Navigate to the Pipelines UI and upload the newly created pipeline from file `spark_job_pipeline.yaml`


8. Trigger a pipeline run. Make sure to set `spark-sa` as Service Account for the execution.


9. Enjoy your orchestrated Spark job execution!
