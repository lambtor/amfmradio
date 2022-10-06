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
    "v": [0, 0, 31, 31, 31, 10, 4],
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
class ltp305:
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
        value = min(int(value), 127)
        # if value > 127:
            # value = 127
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
                # decimal must be treated as if there are 3 extra columns
                # on right matrix. on left it's 3 extra rows
                # leftmost column if we add 3 is 128 in binary
                if (bDecimal == True):
                    temp += 128

            self.sendCommand(col, temp)
            c += 1

    def write(self, disp, map, bDecimal):
        disp = disp.lower()
        if "r" in disp:
            self.writeRight(map, bDecimal)
        if "l" in disp:
            self.writeLeft(map, bDecimal)

    def writeChar(self, disp, char, bDecimal):
        # map = self.getChar(char)
        map = self.getChar2(str(char))
        self.write(disp, map, bDecimal)

    def writeCharPair(self, lChar, rChar, bDecimal):
        self.writeChar("l", lChar, bDecimal)
        self.writeChar("r", rChar, bDecimal)
    
    # display subset of a string on a matrix pair
    def writeSubstring(self, arrText, scrollIndex):
        if (scrollIndex > (len(arrText) - 1)):
            self.writeChar("l", " ", False)
            self.writeChar("r", " ", False)
        elif (scrollIndex == (len(arrText) - 1)):
            self.writeChar("l", arrText[scrollIndex], False)
            self.writeChar("r", " ", False)
        else:
            self.writeChar("l", arrText[scrollIndex], False)
            self.writeChar("r", arrText[scrollIndex + 1], False)
