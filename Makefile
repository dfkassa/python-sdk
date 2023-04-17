# Python executable path
python_exec = python3.8

# Poetry executable path
pdm_exec = pdm

# Reformat code style
format:
	$(pdm_exec) run black dfkassa && \
	git add -u && \
	$(pdm_exec) run isort dfkassa && \
	git add -u && \
	$(pdm_exec) run autoflake \
		--ignore-init-module-imports \
		--remove-unused-variables \
		--recursive \
		--in-place dfkassa tests && \
	git add -u

# Run tests locally
test:
	$(pdm_exec) run pytest tests --cov=dfkassa --cov-report=html

# Tests command for CI with .coveragerc report
test-ci:
	$(pdm_exec) run coverage run --source=dfkassa -m pytest tests

# Serve coverage report
serve-cov:
	python -m http.server -d htmlcov -b 127.0.0.1

# Run mypy checking
check:
	$(pdm_exec) run mypy
