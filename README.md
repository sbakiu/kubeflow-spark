# Kubeflow Spark


## Getting started
1. Start your local cluster
```
sh ./scripts/minikube-start.sh
```

2. Install Kubeflow Pipelines
```
sh ./scripts/install-kubeflow.sh
```

3. Install Spark Operator
```
sh ./scripts/install-spark-operator.sh
```

4. Create Spark Service Account
```
sh ./scripts/add-spark-sa.sh
```

5. Make Kubeflow UI reachable
5a. (Optional) Add Kubeflow UI Ingress
```
sh ./scripts/add-kubeflow-ingress.sh
```
5b. (Optional) Forward service port, e.g:
```
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8005:80
```

6. Create Kubeflow pipeline definition file
```
python kubeflow_pipeline.py
```

Now navigate
## To Do
1. Create Ingress for Kubeflow Pipelines UI
2. Install spark-operator
3. Create Spark SA with proper permissions
4. Create spark deployment, SparkPi