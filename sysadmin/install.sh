#!/bin/bash

set -x
COMPUTOR="https://github.com/JulienBalestra/computor.git"
WORK_DIR="/usr/local/src"

function packages
{
    apt-get update -qq
    apt-get install git build-essential python-pip python-dev
    if [ $? -ne 0 ]
    then
        echo "fail [apt-get install python-pip python-dev]"
        exit 2
    fi
    pip install gunicorn
    if [ $? -ne 0 ]
    then
        echo "fail [pip install gunicorn flask]"
        exit 2
    fi
}

function goto_cwd
{
    cd ${WORK_DIR}
    echo $(pwd -P) $(pwd -L)
}

function clone_project
{
    git clone ${COMPUTOR}
    if [ $? -ne 0 ]
    then
        echo "fail [git clone ${COMPUTOR}]"
        exit 3
    fi
    pip install -r computor/requirements.txt
    if [ $? -ne 0 ]
    then
        echo "fail [pip install -r computor/requirements.txt]"
        exit 3
    fi
}

packages
goto_cwd
clone_project
