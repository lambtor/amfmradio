import board
import busio

# Somewhat based on: https://github.com/pimoroni/ltp305-python
class ltp305:
    # need list of character maps
    CHARMAP
    def commands(self):
        self.MODE = 0b00011000
        self.OPTS = 0b00001110
        self.CMD_BRIGHTNESS = 0x19
        self.CMD_MODE = 0x00
        self.CMD_UPDATE = 0x0C
        self.CMD_OPTIONS = 0x0D

        self.CMD_MATRIX_L = 0x0E
        self.CMD_MATRIX_R = 0x01

    def getChar(self, char):
        chars = {}
        chars[0] = [14, 17, 19, 21, 25, 17, 14]
        chars[1] = [4, 12, 4, 4, 4, 4, 14]
        chars[2] = [14, 17, 1, 14, 16, 16, 31]
        chars[3] = [14, 17, 1, 14, 1, 17, 14]
        chars[4] = [2, 6, 10, 18, 31, 2, 2]
        chars[5] = [31, 16, 30, 1, 1, 17, 14]
        chars[6] = [14, 16, 16, 30, 17, 17, 14]
        chars[7] = [31, 1, 2, 2, 4, 4, 4]
        chars[8] = [14, 17, 17, 14, 17, 17, 14]
        chars[9] = [14, 17, 17, 15, 1, 1, 14]

        return chars[char]

    def __init__(self, sda=board.GP17, scl=board.GP16, i2cAddress=0x61):

        self.i2c = busio.I2C(board.GP17, board.GP16)
        self.i2cAddress = i2cAddress
        if not self.i2c.try_lock():
            m = "Unable to get i2c lock"
            print(m)
        i2cScan = self.i2c.scan()
        intAddress = int(i2cAddress)
        if intAddress not in i2cScan:
            m = "unable to find ltp305"
            print(m)
        self.commands()
        self.sendCommand(self.CMD_MODE, self.MODE)
        self.sendCommand(self.CMD_OPTIONS, self.OPTS)

    def binary(self, num, pre="0b", length=5, spacer=0):
        return "{0}{{:{1}>{2}}}".format(pre, spacer, length).format(bin(num)[2:])

    def sendCommand(self, addr, frame):
        bytearr = bytearray(2)
        bytearr[0] = addr
        bytearr[1] = frame
        self.i2c.writeto(self.i2cAddress, bytearr)

    def update(self):
        self.sendCommand(self.CMD_UPDATE, 0x01)

    def brightness(self, value=127):
        value = int(value)
        if value > 127:
            value = 127
        self.sendCommand(self.CMD_BRIGHTNESS, value)

    def clear(self):
        x = range(1, 19)
        for i in x:
            self.sendCommand(i, 0b00000000)
        # clear decimal on left and right
        self.sendCommand(21, 0b00000000)
        self.update()

    def rowsToCols(self, map):
        ph = {0: "", 1: "", 2: "", 3: "", 4: ""}

        for line in map:

            binLine = self.binary(line)
            ran = range(2, 7)
            for r in ran:
                v = ph[r - 2]
                ph[r - 2] = binLine[r] + v

        col = []
        for p in ph:
            val = ph[p]
            val = "0b" + val
            val = int(val)
            # val = bin(int(val,2))

            col.append(val)
        return col

    def writeLeft(self, map, bDecimal):
        map = self.rowsToCols(map)
        c = 0

        rows = range(14, 19)

        for row in rows:
            self.sendCommand(row, map[c])
            # print("row " + str(row) + "|" + str(map[c]))
            c += 1
            
        # on left side, send row as 21, with full definition as if number must be binary 128
        if (bDecimal):
            self.sendCommand(21, 0b01000000)
        else:
            self.sendCommand(21, 0b00000000)

    def writeRight(self, map, bDecimal):
        c = 0
        cols = range(1, 8)

        for col in cols:
            rmap = map[c]
            rmap = self.binary(rmap)
            rval = rmap[2:]
            temp = ""
            for char in rval:
                t = temp
                temp = char + t
            temp = "0b" + temp            
            temp = int(temp)
            if (col == 7):
                if (bDecimal == True):
                    temp += 128

            self.sendCommand(col, temp)
            # print("col " + str(col) + "|" + str(temp))
            c += 1            

    def write(self, disp, map, bDecimal):
        disp = disp.lower()
        if "r" in disp:
            self.writeRight(map, bDecimal)
        if "l" in disp:
            self.writeLeft(map, bDecimal)

    def writeChar(self, disp, char, bDecimal):
        map = self.getChar(char)
        self.write(disp, map, bDecimal)

    def writeCharPair(self, lChar, rChar, bDecimal):
        self.writeChar("l", lChar, bDecimal)
        self.writeChar("r", rChar, bDecimal)   
    