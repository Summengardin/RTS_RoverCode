print("Starting rover... Importing modules")

import sys

sys.path.append('/home/MartinElias/dev/dependencies/sphero-sdk-raspberrypi-python/')
sys.path.append('/home/MartinElias/dev/')
sys.path.append('/home/MartinElias/dev/RTS_RoverCode/')

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
MAX_TILT = 180
MIN_TILT = -50
MAX_PAN = 180
MIN_PAN = 0

rvr = SpheroRvrObserver()

prev_time = 0



def parse_cmd_dict(cmd_dict) -> dict:
    '''
    Parses the json-command and returns a dictionary with the commands.
    If a command is not included in the json, it returns None for that command.
    '''
    parsed_cmd = {
        "drive_mode": cmd_dict.get('drive_mode'),
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


class Rover():
    def __init__(self, ip) -> None:
        self.rvr = SpheroRvrObserver()
        self.set_all_leds_rgb(255,125,0)

        # Initialize last known states
        self.last_drive_mode = 'tank'
        self.last_left_direction = 0
        self.last_left_velocity = 0
        self.last_right_direction = 0
        self.last_right_velocity = 0
        self.last_speed = 0
        self.last_head = 0
        self.last_tilt = 30
        self.last_pan = 40

        self.servos = pi_servo_hat.PiServoHat()
        self.servos.restart()
        self.move_servo(TILT_SERVO, self.last_tilt)
        self.move_servo(PAN_SERVO, self.last_pan, 180)

        #self.Blinker = blinker.Blinker(1)
        self.rvr.wake()
        time.sleep(2)
        #self.reset_heading()
        #self.sensor_control.add_sensor_data_handler('IMU', imu_handler)
        #self.sensor_control.add_sensor_data_handler('Accelerometer', accelerometer_handler)
        #self.sensor_control.add_sensor_data_handler('Velocity', velocity_handler)
        #print(f"Supported: {self.rvr.sensor_control.supported_sensors}")
        #print(f"Enabled: {self.rvr.sensor_control.enabled_sensors}")
        ##self.sensor_control.start(interval=1000)

        self.controller_ip = ip
        self.controller_port = 9091
        self.connect(self.controller_ip, self.controller_port)
        self.running = False


    def __del__(self):
        self.stop()

    def connect(self, host, port):
        print(f"Connecting to server at: {host}:{port}...")
        self.client = tcp_client.tcp_client()
        self.client.connect(host, port)
        print(f"Connected")
        self.set_all_leds_rgb(0,255,0)

    def stop(self):
        self.running = False
        try:
            self.set_all_leds_rgb(255,0,0)
        except Exception as e:
            print(f"Error setting leds: {e}")
        print("Closing connection...")
        try:
            self.client.close()
        except Exception as e:
            print(f"Error closing connection: {e}")
        print("Closed")
        print("Closing rover...")
        try:
            self.rvr.close()
        except Exception as e:
            print(f"Error closing rover: {e}")
        print("Closed")  

    def drive_rover(self, left_dir, left_vel, right_dir, right_vel):
        self.rvr.raw_motors(left_dir, left_vel, right_dir, right_vel)

    def stop_rover(self):
        self.drive_rover(0,0,0,0)

    def move_servo(self, servo, position, swing = 90):
        print(f"Moving servo {servo} to position {position}")
        self.servos.move_servo_position(servo, position, swing)

    def recv_message(self):
        try:
            return self.client.recv()
        except:
            return ""


    def run(self):
        self.running = True
        try:
            while self.running:

                try:
                    recv = self.client.recv()
                except:
                    print("Connection lost, reconnecting...")
                    self.stop_rover()
                    time.sleep(3)
                    self.connect(self.controller_ip, self.controller_port)
                    continue
                
                if recv == "":
                    break

                try:
                    cmd_dict = json.loads(recv)
                except:
                    print("Error parsing json")
                    continue

                print(cmd_dict)

                #drive_mode, left_direction, left_velocity, right_direction, right_velocity, speed, head, tilt, pan = parse_cmd(cmd_dict)
                parsed_cmd = parse_cmd_dict(cmd_dict)
                self.__update_commands(parsed_cmd)

                
        
                self.tilt = MAX_TILT if self.tilt > MAX_TILT else MIN_TILT if self.tilt < MIN_TILT else self.tilt
                self.pan = MAX_PAN if self.pan > MAX_PAN else MIN_PAN if self.pan < MIN_PAN else self.pan

                if (self.last_tilt != self.tilt):
                    self.move_servo(TILT_SERVO, self.tilt)
                if (self.pan != self.last_pan):
                    self.move_servo(PAN_SERVO, self.pan, 180)

                if (self.left_velocity > MAX_SPEED or self.right_velocity > MAX_SPEED):
                    self.left_velocity = MAX_SPEED
                    self.right_velocity = MAX_SPEED

                if self.drive_mode == 'tank':
                    self.drive_rover(int(self.left_direction), int(self.left_velocity), int(self.right_direction), int(self.right_velocity))
                elif self.drive_mode == 'heading':
                    self.rvr.drive_with_heading(int(self.speed), int(self.heading), 0)

                self.last_drive_mode = self.drive_mode
                self.last_left_direction = self.left_direction
                self.last_left_velocity = self.left_velocity
                self.last_right_direction = self.right_direction
                self.last_right_velocity = self.right_velocity
                self.last_speed = self.speed
                self.last_head = self.head
                self.last_tilt = self.tilt
                self.last_pan = self.pan
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Error: {e}")
        print("Rover not running anymore")

    def set_all_leds_rgb(self, r, g, b):
        self.rvr.set_all_leds(
            RvrLedGroups.all_lights.value,
            [color for x in range(0, 10) for color in [r, g, b]]
        )


    def __update_commands(self, cmd_dict):
            self.drive_mode = cmd_dict['drive_mode'] if cmd_dict['drive_mode'] is not None else self.last_drive_mode
            self.left_direction = int(cmd_dict['left_direction']) if cmd_dict['left_direction'] is not None else self.last_left_direction
            self.left_velocity = int(cmd_dict['left_velocity']) if cmd_dict['left_velocity'] is not None else self.last_left_velocity
            self.right_direction = int(cmd_dict['right_direction']) if cmd_dict['right_direction'] is not None else self.last_right_direction
            self.right_velocity = int(cmd_dict['right_velocity']) if cmd_dict['right_velocity'] is not None else self.last_right_velocity
            self.speed = int(cmd_dict['speed']) if cmd_dict['speed'] is not None else self.last_speed
            self.head = int(cmd_dict['heading']) if cmd_dict['heading'] is not None else self.last_head
            self.tilt = int(cmd_dict['servo_tilt']) if cmd_dict['servo_tilt'] is not None else self.last_tilt
            self.pan = int(cmd_dict['servo_pan']) if cmd_dict['servo_pan'] is not None else self.last_pan
            



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
