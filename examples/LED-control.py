import sys
import time

sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import Colors

rvr = SpheroRvrObserver()

rvr.wake()

time.sleep(2)

try:
    while True:
        rvr.led_control.set_all_leds_color(color=Colors.yellow)

        time.sleep(1)

        rvr.led_control.set_all_leds_rgb(red=255, green=0, blue=0)

        time.sleep(1)

except KeyboardInterrupt:
    print('\nProgram terminated with keyboard interrupt.')

rvr.close()
