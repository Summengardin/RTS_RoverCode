import socket
import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
from protobuf.my_messages_pb2 import VideoFeed, Instruction  # Generated from protoc
import time

# Initialize socket for UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 8080)
MAX_UDP_PACKET_SIZE = 65507  # Maximum size of a UDP packet

# Initialize the Raspberry Pi camera
camera = PiCamera()
camera.resolution = (640, 480)  # Set your desired resolution
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=camera.resolution)

# Allow the camera to warmup
time.sleep(0.1)

try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array  # Grab the numpy array representing the image

        # Your existing code for processing and sending the image
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
            if len(serialized_video_feed) <= MAX_UDP_PACKET_SIZE:
                break
            scale_factor -= 0.1  # Reduce scale factor

            if scale_factor <= 0.1:  # Prevent too small frames
                print("Frame too large to fit into UDP packet even after reducing resolution.")
                break

        # Send serialized video feed to the server
        sock.sendto(serialized_video_feed, server_address)

        # Receive instruction from server
        serialized_instruction, _ = sock.recvfrom(MAX_UDP_PACKET_SIZE)
        instruction = Instruction()
        instruction.ParseFromString(serialized_instruction)

        # Print received instruction - execute it if applicable
        print("Received instruction:", instruction.messageInstruction)

        # Clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Release resources
    camera.close()
    cv2.destroyAllWindows()
    sock.close()
