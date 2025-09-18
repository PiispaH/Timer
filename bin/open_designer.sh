#!/usr/bin/bash

echo "Opening QT designer"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_DIR=$(dirname -- $SCRIPT_DIR)

$PROJECT_DIR/.venv/lib/python3.12/site-packages/PySide6/designer
