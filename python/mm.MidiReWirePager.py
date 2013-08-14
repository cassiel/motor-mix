from mm.motormix import Outputter, StripDriver, MotorMixDriver
from mm.manifest import *

class MyOutputter(Outputter):
    def __init__(self):
        Outputter.__init__(self)

    def doCtrlOut(self, ctrl, val):
        maxObject.outletHigh(0, ['mm.ctrl', val, ctrl])            # Out in Max's ctlout order.

class IACOutputter:
    ''' Output as visible MIDI (controls or notes), any MIDI channel. '''
    def doCtrlOut(self, ctrl, val, chan):
        # Out in Max order:
        maxObject.outletHigh(0, ['iac.ctrl', val, ctrl, chan])

    def doNoteOut(self, pitch, vel, chan):
        maxObject.outletHigh(0, ['iac.note', pitch, vel, chan])

class MyStripDriver(StripDriver):
    def __init__(self, chan):
        StripDriver.__init__(self, MyOutputter(), chan)
        self.__iacOutputter = IACOutputter()

    def setPager(self, pageDriver):
        ''' Plug in a shared page-driving object. '''
        self.__pageDriver = pageDriver

    def doFader(self, pos):
        self.__pageDriver.doPageFader(self.getChannel(), pos)

    def doPress(self, idx, how):
        if idx == 0 and how == 1:
                # Top row, button-down is page select:
            self.__pageDriver.doSetPage(self.getChannel())

        # All buttons get transmitted as notes anyway:
        # Pitches from 0/C-2 onwards.
        pitch = self.getChannel()
        # MIDI channel from LED row (1 upwards):
        chan = idx + 1
        # Standard MIDI velocities of 64 and 0:
        vel = how * 64
        self.__iacOutputter.doNoteOut(pitch, vel, chan)

    def doTouch(self, how):
        # Cosmetic: flash all but the top LED when fader is touched:
        ch = self.getChannel()
        for i in range(1, NUM_STRIPLEDS): self.setLED(i, how)

strips = [MyStripDriver(i) for i in range(NUM_STRIPS)]

NUM_PAGES = 8

class MyMotorMixDriver(MotorMixDriver):
    ''' A page-oriented driver. '''
    def __init__(self, strips):
        MotorMixDriver.__init__(self, strips)
        for s in strips: s.setPager(self)
        self.__pages = [[0 for i in range(NUM_STRIPS)] for j in range(NUM_PAGES)]
        self.__iacOutputter = IACOutputter()
        self.__currentPage = 0

    def doSetPage(self, page):
        for i in range(NUM_STRIPS):
            strip = self.getStrip(i)
            strip.setFader(self.__pages[page][i])
            strip.setLED(0, DO_LED_OFF)

        self.__currentPage = page
        self.getStrip(page).setLED(0, DO_LED_ON)

    def doPageFader(self, chan, pos):
        self.__pages[self.__currentPage][chan] = pos
        self.__iacOutputter.doCtrlOut(chan, pos, self.__currentPage + 1)

myMMDriver = MyMotorMixDriver(strips)

def ctrl(ctl, val):
    myMMDriver.ctrlIn(ctl, val)

def led(chan, row, how):
    strips[chan].setLED(row, how)

def test(ch, val):
    strips[ch].setFader(val)

import time
from java.lang import System

print "Loaded Motor Mix at {t} on {vendor} {ver}/{a}".format(
    t=time.asctime(time.localtime(time.time())),
    vendor=System.getProperty("java.vendor"),
    ver=System.getProperty("java.version"),
    a=System.getProperty("os.arch"))
