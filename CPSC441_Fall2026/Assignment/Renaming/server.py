import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 6767
MAX_CLIENTS = 3
BUFFER_SIZE = 4096

# Directory where downloadable server files are stored.
FOLDR = "files"

# Edit this list to match the files placed in the FOLDR directory.
# Example: create FOLDR/example.txt and keep "example.txt" in this list.
FOLDR_FILES = ["example.txt"]

# Active clients and the session cashe is locked by threading.Lock()
clients_lock = threading.Lock()

# List of active clients
active_clients = {}

# List of client session caches
client_cache = []
next_client_number = 1

def session_timestamp():
    # Threading uses Python's built-in monotonic clock
    return "session-clock=" + str(round(threading._time(), 3))

# Send Message type
def send_line(conn, message):
    conn.sendall((message + "\n").encode("utf-8"))

# Receive Message type
def receive_line(conn, buffer):
    
    # Create Buffer for complete data recieved
    while b"\n" not in buffer:
        complete = conn.recv(BUFFER_SIZE)
        if not complete:
            return None, buffer
        buffer += complete
    line, buffer = buffer.split(b"\n", 1)
    return line.decode("utf-8", errors="replace").rstrip("\r"), buffer

# Find List of files in FOLDR and send to client
def send_file_list(conn):
    try:
        
        entries = []
        for name in FOLDR_FILES:
            entries.append(name)
        if entries:
            send_line(conn, "FILES " + " | ".join(entries))
        else:
            send_line(conn, "FILES (FOLDR is empty)")
    except Exception:
        send_line(conn, "ERROR Could not list files in repo directory.")

# "Stream" or Send file to Client
def stream_file(conn, filename):
    if filename not in FOLDR_FILES:
        send_line(conn, "ERROR File not found: " + filename)
        return

    try: # Try opening file
        file_handling = open(FOLDR + "/" + filename, "rb")
        file_handling.close()
    
    except OSError: # Catch error if file cannot be found or cannot be opened
        send_line(conn, "ERROR File not found: " + filename)
        return

    try: # Try Reading and Sending file to client
        file_handling = open(FOLDR + "/" + filename, "rb")
        with file_handling:
            
            # Use Header for binary transfer
            file_handling.seek(0, 2)
            file_size = file_handling.tell()
            file_handling.seek(0)
            
            send_line(conn, "FILE " + filename + " " + str(file_size))
            
            while True:
                data = file_handling.read(BUFFER_SIZE)
                if not data:
                    break
                conn.sendall(data)
    
    except OSError: # Catch error if file cannot be read or sent
        try:
            send_line(conn, "ERROR Could not read file.")
        except OSError:
            pass

# Handle each client connection in a separate thread
def handle_client(conn, address, client_name):
    buffer = b""

    try: # Try to send welcome message and receive client name for handshake

        send_line(conn, "WELCOME " + client_name)

        # Client must send its assigned name back to complete the handshake.
        received_name, buffer = receive_line(conn, buffer)
        if received_name != client_name:
            send_line(conn, "ERROR Client {client_name} connection failed.")
            return

        send_line(conn, "CONNECTED! Use list, a filename, a message to send, or exit.")

        while True:
            message, buffer = receive_line(conn, buffer)
            
            # If no message recieved, break the loop and close the connection
            if message is None:
                break
            
            # Remove leading or trailing whitespace
            command = message.strip()
            
            # If client wants to exit
            if command.lower() == "exit":
                send_line(conn, "Connection closed. Goodbye!" + client_name)
                break
            
            # If client wants to list the files in server
            elif command.lower() == "list":
                send_line(conn, "List of files in server: ")
                send_file_list(conn)
            
            # If client wants to get a file from server
            elif command.startswith("GET "):
                stream_file(conn, command[4:].strip())
            
            # Else, send an acknowledgment for any other message from client
            else:
                send_line(conn, "ACK - " + message)

    # Catch connection errors
    except (ConnectionError, OSError):
        pass
    
    # Catch any other unexpected errors
    finally:
        disconnect = session_timestamp()
        
        try: # Try to close the connection
            conn.close()
            
        except OSError: # Catch error if connection cannot be closed
            pass
        
        # Update the active clients and client cache with the disconnect timestamp
        with clients_lock:
            active_clients.pop(client_name, None)
            
            # Update the disconnect timestamp in the client cache
            for cache in client_cache:
                if cache["name"] == client_name and cache["disconnect"] is None:
                    cache["disconnect"] = disconnect
                    break
        
        # Print the disconnect message to the console
        print(client_name + " disconnected from " + str(address) + " at " + disconnect)

def main():
    global next_client_number
    
    print("The FOLDR directory in the server: " + FOLDR)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    
    print("Server listening on " + HOST + ":" + str(PORT))
    print("Maximum simultaneous clients: " + str(MAX_CLIENTS))

    try:
        while True:
            conn, address = server.accept()
            with clients_lock:
                if len(active_clients) >= MAX_CLIENTS:
                    try:
                        send_line(conn, "FULL SERVER: MAXIMUM OF THREE CLIENTS REACHED!! TRY AGAIN LATER.")
                    except OSError:
                        pass
                    conn.close()
                    continue

                # Client number counter for each unique 1, 2, 3
                client_name = "Client" + str(next_client_number).zfill(2)
                next_client_number += 1
                accepted = session_timestamp()
                active_clients[client_name] = conn
                client_cache.append({
                    "name": client_name,
                    "address": str(address),
                    "accepted": accepted,
                    "disconnect": None
                })

            print(client_name + " connected from " + str(address) + " at " + accepted)
            thread = threading.Thread(
                target=handle_client,
                args=(conn, address, client_name),
                daemon=True
            )
            thread.start()

    except KeyboardInterrupt: # Catch CTRL + C to shutdown server
        print("\nServer shutting down.")
    
    finally: # Close the server and all active client connections
        server.close()
        with clients_lock:
            for conn in list(active_clients.values()):
                try:
                    conn.close()
                except OSError:
                    pass
            
            # Remove all active clients from the cache
            active_clients.clear()
            
        # Print the connection cache for this session
        print("Connection cache for this session:")
        for cache in client_cache:
            print(cache)

if __name__ == "__main__":
    main()
