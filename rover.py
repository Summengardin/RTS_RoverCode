import argparse

from communication.udp_client import PiCamStreamer

def mainCamera(args):
    streamer = PiCamStreamer(server_address=(args.ip, 8080), resolution=(320, 240), framerate=30)
    streamer.run()

def commsArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', type=str, help='IP address for the RPI to stream to.')
    args = parser.parse_args()
    return args

def testComms ():
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 8080))
    s.listen(1)
    print("Listening on port 8080...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")


if __name__ == "__main__":
    #args = parse_args()
    #main(args)
    # args = commsArgs()
    # print("Streaming to IP address:", args.ip)
    # mainCamera(args)
    testComms()