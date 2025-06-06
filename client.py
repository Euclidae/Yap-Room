import socket
import threading
import customtkinter as ctk
from datetime import datetime
import queue

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ChatClient:
    def __init__(self, host="localhost", port=8080):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.msgQueue = queue.Queue()  # mixed naming style
        
        self.window = ctk.CTk()
        self.window.title("Chat Room Application")
        self.window.geometry("600x500")
        self.window.resizable(True, True)
        
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        self.buildUI()
        
        self.running = True
        self.username = None
        
        recv_thread = threading.Thread(target=self.receiveMessages)
        recv_thread.daemon = True
        recv_thread.start()
        
        self.window.protocol("WM_DELETE_WINDOW", self.cleanup)
        self.checkMessages()
        self.askUsername()

    def buildUI(self):
        # chat area
        self.messageFrame = ctk.CTkFrame(self.window, fg_color="#1C2526")
        self.messageFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.messageFrame.grid_columnconfigure(0, weight=1)
        self.messageFrame.grid_rowconfigure(0, weight=1)
        
        self.chatBox = ctk.CTkTextbox(
            self.messageFrame,
            height=300,
            width=500,
            fg_color="#2D383A",
            text_color="#E0E0E0",
            font=("Arial", 12),
            wrap="word"
        )
        self.chatBox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.chatBox.configure(state="disabled")
        
        # scrollbar
        sb = ctk.CTkScrollbar(
            self.messageFrame,
            command=self.chatBox.yview,
            fg_color="#1C2526",
            button_color="#4A5A6B"
        )
        sb.grid(row=0, column=1, sticky="ns")
        self.chatBox.configure(yscrollcommand=sb.set)
        
        # input stuff
        inputFrame = ctk.CTkFrame(self.window, fg_color="#1C2526")
        inputFrame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        inputFrame.grid_columnconfigure(0, weight=1)
    
        self.msg_var = ctk.StringVar()  # inconsistent naming again
        self.textInput = ctk.CTkEntry(
            inputFrame,
            textvariable=self.msg_var,
            height=40,
            fg_color="#2D383A",
            text_color="#E0E0E0",
            font=("Arial", 12),
            placeholder_text="Type your message..."
        )
        self.textInput.grid(row=0, column=0, padx=(5, 0), pady=5, sticky="ew")
        self.textInput.bind("<Return>", self.on_enter)
        
        sendButton = ctk.CTkButton(
            inputFrame,
            text="Send",
            command=self.sendMsg,
            fg_color="#4A5A6B",
            hover_color="#5B6F8C",
            font=("Arial", 12, "bold")
        )
        sendButton.grid(row=0, column=1, padx=5, pady=5)
        
        # quit
        quitButton = ctk.CTkButton(
            self.window,
            text="Quit",
            command=self.cleanup,
            fg_color="#4A5A6B",
            hover_color="#5B6F8C",
            font=("Arial", 12, "bold")
        )
        quitButton.grid(row=2, column=0, padx=10, pady=5)

    def askUsername(self):
        try:
            dlg = ctk.CTkInputDialog(
                title="Username", 
                text="Enter your username:"
            )
            name = dlg.get_input()
            if name:
                self.username = name
            else:
                self.username = "Anon"  # back to original style
            self.sock.send(self.username.encode("utf-8"))
            self.showMessage(f"Connected as {self.username}")
        except Exception as e:
            self.showMessage("Error setting username: " + str(e))
            self.username = "Anon"
            try:
                self.sock.send(self.username.encode("utf-8"))
            except:
                pass

    def showMessage(self, msg):
        self.chatBox.configure(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chatBox.insert("end", "[" + timestamp + "] " + msg + "\n")  # different string formatting
        self.chatBox.see("end")
        self.chatBox.configure(state="disabled")

    def queueMsg(self, msg):
        self.msgQueue.put(msg)

    def checkMessages(self):
        try:
            while True:
                msg = self.msgQueue.get_nowait()
                self.showMessage(msg)
        except queue.Empty:
            pass
        
        if self.running:
            self.window.after(100, self.checkMessages)  # could have been variable

    def receiveMessages(self):
        while self.running:
            try:
                data = self.sock.recv(1024).decode("utf-8")
                if data:
                    self.queueMsg(data)
            except Exception as e:
                if self.running:  # forgot to check this in some places
                    self.queueMsg("Connection error: " + str(e))
                break

    def on_enter(self, event):  # separate method for enter key
        self.sendMsg()

    def sendMsg(self):
        text = self.msg_var.get().strip()
        if len(text) == 0:  # different way to check empty
            return
            
        try:
            self.sock.send(text.encode("utf-8"))
            
            if text != "#quit":
                self.showMessage("You: " + text)
            
            self.msg_var.set("")
            
            if text == "#quit":
                self.cleanup()
        except Exception as e:
            self.showMessage("Send failed: " + str(e))

    def cleanup(self):
        self.running = False
        try:
            self.sock.send("#quit".encode("utf-8"))
        except:
            pass
        try:
            self.sock.close()
        except:
            pass
        self.window.destroy()

    def run(self):  # back to original method name
        self.window.mainloop()

if __name__ == "__main__":
    client = ChatClient()
    client.run()