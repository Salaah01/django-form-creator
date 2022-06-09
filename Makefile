# Updates the requirements.txt
update-python-pkgs:
	pip-compile requirements.in

# Runs the tests with coverage and generates a report
test-coverage:
	coverage run runtests.py
	coverage report
	coverage html

# Runs linter
lint:
	flake8 form_creator

# Formats	the code
format:
	black form_creator
