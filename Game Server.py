import socket

import threading

class ServerThread(threading.Thread):
	def __init__(self, client):
		threading.Thread.__init__(self)
		self.client = client			
		
	def run(self):
		def enter(room):
			while True:
				rmsg = connectionSocket.recv(1024).decode()
				recv=rmsg.split()
				if recv[0]=="/list":
					f=open("Room"+room+".txt","r")
					players=f.read().splitlines()
					f.close()
					if len(players)==0:
						msg="3001 No players in this room"
					elif len(players)==1:
						msg="3001"+players[0]
					elif len(players)==2:
						msg="3001"+players[0]+players[1]
					connectionSocket.send(msg.encode('ascii'))
				elif recv[0]=="/enter":
					f=open("Rooms.txt", "r")
					rooms=f.read()
					lines=rooms.splitlines()
					verifyroom=lines[room].split()
					if verifyroom[2]=="0/2":
						msg="3011 Wait"
					elif verifyroom[2]=="0/2":
						msg="3012 Game started. Please guess true or false"
					else:
						msg="3013 The room is full"
					connectionSocket.send(msg.encode('ascii'))
				else:
					msg="4002 Unrecognized message"
					connectionSocket.send(msg.encode('ascii'))

		connectionSocket, addr = self.client
		while True:    
			rmsg = connectionSocket.recv(1024).decode()
			recv=rmsg.split()
			if recv[0]=="/login":
				username=recv[1]
				password=recv[2]
				userpass= username+":"+password
				f=open("UserInfo.txt", "r")
				userinfo=f.read()
				lines=userinfo.splitlines()
				i=0
				for line in lines:
					if line==userpass:
						i=1
				if i==1:
					msg="1001 Authentication successful"
				else:
					msg="1002 Authentication failed"
				connectionSocket.send(msg.encode('ascii'))
				f.close()
				f=open("Rooms.txt", "r")
				rooms=f.read()
				lines=rooms.splitlines()
				f.close()
				if len(lines)==1:
					f=open("Rooms.txt", "a")
					f.write("Room 1"+"\t"+"0/2"+"\n")
					f.close()
					f=open("Room1.txt", "w")
					f.close()
				for x in range (1, len(lines)):
					room=lines[x].split()
					if room[2]=="2/2":
						n=x+1
						f=open("Rooms.txt", "a")
						f.write("Room "+str(n)+"\t"+"0/2"+"\n")
						f.close()
						f=open("Room"+str(n)+".txt", "w")
						f.close()	
			elif recv[0]=="/list":
				print('Command Received')
				f=open("Rooms.txt", "r")
				rooms=f.read()
				connectionSocket.send(rooms.encode('ascii'))
				f.close()
			elif recv[0]=="/enter":
				f=open("Rooms.txt", "r")
				rooms=f.read()
				lines=rooms.splitlines()
				f.close()
				if len(recv)!=2:
					msg="Unkown message. Please specify your room."
					connectionSocket.send(msg.encode('ascii'))
				elif int(recv[1])>len(lines)-1:
					msg="Room does not exist. Please choose another one."
					connectionSocket.send(msg.encode('ascii'))
				else:
					room=recv[1]
					msg="Entering Room "+room+". Please use /enter to confirm"
					connectionSocket.send(msg.encode('ascii'))
					enter(room)
			else:
				msg="4002 Unrecognized message"
				connectionSocket.send(msg.encode('ascii'))
				
		
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
