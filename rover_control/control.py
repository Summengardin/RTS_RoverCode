print("Starting rover... Importing modules")

import sys

sys.path.append('../../dependencies/sphero-sdk-raspberrypi-python')
sys.path.append('../')
sys.path.append('D:\Data\Dev\sphero-sdk-raspberrypi-python')

import time
import json
import threading

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RvrLedGroups
import pi_servo_hat

import communication.tcp_client as tcp_client
import blinker

TILT_SERVO = 0
PAN_SERVO = 1

# Create an instance of the Servo Phat
servos = pi_servo_hat.PiServoHat()

servos.restart()



MAX_SPEED = 255
MAX_TILT = 60
MIN_TILT = 40
MAX_PAN = 90
MIN_PAN = 20

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
        "heading": 0-359,
        "servo_tilt": 40-60,
        "servo_pan": 20-90
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

    try:
        tilt = int(cmd_dict['servo_tilt'])
    except:
        tilt = 50

    try:
        pan = int(cmd_dict['servo_pan'])
    except:
        pan = 50


    return drive_mode, left_direction, left_velocity, right_direction, right_velocity, speed, head, tilt, pan


def parse_cmd_dict(cmd_dict) -> dict:
    '''
    Parses the json-command and returns a dictionary with the commands.
    If a command is not included in the json, it returns None for that command.
    '''
    parsed_cmd = {
        "drive_mode": cmd_dict.get('drive_mode', 'tank'),
        "left_direction": cmd_dict.get('left_direction'),
        "left_velocity": cmd_dict.get('left_velocity'),
        "right_direction": cmd_dict.get('right_direction'),
        "right_velocity": cmd_dict.get('right_velocity'),
        "speed": cmd_dict.get('speed'),
        "heading": cmd_dict.get('heading'),
        "servo_tilt": cmd_dict.get('servo_tilt'),
        "servo_pan": cmd_dict.get('servo_pan')
    }

    return parsed_cmd


class Rover(SpheroRvrObserver):
    def __init__(self, ip) -> None:
        SpheroRvrObserver.__init__(self)
        self.set_all_leds_rgb(255,125,0)

        # Initialize last known states
        self.last_left_direction = 0
        self.last_left_velocity = 0
        self.last_right_direction = 0
        self.last_right_velocity = 0
        self.last_speed = 0
        self.last_head = 0
        self.last_tilt = 50
        self.last_pan = 50

        #self.Blinker = blinker.Blinker(1)
        self.wake()
        time.sleep(2)
        #self.reset_heading()
        self.servos = pi_servo_hat.PiServoHat()
        self.servos.restart()


        self.controller_ip = ip
        self.controller_port = 9091
        self.connect(self.controller_ip, self.controller_port)
        self.running = False


    def connect(self, host, port):
        print(f"Connecting to server at: {host}:{port}...")
        self.client = tcp_client.tcp_client()
        self.client.connect(host, port)
        print(f"Connected")
        self.set_all_leds_rgb(0,255,0)

    def stop(self):
        self.running = False
        self.set_all_leds_rgb(255,0,0)
        print("Closing connection...")
        self.client.close()
        print("Closed")
        print("Closing rover...")
        self.close()
        print("Closed")  

    def drive(self, left_dir, left_vel, right_dir, right_vel):
        self.raw_motors(left_dir, left_vel, right_dir, right_vel)

    def stop(self):
        self.drive(0,0,0,0)

    def move_servo(self, servo, position):
        print(f"Moving servo {servo} to position {position}")
        self.servos.move_servo_position(servo, position)

    def run(self):
        self.running = True
        while self.running:
            try:
                recv = self.client.recv()
            except:
                print("Connection lost, reconnecting...")
                self.stop()
                time.sleep(3)
                self.connect(self.controller_ip, self.controller_port)
                continue
            
            if recv == "":
                continue

            try:
                cmd_dict = json.loads(recv)
            except:
                print("Error parsing json")
                continue

            print(cmd_dict)

            drive_mode, left_direction, left_velocity, right_direction, right_velocity, speed, head, tilt, pan = parse_cmd(cmd_dict)
            parsed_cmd = parse_cmd_dict(cmd_dict)

            self.last_left_direction = parsed_cmd['left_direction'] if parsed_cmd['left_direction'] is not None else self.last_left_direction
            self.last_left_velocity = parsed_cmd['left_velocity'] if parsed_cmd['left_velocity'] is not None else self.last_left_velocity
            self.last_right_direction = parsed_cmd['right_direction'] if parsed_cmd['right_direction'] is not None else self.last_right_direction
            self.last_right_velocity = parsed_cmd['right_velocity'] if parsed_cmd['right_velocity'] is not None else self.last_right_velocity
            self.last_speed = parsed_cmd['speed'] if parsed_cmd['speed'] is not None else self.last_speed
            self.last_head = parsed_cmd['heading'] if parsed_cmd['heading'] is not None else self.last_head
            self.last_tilt = parsed_cmd['servo_tilt'] if parsed_cmd['servo_tilt'] is not None else self.last_tilt
            self.last_pan = parsed_cmd['servo_pan'] if parsed_cmd['servo_pan'] is not None else self.last_pan
        

            tilt = MAX_TILT if tilt > MAX_TILT else MIN_TILT if tilt < MIN_TILT else tilt
            pan = MAX_PAN if pan > MAX_PAN else MIN_PAN if pan < MIN_PAN else pan

            self.move_servo(TILT_SERVO, tilt)
            self.move_servo(PAN_SERVO, pan)

            if (left_velocity > MAX_SPEED or right_velocity > MAX_SPEED):
                left_velocity = MAX_SPEED
                right_velocity = MAX_SPEED

            if (drive_mode == 'tank'):
                self.drive(int(left_direction), int(left_velocity), int(right_direction), int(right_velocity))
            elif(drive_mode == 'heading'):
                self.drive_with_heading(int(speed), int(head), 0)
        
        print("Rover not running anymore")

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
    rover_thread.join() 

    print("Rover stopped")


if __name__ == '__main__':
    main()
