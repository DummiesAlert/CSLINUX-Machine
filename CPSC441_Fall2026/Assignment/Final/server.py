import socket
import threading
import os

SERVER_HOST = socket.gethostbyname(socket.gethostname())
PORT = 6767
MAX_CLIENTS = 3
BUFFER_SIZE = 4096

# repo holds server files
REPO = "repo"

# Locks clients list to prevent race conditions
clients_lock = threading.Lock()

# List of active clients
active_clients = {}

# List of client cache
client_cache = []

# Tracks client number
next_client_number = 1

# Threading uses Python's built-in monotonic clock
# Tracks the when each client connects and disconnects from the server
def session_login_time():
    return "session-time=" + str(round(threading._time(), 3))

# Set Send Message type
def send_message(conn, message):
    conn.sendall((message + "\n").encode("utf-8"))

# Receive Message type
def recieve_message(conn, buffer):
    # Create a Buffer to wait for all the data
    while b"\n" not in buffer:
        complete = conn.recv(BUFFER_SIZE)
        if not complete:
            return None, buffer
        buffer += complete
        
    # Split the buffer for next messages
    line, buffer = buffer.split(b"\n", 1)
    return line.decode("utf-8", errors="replace").rstrip("\r"), buffer

# Get the list of files in REPO
def send_file_list(conn):
    
    # Find all files in repo
    try:
        # Store all files in repo
        current_files = []
        
        # Search for repo
        if os.path.exists(REPO) and os.path.isdir(REPO):
            
            # Get the files
            for files in os.listdir(REPO):
                path = os.path.join(REPO, files)
            
                # Add them to current_files
                if os.path.isfile(path):
                    current_files.append(files)

        # Return files in Repo, unless it is empty
        if current_files:
            send_message(conn, "FILES " + " | ".join(current_files))
        else:
            send_message(conn, "FILES WARNING! There are not files in REPO")
    
    # Catch any unexpected errors
    except Exception:
        send_message(conn, "ERROR - Could not retrieve file(s) list.")

# "Stream" or Send file to Client
def stream_file(conn, filename):

    # Try Reading and Sending file to client
    try:
        path = os.path.join(REPO, filename)
        
        if not os.path.isfile(path):
            send_message(conn, f"ERROR File not found: {filename}")
            return
        
        with open(path, "rb") as file_handling:
            
            # Use Header
            file_handling.seek(0, 2)
            file_size = file_handling.tell()
            file_handling.seek(0)
            
            send_message(conn, f"FILE {filename} {str(file_size)}")
            
            while True:
                data = file_handling.read(BUFFER_SIZE)
                if not data:
                    break
                conn.sendall(data)
    
    # If file can not read
    except OSError:
        try:
            send_message(conn, "ERROR Could not read file.")
        
        except OSError:
            pass

# Multi-Threading clients
def handle_client(conn, address, client_name):
    buffer = b""

    # Establish connection/handshake
    try:

        # Welcome the client
        send_message(conn, f"WELCOME {client_name}")
        
        # Get Client Name to verify
        received_name, buffer = recieve_message(conn, buffer)
        if received_name != client_name:
            send_message(conn, "ERROR {client_name} connection failed.")
            return

        # Client is connected
        send_message(conn, f"{client_name} CONNECTED to {SERVER_HOST}: {str(PORT)}! Use list to list files, GET server files, send any message, or exit.")

        # Things Client can do
        while True:
            message, buffer = recieve_message(conn, buffer)
            
            # If no message recieved, break
            if message is None:
                break
            
            # Remove any whitespace
            command = message.strip()
            
            # If client wants to exit, break
            if command.lower() == "exit":
                send_message(conn, f"Connection closed. Goodbye {client_name}!")
                break
            
            # If client wants to list the files
            elif command.lower() == "list":
                send_file_list(conn)
            
            # If client wants to get a file
            elif command.upper().startswith("GET "):
                stream_file(conn, command[4:].strip())
            
            # If client sends any message
            else:
                send_message(conn, f"Server ACK - {message}")

    # Catch any other unexpected errors
    finally:
        disconnect = session_login_time()

        # If the client sends no message or wants to exit
        # Close the connection
        try:
            conn.close()
        
        # If connection cannot be closed
        except OSError:
            pass
        
        # Update the active clients
        with clients_lock:
            
            # Remove client
            active_clients.pop(client_name, None)
            
            # Update the disconnect timestamp
            for cache in client_cache:
                if cache["name"] == client_name and cache["disconnect"] is None:
                    cache["disconnect"] = disconnect
                    break
        
        # Print successful disconnect
        print(f"Current Active Clients {active_clients}")
        print(f"{client_name} disconnected from {str(address)} at {disconnect}")

def main():
    global next_client_number
    
    print(f"The directory in the server is: {REPO}")

    # Initiate Socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_HOST, PORT))
    server.listen()
    
    print(f"Server listening on {SERVER_HOST}: {str(PORT)}")
    print(f"Maximum of simultaneous clients: {str(MAX_CLIENTS)}")

    try:
        while True:
            conn, address = server.accept()
            with clients_lock:
                if len(active_clients) >= MAX_CLIENTS:
                    try:
                        send_message(conn, "SERVER IS FULL: MAXIMUM OF THREE CLIENTS REACHED!! PLEASE TRY AGAIN LATER.")
                    except OSError:
                        pass
                    conn.close()
                    continue
                
                # Client number counter
                client_name = f"Client{next_client_number:02d}"
                next_client_number += 1
                accepted = session_login_time()
                
                active_clients[client_name] = conn
                client_cache.append({
                    "name": client_name,
                    "address": str(address),
                    "accepted": accepted,
                    "disconnect": None
                })

            print(f"Current Active Clients {active_clients}")
            print(f"{client_name} connected from {address} at {accepted}")
            
            threading.Thread(target=handle_client, args=(conn, address, client_name), daemon=True).start()

    # If CTRL + C is used
    except KeyboardInterrupt:
        print("\nSERVER CLOSED!.")
    
    # Close the server
    finally:
        server.close()
        with clients_lock:
            for conn in active_clients.values():
                try:
                    conn.close()
                except OSError:
                    pass
            # Remove all active clients
            active_clients.clear()
            
        # Print session cache
        print("Connection cache for this session:")
        for cache in client_cache:
            print(cache)

if __name__ == "__main__":
    main()
