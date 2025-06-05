# Loki Prometheus Grafana for Upload Sever


Build App:


docker build -t deepakk2212/upload-server:v3 .
docker push deepakk2212/upload-server:v3
kubectl apply -f deployment.yaml 



Then install promtail to forward logs to loki:

helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install promtail grafana/promtail \
  --namespace monitoring --create-namespace \
  --set "loki.serviceName=loki" \
  --set "loki.servicePort=3100"


Upload server:

kubectl port-forward svc/upload-server-service 8080:80







Loki Grafana Prometheus DevOps

Installing Loki:

kubectl create namespace monitoring
helm repo add grafana https://grafana.github.io/helm-charts 

helm search repo grafana 

helm install loki grafana/loki --namespace monitoring --version 6.29.0 --values manifests/loki-values.yaml 

kubectl port-forward --namespace monitoring svc/loki-gateway 3100:80 


![image alt](https://github.com/Dpk808/Grafana_on_UploadServer/blob/main/Grafana%20Screenshots/0.%20Installing%20Loki%20Grafana.png)


kubectl get pods -n monitoring
kubectl get svc -n monitoring




Installing Prometheus Grafana:

helm repo add grafana https://grafana.github.io/helm-charts
helm search repo prometheus-community
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --version 70.7.0 --values manifests/prometheus-values.yaml 
kubectl get svc -n monitoring
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80



![image alt](https://github.com/Dpk808/Grafana_on_UploadServer/blob/main/Grafana%20Screenshots/0.%20Installing%20Prometheus%20Grafana.png)





Pometheus port-forwarding:

kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090:9090




Loki Queries:


{app="upload-server"}
{app="upload-server"} |= "upload"

{app="upload-server"} != "health"



Get Log Counts (for alerting or dashboards):

count_over_time({app="upload-server"}[5m])
rate({app="upload-server"}[1m])








PromQL Queries for Kubernetes & upload-server
(Tested & Working)

1. CPU Usage of upload-server Pod
Measures the CPU usage rate over the past 5 minutes.

rate(container_cpu_usage_seconds_total{pod=~"upload-server.*", container!="POD"}[5m])

2. Memory Usage of upload-server Pod
Shows current memory usage in bytes.

container_memory_usage_bytes{pod=~"upload-server.*", container!="POD"}

3. Pod Uptime
Calculates how long the pod has been running.

time() - kube_pod_start_time{pod=~"upload-server.*"}

4. Pod Status (Running)
Checks if the pod is currently in the "Running" state.

kube_pod_status_phase{pod=~"upload-server.*", phase="Running"}

5. Disk I/O (Read + Write)

Shows the rate of disk reads and writes in bytes per second.


rate(container_fs_reads_bytes_total{pod=~"upload-server.*"}[5m]) + 
rate(container_fs_writes_bytes_total{pod=~"upload-server.*"}[5m])





File Upload WebApp:


![image alt](https://github.com/Dpk808/Grafana_on_UploadServer/blob/main/Grafana%20Screenshots/2.%20UploadServer.png)



Screenshots:

Prometheus metrics Dashboard:

![image alt](https://github.com/Dpk808/Grafana_on_UploadServer/blob/main/Grafana%20Screenshots/3.%20Prometheus_Dashboard.png) 



Loki logs Dashboard:


![image alt](https://github.com/Dpk808/Grafana_on_UploadServer/blob/main/Grafana%20Screenshots/3.%20Loki_Dashboard.png)


