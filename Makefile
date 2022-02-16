test: clean-pyc
	pytest

coverage: clean-pyc
	coverage run --source unityparser -m pytest
	coverage report

cov: coverage

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-dist:
	find dist -name '*.tar.gz' -exec rm -f {} + || true
	find dist -name '*.whl' -exec rm -f {} + || true

checkout:
	git checkout main

deploy-loc:
	python setup.py build
	python setup.py install

lint:
	git fetch
	npx commitlint --from 'main'

check-gh-env:
ifndef GH_TOKEN
	$(error GH_TOKEN is undefined)
endif

check-pypi-env:
ifndef REPOSITORY_PASSWORD
	$(error REPOSITORY_PASSWORD, the API Token used to publish to Pypi, is undefined)
endif

release: REPOSITORY_USER := __token__
release: check-gh-env check-pypi-env clean-dist checkout lint
	python setup.py sdist bdist_wheel
	semantic-release publish
