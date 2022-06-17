# Updates the requirements.txt
update-python-pkgs:
	pip-compile requirements.in


# Runs the tests with coverage and generates a report
test-coverage:
	coverage run runtests.py
	coverage report
	coverage html

define update_readme_cov =
	bash update_readme_cov.sh
endef

update-readme-cov:
	$(update_readme_cov)

# Runs linter
lint:
	python -m flake8 --exclude=migrations form_creator/.

# Formats	the code
format:
	black form_creator

# Builds the package
build:
	python setup.py sdist bdist_wheel

# Uploads the package to PyPI test
upload-test:
	python -m twine upload --repository testpypi dist/*

# Uploads the package to PyPI
upload:
	python -m twine upload dist/*