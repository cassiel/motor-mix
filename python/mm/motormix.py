'''
MotorMix driver.
$Id: motormix.py,v 060cfbaa59e7 2011/02/04 12:06:46 nick $

Controller overview (transmitted):
        15 (0x0F)       - selection of a different block of buttons;
                          0 to 7 are the main channels, 8 is left side,
                          9 is right side, 10 is left minibuttons,
                          11 is right minibuttons

        47 (0x2F)       - 0x40 to 0x4n is ON, 0x00 to 0x0n is OFF for
                          switch inside block identified by "n". 0x40
                          and 0x00 themselves are touch on/touch off
                          sensing from the faders

        0+n (0x0n)      - fader 0..n MSB
        32+n (0x2n)     - fader 0..n LSB (two bits)
                          MSB first

Controller overview (received):
        0+n (0x0n)      - fader motor 0..n MSB
        32+n (0x2n)     - fader motor 0..n LSB (two bits)
                          MSB first

        12 (0x0C)       - selection of light block

        44 (0x2C)       - 0x40 to 0x4n is ON, 0x50 to 0x5n is BLINK,
                          0x00 to 0x0n is OFF
'''

from mm.manifest import *
import sys
import logging

# "Button" 0 is the touch setting for the fader; then from top
# to bottom, 1, 4, 5, 3, 2.

BUTTONVALTOROW = [-1, 0, 4, 3, 1, 2]
ROWTOBUTTONVAL = [1, 4, 5, 3, 2]

class Outputter:
    ''' Abstract class: assumes it can transmit control values. '''
    def __init__(self): pass

    def doCtrlOut(self, ctrl, val):
        pass

    def setLED(self, chan, idx, how):
        ''' Set an LED: how=0 (off), 1 (on), 2 (blink).

        >>> op = Outputter()
        >>> def ctrlOut(ctrl, val): print "[ctrl %02X %02X]" % (ctrl, val)
        >>> op.doCtrlOut = ctrlOut

        >>> op.setLED(2, 2, DO_LED_BLINK)
        [ctrl 0C 02]
        [ctrl 2C 55]

        >>> op.setLED(5, 0, DO_LED_ON)
        [ctrl 0C 05]
        [ctrl 2C 41]
        '''
        self.doCtrlOut(OUT_BLOCKSELECT_CTRL, chan)
        self.doCtrlOut(OUT_LED_CTRL, ([OFF_BASE, ON_BASE, BLINK_BASE][how]) + ROWTOBUTTONVAL[idx])

    def setFader(self, chan, pos):
        ''' Set a fader to a MIDI level. LSB not used.

        >>> op = Outputter()
        >>> def ctrlOut(ctrl, val): print "[ctrl %02X %02X]" % (ctrl, val)
        >>> op.doCtrlOut = ctrlOut

        >>> op.setFader(4, 0x50)
        [ctrl 04 50]
        [ctrl 24 00]
        '''
        self.doCtrlOut(FADER_MSB_BASE_CTRL + chan, pos)
        self.doCtrlOut(FADER_LSB_BASE_CTRL + chan, 0)

class StripDriver:
    ''' Abstract class which drives a channel strip. Override
    doPress(), doTouch() etc. to receive input.
    '''
    def __init__(self, outputter, chan):
        self.__outputter = outputter
        self.__channel = chan

    def getChannel(self):
        return self.__channel

    def setLED(self, idx, how):
        self.__outputter.setLED(self.__channel, idx, how)

    def setFader(self, pos):
        self.__outputter.setFader(self.__channel, pos)

    def doPress(self, idx, how):
        pass

    def doTouch(self, how):
        pass

    def doFader(self, pos):
        pass

class MotorMixDriver:
    ''' MIDI receiver wrapped around an array of strip receivers.
    We currently ignore events for the mini-buttons (blocks
    8 to 11 inclusive).

    >>> sr = StripDriver(None, 3)
    >>> def press(idx, how): print "[press %d -> %d]" % (idx, how)
    >>> sr.doPress = press
    >>> strips = [StripDriver(None, i) for i in range(8)]
    >>> strips[3] = sr
    >>> mmr = MotorMixDriver(strips)
    >>> mmr.ctrlIn(0x0F, 3)
    >>> mmr.ctrlIn(0x2F, 0x43)
    [press 3 -> 1]
    >>> mmr.ctrlIn(0x2F, 0x04)
    [press 1 -> 0]

    >>> sr = StripDriver(None, 5)
    >>> def touch(how): print "[touch %d]" % how
    >>> sr.doTouch = touch
    >>> strips = [StripDriver(None, i) for i in range(8)]
    >>> strips[5] = sr
    >>> mmr = MotorMixDriver(strips)
    >>> mmr.ctrlIn(0x0F, 5)
    >>> mmr.ctrlIn(0x2F, 0x40)
    [touch 1]
    >>> mmr.ctrlIn(0x2F, 0x00)
    [touch 0]

    >>> sr = StripDriver(None, 6)
    >>> def fader(pos): print "[fader %d]" % pos
    >>> sr.doFader = fader
    >>> strips = [StripDriver(None, i) for i in range(8)]
    >>> strips[6] = sr
    >>> mmr = MotorMixDriver(strips)
    >>> mmr.ctrlIn(0x06, 23)
    [fader 23]
    >>> mmr.ctrlIn(0x26, 00)
    '''
    def __init__(self, strips):
        self.__strips = strips
        self.__currStripIndex = 0

    def getStrip(self, i):
        return self.__strips[i]

    def ctrlIn(self, ctrl, val):
        if ctrl == IN_BLOCKSELECT_CTRL:
            if val >= 0 and val < NUM_STRIPS:
                self.__currStripIndex = val
            else:
                logging.warning("channel strip number out of range: %d" % val)
        elif ctrl == IN_SWITCH_CTRL:
            strip = self.__strips[self.__currStripIndex]

            if val == ON_BASE:
                strip.doTouch(True)
            elif val > ON_BASE and val < ON_BASE + NUM_STRIPLEDS + 1:
                strip.doPress(BUTTONVALTOROW[val - ON_BASE], True)
            elif val == OFF_BASE:
                strip.doTouch(False)
            elif val > OFF_BASE and val < OFF_BASE + NUM_STRIPLEDS + 1:
                strip.doPress(BUTTONVALTOROW[val - OFF_BASE], False)
            else:
                logging.warning("channel LED index out of range: %d" % val)
        elif ctrl >= FADER_MSB_BASE_CTRL and ctrl < FADER_MSB_BASE_CTRL + NUM_STRIPS:
            strip = self.__strips[ctrl - FADER_MSB_BASE_CTRL]
            strip.doFader(val)
        elif ctrl >= FADER_LSB_BASE_CTRL and ctrl < FADER_LSB_BASE_CTRL + NUM_STRIPS:
            pass

if __name__ == "__main__":
    # PYTHONPATH=.. python <...>
    import doctest
    sys.path.append("/Users/nick/CASSIEL/MAXSEARCH/peal/python")
    from mock import Mock
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=False)
