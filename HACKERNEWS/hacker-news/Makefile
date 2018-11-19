.PHONY: test dev

test:
	PYTHONPATH=.:./src:${PYTHONPATH} pytest --capture=fd --cov=src/ --cov-report html

dev:
	python src/server.py
