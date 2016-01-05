#!/bin/bash

set -x
COMPUTOR="https://github.com/JulienBalestra/computor.git"
WORK_DIR="/usr/local/src"

function check_ret
{
    if [ $1 -ne 0 ]
    then
        echo "fail [$2]"
        exit 2
    fi
}

function packages
{
    apt-get update -qq
    apt-get install python-pip python-dev
    check_ret $? "apt-get install python-pip python-dev"
    pip install gunicorn
    check_ret $? "pip install gunicorn flask"
}

function goto_cwd
{
    cd ${WORK_DIR}
    echo $(pwd -P) $(pwd -L)
}

function clone_project
{
    git clone ${COMPUTOR}
    check_ret $? "git clone ${COMPUTOR}"
    pip install -r computor/requirements.txt
}

packages
goto_cwd
clone_project
