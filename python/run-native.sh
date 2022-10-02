#!/bin/zsh

### workon motor-mix

python console-native.py \
       --from_mm="USB.*Port 1" \
       --to_mm="USB.*Port 1" \
       --output="IAC.*1"

#python console-native.py \
#       --from_mm="iConnect.*DIN 1" \
#       --to_mm="iConnect.*DIN 1" \
#       --output="IAC.*1"
