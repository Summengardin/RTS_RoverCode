print("Starting rover... Importing modules")

import sys

sys.path.append('../../dependencies/sphero-sdk-raspberrypi-python')
sys.path.append('../')
sys.path.append('D:\Data\Dev\sphero-sdk-raspberrypi-python')

import time
import communication.tcp_client as tcp_client
import json
from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RvrLedGroups

import blinker
import threading


MAX_SPEED = 255

rvr = SpheroRvrObserver()

prev_time = 0

def parse_cmd(cmd_dict):
    '''
    Parses the json-command and returns the drive mode and motor commands
    Expects a json with the following format:
    {
        "drive_mode": "tank" or "heading",
        "left_direction": 0, 1 or 2,
        "left_velocity": 0-255,
        "right_direction": 0, 1 or 2,
        "right_velocity": 0-255,
        "speed": 0-255,
        "heading": 0-359
    }
    
    '''
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



class Rover(SpheroRvrObserver):
    def __init__(self, ip) -> None:
        SpheroRvrObserver.__init__(self)
        self.set_all_leds_rgb(255,125,0)
        #self.Blinker = blinker.Blinker(1)
        self.wake()
        time.sleep(2)
        #self.reset_heading()

        self.controller_ip = ip
        self.controller_port = 9091
        self.connect(self.controller_ip, self.controller_port)


    def connect(self, host, port):
        print(f"Connecting to server at: {host}:{port}...")
        self.client = tcp_client.tcp_client()
        self.client.connect(host, port)
        print(f"Connected")
        self.set_all_leds_rgb(0,255,0)

    def stop(self):
        self.set_all_leds_rgb(255,0,0)
        self.close()
        self.client.close()


    def run(self):
        while True:
            try:
                recv = self.client.recv()
            except:
                print("Connection lost, reconnecting...")
                time.sleep(3)
                self.connect(self.controller_ip, self.controller_port)
                continue
            
            try:
                cmd_dict = json.loads(recv)
            except:
                print("Error parsing json")
                continue

            print(cmd_dict)

            drive_mode, left_direction, left_velocity, right_direction, right_velocity, speed, head = parse_cmd(cmd_dict)

            if (left_velocity > MAX_SPEED or right_velocity > MAX_SPEED):
                left_velocity = MAX_SPEED
                right_velocity = MAX_SPEED

            if (drive_mode == 'tank'):
                self.raw_motors(int(left_direction), int(left_velocity), int(right_direction), int(right_velocity))
            elif(drive_mode == 'heading'):
                rvr.drive_with_heading(int(speed), int(head), 0)
        

    def set_all_leds_rgb(self, r, g, b):
        self.set_all_leds(
            RvrLedGroups.all_lights.value,
            [color for x in range(0, 10) for color in [r, g, b]]
        )

            


def main():
    ip = sys.argv[1] if len(sys.argv) > 1 else "10.22.192.34"
    

    print(f"Starting rover")
    rover = Rover(ip)

    rover_thread = threading.Thread(target=rover.run)
    rover_thread.daemon = True

    rover_thread.start()

    try:
        while True:
            time.sleep(1)   
    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    rover.stop() 



if __name__ == '__main__':
    main()
