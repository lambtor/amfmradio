import time
import board
import digitalio
from ltp305chain import ltp305chain
import rotaryio
import busio
from adafruit_bus_device.i2c_device import I2CDevice
import tinkeringtech_rda5807m

# timeout is in seconds
TIMEOUT = 0.2
ROTARY_TIMEOUT = 1.0
mnLastPoll = 0
mnSongPoll = 0
mnBrightness = 20
mnDispVal = 0
mbBrightAsc = True
mbRightDec = True
mbLeftDec = False
# moMatrix = ltp305(sda=board.GP16, scl=board.GP17, i2cAddress=0x61)
moI2C = busio.I2C(sda=board.GP4, scl=board.GP5, frequency=100000)
moMatrix0 = ltp305chain(sda=board.GP4, scl=board.GP5, i2cAddress=[0x61, 0x62], i2cDef=moI2C)
moMatrix0.brightness(mnBrightness, 0)
moMatrix0.brightness(mnBrightness, 1)
moMatrix0.clear(0)
moMatrix0.clear(1)

mpEncodeA = board.GP12
mpEncodeB = board.GP11
btnCENTER = digitalio.DigitalInOut(board.GP10)
btnDOWN = digitalio.DigitalInOut(board.GP9)
btnRIGHT = digitalio.DigitalInOut(board.GP8)
btnUP = digitalio.DigitalInOut(board.GP7)
btnLEFT = digitalio.DigitalInOut(board.GP6)
btnUP.switch_to_input(digitalio.Pull.UP)
btnCENTER.switch_to_input(digitalio.Pull.UP)
btnDOWN.switch_to_input(digitalio.Pull.UP)
btnRIGHT.switch_to_input(digitalio.Pull.UP)
btnLEFT.switch_to_input(digitalio.Pull.UP)
moRotary = rotaryio.IncrementalEncoder(mpEncodeA, mpEncodeB)
moCurrentRotary = moRotary.position
moLastRotary = moRotary.position
moLastRotaryTime = 0

# add optional support for tea5767?
# all stations use no decimal place, have trailing zero
marrPresets = [9310, 9470, 9550, 10030, 10110, 10190, 10710]
moInitStation = marrPresets[4]
mnCurrentStation = moInitStation
mnLastStation = mnCurrentStation
mnMinFreq = 8700
mnMaxFreq = 10800
moRDS = tinkeringtech_rda5807m.RDSParser()
mnVol = 15
moRadioI2C = I2CDevice(moI2C, 0x11)
moRadio = tinkeringtech_rda5807m.Radio(moRadioI2C, moRDS, moInitStation, mnVol)
moRadio.set_band("FM")
moRadio.set_mono(False)
moRadio.set_bass_boost(False)

# msTestString = "It's Chee Paw Paw time (ft Fidget)!! LOL      "
msTestString = str(moInitStation)
mnScrollIndex = 0
if (int(msTestString) < 10000):
    msTestString = " " + str((marrPresets[0]))[0:3]

def ChangeStation(nRawFrequency):
    global moRadio
    moRadio.set_freq(nRawFrequency)
    
def ShowStation(nStation):
    global moMatrix0
    strStationFreq = str(nStation / 10)
    # leading space for stations with only 3 digits
    if (nStation < 10000):
        strStationFreq = " " + str(nStation)
    # convert station to display value
    c1LChar = strStationFreq[:1]
    c1RChar = strStationFreq[1:2]
    c0LChar = strStationFreq[2:3]
    c0RChar = strStationFreq[3:4]
    moMatrix0.writeCharPair(c1LChar, c1RChar, False, False, 1)    
    moMatrix0.writeCharPair(c0LChar, c0RChar, False, True, 0)
    moMatrix0.update(0)
    moMatrix0.update(1)

def UpdateDisplayStation():
    global moCurrentRotary
    global moLastRotary
    global mnCurrentStation
    global mnLastStation
    global mnMaxFreq
    global mnMinFreq
    # 10 mhz per rotary step
    distMult = 10    
    if (moCurrentRotary == moLastRotary):
        return
    # print(str(moCurrentRotary) + " " + str(moLastRotary))
    distance = (max(moCurrentRotary, moLastRotary) - min(moCurrentRotary, moLastRotary)) * distMult
    print(distance)
    # get distance from old to new, convert to display value	
    if (moCurrentRotary > moLastRotary):
        if (mnLastStation + distance > mnMaxFreq):
            mnCurrentStation = mnMaxFreq
            ShowStation(mnCurrentStation)
            mnLastStation = mnCurrentStation
        else:
            mnCurrentStation = mnLastStation + distance
            ShowStation(mnCurrentStation)
            mnLastStation = mnCurrentStation
    else:
        if (moCurrentRotary < moLastRotary):
            if (mnLastStation + distance < mnMinFreq):
                mnCurrentStation = mnMinFreq
                ShowStation(mnCurrentStation)
                mnLastStation = mnCurrentStation
            else:
                mnCurrentStation = mnLastStation - distance
                ShowStation(mnCurrentStation)
                mnLastStation = mnCurrentStation
        else:
            mnCurrentStation = mnLastStation + distance
            ShowStation(mnCurrentStation)
            mnLastStation = mnCurrentStation

ShowStation(mnCurrentStation)

while True:
    # workflow: 
    # 1 process inputs, set mode if necessary
    # 2 check mode
    # update display based on mode
    if (moRotary.position != moCurrentRotary):
        moCurrentRotary = moRotary.position
        moLastRotaryTime = time.monotonic()
        # print(moCurrentRotary)
        UpdateDisplayStation()
    if ((time.monotonic() - moLastRotaryTime) > ROTARY_TIMEOUT):
        # update display        
        # UpdateDisplayStation()
        if (moLastRotary != moCurrentRotary):
            ChangeStation(mnCurrentStation)
        # convert rotary to station number
        moLastRotary = moCurrentRotary
    if ((time.monotonic() - mnLastPoll) > TIMEOUT):
        # print(str(moRadio.mono))
        # scroll string
        # moMatrix0.writeSubstring([char1 for char1 in msTestString], mnScrollIndex)
        # moMatrix0.update(0)
        # moMatrix0.update(1)
        # mnScrollIndex += 1
        # cLeftChar = msTestString[:1]
        # substring uses start & end indexes. don't use zero as a start, use empty char
        # cRightChar = msTestString[1:2]
        # print(cLeftChar + " | " + cRightChar)
        # moMatrix0.writeCharPair(cLeftChar, cRightChar, False, False, 1)
        # cLeftChar = msTestString[2:3]
        # cRightChar = msTestString[3:4]
        # moMatrix0.writeCharPair(cLeftChar, cRightChar, False, True, 0)
        # moMatrix0.update(0)
        # moMatrix0.update(1)
        if (mnScrollIndex >= (len(msTestString) + 1)):
            mnScrollIndex = 0
            # moMatrix0.brightness(48, 0)
            # moMatrix0.brightness(48, 1)
            # moMatrix0.brightness(48, 2)
        mnLastPoll = time.monotonic()
