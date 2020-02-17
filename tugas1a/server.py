import sys
import socket

SERVER_ADDRESS = ('127.0.0.1', 10000)
BUFFER_SIZE = 32

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
print(f"starting up on {SERVER_ADDRESS}")
sock.bind(SERVER_ADDRESS)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print("waiting for a connection")
    connection, client_address = sock.accept()
    print(f"connection from {client_address}")

    with open('output', 'wb+') as f:
        while True:
            data = connection.recv(BUFFER_SIZE)
            print(f"received {data}")
            f.write(data)
            if not data:
                break

    connection.close()
