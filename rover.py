print("Importing modules...")
import threading
import time
import sys

from communication.udp_client import PiCamStreamer
from rover_control import control


if __name__ == "__main__":
    print("Running... ctrl+c to exit")
    ip = sys.argv[1] if len(sys.argv) > 1 else "10.22.192.34"

    controller = control.Rover(ip)
    controller_thread = threading.Thread(name="controller_thread", target=controller.run)
    controller_thread.daemon = True
    controller_thread.start()

    stream = PiCamStreamer(server_address=(ip, 8080), resolution=(320, 240), framerate=30)
    stream_thread = threading.Thread(name="stream_thread", target=stream.run)
    stream_thread.daemon = True
    stream_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")

    stream.stop()
    stream_thread.join()
    controller.stop()
    controller_thread.join()
    
    print ("Goodbye!")

