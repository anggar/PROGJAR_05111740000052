import sys
import socket


SERVER_ADDRESS = ('127.0.0.1', 10001)
BUFFER_SIZE = 32


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
print(f"connecting to {SERVER_ADDRESS}")
sock.connect(SERVER_ADDRESS)


filepath = sys.argv[1]
try:
    sock.send(filepath.encode())
    sock.shutdown(socket.SHUT_WR)  # stop sending
    with open(f'requested/{filepath}', 'wb+') as f:
        while True:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                break
            f.write(data)

    # sock.shutdown(socket.SHUT_RD)

finally:
    print("closing")
    sock.close()
