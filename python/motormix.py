'''
MotorMix driver.

Controller overview (transmitted):
        15 (0x0F)       - selection of a different block of buttons;
                          0 to 7 are the main channels, 8 is left side,
                          9 is right side, 10 is left minibuttons,
                          11 is right minibuttons

        47 (0x2F)       - 0x40 to 0x4n is ON, 0x00 to 0x0n is OFF for
                          switch inside block identified by "n"

        0+n (0x0n)      - fader 0..n MSB.
        32+n (0x2n)     - fader 0..n LSB (two bits)
                          MSB first

Controller overview (received):
        0+n (0x0n)      - fader motor 0..n MSB
        32+n (0x2n)     - fader motor 0..n LSB (two bits)
                          MSB first

        12 (0x0C)       - selection of light block

        44 (0x2C)       - 0x40 to 0x4n is ON, 0x50 to 0x5n is BLINK,
                          0x00 to 0x0n is OFF.
'''

from manifest import *
from comms import MotorMixReceiver

def ctrlOut(ctl, val):
#    print "ctrl %02x %02x" % (ctl, val)
    maxObject.outletHigh(0, ['ctrl', ctl, val])

def pressOut(x, y, how):
    maxObject.outletHigh(0, ['press', x, y, [0, 1][how]])

def test(ch, val):
    ctrlOut(OUT_BLOCKSELECT_CTRL, ch)
    ctrlOut(OUT_LED_CTRL, [OFF_BASE, ON_BASE][val > 0] + 3)   # Fourth LED down (SOLO).
    ctrlOut(FADER_MSB_BASE_CTRL + ch, val)
    ctrlOut(FADER_LSB_BASE_CTRL + ch, 0)

incomingBlock = 0

# "Button" 0 is the touch setting for the fader; then from top
# to bottom, 1, 4, 5, 3, 2.

BUTTONVALTOROW = [-1, 0, 4, 3, 1, 2]
ROWTOBUTTONVAL = [1, 4, 5, 3, 2]

def ctrl(ctl, val):
    ''' Incoming controller messages (ctrl# * value). '''
    global incomingBlock

    if ctl == IN_BLOCKSELECT_CTRL:
        incomingBlock = val
    elif ctl == IN_SWITCH_CTRL:
        row = BUTTONVALTOROW[val & ~ON_BASE]
        if row != -1: pressOut(incomingBlock, row, (val & ON_BASE != 0))
    else:
        print "ctrl %02x val %02x" % (ctl, val)

def led(x, y, how):
    ctrlOut(OUT_BLOCKSELECT_CTRL, x)
    ctrlOut(OUT_LED_CTRL, [OFF_BASE, ON_BASE][how != 0] + ROWTOBUTTONVAL[y])

def led_row(row, rowBits):
    if row >= 0 and row < 5:
        for col in range(8):
            led(col, row, ((rowBits & (1 << col)) != 0))
