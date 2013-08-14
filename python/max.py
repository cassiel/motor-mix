"""
Drive the Motor Mix from inside Max. Assumes `maxObject` for output; call
`ctrl` to input control messages.
"""

from mm.motormix import Outputter
from mm.pager import driver

class MMOutputter(Outputter):
    def __init__(self, maxObject):
        Outputter.__init__(self)
        self.__maxObject = maxObject

    def doCtrlOut(self, ctrl, val):
        self.__maxObject.outletHigh(0, ['mm.ctrl', val, ctrl, 1])
        # Out in Max's ctlout order.

class IACOutputter:
    def __init__(self, maxObject):
        self.__maxObject = maxObject

    ''' Output as visible MIDI (controls or notes), any MIDI channel. '''
    def doCtrlOut(self, ctrl, val, chan):
        # Out in Max order:
        self.__maxObject.outletHigh(0, ['iac.ctrl', val, ctrl, chan])

    def doNoteOut(self, pitch, vel, chan):
        self.__maxObject.outletHigh(0, ['iac.note', pitch, vel, chan])

d = driver(MMOutputter(maxObject), IACOutputter(maxObject))

def ctrl(ctl, val):
    d.ctrlIn(ctl, val)

import time
from java.lang import System

print "Loaded Motor Mix at {t} on {vendor} {ver}/{a}".format(
    t=time.asctime(time.localtime(time.time())),
    vendor=System.getProperty("java.vendor"),
    ver=System.getProperty("java.version"),
    a=System.getProperty("os.arch"))
