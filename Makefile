run:
	uv run src/gha_versioned_docs/main.py

docs:
	mv ./documentation/build/.gitignore ./documentation/.gitignore
	rm -rf ./documentation/build/
	mkdir ./documentation/build/
	mv ./documentation/.gitignore ./documentation/build/.gitignore
	uv run sphinx-build -b html ./documentation/source ./documentation/build

test:
	mv ./artifacts/test_report/.gitignore ./artifacts/.gitignore
	rm -rf ./artifacts/test_report/
	mkdir ./artifacts/test_report/
	mv ./artifacts/.gitignore ./artifacts/test_report/.gitignore
	uv run pytest --cov=src/ --cov-report=html:./artifacts/test_report

sync:
	uv sync