#!/bin/bash
minikube start  --memory 8192 --cpus 4 --driver=docker --kubernetes-version=v1.22.9
minikube addons enable metrics-server
#minikube addons enable registry
#minikube addons enable ingress