import argparse

from communication.udp_client import PiCamStreamer

def mainCamera(args):
    streamer = PiCamStreamer(server_address=(args.ip, 8080), resolution=(320, 240), framerate=30)
    streamer.run()

def comms_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', type=str, help='IP address for the RPI to stream to.')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    #args = parse_args()
    #main(args)
    args = comms_args()
    print("Streaming to IP address:", args.ip)
    mainCamera(args)