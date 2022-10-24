import board
import busio
import digitalio
import time

# try the q101
# mhz station values need to be multiplied by 1000 to convert to khz used by board
# am needs an antenna
nTestkHz = 10110

oRstPin = digitalio.DigitalInOut(board.GP27)
oRstPin.direction = digitalio.Direction.OUTPUT

oPWMPin = digitalio.DigitalInOut(board.GP26)
oPWMPin.direction = digitalio.Direction.OUTPUT
oPWMPin.value = False
# this enables serial input, setting this pin low
oSenPin = digitalio.DigitalInOut(board.GP25)
oSenPin.direction = digitalio.Direction.OUTPUT
oSenPin.value = False
# set reset pin low on click dev
time.sleep(0.3)
oRstPin.value = True
oPWMPin.value = True
# set reset pin high on click dev
time.sleep(0.3)

# Initialize and lock the I2C bus.
i2c = busio.I2C(scl=board.GP7, sda=board.GP6, frequency=100000)
while not i2c.try_lock():
    pass

def amfm_reset():
    global oRstPin
    global oPWMPin
    oRstPin.value = False
    oPWMPin.value = False
    time.sleep(0.3)
    oRstPin.value = True
    oPWMPin.value = True

def fmStartup():
    global i2c
    # initCmdBuffer = [0x00, 0x00, 0x00]
    # power up
    # initCmdBuffer[0] = 0x01
    # initCmdBuffer[1] = 0x80 | 0x40 | 0x10 | 0x00
    # initCmdBuffer[2] = 0x05
    initCmdBuffer = [0x01, (0x80 | 0x40 | 0x10 | 0x00), 0x05]
    i2c.writeto(0x11, bytearray(initCmdBuffer))
    # FM hardware cfg
    amfmSetProperty(0x0001, (0x0001 | 0x0004))
    # general cfg
    amfmSetProperty(0x1403, 3)
    amfmSetProperty(0x1404, 20)
    # regional USA
    amfmSetProperty(0x1500, 0x0004)
    amfmSetProperty(0x1502, (0x0001 | (3 << 14) | (3 << 12) | (3 << 10) |  (3 << 8)))    
    amfmSetProperty(0x1100, 0x2)
    # seek step 100khz
    amfmSetProperty(0x1402, 0x2)

def amfmSetVolume(nVolume):
    if (nVolume < 0):
        nVolume = 0
    if (nVolume > 63):
        nVolume = 63
    byVol = (nVolume & 0x003F).to_bytes(2, 'big')
    nVolID = int(0x4000)
    byVolID = nVolID.to_bytes(2, 'big')
    global i2c
    arrVolBuffer = bytearray([0x12, 0x00, 0x00, 0x00, 0x00, 0x00])
    # max volume value
    arrVolBuffer[2] = byVolID[0]
    # min volume value
    arrVolBuffer[3] = byVolID[1]
    arrVolBuffer[4] = byVol[0]
    arrVolBuffer[5] = byVol[1]
    i2c.writeto(0x11, arrVolBuffer)

# full range from am 520 to fm 108 is 520 -> 108000
def fmSetFrequency(nKhz):
    global i2c
    nKhzBytes = nKhz.to_bytes(2, 'big')
    arrFreqBuffer = [0x20, 0x00, nKhzBytes[0], nKhzBytes[1], 0x00]
    i2c.writeto(0x11, bytearray(arrFreqBuffer))

def amfmMute():
    global i2c
    arrMuteBuffer = [0x12, 0x00, 0x40, 0x01, 0x00, 0x00]
    arrMuteBuffer[5] = 0x02 | 0x01
    i2c.writeto(0x11, bytearray(arrMuteBuffer))

def amfmUnMute():
    global i2c
    arrMuteBuffer = [0x12, 0x00, 0x40, 0x01, 0x00, 0x00]
    i2c.writeto(0x11, bytearray(arrMuteBuffer))

# time.sleep(0.11)
def amfmSetProperty(oPropID, oPropVal):
    global i2c
    nPropID = int(oPropID)
    byPropID = nPropID.to_bytes(2, 'big')
    nPropVal = int(oPropVal)
    byPropVal = nPropVal.to_bytes(2, 'big')
    cmdBuffer = bytearray([0x12, 0x00, byPropID[0], byPropID[1], byPropVal[0], byPropVal[1]])
    i2c.writeto(0x11, cmdBuffer)

try:
    fmStartup()
    amfmSetProperty(0x4001, 0)
    amfmSetVolume(40)
    fmSetFrequency(nTestkHz)
    
    while (True):
        pass
finally:
    # Unlock the I2C bus when finished.  Ideally put this in a try-finally!
    i2c.unlock()
