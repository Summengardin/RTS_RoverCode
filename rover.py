import argparse

from communication.udp_client import PiCamStreamer

def mainCamera(args):
    streamer = PiCamStreamer(server_address=(args.ip, 8080), resolution=(160, 120), framerate=30)
    streamer.run()

def commsArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', type=str, help='IP address for the RPI to stream to.')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    #args = parse_args()
    #main(args)
    args = commsArgs()
    print("Streaming to IP address:", args.ip)
    mainCamera(args)