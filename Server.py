import cgi
import sys
import json
import pandas as pd
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from sklearn import neighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
import pickle

class MainHandler(BaseHTTPRequestHandler):
	def do_GET(self): 
	# if self.path == '/offers/':       
		parsed_path = urlparse(self.path)
		if parsed_path.query == '':
			return self.wfile.write(str.encode("error"))
		params = parsed_path.query.split(",")
		print(params)
		users = offers(45,int(params[0]),int(params[1]),int(params[2]))
		message_parts = str(users)       
		message = message_parts
		self.send_response(200)
		self.end_headers()
		self.wfile.write(str.encode(str(message).replace("[","").replace("]","")))
		return
		if self.path == '/spam_check/': 
			params = parsed_path.query
			message = spamRecog(params)
			result = ""
			if message[0] == "spam":
				result = "1"
			else:
				result = "0"
			self.send_response(200)
			self.end_headers()
			self.wfile.write(str.encode(result))
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

def spamRecog(descr):
	df = pd.read_csv('./SMSSpamCollection.csv', delimiter='\t',header=None)

	X_train_raw, X_test_raw, y_train, y_test = train_test_split(df[1],df[0])

	vectorizer = TfidfVectorizer()
	X_train = vectorizer.fit_transform(X_train_raw)
	classifier = LogisticRegression()
	classifier.fit(X_train, y_train)

	X_test = vectorizer.transform( [descr] )
	predictions = classifier.predict(X_test)
	return predictions
	
def offers(usersCount, tid, duration, timePeriod):
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



