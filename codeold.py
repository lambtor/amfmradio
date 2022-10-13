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
oRstPin.value = False
# set reset pin low on click dev
time.sleep(0.3)
oRstPin.value = True
# set reset pin high on click dev
time.sleep(0.3)

# Initialize and lock the I2C bus.
i2c = busio.I2C(scl=board.GP7, sda=board.GP6, frequency=200000)
while not i2c.try_lock():
    pass

obStartup = 0x40
obStartup |= 0x00
# send power up command
i2c.writeto(0x11, bytes([0x01, obStartup, 0x05]))
time.sleep(0.1)
i2c.writeto(0x11, bytes([0x15, 0x00, 0x00, 0x04]))
time.sleep(0.1)
# turn off hard mute
i2c.writeto(0x11, bytes([0x40, 0x01, 0x00, 0x00]))
time.sleep(0.1)
i2c.writeto(0x11, bytes([0x40, 0x00, (0x20 & 0x3F)]))
time.sleep(0.1)


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