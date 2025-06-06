import socket
from threading import Thread
import requests

host = 'localhost'
port = 8080

clients = {}
addresses = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#internet version 4, secure tcp stream
sock.bind((host,port))

sock.listen(1)

def broadcast(msg,prefix=""):
    for x in clients:
        x.send(bytes(prefix,"utf8" + msg))

def handle_clients(conn,address):
    name = conn.recv(1024).decode()
    welcome = f"Welcome {name}. You can type #quit if you want to leave this chat room"
    conn.send(bytes(welcome,"utf8"))
    msg = name + "Has just joined the chat room"
    broadcast(bytes(msg,"utf8 "))
    clients[conn] = name

    while True:
        msg = conn.recv(1024)
        if msg != bytes("#quit"):
            broadcast(msg,name+":")
        else:
            conn.send(bytes("#quit","utf8"))
            conn.close()
            del clients[conn]
            broadcast(bytes(name + "Has Left the Chat Room"))


def accept_client_connections():
    while True:
        client_conn, client_addr = sock.accept()
        print(client_addr, " Has Connected")
        client_conn.send("Welcome to the Chat Eoom, Please type your name to continue".encode("utf-8"))
        addresses[client_conn] = client_addr
        
        Thread(target=handle_clients,args=(client_conn,client_addr)).start()

if __name__ == "__main__":
    sock.listen(8)
    print("The server is running and is listening to client requests.")
    conn, address = sock.accept()

    t1 = Thread(target = accept_client_connections)
    t1.start()
    t1.join()

