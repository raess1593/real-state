.PHONY: lint

lint:
	black src main.py
	isort src main.py