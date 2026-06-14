.PHONY: lint

lint:
	black src
	isort src