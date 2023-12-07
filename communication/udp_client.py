import io
import socket
from picamera import PiCamera
from picamera.array import PiRGBArray
from protobuf.my_messages_pb2 import VideoFeed, Instruction
import time


class PiCamStreamer:
    def __init__(self, server_address=("10.22.192.34", 8080), resolution=(320, 240), framerate=30):
        self.server_address = server_address
        self.resolution = resolution
        self.framerate = framerate
        self.MAX_UDP_PACKET_SIZE = 65507  # Maximum size of a UDP packet
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Initialize the Raspberry Pi camera
        self.camera = PiCamera()
        self.camera.resolution = self.resolution
        self.camera.framerate = self.framerate

        # Warm up the camera
        self.camera.start_preview()
        time.sleep(2)
        self.camera.stop_preview()

    def stream_video(self):
        stream = io.BytesIO()
        for _ in self.camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            stream.truncate()
            stream.seek(0)

            image_bytes = stream.getvalue()
            if len(image_bytes) <= self.MAX_UDP_PACKET_SIZE:
                video_feed = VideoFeed()
                video_feed.messageFeed = image_bytes
                serialized_video_feed = video_feed.SerializeToString()

                try:
                    self.sock.sendto(serialized_video_feed, self.server_address)
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print("Image too large to send over UDP")

            if not self.running:
                break

            # Reset the stream for the next capture
            #stream.seek(0)
            #stream.truncate()
        
        print("Closing streamer")
        self.camera.close()
        stream.close()

    def run(self):
        self.running = True
        self.stream_video()

    def stop(self):
        self.running = False
        print("Closing socket...")
        self.socket.shutdown(socket.SHUT_RDWR)    
        self.sock.close()
        print("Closed")


if __name__ == "__main__":
    streamer = PiCamStreamer(server_address=("10.22.192.34", 8080))
    try:
        streamer.run()
    except KeyboardInterrupt:
        print("Stopping streamer")
    finally:
        streamer.stop()
