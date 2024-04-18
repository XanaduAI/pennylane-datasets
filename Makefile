.DEFAULT_GOAL=help
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


.PHONY: test
test:
	$(.POETRY) run pytest lib/tests $(args)
	

.PHONY: fmt
fmt:
	$(.POETRY) run ruff --fix lib
	$(.POETRY) run ruff format lib


.PHONY: lint
lint:
	$(.POETRY) run ruff check lib
	$(.POETRY) run ruff format --check lib


.PHONY: clean
clean:
	$(.POETRY) env remove --all
