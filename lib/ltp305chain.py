import board
import busio

# character map - this is how you define a dictionary in python
fontDictionary = {
    " ": [0, 0, 0, 0, 0, 0, 0],
    # "a": [0, 0, 13, 19, 17, 19, 13],
    "a": [0, 0, 14, 1, 15, 17, 15],
    "b": [16, 16, 28, 18, 18, 18, 28],
    "c": [0, 0, 14, 16, 16, 16, 14],
    "d": [1, 1, 7, 9, 9, 9, 7],
    "e": [0, 0, 14, 17, 31, 16, 14],
    "f": [2, 4, 4, 14, 4, 4, 4],
    "g": [0, 0, 15, 17, 15, 1, 14],
    "h": [16, 16, 16, 28, 18, 18, 18],
    "i": [0, 4, 0, 4, 4, 4, 4],
    "j": [4, 0, 4, 4, 4, 20, 8],
    "k": [16, 16, 18, 20, 24, 20, 18],
    "l": [4, 4, 4, 4, 4, 4, 4],
    "m": [0, 0, 0, 26, 21, 21, 21],
    "n": [0, 0, 0, 28, 18, 18, 18],
    "o": [0, 0, 14, 17, 17, 17, 14],
    "p": [0, 0, 28, 18, 28, 16, 16],
    "q": [0, 0, 7, 9, 7, 1, 1],
    "r": [0, 0, 22, 24, 16, 16, 16],
    "s": [0, 0, 14, 16, 14, 1, 14],
    "t": [0, 4, 14, 4, 4, 4, 4],
    "u": [0, 0, 17, 17, 17, 19, 13],
    "v": [0, 0, 17, 17, 17, 10, 4],
    "w": [0, 0, 17, 17, 21, 21, 10],
    "x": [0, 0, 17, 10, 4, 10, 17],
    "y": [0, 0, 17, 17, 15, 1, 14],
    "z": [0, 0, 31, 2, 4, 8, 31],
    "A": [4, 10, 17, 31, 17, 17, 17],
    "B": [30, 17, 17, 30, 17, 17, 30],
    "C": [14, 17, 16, 16, 16, 17, 14],
    "D": [28, 18, 17, 17, 17, 18, 28],
    "E": [31, 16, 16, 30, 16, 16, 31],
    "F": [31, 16, 16, 30, 16, 16, 16],
    "G": [14, 16, 16, 19, 17, 17, 14],
    "H": [17, 17, 17, 31, 17, 17, 17],
    "I": [31, 4, 4, 4, 4, 4, 31],
    "J": [2, 2, 2, 2, 2, 18, 12],
    "K": [17, 18, 20, 24, 20, 18, 17],
    "L": [16, 16, 16, 16, 16, 16, 31],
    "M": [17, 27, 21, 17, 17, 17, 17],
    "N": [17, 17, 25, 21, 19, 17, 17],
    "O": [14, 17, 17, 17, 17, 17, 14],
    "P": [30, 17, 17, 30, 16, 16, 16],
    "Q": [14, 17, 17, 17, 21, 18, 13],
    "R": [30, 17, 17, 30, 20, 18, 17],
    "S": [14, 17, 16, 14, 1, 17, 14],
    "T": [31, 4, 4, 4, 4, 4, 4],
    "U": [17, 17, 17, 17, 17, 17, 14],
    "V": [17, 17, 17, 17, 17, 10, 4],
    "W": [17, 17, 17, 21, 21, 21, 10],
    "X": [17, 17, 10, 4, 10, 17, 17],
    "Y": [17, 17, 10, 4, 4, 4, 4],
    "Z": [31, 1, 2, 4, 8, 16, 31],
    "0": [14, 17, 19, 21, 25, 17, 14],
    "1": [4, 12, 4, 4, 4, 4, 14],
    "2": [14, 17, 1, 2, 4, 8, 31],
    "3": [31, 2, 4, 2, 1, 17, 14],
    "4": [2, 6, 10, 18, 31, 2, 2],
    "5": [31, 16, 30, 1, 1, 17, 14],
    "6": [6, 8, 16, 30, 17, 17, 14],
    "7": [31, 1, 2, 2, 4, 4, 4],
    "8": [14, 17, 17, 14, 17, 17, 14],
    "9": [14, 17, 17, 15, 1, 2, 12],
    "'": [4, 4, 0, 0, 0, 0, 0],
    "(": [4, 8, 8, 8, 8, 8, 4],
    ")": [4, 2, 2, 2, 2, 2, 4],
    ",": [0, 0, 0, 0, 4, 4, 8],
    ".": [0, 0, 0, 0, 0, 6, 6],
    ":": [0, 0, 4, 0, 4, 0, 0],
    "-": [0, 0, 0, 14, 0, 0, 0],
    "_": [0, 0, 0, 0, 0, 0, 31],
    "!": [4, 4, 4, 4, 4, 0, 4],
    "@": [14, 17, 1, 13, 21, 21, 14],
    "#": [0, 10, 31, 10, 31, 10, 0],
    "$": [14, 21, 20, 14, 5, 21, 14],
    "%": [24, 25, 2, 4, 8, 19, 3],
    "^": [4, 10, 17, 0, 0, 0, 0],
    "&": [0, 8, 20, 8, 21, 18, 13],
    "*": [0, 4, 21, 14, 21, 4, 0],
    "+": [0, 0, 4, 14, 4, 0, 0],
    "=": [0, 0, 14, 0, 14, 0, 0],
    "/": [2, 2, 4, 4, 4, 8, 8],
    "|": [6, 6, 6, 6, 6, 6, 6],
    "\"": [10, 10, 0, 0, 0, 0, 0],
    "~": [0, 0, 24, 4, 3, 0, 0],
    "`": [8, 4, 0, 0, 0, 0, 0]
}

