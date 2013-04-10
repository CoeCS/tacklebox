#!/bin/bash

if [[ $# < 1 ]]; then
    echo "Argument required."
    echo "Usage: $0 [commit-activity | contributors | code-frequency | punch-card]"
    exit 10
fi

for repo in `ssh cscience -- 'cd var/345/ && ls -d */'`; do open https://github.com/CoeCS/${repo}graphs/${1}; done
