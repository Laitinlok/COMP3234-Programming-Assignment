import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverName = "127.0.0.1"
serverPort = 12000
clientSocket.connect( (serverName, serverPort) )
rmsg=""
while rmsg!="1001 Authentication successful":
	username= input("Please input your user name:")
	password=input("Please input your password:")
	msg="/login "+username+" "+password
	clientSocket.send(msg.encode('ascii'))
	rmsg = clientSocket.recv(1024).decode()
	print(rmsg)
while rmsg=="1001 Authentication successful":
	command=input("Please input your command:")
	clientSocket.send(command.encode('ascii'))