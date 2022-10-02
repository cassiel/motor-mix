from mm.motormix import StripDriver, MotorMixDriver
from mm.manifest import *

class MyStripDriver(StripDriver):
    def __init__(self, mmOutputter, iacOutputter, chan):
        StripDriver.__init__(self, mmOutputter, chan)
        self.__iacOutputter = iacOutputter

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
        ### TODO: send notes to different virtual device (Bitwig can't distinguish controller types)
        ###self.__iacOutputter.doNoteOut(pitch, vel, chan)

    def doTouch(self, how):
        # Cosmetic: flash all but the top LED when fader is touched:
        ch = self.getChannel()
        for i in range(1, NUM_STRIPLEDS): self.setLED(i, how)

NUM_PAGES = 8

class MyMotorMixDriver(MotorMixDriver):
    ''' A page-oriented driver. '''
    def __init__(self, iacOutputter, strips):
        MotorMixDriver.__init__(self, strips)
        for s in strips: s.setPager(self)
        self.__pages = [[0 for i in range(NUM_STRIPS)] for j in range(NUM_PAGES)]
        self.__iacOutputter = iacOutputter
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

def driver(mmOutputter, iacOutputter):
    return MyMotorMixDriver(iacOutputter,
                            [MyStripDriver(mmOutputter, iacOutputter, i)
                             for i in range(NUM_STRIPS)])
