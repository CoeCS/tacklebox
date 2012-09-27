#!/bin/bash

for r in `cat repos.csv`; do
    git clone https://`git config github.oauth`:x-oauth-basic@github.com/CoeCS/${r}.git
done



