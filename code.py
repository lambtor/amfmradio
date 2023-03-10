import time
import board
import digitalio
from ltp305chain import ltp305chain
import rotaryio
import busio
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_debouncer import Debouncer
import tinkeringtech_rda5807m

# timeout is in seconds
TIMEOUT = 0.2
ROTARY_TIMEOUT = 1.0
VOL_TIMEOUT = 3.0
mnLastPoll = 0
mnSongPoll = 0
mnBrightness = 10
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

PIN_CENTER = board.GP10
PIN_DOWN = board.GP9
PIN_RIGHT = board.GP8
PIN_UP = board.GP7
PIN_LEFT = board.GP6

moRotary = rotaryio.IncrementalEncoder(mpEncodeA, mpEncodeB)
moCurrentRotary = moRotary.position
moLastRotary = moRotary.position
moLastRotaryTime = 0
mnDisplayMode = 0
FREQ_MODE = 0
RDS_MODE = 1
VOLUME_MODE = 2
BATTERY_MODE = 3
BRIGHTNESS_MODE = 4

# add optional support for tea5767?
# all stations use no decimal place, have trailing zero
marrPresets = [9310, 9470, 9550, 10030, 10110, 10190, 10710]
moInitStation = marrPresets[4]
mnCurrentStation = moInitStation
mnCurrStationDisp = mnCurrentStation
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
mnScrollIndex = 0
def ButtonRead(pin):
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.UP
    return lambda: io.value

btnLEFT = Debouncer(ButtonRead(PIN_LEFT))
btnRIGHT = Debouncer(ButtonRead(PIN_RIGHT))
btnUP = Debouncer(ButtonRead(PIN_UP))
btnDOWN = Debouncer(ButtonRead(PIN_DOWN))
btnCENTER = Debouncer(ButtonRead(PIN_CENTER))
mbLRInitClick = True
mnBtnLRTime = 0
mnBtnPrevLRTime = 0
mnBtnUDTime = 0

def SetNextDispMode():
    global mnDisplayMode
    nMaxMode = 1
    if (mnDisplayMode == nMaxMode):
        mnDisplayMode = 0
    else:
        mnDisplayMode += 1

def SetDispMode(nDispMode):
    global mnDisplayMode
    mnDisplayMode = nDispMode

def UpdateStationDisp(nUpdateDir):
    global mnCurrStationDisp
    global mnDisplayMode
    if (mnDisplayMode != FREQ_MODE):
        SetDispMode(FREQ_MODE)
    mnCurrStationDisp += (10 * nUpdateDir)
    ShowStation(mnCurrStationDisp)
    
def UpdateVolume(nDirection):
    global moRadio
    global moMatrix0
    global mnVol
    if ((mnVol + nDirection) < 16 and (mnVol + nDirection) > -1):        
        mnVol += nDirection        
    strVol = str(mnVol)
    if (len(strVol) < 2):
        strVol = " " + strVol
    if (mnVol < 15 and mnVol > 0): 
        moMatrix0.writeCharPair("v", " ", False, False, 1)
        moMatrix0.writeCharPair(strVol[:1], strVol[1:2], False, False, 0)
        moRadio.set_mute(False)
        moRadio.set_volume(mnVol)
    elif (mnVol == 15):
        moMatrix0.writeCharPair("v", "M", False, False, 1)
        moMatrix0.writeCharPair("A", "X", False, False, 0)
        moRadio.set_volume(mnVol)
    elif (mnVol <= 0):
        moMatrix0.writeCharPair("m", "u", False, False, 1)
        moMatrix0.writeCharPair("t", "e", False, False, 0)
        moRadio.set_mute(True)
    moMatrix0.update(0)
    moMatrix0.update(1)
    

def SetStation(nRawFrequency):
    global moRadio
    global mnCurrentStation
    print("station set " + str(nRawFrequency))
    moRadio.set_freq(nRawFrequency)
    mnCurrentStation = nRawFrequency

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
    # print(distance)
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
    btnLEFT.update()
    btnRIGHT.update()
    btnUP.update()
    btnDOWN.update()
    btnCENTER.update()

    if (moRotary.position != moCurrentRotary):
        moCurrentRotary = moRotary.position
        moLastRotaryTime = time.monotonic()
        # print(moCurrentRotary)
        UpdateDisplayStation()
    if ((time.monotonic() - moLastRotaryTime) > ROTARY_TIMEOUT):
        # update display
        # UpdateDisplayStation()
        if (moLastRotary != moCurrentRotary):
            SetStation(mnCurrStationDisp)
        # convert rotary to station number
        moLastRotary = moCurrentRotary
    # set station on button timeouts
    # if current station != displayed station
    nNow = time.monotonic()
    if (mbLRInitClick is False and mnCurrStationDisp != mnCurrentStation and (nNow - mnBtnLRTime) > ROTARY_TIMEOUT):
        mbLRInitClick = True
        SetStation(mnCurrStationDisp)
    if (mnDisplayMode == VOLUME_MODE and nNow - mnBtnUDTime > VOL_TIMEOUT and mnVol > 0):
        ShowStation(mnCurrentStation)
        SetDispMode(FREQ_MODE)
    if btnLEFT.rose:
        if (mbLRInitClick is True):
            mnBtnLRTime = nNow
            mnBtnPrevLRTime = mnBtnLRTime
            mbLRInitClick = False
        else:
            mnBtnPrevLRTime = mnBtnLRTime
            mnBtnLRTime = nNow
        UpdateStationDisp(-1)        
    if btnRIGHT.rose:
        if (mbLRInitClick is True):
            mnBtnLRTime = nNow
            mnBtnPrevLRTime = mnBtnLRTime
            mbLRInitClick = False
        else:
            mnBtnPrevLRTime = mnBtnLRTime
            mnBtnLRTime = nNow
        UpdateStationDisp(1)
    if btnUP.rose:
        print("up hit")
        if (mnDisplayMode != BRIGHTNESS_MODE and mnDisplayMode != VOLUME_MODE):
            SetDispMode(VOLUME_MODE)
        mnBtnUDTime = nNow
        UpdateVolume(1)
    if btnDOWN.rose:
        print("down hit")
        if (mnDisplayMode != BRIGHTNESS_MODE and mnDisplayMode != VOLUME_MODE):
            SetDispMode(VOLUME_MODE)
        mnBtnUDTime = nNow
        UpdateVolume(-1)
    if btnCENTER.rose:
        SetNextDispMode()
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
        mnLastPoll = time.monotonic()
