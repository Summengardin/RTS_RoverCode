import sys  # Allows us to use sys.path.append below
import time  # Allows us to insert delays in our script

sys.path.append('../../dependencies/sphero-sdk-raspberrypi-python')

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()

def main():
    rvr.wake()

    time.sleep(2)

    rvr.drive_control.reset_heading()

    rvr.drive_control.drive_forward_seconds(
        speed=64,  # This is out of 255, where 255 corresponds to 2 m/s
        heading=0,  # Valid heading values are 0-359
        time_to_drive=1  # Driving duration in seconds
    )

    rvr.drive_control.drive_backward_seconds(
        speed=64,
        heading=0,
        time_to_drive=1
    )

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()
