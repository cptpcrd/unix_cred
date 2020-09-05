#!/bin/bash
cd "$(dirname -- "$(dirname -- "$(readlink -f "$0")")")"

for cmd in flake8 isort mypy pylint pytype; do
    if [[ ! -x "$(which "$cmd")" ]]; then
        echo "Could not find $cmd. Please make sure that flake8, isort, mypy, pylint, and pytype are all installed."
        exit 1
    fi
done

flake8 unix_cred tests && isort --check unix_cred tests && mypy --strict -p unix_cred -p tests && pytype unix_cred tests && pylint unix_cred tests
