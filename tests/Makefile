# Makefile for running tests

# These variables can be overridden from the command-line
python = not-set
verbose = not-set
debug = not-set

ifneq ($(python), not-set)
    PYTHON=$(python)
else
    PYTHON=python
endif

# we need the python path to point one level up to access the package
# and executables
PYPATH=PYTHONPATH=..:

# common args for running tests
TEST_ARGS=-m unittest discover

ifeq ($(debug), not-set)
    ifeq ($(verbose), not-set)
        # summary only output
        TEST_ARGS+=--buffer
    else
        # show individual test summary
        TEST_ARGS+=--buffer --verbose
    endif
else
    # show detailed test output
    TEST_ARGS+=--verbose
endif

PYLINT=pylint
PYLINT_ARGS=-j 4 --rcfile=.pylintrc

all: test lint
test: utest stest

.PHONY: utest
utest: FORCE
	$(PYPATH) $(PYTHON) $(TEST_ARGS) --pattern 'test_unit_*.py'

.PHONY: stest
stest: FORCE
	$(PYPATH) $(PYTHON) $(TEST_ARGS) --pattern 'test_sys_*.py'

.PHONY: lint
lint: FORCE
	$(PYLINT) $(PYLINT_ARGS) *.py ../ghtools

FORCE:

