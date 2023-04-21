import time
import board
import digitalio
from ltp305chain import ltp305chain
import rotaryio
import busio
import analogio
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_debouncer import Debouncer
import tinkeringtech_rda5807m

# timeout is in seconds
SCROLL_TIMEOUT = 0.75
ROTARY_TIMEOUT = 1.0
VOL_TIMEOUT = 3.0
RDS_TIMEOUT = 10.0
RDSWARM_TIMEOUT = 180.0
EMPTY_BATTERY = 2.8
FULL_BATTERY = 4.2
BATTERY_TIMEOUT = 300
BRIGHT_TIMEOUT = 10
MIN_BRIGHTNESS = 2
MAX_BRIGHTNESS = 50
mnLastBrightPoll = 0
mbBattUpdate = False
mbBrightUpdate = False
mnLastBattPoll = 0
mnLastPoll = 0
mnLastRDSPoll = 0
mnSongPoll = 0
mnBrightness = 11
mnDispVal = 0
mbBrightAsc = True
mbRightDec = True
mbLeftDec = False
# moMatrix = ltp305(sda=board.GP16, scl=board.GP17, i2cAddress=0x61)
moI2C = busio.I2C(sda=board.GP4, scl=board.GP5, frequency=100000)
moMatrix0 = ltp305chain(
    sda=board.GP4, scl=board.GP5, i2cAddress=[0x61, 0x62], i2cDef=moI2C
)
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
# BAT_SENSE used for battery monitoring, despite pimoroni page saying it's 29?
###
'A0', 'A1', 'A2', 'A3', 'BAT_SENSE', 'GP0', 'GP1', 'GP10',
'GP11', 'GP12', 'GP13', 'GP14', 'GP15',
'GP16', 'GP17', 'GP18', 'GP19', 'GP2', 'GP20',
'GP21', 'GP22', 'GP25', 'GP26', 'GP26_A0',
'GP27', 'GP27_A1', 'GP28', 'GP28_A2', 'GP3', 'GP4',
'GP5', 'GP6', 'GP7', 'GP8', 'GP9',
'I2C', 'LED', 'SCL', 'SDA', 'STEMMA_I2C', 'USER_SW', 'VBUS_DETECT'
###
moVoltPin = analogio.AnalogIn(board.BAT_SENSE)

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
mnVol = 10
moRadioI2C = I2CDevice(moI2C, 0x11)
msActRDSText = "    "
msRDSText = "no detail available     "
mbRDSUpdate = False
mbRDSWarmedup = False

def GetRDSText(sPulledText):
    global msRDSText
    global mbRDSUpdate
    sEmpty = " "
    if (sEmpty in sPulledText):
        sPulledText = sPulledText.strip().split(sEmpty)[0]
    # print("rds callback~")
    # print(msRDSText + "~ " + str(time.monotonic()))
    if msRDSText != (sPulledText.strip() + "    "):
        mbRDSUpdate = True
    msRDSText = sPulledText.strip() + "    "


moRDS.attach_text_callback(GetRDSText)
moRadio = tinkeringtech_rda5807m.Radio(moRadioI2C, moRDS, moInitStation, mnVol)
moRadio.set_band("FM")
moRadio.set_mono(False)
moRadio.set_bass_boost(False)
print("station set " + str(mnCurrentStation) + "|" + str(time.monotonic()))
# moRadio.check_rds()

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
mnInitTime = 0

def SetNextDispMode():
    global mnDisplayMode
    global moRadio
    global msActRDSText
    global msRDSText
    global mnCurrentStation
    global moMatrix0
    global mbBattUpdate
    global mbBrightUpdate
    nMaxMode = 4
    mbBattUpdate = True
    mbBrightUpdate = True
    if mnDisplayMode == nMaxMode:
        mnDisplayMode = 0
    else:
        mnDisplayMode += 1
    moMatrix0.writeCharPair(" ", " ", False, False, 1)
    moMatrix0.writeCharPair(" ", " ", False, False, 0)
    moMatrix0.update(0)
    moMatrix0.update(1)
    if mnDisplayMode == RDS_MODE:
        print("dispR: " + str(mnDisplayMode))
        # moRadio.check_rds()
        msActRDSText = msRDSText
    elif mnDisplayMode == FREQ_MODE:
        ShowStation(mnCurrentStation)
    else:
        pass


def SetDispMode(nDispMode):
    global mnDisplayMode
    mnDisplayMode = nDispMode


def UpdateStationDisp(nUpdateDir):
    global mnCurrStationDisp
    global mnDisplayMode
    if mnDisplayMode != FREQ_MODE:
        SetDispMode(FREQ_MODE)
    mnCurrStationDisp += 10 * nUpdateDir
    ShowStation(mnCurrStationDisp)


def UpdateVolume(nDirection):
    global moRadio
    global moMatrix0
    global mnVol
    if (mnVol + nDirection) < 16 and (mnVol + nDirection) > -1:
        mnVol += nDirection
    strVol = str(mnVol)
    if len(strVol) < 2:
        strVol = " " + strVol
    if mnVol < 15 and mnVol > 0:
        moMatrix0.writeCharPair("γ", " ", False, False, 1)
        moMatrix0.writeCharPair(strVol[:1], strVol[1:2], False, False, 0)
        moRadio.set_mute(False)
        moRadio.set_volume(mnVol)
    elif mnVol == 15:
        moMatrix0.writeCharPair("γ", "M", False, False, 1)
        moMatrix0.writeCharPair("A", "X", False, False, 0)
        moRadio.set_volume(mnVol)
    elif mnVol <= 0:
        moMatrix0.writeCharPair("m", "u", False, False, 1)
        moMatrix0.writeCharPair("t", "e", False, False, 0)
        moRadio.set_mute(True)
    moMatrix0.update(0)
    moMatrix0.update(1)


def SetStation(nRawFrequency):
    global moRadio
    global mnCurrentStation
    global mnCurrStationDisp
    print("station set " + str(nRawFrequency))
    moRadio.set_freq(nRawFrequency)
    mnCurrentStation = nRawFrequency
    if (mnCurrStationDisp != mnCurrentStation):
        mnCurrStationDisp = mnCurrentStation
    # moRadio.check_rds()


def ShowStation(nStation):
    global moMatrix0
    strStationFreq = str(nStation / 10)
    # leading space for stations with only 3 digits
    if nStation < 10000:
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
    if moCurrentRotary == moLastRotary:
        return
    # print(str(moCurrentRotary) + " " + str(moLastRotary))
    distance = (
        max(moCurrentRotary, moLastRotary) - min(moCurrentRotary, moLastRotary)
    ) * distMult
    # print(distance)
    # get distance from old to new, convert to display value
    if moCurrentRotary > moLastRotary:
        if mnLastStation + distance > mnMaxFreq:
            mnCurrentStation = mnMaxFreq
            ShowStation(mnCurrentStation)
            mnLastStation = mnCurrentStation
        else:
            mnCurrentStation = mnLastStation + distance
            ShowStation(mnCurrentStation)
            mnLastStation = mnCurrentStation
    else:
        if moCurrentRotary < moLastRotary:
            if mnLastStation + distance < mnMinFreq:
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

def GetBatteryPercentText():
    global moVoltPin
    global mdRawVoltage
    global EMPTY_BATTERY
    global FULL_BATTERY
    sBattPct = ""
    # otherwise use value * (9.9 / 65535). pin.reference_voltage not giving decent value
    mdRawVoltage = (moVoltPin.value * 9.9) / 65535
    # print("[" + str(mdRawVoltage))
    nBattPct = 100 * ((mdRawVoltage - EMPTY_BATTERY) / (FULL_BATTERY - EMPTY_BATTERY))
    nBattPct = int(max(min(nBattPct, 100), 0))
    sBattPct = str(nBattPct) + "%"
    # use α as battery icon
    if nBattPct < 10:
        sBattPct = "α " + sBattPct
    elif nBattPct < 100:
        sBattPct = "α" + sBattPct
    return sBattPct

