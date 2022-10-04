import time
import board
import digitalio
from ltp305 import ltp305

# timeout is in seconds
TIMEOUT = 0.015
mnLastPoll = 0
mnBrightness = 0
mnDispVal = 0
mbBrightAsc = True
mbRightDec = True
mbLeftDec = False
moMatrix = ltp305(sda=board.GP16, scl=board.GP17, i2cAddress=0x61)
moMatrix.clear()
moMatrix.brightness(48)
# moMatrix.writeChar("l", 4, True)
# moMatrix.writeChar("r", 1, True)
# moMatrix.update()
# moMatrix.setDecimal(True, False)

while False:    
    if ((time.monotonic() - mnLastPoll) > TIMEOUT):
        lstVal = [int(a) for a in str(mnDispVal)]
        if (len(lstVal) == 1):
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
        if (mnDispVal > 99):
            mnDispVal = 0
             
        