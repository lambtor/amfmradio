# amfmradio
circuitpython am fm radio with mp3 play from sd storage

ltp305.py library forked from<br>
https://github.com/gbit-is/LTP305-CircuitPython-class<br>
added support for decimal point
<br>
<ul>
<li>need function to scroll text across 3 pairs of led matrices</li>
<li>need full led maps for alphanumeric characters</li>
<li>need to test direct mp3 playback via pwmaudioio - digital pins for left and right channel</li>
  <ul>
		<li>need an amplifier for headphone output?</li>
		<li>need tests with signal pin connected to potentiometer and capacitor for volume, shared across both output signals</li>
   </ul>
<li>need to figure out how to interface with the am/fm module. use separate i2c bus.	0x11 i2c address, need to use 2 wire mode.</li>
<li>switch between am and fm bands</li>
<li>potentiometer for tuning</li>
<li>migrate the entire .h and .c files to circuitpython by using i2c sendcommand</li>
 </ul>
