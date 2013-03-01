#!/bin/bash


if [ $# -lt 1 ]; then
    echo "requires an argument"
    exit -1
fi

#for repo in `find ./ -name .git | cut -d/ -f2`
for repo in `find ./ -name .git | sed "s/^.*\/\(.*\)\/.git/\1/"`
do
    echo "cd $repo"
    cd $repo
    echo $@
    $@
    echo "cd .."
    cd ..
    echo
done


