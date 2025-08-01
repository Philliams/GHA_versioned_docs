release_name ?= dummy-release
tag ?= main-$$(date +%s)

run:
	uv run src/gha_versioned_docs/main.py

test:
	uv run pytest --cov=src/ --cov-report=html:./tmp/test_report

api_docs:
	uv run pdoc ./src/gha_versioned_docs/ -o ./tmp/api_docs/

release: preprocess_docs
	-rm ./release_artifacts.zip
	cd ./documentation/versioned_docs && zip -r ../../release_artifacts_${tag}.zip ./
	gh release create ${tag} \
	./release_artifacts_${tag}.zip \
	--title "Release ${tag}" \
	--notes "This is an autogenerated release" \
	--target main

clean:
	rm -rf ./documentation/versioned_docs/_static/
	mkdir ./documentation/versioned_docs/_static/
	echo "*\n!.gitignore" > ./documentation/versioned_docs/_static/.gitignore

	rm -rf ./documentation/versioned_docs/rst/
	mkdir ./documentation/versioned_docs/rst/
	echo "*\n!.gitignore" > ./documentation/versioned_docs/rst/.gitignore

	rm -rf ./tmp
	mkdir ./tmp
	echo "*\n!.gitignore" > ./tmp/.gitignore

	rm -rf ./documentation/combined_docs/build/
	mkdir ./documentation/combined_docs/build/
	echo "*\n!.gitignore" > ./documentation/combined_docs/build/.gitignore

preprocess_docs: clean test api_docs
	uv run src/gha_versioned_docs/preprocess_docs.py

combined_docs:
	-rm -rf ./download
	-mkdir ./download
	echo "*\n!.gitignore" > ./download/.gitignore
	gh release list --json tagName --exclude-drafts --jq '.[].tagName' \
	| xargs -ITAG gh release download -D ./download/ TAG
	uv run src/gha_versioned_docs/script.py
	uv run sphinx-build -b html \
	./documentation/combined_docs/source \
	./documentation/combined_docs/build

sync:
	uv sync