.PHONY: image run validate test-mcp-search pages-deploy

IMAGE ?= k8s-platform-docs-blume:local
PORT ?= 4321
CONTAINER ?= docker
PAGES_IMAGE ?= sample-document-site-pages:local
CLOUDFLARE_PAGES_PROJECT ?= sample-document-site
CLOUDFLARE_PAGES_BRANCH ?= main

image:
	$(CONTAINER) build -f Dockerfile -t $(IMAGE) .

run: image
	$(CONTAINER) run --rm -p $(PORT):4321 $(IMAGE)

validate:
	$(CONTAINER) build --target validator -f Dockerfile -t $(IMAGE)-validator .

test-mcp-search:
	$(CONTAINER) build --target mcp-search-test -f Dockerfile -t $(IMAGE)-mcp-search-test .

pages-deploy:
	$(CONTAINER) build -f hack/pages/Dockerfile --target pages-deploy -t $(PAGES_IMAGE) .
	$(CONTAINER) run --rm \
		-e CLOUDFLARE_API_TOKEN \
		-e CLOUDFLARE_ACCOUNT_ID \
		-e CLOUDFLARE_PAGES_PROJECT=$(CLOUDFLARE_PAGES_PROJECT) \
		-e CLOUDFLARE_PAGES_BRANCH=$(CLOUDFLARE_PAGES_BRANCH) \
		-e BLUME_SITE_URL \
		$(PAGES_IMAGE)
