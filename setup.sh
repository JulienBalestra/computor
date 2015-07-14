#!/bin/bash

function go_to_dirname
{
    echo "Go to working directory..."
    cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
    if [ $? -ne 0 ]
    then
        echo "go_to_dirname failed";
        exit 1
    fi
    echo "-> Current directory is" $(pwd)
}

function apt
{
    apt-get update -qq
    if [ $? -ne 0 ]
    then 
        echo "failed to update"
    fi    
    apt-get install -y python-pip python-dev nose gunicorn nginx
    if [ $? -ne 0 ]
    then 
        echo "failed to install packages"
    fi
    return $?
}

function main
{
    go_to_dirname
    apt
    return $?
}

main
exit $?