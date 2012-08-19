#!/bin/bash

if [ $# -lt 1 ]; then
    echo "requires an argument"
    exit -1
fi

for repo in `find ./ -maxdepth 1 -mindepth 1 | xargs basename`
do
    cd $repo
    $@
    cd ..
done


