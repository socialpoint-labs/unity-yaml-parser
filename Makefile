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
	find dist -name '*.tar.gz' -exec rm -f {} +
	find dist -name '*.whl' -exec rm -f {} +

deploy-loc:
	python setup.py build
	python setup.py install

update-changelog:
	npx conventional-changelog -p angular -k config/package.json -i CHANGELOG.md -s

release: clean-dist
	python setup.py sdist bdist_wheel
	twine upload dist/*
