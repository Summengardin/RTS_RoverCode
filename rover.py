import argparse

from communication import udp_client
from communication import tcp_client

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    args = parser.parse_args()
    return args


def main(args):
    #tcp_client = tcp_client()
    streamer = PiCamStreamer(server_address=('192.168.1.10', 8080), resolution=(640, 480), framerate=30)
    streamer.run()

if __name__ == "__main__":
    args = parse_args()
    main(args)