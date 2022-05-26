#!/bin/bash
minikube start  --memory 8192 --cpus 4 --insecure-registry "10.0.0.0/24" --driver=docker --kubernetes-version=v1.20.12
minikube addons enable metrics-server
minikube addons enable registry
#minikube addons enable ingress