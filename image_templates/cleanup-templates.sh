#!/bin/bash

# Removes any unused image template files

unused=$(comm -23 <(ls *.png | sort) <(grep -h -R -P -o "(?<=move_image_relative\(\")[^\"]+" .. | sort))

if [ -n "$unused" ];then
    rm $unused
fi
