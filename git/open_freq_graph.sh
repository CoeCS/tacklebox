#!/bin/bash


for repo in `ssh cscience -- 'cd var/345/ && ls -d */'`; do open https://github.com/CoeCS/${repo}graphs/code-frequency; done
