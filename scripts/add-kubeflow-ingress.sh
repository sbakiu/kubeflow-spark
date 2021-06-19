#!/bin/bash
kubectl apply -f kubeflow-ui-ingress.yaml
# echo "$(minikube ip) kubeflow.myplatform.ai" | sudo tee -a /etc/hosts