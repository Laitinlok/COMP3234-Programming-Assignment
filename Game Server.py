import socket

import threading

class ServerThread(threading.Thread):
	def __init__(self, client):
		threading.Thread.__init__(self)
		self.client = client

	def run(self):
		connectionSocket, addr = self.client    
		rmsg = connectionSocket.recv(1024).decode()
		recv=rmsg.split()
		if recv[0]=="/login":
			username=recv[1]
			password=recv[2]
			userpass= username+":"+password
			f = open("UserInfo.txt", "r")
			i=0
			for x in f:
				if x==userpass:
					i=1
			if i==1:
				msg="1001 Authentication successful"
			else:
				msg="1002 Authentication failed"
		
class ServerMain:
	def server_run(self):  
		serverPort = 12000
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serverSocket.bind( ("", serverPort) )
		serverSocket.listen(5)
		print("The server is ready to receive")
		while True:
			client = serverSocket.accept()
			t = ServerThread(client)
			t.start()


if __name__ == '__main__':
	server = ServerMain()
	server.server_run()
