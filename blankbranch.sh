#!/bin/bash


if [[ -n `git branch | grep "^[ \t*]\+$1$"` ]]; then
    echo "branch '$1' already exists."
    exit 5
fi

if [[ $# < 1 ]]; then
    echo "$0: you must specify the repository name"
    echo "usage: $0 <branchname>"
    exit 10
fi

read -p "Really create blank branch '$1' (y/n)? " -n 1
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi




git symbolic-ref HEAD refs/heads/$1
rm .git/index
git clean -fdx
echo "$1" > README.md
git add README.md
git commit -m 'Initial blank branch commit'
