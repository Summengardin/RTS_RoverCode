
import sys
sys.path.append('../../dependencies/sphero-sdk-raspberrypi-python')
sys.path.append('../')
sys.path.append('D:\Data\Dev\sphero-sdk-raspberrypi-python')



import time
import communication.tcp_client as tcp_client
import json
from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()

prev_time = 0


def main():
    rvr.wake()
    time.sleep(2)
    client = tcp_client.tcp_client()
    client.connect("10.22.192.34", 9091)


    rvr.drive_control.reset_heading()

    try:
        head = 0
        speed = 64
        while True:
            recv = client.recv()
            cmd_dict = json.loads(recv)
            print(cmd_dict)
            if cmd_dict['command'] == 'move':
                speed = cmd_dict['speed']
                head = cmd_dict['heading']
            elif cmd_dict['command'] == 'stop':
                speed = 0
                head = 0

            if (speed > 255):
                speed = 255
            elif (speed < 0):
                speed = 0
            
            head = head % 360

            print("Heading: " + str(head))

            rvr.drive_with_heading(int(speed), int(head), 0)
            time.sleep(0.1)


    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()



