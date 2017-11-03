#!/bin/bash
set -e

if [ "$1" == "" ]; then
    exec /bin/bash
fi

exec "$@"
