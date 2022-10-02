"""
Drive the Motor Mix from the console.
Python 3-native.
"""

import mido
import time
import argparse
import re
import logging

import mm.ports as mm_ports
from mm.motormix import Outputter
from mm.pager import driver

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.ERROR)

mm_ports.print_ports()

ap = argparse.ArgumentParser()
ap.add_argument("--from_mm", required=True, help="regex: MIDI port from Motor Mix")
ap.add_argument("--to_mm", required=True, help="regex: MIDI port to Motor Mix")
ap.add_argument("--output", required=True, help="regex: MIDI port for output")

args = ap.parse_args()

from_mm = mm_ports.find_input_port_matching(args.from_mm)
to_mm = mm_ports.find_output_port_matching(args.to_mm)
output = mm_ports.find_output_port_matching(args.output)

logging.info(f"FROM MM: {from_mm}")
logging.info(f"  TO MM: {to_mm}")
logging.info(f" OUTPUT: {output}")

# Some naming confusion: iac means "output" as above, to other application.

class MMOutputter(Outputter):
    def __init__(self, port):
        Outputter.__init__(self)
        self.__port = port

    def doCtrlOut(self, ctrl, val):
        #self.__out.sendController(0, ctrl, val)
        self.__port.send(mido.Message('control_change', control=ctrl, value=val))

class IACOutputter(Outputter):
    def __init__(self, port):
        Outputter.__init__(self)
        self.__port = port

    def doCtrlOut(self, ctrl, val, chan):
        #self.__out.sendController(chan - 1, ctrl, val)
        self.__port.send(mido.Message('control_change', channel=chan - 1, control=ctrl, value=val))

    def doNoteOut(self, pitch, vel, chan):
        if vel > 0:
            #self.__out.sendNoteOn(chan - 1, pitch, vel)
            self.__port.send(mido.Message('note_on', channel=chan - 1, note=pitch, velocity=64))
        else:
            #self.__out.sendNoteOff(chan - 1, pitch, 0)
            self.__port.send(mido.Message('note_off', channel=chan - 1, note=pitch))

def process_msg(driver, msg):
    logging.info(f"{msg.hex()}: {msg}")

    if msg.type == "control_change":
        driver.ctrlIn(msg.control, msg.value)

def test_sysex(port):
    # LCD display (initial 0xF0 is implicit):
    msg = mido.Message('sysex', data=[0x00, 0x01, 0x0F, 0x00, 0x11, 0x00])
    msg.data += [0x10]          # Text display (vs. rotary graphics).
    msg.data += [0x00]          # Address, column by column.
    msg.data += [ord(c) for c in "Project Cassiel"]
    # Final 0xF7 is implicit.
    port.send(msg)

def process():
    with mido.open_output(to_mm) as to_mm_port:
        with mido.open_output(output) as output_port:
            mm_outputter = MMOutputter(to_mm_port)
            iac_outputter = IACOutputter(output_port)
            d = driver(mm_outputter, iac_outputter)

            #test_sysex(to_mm_port)

            with mido.open_input(from_mm, callback=lambda msg: process_msg(d, msg)):
                while True:
                    logging.info("TICK")
                    time.sleep(5)

if from_mm and to_mm and output:
    process()
else:
    raise Exception("Not all ports identified")
