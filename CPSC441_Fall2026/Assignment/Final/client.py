import socket
import threading

SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 6767
BUFFER_SIZE = 4096

# Recieve from server
def receive_line(conn, buffer):
    
    # Create Buffer for complete data recieved
    while b"\n" not in buffer:
        complete = conn.recv(BUFFER_SIZE)
        if not complete:
            return None, buffer
        buffer += complete
        
    # Split the buffer for next messages
    line, buffer = buffer.split(b"\n", 1)
    return line.decode("utf-8", errors="replace").rstrip("\r"), buffer

# Counter Buffer to ensure complete file transfer
def recieved_all(conn, count, buffer):
    # When buffer is less than message
    while len(buffer) < count:
        complete = conn.recv(min(BUFFER_SIZE, count - len(buffer)))
        
        # If not enough buffer
        if not complete:
            return False
        
        # Update buffer
        buffer += complete
    return buffer[:count], buffer[count:]

# Save the file to client
def save_file(filename, data):
    
    # Open file, and save
    with open("server_file_" + filename, "wb") as file_handling:
        file_handling.write(data)
        
    print("Saved as server_file_" + filename)

# Client Things
def main():
    
    # Initiate Socket
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    buffer = b""

    # Connect to server
    try:
        conn.connect((SERVER_HOST, SERVER_PORT))
        server_message, buffer = receive_line(conn, buffer)
        
        # If server sends nothing
        if server_message is None:
            print("Server closed the connection.")
            return

        # If server is full of clients
        if server_message.startswith("SERVER IS FULL:"):
            print(server_message[15:].strip())
            return
        
        # If the server does not send WELCOME
        if not server_message.startswith("WELCOME "):
            print(server_message)
            return

        # Tell client, its client_name
        client_name = server_message[8:]
        print(f"Hello, you are {client_name}")
        conn.sendall((client_name + "\n").encode("utf-8"))

        # Receive the ready message from the server
        server_is_ready, buffer = receive_line(conn, buffer)
        if server_is_ready is None:
            print("Server closed the connection.")
            return
        print(server_is_ready)

        # Possible client options
        print("Client Options: list | GET filename | exit")
        while True:
            message = input(client_name + "> ")
            conn.sendall((message + "\n").encode("utf-8"))

            # If the client wants to exit
            if message.strip().lower() == "exit":
                reply, buffer = receive_line(conn, buffer)
                if reply:
                    print(reply)
                break

            # If the client wants to list the files in the server
            if message.strip().lower() == "list":
                reply, buffer = receive_line(conn, buffer)
                if reply is None:
                    print("Server failed.")
                    break
                print(reply)
                continue

            # This removed bugs
            reply, buffer = receive_line(conn, buffer)
            if reply is None:
                print("Server failed.")
                break

            # If client repeats FILE header
            if reply.startswith("FILE "):
                handler = reply.split(" ", 2)
                if len(handler) != 3:
                    print("Invalid server header.")
                    break
                filename = handler[1]
                try:
                    file_size = int(handler[2])
                except ValueError:
                    print("Invalid file size.")
                    break

                # Get the file and save it
                file_data, buffer = recieved_all(conn, file_size, buffer)
                save_file(filename, file_data)
            else:
                print(reply)

    # If all else fails
    except (OSError, ConnectionError) as error:
        print("CONNECTION ERROR: " + str(error))
    
    # If CTRL + C is used
    except KeyboardInterrupt:
        print("\nClient interrupted.")
    
    # Close the connection
    finally:
        try:
            conn.close()
        except OSError:
            pass

if __name__ == "__main__":
    main()
