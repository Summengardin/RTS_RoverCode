import socket
import json
import time


class tcp_client:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.socket.connect((host, port))

    def close(self):
        self.socket.close()

    def send(self, data):
        msg = f"{data}".encode("utf-8")
        msg_size = len(msg)

        self.socket.send(msg_size.to_bytes(4, byteorder="little"))
        self.socket.send(msg)

    def recv(self):
        msg_size = int.from_bytes(self.socket.recv(4), byteorder="little")
        data = self.socket.recv(msg_size).decode("utf-8")

        return data


if __name__ == "__main__":
    
    print("Connecting to server...")
    client = tcp_client()
    client.connect("localhost", 9091)
    print("Connected!")

    while True:
        try:
            
            recv = client.recv()
            cmd_dict = json.loads(recv)
            print(cmd_dict)
            if cmd_dict['command'] == 'move':
                print("move")
                print(cmd_dict['speed'])
                print(cmd_dict['heading'])
            elif cmd_dict['command'] == 'stop':
                print("stop")

            dummy_data = {"temperature": 20, "humidity": 50}
            client.send(json.dumps(dummy_data))
        except KeyboardInterrupt:
            print("Closing connection...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)
            print("Connecting to server...")
            client = tcp_client()
            client.connect("localhost", 9091)
            print("Connected!")
            continue

        
