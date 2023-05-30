#!/bin/bash

set -x

python -m pytest -v

exit ${TESTS_EXIT_CODE}