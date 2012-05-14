#!/bin/bash

if [ $# -lt 1 ]; then
    echo "requires an argument"
    exit -1
fi


for repo in `find ./ -maxdepth 1 -mindepth 1 -printf "%P\n"`
do
    cd $repo
    git checkout `git rev-list -n 1 --before="$@" master` 
    cd ..
done


