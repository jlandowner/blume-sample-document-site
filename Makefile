.PHONY: image blume-image blume-run blume-validate run validate

IMAGE ?= k8s-platform-docs:local
BLUME_IMAGE ?= k8s-platform-docs-blume:local
PORT ?= 8080
BLUME_PORT ?= 4321
CONTAINER ?= docker

image:
	$(CONTAINER) build -f docker/Dockerfile -t $(IMAGE) .

blume-image:
	$(CONTAINER) build -f docker/Dockerfile.blume -t $(BLUME_IMAGE) .

blume-run: blume-image
	$(CONTAINER) run --rm -p $(BLUME_PORT):4321 $(BLUME_IMAGE)

blume-validate:
	$(CONTAINER) build --target builder -f docker/Dockerfile.blume -t $(BLUME_IMAGE)-validator .

run: image
	$(CONTAINER) run --rm -p $(PORT):8080 $(IMAGE)

validate:
	$(CONTAINER) build --target builder -f docker/Dockerfile -t $(IMAGE)-validator .
