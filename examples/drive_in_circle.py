import sys
import time


sys.path.append('../../dependencies/sphero-sdk-raspberrypi-python')
sys.path.append('D:\Data\Dev\sphero-sdk-raspberrypi-python')
from sphero_sdk import SpheroRvrObserver


rvr = SpheroRvrObserver()

prev_time = 0

def main():
    rvr.wake()
    time.sleep(2)
    
    rvr.drive_control.reset_heading()
    
    try:
        deg_per_second = 90
        head = 0
        prev_time = time.time()
        while True:
            dt = time.time() - prev_time
            prev_time = time.time()

            head += deg_per_second * dt
            head = head % 360

            print("Heading: " + str(head))
            
            rvr.drive_with_heading(64, int(head), 0)
            time.sleep(0.1)

    
    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()

if __name__ == '__main__':
    main()
