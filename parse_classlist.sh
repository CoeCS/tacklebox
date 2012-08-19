#!/bin/bash

sed -n 's/.*>\([a-zA-Z ]*,[a-zA-Z ]*\)<.*>\([a-zA-Z]*\@coe.edu\).*<.*/\2;\1/p' $@
