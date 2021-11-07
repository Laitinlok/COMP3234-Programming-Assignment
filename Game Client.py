import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverName = "127.0.0.1"
serverPort = 12000
clientSocket.connect( (serverName, serverPort) )
username= input("Please input your user name:")
password=input("Please input your password:")
msg="/login "+username+" "+password
clientSocket.send(msg.encode('ascii'))
rmsg = clientSocket.recv(1024).decode
print(rmsg)