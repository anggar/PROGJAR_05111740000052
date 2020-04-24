import sys
import os.path
import uuid
from glob import glob
from datetime import datetime

from req import Request

def html_tags(tag, el):
	return f"<{tag}>{el}</{tag}>"

class HttpServer:
	def __init__(self):
		self.sessions={}
		self.types={}
		self.types['.pdf']='application/pdf'
		self.types['.jpg']='image/jpeg'
		self.types['.txt']='text/plain'
		self.types['.html']='text/html'
	def response(self,kode=404,message='Not Found',messagebody='',headers={}):
		tanggal = datetime.now().strftime('%c')
		resp=[]
		resp.append("HTTP/1.0 {} {}\r\n" . format(kode,message))
		resp.append("Date: {}\r\n" . format(tanggal))
		resp.append("Connection: close\r\n")
		resp.append("Server: myserver/1.0\r\n")
		resp.append("Content-Length: {}\r\n" . format(len(messagebody)))
		for kk in headers:
			resp.append("{}:{}\r\n" . format(kk,headers[kk]))
		resp.append("\r\n")
		resp.append("{}" . format(messagebody))
		response_str=''
		for i in resp:	
			response_str="{}{}" . format(response_str,i)
		return response_str

	def proses(self,req: Request):
		# requests = data.split("\r\n")

		# baris = requests[0]
		#print(baris)

		# all_headers = [n for n in requests[1:] if n!='']

		# j = baris.split(" ")
		try:
			if (req.method=='GET'):
				return self.http_get(req)
			elif (req.method=='POST'):
				return self.http_post(req)
			else:
				return self.response(400,'Bad Request','',{})
		except IndexError:
			return self.response(400,'Bad Request','',{})
	def http_get(self,req: Request):
		files = glob('./*')
		thedir='.'
		if thedir+req.address not in files:
			return self.response(404,'Not Found','',{})
		fp = open(thedir+req.address,'r')
		isi = fp.read()
		
		fext = os.path.splitext(thedir+req.address)[1]
		content_type = self.types[fext]
		
		headers={}
		headers['Content-type']=content_type
		
		return self.response(200,'OK',isi,headers)
	def http_post(self,req: Request):
		marsh_p = lambda x: html_tags("p", x)
		
		content_h = [html_tags("h2", name) for name in ["Request Header", "Content"]]
		content_p = [
			"".join(list(map(marsh_p, req.headers_list))), 
			req.body]

		isi = ""
		for (x, y) in zip(content_h, content_p):
			isi += f"{x}{y}"

		headers={}
		headers['Content-type']=self.types['.html']
		return self.response(200,'OK',isi,headers)
		
			 	
#>>> import os.path
#>>> ext = os.path.splitext('/ak/52.png')

if __name__=="__main__":
	httpserver = HttpServer()
	# d = httpserver.proses('GET testing.txt HTTP/1.0')
	# print(d)