#!/bin/bash

# Need sudo

PYTHONPATH="/usr/local/src/computor"
CHDIR="/usr/local/src/computor/srcs"
APP="web_engine:application"
BIND="0.0.0.0:80"
LOG="/var/log/computor.log"
LOG_LEVEL="debug"

/usr/local/bin/gunicorn ${APP} --chdir ${CHDIR} --pythonpath ${PYTHONPATH} --bind ${BIND} --log-file ${LOG} --log-level ${LOG_LEVEL} --daemon