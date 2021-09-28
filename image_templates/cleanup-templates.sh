#!/bin/bash

# Removes any unused image template files

unused=$(comm -23 <(ls *.png) <(grep -h -R -P -o "(?<=move_image_relative\(\")[^\"]+" ..))

rm $unused
