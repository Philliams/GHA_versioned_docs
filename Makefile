release_name ?= dummy-release
tag ?= main-$$(date +%s)

run:
	uv run src/gha_versioned_docs/main.py

docs:
	mv ./documentation/build/.gitignore ./documentation/.gitignore
	rm -rf ./documentation/build/
	rm -rf ./artifacts/docs/
	mkdir ./documentation/build/
	mkdir ./artifacts/docs/
	uv run sphinx-build -b html ./documentation/source ./documentation/build
	mv ./documentation/.gitignore ./documentation/build/.gitignore
	cp -R ./documentation/build/ ./artifacts/docs

test:
	mv ./artifacts/test_report/.gitignore ./artifacts/.gitignore
	rm -rf ./artifacts/test_report/
	mkdir ./artifacts/test_report/
	mv ./artifacts/.gitignore ./artifacts/test_report/.gitignore
	uv run pytest --cov=src/ --cov-report=html:./artifacts/test_report

release:
	-rm ./release_artifacts.zip
	zip -r ./release_artifacts.zip ./artifacts
	gh release create ${tag} \
	./release_artifacts.zip \
	--title "My First Release" \
	--notes "This is the initial stable release." \
	--target main

sync:
	uv sync