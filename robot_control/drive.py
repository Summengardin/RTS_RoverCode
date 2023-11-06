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
    print(f"Connected to server at: 10.22.192.34:9091")

    rvr.drive_control.reset_heading()

    try:
        head = 0
        speed = 64
        while True:
            try:
                recv = client.recv()
                cmd_dict = json.loads(recv)
                print(cmd_dict)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
                continue

            left_direction = int(cmd_dict['left_direction'])
            left_velocity = int(cmd_dict['left_velocity'])
            right_direction = int(cmd_dict['right_direction'])
            right_velocity = int(cmd_dict['right_velocity'])
            speed = int(cmd_dict['speed'])
            head = int(cmd_dict['heading'])


            if (speed > 60):
                speed = 60
                left_velocity = 60/255 * left_velocity
                right_velocity = 60/255 * right_velocity
            elif (speed < 0):
                speed = 0

            head = head % 360

            print("Heading: " + str(head))

            if (cmd_dict['drive_mode'] == 'tank'):
                rvr.raw_motors(int(left_velocity), int(left_direction), int(right_velocity), int(right_direction))
            elif(cmd_dict['drive_mode'] == 'heading'):
                rvr.drive_with_heading(int(speed), int(head), 0)


    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')


    finally:
        rvr.close()


if __name__ == '__main__':
    main()
