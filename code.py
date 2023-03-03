import time
import board
import digitalio
import rotaryio
from ltp305 import ltp305
from font import font
from adafruit_bus_device.i2c_device import I2CDevice
import tinkeringtech_rda5807m

# timeout is in seconds
TIMEOUT = 0.015
mnLastPoll = 0
mnBrightness = 0
mnDispVal = 0
mbBrightAsc = True
mbRightDec = True
mbLeftDec = False
mpEncodeA = board.GP7
mpEncodeB = board.GP8

btnCENTER = digitalio.DigitalInOut(board.GP9)
btnUP = digitalio.DigitalInOut(board.GP12)
btnDOWN = digitalio.DigitalInOut(board.GP10)
btnRIGHT = digitalio.DigitalInOut(board.GP11)
btnLEFT = digitalio.DigitalInOut(board.GP13)

btnUP.switch_to_input(digitalio.Pull.UP)
btnCENTER.switch_to_input(digitalio.Pull.UP)
btnDOWN.switch_to_input(digitalio.Pull.UP)
btnRIGHT.switch_to_input(digitalio.Pull.UP)
btnLEFT.switch_to_input(digitalio.Pull.UP)

moRotary = rotaryio.IncrementalEncoder(mpEncodeA, mpEncodeB)
# stemma connector is i2c0 -> GP4, SCL -> GP5
# need to refactor this to be a list of 2 pairs of matrices
# also need to change this to use i2c1 instead of i2c0
# i2c1 -> GP18, GP19
moMatrix = ltp305(sda=board.GP16, scl=board.GP17, i2cAddress=0x61)
moMatrix.clear()
moMatrix.brightness(20)
# i2c0 is for stemma - fm module
# GP29 on pico lipo is for battery voltage
msTemp = font.get("a")

# all stations use no decimal place, have trailing zero
marrPresets = [9310, 9470, 9550, 10030, 10110, 10190, 10710]
moRDS = tinkeringtech_rda5807m.RDSParser()
mnVol = 3
moI2C = board.STEMMA_I2C()
moRadioI2C = I2CDevice(moI2C, 0x11)
moRadio = tinkeringtech_rda5807m.Radio(moRadioI2C, moRDS, marrPresets[1], mnVol)
moRadio.set_band("FM")

while False:    
    # handle button presses for status changes
    # use timer for all display updates
    if (time.monotonic() - mnLastPoll) > TIMEOUT:
        lstVal = [int(a) for a in str(mnDispVal)]
        if len(lstVal) == 1:
            moMatrix.writeChar("r", lstVal[0], mbRightDec)
            moMatrix.writeChar("l", 0, mbRightDec)
        else:
            moMatrix.writeChar("r", lstVal[1], mbRightDec)
            moMatrix.writeChar("l", lstVal[0], mbLeftDec)
        # moMatrix.brightness(mnBrightness)
        mbLeftDec = not mbLeftDec
        mbRightDec = not mbRightDec
        moMatrix.update()
        mnLastPoll = time.monotonic()
        mnDispVal += 1
        if mnDispVal > 99:
            mnDispVal = 0
