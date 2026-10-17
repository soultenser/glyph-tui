
.PHONY: clean lint

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +

lint:
	flake8 .
	mypy --strict .
