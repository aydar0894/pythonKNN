import cgi
import sys
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import pickle

class MainHandler(BaseHTTPRequestHandler):
	def do_GET(self):        
		parsed_path = urlparse(self.path)
		if parsed_path.query == '':
			return
		params = parsed_path.query.split(",")
		print(params)
		users = ann(45,int(params[0]),int(params[1]),int(params[2]))
		message_parts = str(users)       
		message = '\r\n'.join(message_parts)
		self.send_response(200)
		self.end_headers()
		self.wfile.write(str.encode(message))
		return

	def do_POST(self):
		a = 1

	def DoSomethingWithUploadedFile(self, groupId):
		ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
		query = cgi.parse_multipart(self.rfile, pdict)
		self.send_response(200)
		self.end_headers()
		fileContent = query.get('file')[0]
		# do something with fileContent
		self.wfile.write("POST OK.");

	def RedirectTo(self, url, timeout=0):
		self.wfile.write("""<html><head>
		 <meta HTTP-EQUIV="REFRESH"
			   content="%i; url=%s"/></head>""" % (timeout, url))

	def WriteCookie(self):
	   
		form = cgi.FieldStorage(headers=self.headers, fp=self.rfile,
		environ={'REQUEST_METHOD':'POST',
				'CONTENT_TYPE':self.headers['Content-Type']})

		val = form.getfirst('myvalue', None)
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		if val:
			c = Cookie.SimpleCookie()
			c['value'] = val
			self.send_header('Set-Cookie', c.output(header=''))
			self.end_headers()
			self.RedirectTo(form.getfirst('follow', '/'))
		else:
			self.end_headers()
			self.wfile.write("No username ?")

		def ReadCookie(self):
			if "Cookie" in self.headers:
				c = Cookie.SimpleCookie(self.headers["Cookie"])
				return c['value'].value
		return None

def main(port):
	try:
		server = HTTPServer(('', int(port)), MainHandler)
		print('started httpserver...')
		server.serve_forever()
	except KeyboardInterrupt:
		print('^C received, shutting down server')
		server.socket.close()
		
def ann(usersCount, tid, duration, timePeriod):
	with open('KNN_offers.pkl', 'rb') as f:
		clf = pickle.load(f)
	
	result = []
	for i in range(usersCount):
		tmp = []
		tmp.append(i)
		tmp.append(tid)
		tmp.append(duration)
		tmp.append(timePeriod)
		result.append(tmp)    
	Z = clf.predict(result)
	ret = []
	print(Z[0])
	k = 0
	for z in Z:
		if z[2] == 1:
			ret.append(k)   
		k = k+1
	return ret


# In[ ]:

main(8005)


# In[ ]:



