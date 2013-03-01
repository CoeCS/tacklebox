#!/bin/bash

if [ $# -lt 1 ]; then
    echo "requires an argument"
    exit -1
fi


git checkout `git rev-list -n 1 --before="$@" master`
