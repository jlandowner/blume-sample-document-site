.PHONY: image run validate test-mcp-search

IMAGE ?= k8s-platform-docs-blume:local
PORT ?= 4321
CONTAINER ?= docker

image:
	$(CONTAINER) build -f Dockerfile -t $(IMAGE) .

run: image
	$(CONTAINER) run --rm -p $(PORT):4321 $(IMAGE)

validate:
	$(CONTAINER) build --target validator -f Dockerfile -t $(IMAGE)-validator .

test-mcp-search:
	$(CONTAINER) build --target mcp-search-test -f Dockerfile -t $(IMAGE)-mcp-search-test .
