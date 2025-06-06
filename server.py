import socket
from threading import Thread

# Basic server config - nothing fancy here
HOST = 'localhost'
PORT = 8080

# Yeah I know global vars aren't great but it works
connected_clients = {}  # socket -> username mapping
client_addresses = {}   # socket -> address mapping

# Set up the main socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents "address already in use" errors
server_socket.bind((HOST, PORT))

def send_to_everyone(message, sender_prefix=""):
    # Send a message to all connected clients
    if sender_prefix:
        full_msg = sender_prefix + message
    else:
        full_msg = message
    
    # Keep track of dead connections
    dead_connections = []
    
    for client_socket in connected_clients:
        try:
            if isinstance(full_msg, str):
                client_socket.send(full_msg.encode("utf-8"))
            else:
                client_socket.send(full_msg)  # already bytes
        except Exception:
            # Connection is probably dead, mark for removal
            dead_connections.append(client_socket)
    
    # Clean up dead connections
    for dead_client in dead_connections:
        if dead_client in connected_clients:
            del connected_clients[dead_client]
        if dead_client in client_addresses:
            del client_addresses[dead_client]

def handle_client(client_conn, client_addr):
    # Deal with each client in their own thread
    username = None
    
    try:
        # First thing - get their name
        raw_name = client_conn.recv(1024).decode("utf-8")
        username = raw_name.strip()  # clean up any whitespace
        
        # Send them a welcome message
        welcome_text = f"Welcome {username}! Type #quit to leave the chat"
        client_conn.send(welcome_text.encode("utf-8"))
        
        # Let everyone know someone joined
        join_announcement = f"{username} joined the chat!"
        send_to_everyone(join_announcement)
        connected_clients[client_conn] = username
        
        # Main message loop
        while True:
            try:
                incoming_data = client_conn.recv(1024)
                if not incoming_data:  # empty message = client disconnected
                    break
                
                message_text = incoming_data.decode("utf-8")
                
                if message_text.strip() == "#quit":
                    # Client wants to leave
                    client_conn.send("#quit".encode("utf-8"))
                    break
                else:
                    # Regular message - broadcast it with their name
                    formatted_msg = f"{username}: {message_text}"
                    send_to_everyone(formatted_msg)
                    
            except socket.error:
                # Something went wrong with this client
                break
            except Exception as e:
                print(f"Unexpected error with client: {e}")
                break
                
    except Exception as err:
        print(f"Error setting up client {client_addr}: {err}")
    
    finally:
        # Cleanup time
        try:
            client_conn.close()
        except:
            pass  # don't care if close() fails
        
        # Remove from our tracking dicts
        if client_conn in connected_clients:
            username = connected_clients[client_conn]
            del connected_clients[client_conn]
            # Tell everyone they left
            send_to_everyone(f"{username} left the chat")
        
        if client_conn in client_addresses:
            del client_addresses[client_conn]
        
        print(f"Client {client_addr} disconnected")

def start_accepting_connections():
    # Main server loop - accept new connections
    while True:
        try:
            new_client, new_addr = server_socket.accept()
            print(f"New connection from {new_addr}")
            
            # Send initial prompt
            greeting = "Welcome! Please enter your username:"
            new_client.send(greeting.encode("utf-8"))
            
            client_addresses[new_client] = new_addr
            
            # Spin up a thread for this client
            client_thread = Thread(target=handle_client, args=(new_client, new_addr))
            client_thread.start()
            
        except Exception as e:
            print(f"Error accepting new connection: {e}")
            break

# Main execution
if __name__ == "__main__":
    server_socket.listen(8)  # allow up to 8 pending connections
    print("Chat server is running...")
    print(f"Listening on {HOST}:{PORT}")
    
    try:
        start_accepting_connections()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()