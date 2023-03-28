# amfmradio
circuitpython am fm radio

ltp305.py library forked from<br>
https://github.com/gbit-is/LTP305-CircuitPython-class<br>
added support for decimal point
<br>
<ul>
<li>need function to scroll text across 2 pairs of led matrices</li>
<li>need full led maps for alphanumeric characters</li>
<li>need to figure out how to interface with the am/fm module. shared i2c bus.</li>
<li>rotary encoder for tuning</li>
 </ul>
 NEVER USE ANYTHING MADE BY MIKROE COMPANY.
<br>
<br>
need mode toggle via center button:<br>
<ul>
 <li>show current station
 </li>
 <li>get rds data, display scrolling on matrices
 </li>
 <li>show current battery %
 </li>
 </ul>
 <br> up/down buttons for volume
 <br> hold left or right buttons for half a second to jump to nearest saved station above/below current one
 <br>rotary behavior needs refinement - this may need a timeout to throttle input so display can catch up
