import mido
import time
import argparse
import re

def find_port_from_patt(ports, patt):
    matching = list(filter(lambda x: re.search(patt, x) is not None, ports))

    if len(matching) >= 1:
        return matching[0]
    else:
        return None



l = list(set(mido.get_output_names()))
l.sort()

for p in l:
    print("    {p}".format(p=p))

ap = argparse.ArgumentParser()
ap.add_argument("--from_mm", required=True, help="regex: MIDI port from Motor Mix")

args = ap.parse_args()

from_mm = find_port_from_patt(mido.get_input_names(), args.from_mm)

print("FOUND INPUT: {port}".format(port=from_mm))

def f(msg):
    print(msg)

with mido.open_input(from_mm, callback=f) as p:
    while True:
        print("TICK")
        time.sleep(1)
