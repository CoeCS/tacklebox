#!/bin/bash

for repo in `find ./ -maxdepth 1 -mindepth 1 -printf "%P\n"`
do
    echo $repo
    cd $repo
    git checkout master
    git pull
    cd ..
done


