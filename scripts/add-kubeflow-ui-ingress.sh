#!/bin/bash
kubectl apply -f ./scripts/kubeflow-ui-ingress.yaml
# echo "$(minikube ip) kubeflow.myplatform.ai" | sudo tee -a /etc/hosts