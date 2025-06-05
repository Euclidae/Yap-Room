import socket
import requests

host = 'localhost'
port = 8080\

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#internet version 4, secure tcp stream
sock.bind((host,port))

sock.listen(1)
print("The server is running and is listening to client request")
conn, address = sock.accept()

message = "Hey, there is something important for you."
conn.send(message,message.encode())

conn.close()
