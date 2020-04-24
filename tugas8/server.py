import socket
import threading
import time
import sys
import logging
from http import HttpServer
from req import Request

httpserver = HttpServer()


class ProcessTheClient(threading.Thread):
	def __init__(self, connection, address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def run(self):
		rcv=""
		rbd=""
		time_to_read = False
		left_to_read = 1
		req=Request()
		while True:
			try:
				data = self.connection.recv(32)
				if data:
					d = data.decode()
					
					if time_to_read:
						print(rbd)
						rbd += d
					else:
						rcv+=d

					if rcv[-4:]=='\r\n\r\n':
						req.load_header(rcv)
						time_to_read=True
						left_to_read=req.headers.get('content-length')
						left_to_read=0 if left_to_read == None else int(left_to_read)

					if len(rbd) >= left_to_read:
						#end of command, proses string
						req.load_body(rbd)
						logging.warning("data dari client: {}" . format(rcv))
						hasil = httpserver.proses(req)
						hasil=hasil+"\r\n\r\n"
						logging.warning("balas ke  client: {}" . format(hasil))
						self.connection.sendall(hasil.encode())
						rcv=""
						self.connection.close()
					
				else:
					break
			except OSError as e:
				pass
		self.connection.close()



class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('127.0.0.1', 10002))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning("connection from {}".format(self.client_address))

			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()
			self.the_clients.append(clt)



def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()

