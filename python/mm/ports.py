"""
Port handling.
"""

import mido
import re

def print_port_list(L):
    L = list(set(L))
    L.sort()

    for p in L:
        print("    {p}".format(p=p))

def print_ports():
    print("INPUTS")
    print_port_list(mido.get_input_names())
    print("OUTPUTS")
    print_port_list(mido.get_output_names())

def find_port_from_patt(ports, patt):
    matching = list(filter(lambda x: re.search(patt, x) is not None, ports))

    if len(matching) >= 1:
        return matching[0]
    else:
        return None

def find_input_port_matching(patt):
    return find_port_from_patt(mido.get_input_names(), patt)

def find_output_port_matching(patt):
    return find_port_from_patt(mido.get_output_names(), patt)
