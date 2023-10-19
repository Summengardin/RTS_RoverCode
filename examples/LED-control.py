import sys  # Allows us to use sys.path.append below
import time  # Allows us to insert delays in our script

# sys.path tells the interpreter where to look for modules.
# Tell it to look in the SDK directory as well.
sys.path.append('/home/pi/sphero-sdk-raspberrypi-python')

# Now that it can find the SDK, we can import some useful SDK modules
from sphero_sdk import SpheroRvrObserver
from sphero_sdk import Colors

# Instantiate (create) a SpheroRvrObserver object
rvr = SpheroRvrObserver()

# Make sure RVR is awake and ready to receive commands
rvr.wake()

# Wait for RVR to wake up
time.sleep(2)

try:
    while True:
        # Set all of RVR's LEDs to a named color
        rvr.led_control.set_all_leds_color(color=Colors.yellow)

        # Wait a second so we get to see the color change
        time.sleep(1)

        # Now try using RGB (Red Green Blue) values.  
        # This allows us to pick any color in the RGB colorspace.
        rvr.led_control.set_all_leds_rgb(red=255, green=0, blue=0)

        time.sleep(1)

except KeyboardInterrupt:
    print('\nProgram terminated with keyboard interrupt.')

# Call this at the end of your program to close the serial port
rvr.close()