def UpdateBrightness(nDirection):
    global moMatrix0
    global mnBrightness
    global MAX_BRIGHTNESS
    global MIN_BRIGHTNESS
    if (
        (mnBrightness + nDirection) <= MAX_BRIGHTNESS
        and (mnBrightness + nDirection) >= MIN_BRIGHTNESS
    ):
        mnBrightness += nDirection
    strBr = str(mnBrightness)
    if len(strBr) < 2:
        strBr = " " + strBr
    if mnBrightness < MAX_BRIGHTNESS and mnBrightness > MIN_BRIGHTNESS:
        moMatrix0.writeCharPair("β", " ", False, False, 1)
        moMatrix0.writeCharPair(strBr[:1], strBr[1:2], False, False, 0)
    elif mnBrightness == MAX_BRIGHTNESS:
        moMatrix0.writeCharPair("β", "M", False, False, 1)
        moMatrix0.writeCharPair("A", "X", False, False, 0)
    elif mnBrightness <= MIN_BRIGHTNESS:
        moMatrix0.writeCharPair("β", "m", False, False, 1)
        moMatrix0.writeCharPair("i", "n", False, False, 0)
    moMatrix0.brightness(mnBrightness, 0)
    moMatrix0.brightness(mnBrightness, 1)
    moMatrix0.update(0)
    moMatrix0.update(1)

