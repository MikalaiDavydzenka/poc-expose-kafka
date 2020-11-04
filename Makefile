NAMESPACE = expose-kafka
RELEASE_NAME = expose-kafka
CHART = bitnami/kafka

install:
	kubectl create namespace $(NAMESPACE) || true
	helm install $(RELEASE_NAME) $(CHART) -f values.yaml --namespace $(NAMESPACE)

update:
	helm upgrade $(RELEASE_NAME) $(CHART) -f values.yaml --namespace $(NAMESPACE)

uninstall:
	helm uninstall $(RELEASE_NAME) --namespace $(NAMESPACE)

dry:
	helm install $(RELEASE_NAME) $(CHART) -f values.yaml --namespace $(NAMESPACE) --dry-run --debug
