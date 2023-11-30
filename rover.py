import argparse
import threading
import time

from communication.udp_client import PiCamStreamer
from rover_control import control


def mainCamera(args):
    streamer = PiCamStreamer(server_address=(args.ip, 8080), resolution=(320, 240), framerate=30)
    streamer.run()


def commsArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', type=str, help='IP address for the RPI to stream to.')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = commsArgs()
    if args.ip == '':
        args.ip = '10.22.192.34'
    # args = parse_args()
    # main(args)
    controller = control.Rover(args.ip, 9091)
    controller_thread = threading.Thread(target=controller.run)
    controller_thread.daemon = True
    controller_thread.start()

    camera_thread = threading.Thread(target=mainCamera, args=(args,))
    camera_thread.daemon = True
    camera_thread.start()
    
    print("Streaming to IP address:", args.ip)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")


    controller.stop()
    controller_thread.join()
    camera_thread.join()

    print ("Done")
