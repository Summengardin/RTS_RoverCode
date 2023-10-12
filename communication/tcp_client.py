import socket

class tcp_client:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect(self, host, port):
        self.socket.connect((host, port))


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
    client = tcp_client()
    client.connect("localhost", 9090)
    client.send("Hello World!")
    print(client.recv())