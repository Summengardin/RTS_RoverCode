import socket

# Set the server IP and the port
server_ip = 'your_server_ip'
port = 8080

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Send data to server
    message = 'Hello, Server!'
    client_socket.sendto(message.encode(), (server_ip, port))

    # Receive response from server
    response, server = client_socket.recvfrom(4096)
    print(f"Server response: {response.decode()}")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    client_socket.close()
