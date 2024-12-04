--- WINDOWS ---

$env:KUBECONFIG = "C:\Users\fredg\OneDrive\Bureau\ETS\LOG680\oxygencs-grp01-eq6\kubernetes\kubeconfig.yaml"

kubectl get pods 

kubectl get deployments

--- HVAC ---

kubectl apply -f kubernetes/hvac-configmap.yaml

kubectl apply -f kubernetes/hvac-secret.yaml

kubectl apply -f kubernetes/hvac-deployment.yaml

--- METRICS ---

kubectl apply -f kubernetes/metrics-secret.yaml

kubectl apply -f kubernetes/metrics-deployment.yaml

kubectl apply -f kubernetes/metrics-service.yaml

--- CRONJOB ---

kubectl apply -f kubernetes/cronjob.yaml

---

kubectl apply -f kubernetes/ingress.yaml
