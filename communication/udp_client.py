import socket
import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
from protobuf.my_messages_pb2 import VideoFeed, Instruction  # Generated from protoc
import time

class PiCamStreamer:
    def __init__(self, server_address=('127.0.0.1', 8080), resolution=(640, 480), framerate=32):
        self.server_address = server_address
        self.resolution = resolution
        self.framerate = framerate
        self.MAX_UDP_PACKET_SIZE = 65507  # Maximum size of a UDP packet
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Initialize the Raspberry Pi camera
        self.camera = PiCamera()
        self.camera.resolution = self.resolution
        self.camera.framerate = self.framerate
        self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        time.sleep(0.1)  # Allow the camera to warm up

    def stream_video(self):
        try:
            for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                image = frame.array  # Grab the numpy array representing the image
                scale_factor = 1.0
                while True:
                    # Resize frame with the current scaling factor
                    dim = (int(image.shape[1] * scale_factor), int(image.shape[0] * scale_factor))
                    resized_frame = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
                    # Encode frame to JPEG format
                    is_success, buffer = cv2.imencode(".jpg", resized_frame)

                    if not is_success:
                        print("Failed to encode image!")
                        break

                    # Serialize frame data to protobuf
                    video_feed = VideoFeed()
                    video_feed.messageFeed = buffer.tobytes()
                    serialized_video_feed = video_feed.SerializeToString()

                    # Check if the serialized data fits in one UDP packet
                    if len(serialized_video_feed) <= self.MAX_UDP_PACKET_SIZE:
                        break
                    scale_factor -= 0.1  # Reduce scale factor

                    if scale_factor <= 0.1:  # Prevent too small frames
                        print("Frame too large to fit into UDP packet even after reducing resolution.")
                        break

                # Send serialized video feed to the server
                self.sock.sendto(serialized_video_feed, self.server_address)

                # Receive instruction from server
                serialized_instruction, _ = self.sock.recvfrom(self.MAX_UDP_PACKET_SIZE)
                instruction = Instruction()
                instruction.ParseFromString(serialized_instruction)

                # Print received instruction - execute it if applicable
                print("Received instruction:", instruction.messageInstruction)

                # Clear the stream in preparation for the next frame
                self.rawCapture.truncate(0)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            # Release resources
            self.camera.close()
            cv2.destroyAllWindows()
            self.sock.close()

    def run(self):
        self.stream_video()

# If you want the script to start streaming as soon as it is run, include this at the end of your file
if __name__ == "__main__":
    streamer = PiCamStreamer(server_address=('127.0.0.1', 8080))
    streamer.run()
