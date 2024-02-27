.DEFAULT_GOAL=help
.VENV:=.venv
.POETRY=python3.11 -m poetry

define HELP_BODY
Please use 'make [target]'. Available targets:
help                  Print this message

Development
setup                 Installs poetry app dependencies and environment.
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
	

.PHONY: fmt
fmt:
	$(.POETRY) run ruff --fix lib/
	$(.POETRY) run ruff format lib/


.PHONY: lint
lint:
	$(.POETRY) run ruff check lib/


.PHONY: clean
clean:
	$(.POETRY) env remove --all
