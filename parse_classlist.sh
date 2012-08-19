#!/bin/bash

sed -n 's/.*>\([a-zA-Z ]*,[a-zA-Z ]*\)<.*>\([a-zA-Z]*\@coe.edu\).*<.*/\1;\2/p' $@
