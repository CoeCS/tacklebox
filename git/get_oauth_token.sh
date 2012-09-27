#!/bin/bash

read -p "Enter GitHub Username: " GITHUB_USERNAME


curl -u $GITHUB_USERNAME -i -d "{\"scopes\" : [\"repo\"], \"note\" : \"Shell Auth - $(hostname)\"}" https://api.github.com/authorizations
