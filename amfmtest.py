import board
import busio
import digitalio
import time

REGISTERS = (0, 256)  # Range of registers to read, from the first up to (but
                      # not including!) the second value.

REGISTER_SIZE = 2     # Number of bytes to read from each register.

#try the score
nTestkHz = 670

oRstPin = digitalio.DigitalInOut(board.GP27)
oRstPin.direction = digitalio.Direction.OUTPUT

oPWMPin = digitalio.DigitalInOut(board.GP26)
oPWMPin.direction = digitalio.Direction.OUTPUT
oPWMPin.value = False
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

obStartup = 0x40
obStartup |= 0x00
def amfm_reset():
    global oRstPin
    global oPWMPin
    oRstPin.value = False
    oPWMPin.value = False
    time.sleep(0.2)
    oRstPin.value = True
    oPWMPin.value = True

def amfm_init():
    global i2c
    initCmdBuffer = [0x00, 0x00, 0x00]
    initCmdBuffer[0] = 0x01
    initCmdBuffer[1] = 0x80 | 0x40 | 0x10 | 0x00
    initCmdBuffer[2] = 0x05
    i2c.writeto(0x11, initCmdBuffer)

def amfmSetVolume(nVolume):
    if (nVolume < 0):
        nVolume = 0
    if (nVolume > 63):
        nVolume = 63
    global i2c
    arrVolBuffer = [0x12, 0x00, 0x00, 0x00, 0x00, 0x00]
    # max volume value
    arrVolBuffer[2] = 0x40
    # min volume value
    arrVolBuffer[3] = 0x00
    arrVolBuffer[5] = hex(nVolume)
    i2c.writeto(0x11, arrVolBuffer)

# full range from am 520 to fm 108 is 520 -> 108000
def amfmSetFrequency(nKhz):
    global i2c
    nKhzBytes = nKhz.to_bytes(2, 'big')
    arrFreqBuffer = [0x20, 0x00, nKhzBytes[0], nKhzBytes[1], 0x00]
    i2c.writeto(0x11, arrFreqBuffer)

def amfmMute():
    global i2c
    arrMuteBuffer = [0x12, 0x00, 0x40, 0x01, 0x00, 0x00]
    arrMuteBuffer[5] = 0x02 | 0x01
    i2c.writeto(0x11, arrMuteBuffer)

def amfmUnMute():
    global i2c
    arrMuteBuffer = [0x12, 0x00, 0x40, 0x01, 0x00, 0x00]
    i2c.writeto(0x11, arrMuteBuffer)

# Find the first I2C device available.
devices = i2c.scan()
while len(devices) < 1:
    devices = i2c.scan()
device = devices[0]
print('Found device with address: {}'.format(hex(device)))
time.sleep(0.11)


try:
    for nDev in devices:
        print("device at " + str(hex(nDev)) + " on bus")
    # Scan all the registers and read their byte values.
    result = bytearray(REGISTER_SIZE)
    for register in range(*REGISTERS):
        try:
            if (register == 32):
                nStation = int(0)
                arrStationBytes = nStation.to_bytes(2, 'big')
                print(arrStationBytes)
                oTmpBytes = [0x20, 0x00, arrStationBytes[0], arrStationBytes[1], 0x00]
                i2c.writeto(device, bytes(arrStationBytes))
            else:
                i2c.writeto(device, bytes([register]))
            i2c.readfrom_into(device, result)
        except OSError:
            continue  # Ignore registers that don't exist!
        print('Address {0}: {1}'.format(hex(register), ' '.join([hex(x) for x in result])) + " | " + str(register))
finally:
    # Unlock the I2C bus when finished.  Ideally put this in a try-finally!
    i2c.unlock()
