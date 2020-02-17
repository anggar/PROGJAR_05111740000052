import sys
import socket


SERVER_ADDRESS = ('127.0.0.1', 10000)
BUFFER_SIZE = 1024


filepath = sys.argv[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # create TCP/IP socket
    sock.connect(SERVER_ADDRESS)
    print(f"Connecting to {SERVER_ADDRESS}")

    with open(filepath, 'rb') as f:
        sock.sendfile(f)
        sock.shutdown(socket.SHUT_RD)
