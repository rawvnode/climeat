#!/bin/sh

set -e

#activate virtual env
. /opt/pysetup/.venv/bin activate

# evaluating passed command:
exec "$@"