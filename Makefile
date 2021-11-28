all: minikube kubeflow spark rbac port-forward

minikube:
		./scripts/start-minikube.sh

kubeflow:
		./scripts/install-kubeflow.sh

spark:
		./scripts/install-spark-operator.sh

rbac:
		./scripts/add-spark-rbac.sh

port-forward:
		kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8005:80
