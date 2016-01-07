#!/bin/bash

# Need sudo : bind over 0.0.0.0:80

PYTHONPATH="/usr/local/src/computor"
CHDIR="/usr/local/src/computor/srcs"
APP="web_engine:application"
BIND="0.0.0.0:80"

gunicorn ${APP} --chdir=${CHDIR} --pythonpath=${PYTHONPATH} --bind ${BIND} --daemon