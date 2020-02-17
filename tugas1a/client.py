import sys
import socket


SERVER_ADDRESS = ('127.0.0.1', 10000)
BUFFER_SIZE = 32


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
print(f"connecting to {SERVER_ADDRESS}")
sock.connect(SERVER_ADDRESS)


filepath = sys.argv[1]
try:
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(BUFFER_SIZE), b''):
            sock.sendall(chunk)
        sock.shutdown(socket.SHUT_RD)

finally:
    print("closing")
    sock.close()
