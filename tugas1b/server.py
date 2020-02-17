import socket

SERVER_ADDRESS = ('127.0.0.1', 10001)
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

    filename = ""
    while True:
        data = connection.recv(BUFFER_SIZE)
        filename += data.decode()
        if not data:
            break

    try:
        with open(filename, 'rb') as f:
            connection.sendfile(f)
    except FileNotFoundError:
        connection.send("FILE NOT FOUND!!".encode())

    connection.close()
