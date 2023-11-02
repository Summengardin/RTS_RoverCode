import argparse

from communication.udp_client import PiCamStreamer
from communication import udp_client
from communication import tcp_client

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    args = parser.parse_args()
    return args


#def main(args):
#    tcp_client = tcp_client()

def mainCamera(args):
    streamer = PiCamStreamer(server_address=(args.ip, 8080), resolution=(640, 480), framerate=30)
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
    mainCamera(args)