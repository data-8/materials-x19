#!/bin/bash
set -euo pipefail

IPYNB_PATH=${1}

cat /dev/stdin > $IPYNB_PATH

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Allow overrides
cp -r ${DIR}/../materials-grading-overrides/* ${DIR}/../materials/

ipython ${DIR}/grade.py ${IPYNB_PATH}