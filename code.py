import time
import board
import digitalio
from audiomp3 import MP3Decoder
from ltp305 import ltp305
import os

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

# timeout is in seconds
TIMEOUT = 0.25
mnLastPoll = 0
mnSongPoll = 0
mnBrightness = 0
mnDispVal = 0
mbBrightAsc = True
mbRightDec = True
mbLeftDec = False
# moMatrix = ltp305(sda=board.GP16, scl=board.GP17, i2cAddress=0x61)
moMatrix = ltp305(sda=board.GP16, scl=board.GP17, i2cAddress=0x63)
moMatrix.clear()
moMatrix.brightness(48)
# moMatrix.writeChar("l", "a", True)
# moMatrix.writeChar("r", "b", False)
# moMatrix.update()
# moMatrix.setDecimal(True, False)
# msTestString = " It's FIDGET TIME dawg (cat)! "
msTestString = list(filter(lambda x: x.lower().endswith("mp3"), os.listdir("/")))[0].replace(".mp3", "")
mnScrollIndex = 0
# moLeftPin = digitalio.DigitalInOut(board.GP14)
# moLeftPin.switch_to_output(value=True)
# moRightPin = digitalio.DigitalInOut(board.GP13)
# moRightPin.switch_to_output(value=True)

moAudioPlaying = False
mp3Filename = open(list(filter(lambda x: x.lower().endswith("mp3"), os.listdir("/")))[0], "rb")
moDecoder = MP3Decoder(mp3Filename)
moDecoder.file = open(list(filter(lambda x: x.lower().endswith("mp3"), os.listdir("/")))[0], "rb")
# right is red - pins connected with alligator clips right now
# right_channel=board.GP13, 
moAudio = AudioOut(board.GP28, quiescent_value=-32768)

while True:
    if ((time.monotonic() - mnLastPoll) > TIMEOUT):
        # scroll string
        mnLastPoll = time.monotonic()
        moMatrix.writeSubstring([char1 for char1 in msTestString], mnScrollIndex)
        moMatrix.update()
        mnScrollIndex += 1
        
        if (mnScrollIndex >= (len(msTestString) + 1)):
            mnScrollIndex = 0
        if (moAudioPlaying == False and (time.monotonic() - mnSongPoll) > 10):            
            moAudioPlaying = True
            print("started playing " + str(msTestString))
            # moAudio.play(moDecoder)
            # while moAudio.playing:
             # pass
        """
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
        """

