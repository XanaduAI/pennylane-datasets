.DEFAULT_GOAL=help
.VENV:=.venv
.POETRY=python3.11 -m poetry

define HELP_BODY
Please use 'make [target]'. Available targets:
help                  Print this message

Development
setup                 Installs poetry app dependencies and environment.
test                  Run tests, use with args=[...] to pass arguments to pytest
fmt                   Apply code formatters.
lint                  Run code linters.
clean                 Remove all build artifacts.

endef

.PHONY: help
help:
	@: $(info $(HELP_BODY))


.PHONY: setup
setup:
	$(.POETRY) install --with dev


args=tests/
.PHONY: test
test:
	$(.POETRY) run pytest $(args)
	

.PHONY: fmt
fmt:
	$(.POETRY) run ruff --fix lib/ tests/
	$(.POETRY) run ruff format lib/ tests/


.PHONY: lint
lint:
	$(.POETRY) run ruff check lib/ tests/


.PHONY: clean
clean:
	$(.POETRY) env remove --all
