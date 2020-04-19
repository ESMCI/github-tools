# Makefile for running tests on the python code here

# These variables can be overridden from the command-line
python = not-set
verbose = not-set
debug = not-set

ifneq ($(python), not-set)
    PYTHON=$(python)
else
    PYTHON=python
endif

ifneq ($(debug), not-set)
    TEST_ARGS+=--debug
endif
ifneq ($(verbose), not-set)
    TEST_ARGS+=--verbose
endif

PYLINT=pylint
PYLINT_ARGS=-j 4 --rcfile=ghtools/.pylintrc
PYLINT_SRC = \
	ghtools

.PHONY: test
test: FORCE
	$(PYTHON) ./run_tests $(TEST_ARGS)

.PHONY: lint
lint: FORCE
	$(PYLINT) $(PYLINT_ARGS) $(PYLINT_SRC)

.PHONY: clean
clean: FORCE
	rm -rf ghtools/__pycache__/
	find . -name '*.pyc' -exec rm {} \;

FORCE:

