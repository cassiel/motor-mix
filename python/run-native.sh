#!/bin/zsh

### workon motor-mix

python console-native.py \
       --from_mm="USB.*1" \
       --to_mm="USB.*1" \
       --output=IAC
