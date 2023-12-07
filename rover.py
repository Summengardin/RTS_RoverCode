import argparse
import threading
import time
import sys

from communication.udp_client import PiCamStreamer
from rover_control import control


def mainCamera(ip):
    streamer = PiCamStreamer(server_address=(ip, 8080), resolution=(320, 240), framerate=30)
    print("Streaming to IP address:", ip)
    streamer.run()


def commsArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', type=str, help='IP address for the RPI to stream to.')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    ip = sys.argv[1] if len(sys.argv) > 1 else "10.22.192.34"
    # args = parse_args()
    # main(args)
    controller = control.Rover(ip)
    controller_thread = threading.Thread(target=controller.run)
    controller_thread.daemon = True
    controller_thread.start()

    camera_thread = threading.Thread(target=mainCamera, args=(ip,))
    camera_thread.daemon = True
    camera_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")


    controller.stop()
    controller_thread.join()
    camera_thread.join()

    print ("Done")
