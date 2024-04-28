
.PHONY: deps dev help test

# Self-documenting makefile method using the double-hash (##) for comments
help:  ## Show this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

deps:  ## Install dependencies.
	pip install -r requirements.txt

dev: deps  ## Install development dependencies.
	pip install -r requirements-dev.txt

test:  ## Run tests.
	pytest
