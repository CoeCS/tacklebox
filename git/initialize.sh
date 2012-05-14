#!/bin/bash

if [[ $# < 1 ]]; then
    echo "$0: you must specify the repository name"
    echo "usage: $0 <repo>"
    exit 10
fi

mkdir $1
cd $1

git init
echo "# ${1}" > README.md

git add README.md

git commit -m "Initial Commit"

git remote add origin git@github.com:CoeCS/${1}.git

git push -u origin master