# Somewhat based on: https://github.com/pimoroni/ltp305-python
class ltp305chain:
    # need list of character maps
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

    def getChar2(self, char):
        # print(str(fontDictionary[char]))
        return fontDictionary.get(char)

    def __init__(self, sda=board.GP4, scl=board.GP5, i2cAddress=[0x61, 0x62], i2cDef=None):
        if (i2cDef is None):
            self.i2c = busio.I2C(sda=board.GP4, scl=board.GP5, frequency=100000)
        else:
            self.i2c = i2cDef
        self.i2cAddress1 = i2cAddress[0]
        intAddress2 = 0
        if (len(i2cAddress) > 1):
            self.i2cAddress2 = i2cAddress[1]
            intAddress2 = int(i2cAddress[1])
        # self.i2cAddress2 = i2cAddress[1]
        if (len(i2cAddress) > 2):
            self.i2cAddress3 = i2cAddress[2]
            intAddress3 = int(i2cAddress[2])

        self.i2cAddresses = i2cAddress
        if not self.i2c.try_lock():
            m = "Unable to get i2c lock"
            print(m)
        i2cScan = self.i2c.scan()
        intAddress1 = int(i2cAddress[0])
        # intAddress2 = int(i2cAddress[1])

        if intAddress1 not in i2cScan:
            m = "unable to find ltp305 " + str(i2cAddress[0])
            print(m)
        if intAddress2 not in i2cScan:
            m = "unable to find ltp305 #2" + str(intAddress2)
            print(m)
        # if intAddress3 not in i2cScan:
           # m = "unable to find ltp305 #3" + str(i2cAddress[2])
           # print(m)
        self.commands()
        self.sendCommand(self.CMD_MODE, self.MODE, 0)
        self.sendCommand(self.CMD_OPTIONS, self.OPTS, 0)
        self.sendCommand(self.CMD_MODE, self.MODE, 1)
        self.sendCommand(self.CMD_OPTIONS, self.OPTS, 1)
        if (len(i2cAddress) > 2):
            self.sendCommand(self.CMD_MODE, self.MODE, 2)
            self.sendCommand(self.CMD_OPTIONS, self.OPTS, 2)

    def binary(self, num, pre="0b", length=5, spacer=0):
        return "{0}{{:{1}>{2}}}".format(pre, spacer, length).format(bin(num)[2:])

    def sendCommand(self, addr, frame, dispIndex=0):
        # tempAddresses = [0x61, 0x62]
        bytearr = bytearray(2)
        bytearr[0] = addr
        bytearr[1] = frame
        self.i2c.try_lock()
        # self.i2c.writeto(self.i2cAddress, bytearr)
        self.i2c.writeto(self.i2cAddresses[dispIndex], bytearr)
        # self.i2c.writeto(tempAddresses[dispIndex], bytearr)
        self.i2c.unlock()

    def update(self, dispIndex=0):
        self.sendCommand(self.CMD_UPDATE, 0x01, dispIndex)

    def brightness(self, value=127, index=0):
        value = min(int(value), 127)
        # if value > 127:
            # value = 127
        self.sendCommand(self.CMD_BRIGHTNESS, value, index)

    def clear(self, dispIndex=0):
        x = range(1, 19)
        for i in x:
            self.sendCommand(i, 0b00000000, dispIndex)
        # clear decimal on left and right
        self.sendCommand(21, 0b00000000, dispIndex)
        self.update(dispIndex)

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

    def writeLeft(self, map, bDecimal, dispIndex=0):
        map = self.rowsToCols(map)
        c = 0
        rows = range(14, 19)
        for row in rows:
            self.sendCommand(row, map[c], dispIndex)
            c += 1
        # on left side, send row as 21, with full definition as if number must be binary 128
        if (bDecimal is True):
            self.sendCommand(21, 0b01000000, dispIndex)
        else:
            self.sendCommand(21, 0b00000000, dispIndex)

    def writeRight(self, map, bDecimal, dispIndex=0):
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
            temp2 = temp
            # print(temp2)
            temp = int(temp)
            if (col == 7):
                # decimal must be treated as if there are 3 extra columns
                # on right matrix. on left it's 3 extra rows
                # leftmost column if we add 3 is 128 in binary
                if (bDecimal == True):
                    temp += 128
                    # print(temp)
            self.sendCommand(col, temp, dispIndex)
            c += 1

    def write(self, disp, map, bDecimal, dispIndex=0):
        disp = disp.lower()
        if "r" in disp:
            self.writeRight(map, bDecimal, dispIndex)
        if "l" in disp:
            self.writeLeft(map, bDecimal, dispIndex)

    def writeChar(self, disp, char, bDecimal, dispIndex=0):
        # map = self.getChar(char)
        map = self.getChar2(str(char))
        # if (dispIndex == 1 and disp == "l"):
        # print(char)
        self.write(disp, map, bDecimal, dispIndex)

    def writeCharPair(self, lChar, rChar, bDecimalL=False, bDecimalR=False, dispIndex=0):
        self.writeChar("l", lChar, bDecimalL, dispIndex)
        self.writeChar("r", rChar, bDecimalR, dispIndex)

    # display subset of a string on a matrix pair
    def writeSubstring(self, arrText, scrollIndex):
        if (scrollIndex <= 1):
            self.writeChar("r", arrText[scrollIndex], False, 0)
            if (scrollIndex == 0):
                self.writeChar("l", " ", False, 0)
            else:
                self.writeChar("l", arrText[scrollIndex - 1], False, 0)
            # print(str(scrollIndex) + " t1 " + str(arrText[scrollIndex]))
        elif (scrollIndex <= 3):
            self.writeChar("r", arrText[scrollIndex], False, 0)
            self.writeChar("l", arrText[scrollIndex - 1], False, 0)
            self.writeChar("r", arrText[scrollIndex - 2], False, 1)
            if (scrollIndex == 2):
                self.writeChar("l", " ", False, 1)
            else:
                self.writeChar("l", arrText[scrollIndex - 3], False, 1)
            # print(str(scrollIndex) + " t3 " + str(arrText[scrollIndex]))
        elif (scrollIndex <= 5):
            self.writeChar("l", arrText[scrollIndex - 3], False, 1)
            self.writeChar("r", arrText[scrollIndex - 2], False, 1)
            self.writeChar("l", arrText[scrollIndex - 1], False, 0)
            self.writeChar("r", arrText[scrollIndex], False, 0)
            if (len(self.i2cAddresses) > 2):
                self.writeChar("r", arrText[scrollIndex - 4], False, 2)
                if (scrollIndex == 4):
                    self.writeChar("l", " ", False, 2)
                else:
                    self.writeChar("l", arrText[scrollIndex - 5], False, 2)
            # print(str(scrollIndex) + " t5 " + str(arrText[scrollIndex]))
        elif (scrollIndex < (len(arrText))):
            self.writeChar("r", arrText[scrollIndex], False, 0)
            self.writeChar("l", arrText[scrollIndex - 1], False, 0)
            self.writeChar("r", arrText[scrollIndex - 2], False, 1)
            self.writeChar("l", arrText[scrollIndex - 3], False, 1)
            if (len(self.i2cAddresses) > 2):
                self.writeChar("r", arrText[scrollIndex - 4], False, 2)
                self.writeChar("l", arrText[scrollIndex - 5], False, 2)
            # print(str(scrollIndex) + " t6 " + str(arrText[scrollIndex]))
        pass

