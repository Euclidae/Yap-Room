import socket
from threading import Thread
from tkinter import *

def receive():
    while True:
        try:
            msg = socket.recv(1024).dpyecode("utf8")
            msg_list.insert(END,msg)
        except:
            print("There is an Error receiving the message") 
def send():
    msg = my_msg.get()
    my_msg.set("")
    socket.send(bytes(msg,"utf8"))
    
    if msg=="#quit":
        socket.close()
        window.close()


def on_closing():
    my_msg.set("#quit")
    send()

window = Tk()
window.title("Chat Room Application")
window.configure(bg="blue")

message_frame = Frame(window,height=100,width=100,bg="indigo")
message_frame.pack()

my_msg=StringVar()
my_msg.set("")

scroll_bar = Scrollbar(message_frame)
msg_list = Listbox(message_frame,height=15,width=100,bg="orange",yscrollcommand=scroll_bar.set)
scroll_bar.pack(side=RIGHT,fill=Y)

msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()

label = Label(window,text="Enter the Message", fg = 'blue', font='Aeria',bg='blue')
label.pack()

entry_field = Entry(window,textvariable=my_msg,fg='blue',width=50)
entry_field.pack()

send_button = Button(window,text='Send',font="Aerial",fg="white",command=send)
send_button.pack()

quit_button = Button(window,text="Quit",font="Aerial",fg="white",command=on_closing)
quit_button.pack()

host = "localhost"
port = 8080

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((host,port))

receive_thread = Thread(target=receive)
receive_thread.start()

message = sock.recv(1024)#this is in bytes

while message:
    print("Message Received : ", message.decode())
    message = sock.recv(1024)#this is in bytes

sock.close()

mainloop()

