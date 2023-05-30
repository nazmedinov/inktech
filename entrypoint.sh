#!/bin/bash

set -x

python -m pytest -v \
  -n=1 \
  --reruns 1 \

TESTS_EXIT_CODE=$?

TESTS_EXIT_CODE=$?

python utils/zip-allure-results.py -n tests/allure-results
curl -F "tests/allure-results.zip" http://allure-server:8081/allure-docker-service/upload

exit ${TESTS_EXIT_CODE}