ShowStation(mnCurrentStation)
SetDispMode(FREQ_MODE)
mnInitTime = time.monotonic()

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

    if moRotary.position != moCurrentRotary:
        moCurrentRotary = moRotary.position
        moLastRotaryTime = time.monotonic()
        # need cleanup for rotary conversion to frequency display
        # print(moCurrentRotary)
        UpdateDisplayStation()
    if (time.monotonic() - moLastRotaryTime) > ROTARY_TIMEOUT:
        # update display
        # UpdateDisplayStation()
        if moLastRotary != moCurrentRotary:
            SetStation(mnCurrStationDisp)
        # convert rotary to station number
        moLastRotary = moCurrentRotary
    # set station on button timeouts
    # if current station != displayed station
    nNow = time.monotonic()
    if (mbRDSWarmedup is False and (nNow - mnInitTime) > RDSWARM_TIMEOUT):
        print("rds warmed")
        mbRDSWarmedup = True

    if (
        mbLRInitClick is False
        and mnCurrStationDisp != mnCurrentStation
        and (nNow - mnBtnLRTime) > ROTARY_TIMEOUT
    ):
        mbLRInitClick = True
        SetStation(mnCurrStationDisp)
    if mnDisplayMode == VOLUME_MODE and nNow - mnBtnUDTime > VOL_TIMEOUT and mnVol > 0:
        ShowStation(mnCurrentStation)
        SetDispMode(FREQ_MODE)
    if btnLEFT.rose:
        if mbLRInitClick is True:
            mnBtnLRTime = nNow
            mnBtnPrevLRTime = mnBtnLRTime
            mbLRInitClick = False
        else:
            mnBtnPrevLRTime = mnBtnLRTime
            mnBtnLRTime = nNow
        UpdateStationDisp(-1)
    if btnRIGHT.rose:
        if mbLRInitClick is True:
            mnBtnLRTime = nNow
            mnBtnPrevLRTime = mnBtnLRTime
            mbLRInitClick = False
        else:
            mnBtnPrevLRTime = mnBtnLRTime
            mnBtnLRTime = nNow
        UpdateStationDisp(1)
    if btnUP.rose:
        print("up hit")
        # up button only changes volume if not in brightness mode
        # otherwise up / down changes brightness
        if mnDisplayMode == BRIGHTNESS_MODE:
            UpdateBrightness(1)
        elif mnDisplayMode != VOLUME_MODE:
            SetDispMode(VOLUME_MODE)
            UpdateVolume(1)
        elif mnDisplayMode == VOLUME_MODE:
            UpdateVolume(1)
        mnBtnUDTime = nNow
    if btnDOWN.rose:
        print("down hit")
        if mnDisplayMode == BRIGHTNESS_MODE:
            UpdateBrightness(-1)
        elif mnDisplayMode != VOLUME_MODE:
            SetDispMode(VOLUME_MODE)
            UpdateVolume(-1)
        elif mnDisplayMode == VOLUME_MODE:
            UpdateVolume(-1)
        mnBtnUDTime = nNow
    if btnCENTER.rose:
        SetNextDispMode()
    # RDS MODE, scroll RDS data line
    if mnDisplayMode == RDS_MODE:
        if (nNow - mnLastPoll) > SCROLL_TIMEOUT:
            # print("idx:" + str(mnScrollIndex))
            # scroll string
            if len(msActRDSText) >= 8:
                # print(msActRDSText + "|")
                moMatrix0.writeSubstring([char1 for char1 in msActRDSText], mnScrollIndex)
                moMatrix0.update(0)
                moMatrix0.update(1)
            mnScrollIndex += 1
            if mnScrollIndex >= len(msActRDSText):
                mnScrollIndex = 0
                bRefreshDispString = True
            if mbRDSWarmedup is True and (nNow - mnLastRDSPoll) > RDS_TIMEOUT:
                # print("hit rds recheck:" + msRDSText + "|")
                # refresh RDS data-
                moRadio.check_rds()
                if msActRDSText != msRDSText:
                    # mbRDSUpdate = False
                    print(msActRDSText + "||")
                    msActRDSText = msRDSText
                    if len(msActRDSText) < 8:
                        msActRDSText = msActRDSText + "    "
                mnLastRDSPoll = nNow
            mnLastPoll = nNow
    elif mnDisplayMode == FREQ_MODE:
        if (nNow - mnLastRDSPoll) > RDS_TIMEOUT:
            moRadio.check_rds()
            mnLastRDSPoll = nNow
            # print(str(moRadio.rds) + "|")
            if mbRDSUpdate is True:
                print(msRDSText + " 2")
                mbRDSUpdate = False
            # msActRDSText = msRDSText
            # print(msRDSText + " 1")
    elif mnDisplayMode == VOLUME_MODE:
        if (nNow - mnBtnUDTime > VOL_TIMEOUT):
            mnBtnUDTime = nNow
            SetDispMode(VOLUME_MODE)
            UpdateVolume(0)
    elif mnDisplayMode == BRIGHTNESS_MODE:
        if mbBrightUpdate is True or (nNow - mnLastBrightPoll) > BRIGHT_TIMEOUT:
            mnLastBrightPoll = nNow
            UpdateBrightness(0)
            mbBrightUpdate = False
            # print("bright")
    elif mnDisplayMode == BATTERY_MODE:
        if (
            mbBattUpdate is True
            or mnLastBattPoll == 0
            or (nNow - mnLastBattPoll) > BATTERY_TIMEOUT
        ):
            mnLastBattPoll = nNow
            mbBattUpdate = False
            # only poll every 5 min, 300 sec
            sBatteryTxt = GetBatteryPercentText()
            if len(sBatteryTxt) == 4:
                moMatrix0.writeCharPair(
                    sBatteryTxt[:1], sBatteryTxt[1:2], False, False, 1
                )
                moMatrix0.writeCharPair(
                    sBatteryTxt[2:3], sBatteryTxt[3:4], False, False, 0
                )
                moMatrix0.update(0)
                moMatrix0.update(1)
            elif len(sBatteryTxt) == 3:
                moMatrix0.writeCharPair("β", sBatteryTxt[:1], False, False, 1)
                moMatrix0.writeCharPair(
                    sBatteryTxt[1:2], sBatteryTxt[2:3], False, False, 0
                )
                moMatrix0.update(0)
                moMatrix0.update(1)
            elif len(sBatteryTxt) == 2:
                moMatrix0.writeCharPair("β", " ", False, False, 1)
                moMatrix0.writeCharPair(sBatteryTxt[:1], sBatteryTxt[1:2], False, False, 0)
                moMatrix0.update(0)
                moMatrix0.update(1)
            # print("battery " + str(mnLastBattPoll))
