import socket

SERVER_ADDRESS = ('127.0.0.1', 10000)
BUFFER_SIZE = 1024

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

    rcv_fname = connection.recv(BUFFER_SIZE).decode()
    with open(f'recv/{rcv_fname}', 'wb+') as f:
        while True:
            data = connection.recv(BUFFER_SIZE)
            f.write(data)
            if not data:
                break

    connection.close()
