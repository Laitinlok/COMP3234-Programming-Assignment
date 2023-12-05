import socket
import fileinput
import sys
import threading
import random
from datetime import datetime

class ServerThread(threading.Thread):
	def __init__(self, client):
		threading.Thread.__init__(self)
		self.client = client

	def run(self):
		def game(room,player):
			rmsg = connectionSocket.recv(1024).decode()
			recv=rmsg.split()
			if recv[0]=="/guess":
				if recv[2]=="true":
					games[room][player]==2
				if recv[2]=="false":
					games[room][player]==1
				if games[room][player]==games[room][player-1]:
					msg="3023 The result is a tie"
				elif games[room][player]==answer:
					msg="3021 You are the winner"
				elif games[room][player]!=answer:
					msg="3022 You lost the game"
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
			if i == 1:
				if recv[0]=="/list":
					msg="Room\tPlayers\n"
					i=0
					for room in rooms:
						i+=1
						msg+=str(i)+"\t"+str(room)
						connectionSocket.send(msg.encode('ascii'))
				if recv[0]=="/enter":
					if len(rooms)>=int(recv[1])-1:
						if rooms[int(recv[1])-1]==0:
							msg="3011 Wait"
							rooms[int(recv[1])-1]+=1
							connectionSocket.send(msg.encode('ascii'))
							roomwait(int(recv[1])-1)
						elif rooms[int(recv[1])-1]==1:
							msg="3012 Game started. Please guess true or false"
							rooms[int(recv[1])-1]+=1
							random.seed(datetime.now().timestamp())
							global answer
							answer=random.randint(1,2)
							connectionSocket.send(msg.encode('ascii'))
							game(int(recv[1])-1,1)
						else:
							msg="3013 The room is full"
							connectionSocket.send(msg.encode('ascii'))
					else:
						msg="3014 Invalid room"
		def roomwait(room):
			while rooms[room]!=2:
				continue
			msg="3012 Game started. Please guess true or false"
			game(room,0)
			connectionSocket.send(msg.encode('ascii'))

class ServerMain:
	def server_run(self):
		serverPort = 12000
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serverSocket.bind( ("", serverPort) )
		serverSocket.listen(5)
		print("The server is ready to receive")
		global rooms
		global games
		rooms=[0]
		games=[[]]
		while True:
			client = serverSocket.accept()
			t = ServerThread(client)
			t.start()
			j=0
			for room in rooms:
				if room == 2:
					i=1
				else:
					i=0
				j+=i
			if j==len(rooms):
				rooms.append(0)
				games.append([])


if __name__ == '__main__':
	server = ServerMain()
	server.server_run()
