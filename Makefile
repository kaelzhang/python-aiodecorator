files = aiodecorator test *.py
test_files = *
# test_target = exception_handler

test:
	pytest -s -v test/test_$(test_files).py --doctest-modules --cov aiodecorator --cov-config=.coveragerc --cov-report term-missing

test-ci:
	pytest -s -v test/test_$(test_files).py --doctest-modules --cov aiodecorator --cov-config=.coveragerc --cov-report=xml

lint:
	@echo "\033[1m>> Running ruff... <<\033[0m"
	@ruff check $(files)
	@echo "\033[1m>> Running mypy... <<\033[0m"
	@mypy $(files)

fix:
	ruff check --fix $(files)

install:
	pip install -U .[dev]

report:
	codecov

clean:
	rm -rf dist build
	rm -rf aiodecorator.egg-info/
	rm -rf aiodecorator/aiodecorator.egg-info/

build:
	make clean
	@python -m build --sdist --wheel

build-doc:
	sphinx-build -b html docs build_docs

publish:
	make build
	twine upload --config-file ~/.pypirc -r pypi dist/*

.PHONY: test build report install
