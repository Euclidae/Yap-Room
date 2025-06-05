import socket
import requests

host = 'localhost'
port = 8080\

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#internet version 4, secure tcp stream
sock.bind((host,port))

sock.listen(1)
conn, address = sock.accept()

message = "Hey, there is something important for you."

