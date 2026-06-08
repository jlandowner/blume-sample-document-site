.PHONY: image run validate clean

IMAGE ?= k8s-platform-docs:local
PORT ?= 8080
CONTAINER ?= docker

image:
	$(CONTAINER) build -f docker/Dockerfile -t $(IMAGE) .

run: image
	$(CONTAINER) run --rm -p $(PORT):8080 $(IMAGE)

validate:
	$(CONTAINER) build --target builder -f docker/Dockerfile -t $(IMAGE)-validator .

clean:
	rm -rf site ai
