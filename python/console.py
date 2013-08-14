"""
Drive the Motor Mix from the console, via RWMidi.
"""

from mm.motormix import Outputter
from mm.pager import driver

from java.lang import Thread
from rwmidi import RWMidi
from net.loadbang.midiwrapper import IReceiver

MM_INPUT   = 'MIDI Port MOTU'
MM_OUTPUT  = 'MIDI Port MOTU'
IAC_OUTPUT = 'IAC_2 Apple Inc.'

print "inputs"
for dev in RWMidi.getInputDevices():
    print "   {0}".format(dev)

print "outputs"
for dev in RWMidi.getOutputDevices():
    print "   {0}".format(dev)

class MMOutputter(Outputter):
    def __init__(self):
        Outputter.__init__(self)
        dev = RWMidi.getOutputDevice(MM_OUTPUT)
        print("MM Out:  {0}".format(dev))
        self.__out = dev.createOutput()

    def doCtrlOut(self, ctrl, val):
        self.__out.sendController(0, ctrl, val)

class IACOutputter:
    def __init__(self):
        dev = RWMidi.getOutputDevice(IAC_OUTPUT)
        print("IAC Out: {0}".format(dev))
        self.__out = dev.createOutput()

    def doCtrlOut(self, ctrl, val, chan):
        self.__out.sendController(chan - 1, ctrl, val)

    def doNoteOut(self, pitch, vel, chan):
        if vel > 0:
            self.__out.sendNoteOn(chan - 1, pitch, vel)
        else:
            self.__out.sendNoteOff(chan - 1, pitch, 0)

class CtrlIn(IReceiver):
    def __init__(self, driver):
        self.__driver = driver
        dev = RWMidi.getInputDevice(MM_INPUT)
        print("MM In:   {0}".format(dev))
        dev.createInput(self)

    def noteOnReceived(self, note):
        print note

    def noteOffReceived(self, note):
        print note

    def controllerChangeReceived(self, controller):
        self.__driver.ctrlIn(controller.getCC(), controller.getValue())

    def programChangeReceived(self, programChange):
        print programChange

    def sysexReceived(self, sysexMessage):
        print sysexMessage

_ = CtrlIn(driver(MMOutputter(), IACOutputter()))

import time

while True:
    Thread.sleep(5000)
    print(time.asctime(time.localtime(time.time())))
