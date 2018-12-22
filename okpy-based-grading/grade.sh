#!/bin/bash
set -euxo pipefail
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
LAB_IPYNB="${1}"
LAB_DIR=$( dirname "${LAB_IPYNB}" )
LAB_FILE_NAME=$( basename ${LAB_IPYNB} )
LAB_BASE_NAME="${LAB_FILE_NAME%.*}"
TESTS_COUNT=$(ls ${LAB_DIR}/tests/q*.py | wc -l)

python3 ${DIR}/oknb.py ${LAB_IPYNB} ${LAB_IPYNB}.oknb score-file.txt --config ${LAB_DIR}/${LAB_BASE_NAME}.ok
jupyter nbconvert --to markdown --execute --allow-errors ${LAB_IPYNB}.oknb
python3 ${DIR}/parse_output.py ${LAB_DIR}/score-file.txt --max-score ${TESTS_COUNT}
