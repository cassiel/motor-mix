"""
Drive the Motor Mix from the console.
Python 3-native.
"""

import mido
import time
import argparse
import re

import mm.ports as mm_ports

mm_ports.print_ports()

ap = argparse.ArgumentParser()
ap.add_argument("--from_mm", required=True, help="regex: MIDI port from Motor Mix")
ap.add_argument("--to_mm", required=True, help="regex: MIDI port to Motor Mix")
ap.add_argument("--output", required=True, help="regex: MIDI port for output")

args = ap.parse_args()

from_mm = mm_ports.find_input_port_matching(args.from_mm)
to_mm = mm_ports.find_output_port_matching(args.to_mm)
output = mm_ports.find_output_port_matching(args.output)

print("FROM MM: {p}".format(p=from_mm))
print("  TO MM: {p}".format(p=to_mm))
print(" OUTPUT: {p}".format(p=output))

if from_mm and to_mm and output:
    print("OK")
else:
    raise Exception("Not all ports identified")
