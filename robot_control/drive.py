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

def parse_cmd(cmd_dict):
    try :
        drive_mode = cmd_dict['drive_mode']
    except:
        drive_mode = 'tank'

    try:
        left_direction = int(cmd_dict['left_direction'])
    except:
        left_direction = 0
    
    try:
        left_velocity = int(cmd_dict['left_velocity'])
    except:
        left_velocity = 0

    try:
        right_direction = int(cmd_dict['right_direction'])
    except:
        right_direction = 0

    try:
        right_velocity = int(cmd_dict['right_velocity'])
    except:
        right_velocity = 0

    try:
        speed = int(cmd_dict['speed'])
    except:
        speed = 0

    try:
        head = int(cmd_dict['heading'])
    except:
        head = 0

    return drive_mode, left_direction, left_velocity, right_direction, right_velocity, speed, head


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
            except:
                print("Connection lost, reconnecting...")
                time.sleep(3)
                client = tcp_client.tcp_client()
                client.connect("10.22.192.34", 9091)
                print(f"Connected to server at: 10.22.192.34:9091")
                continue

            cmd_dict = json.loads(recv)
            print(cmd_dict)


            drive_mode, left_direction, left_velocity, right_direction, right_velocity, speed, head = parse_cmd(cmd_dict)


            if (speed > 60):
                speed = 60
            elif (speed < 0):
                speed = 0

            head = head % 360

            print("Heading: " + str(head))
            print("left_velocity: " + str(left_velocity))
            print("right_velocity: " + str(right_velocity))

            if (drive_mode == 'tank'):
                rvr.raw_motors(int(left_direction), int(left_velocity), int(right_direction), int(right_velocity))
            elif(drive_mode == 'heading'):
                rvr.drive_with_heading(int(speed), int(head), 0)


    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')


    finally:
        rvr.close()


if __name__ == '__main__':
    main()
