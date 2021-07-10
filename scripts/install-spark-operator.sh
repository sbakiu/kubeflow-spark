#!/bin/bash
# https://github.com/GoogleCloudPlatform/spark-on-k8s-operator#installation
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm install my-release spark-operator/spark-operator --namespace kubeflow --create-namespace
