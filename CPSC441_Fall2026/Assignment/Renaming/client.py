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
    line, buffer = buffer.split(b"\n", 1)
    return line.decode("utf-8", errors="replace").rstrip("\r"), buffer

# Counter Buffer to ensure complete file transfer
def receive_exactly(conn, count, buffer):
    while len(buffer) < count:
        complete = conn.recv(min(BUFFER_SIZE, count - len(buffer)))
        if not complete:
            raise ConnectionError("Connection closed during file transfer.")
        buffer += complete
    return buffer[:count], buffer[count:]

# Save the file to client directory with prefix "downloaded_"
def save_received_file(filename, data):
    with open("downloaded_" + filename, "wb") as file_handling:
        file_handling.write(data)
    print("Saved as downloaded_" + filename)

# Client Things
def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    buffer = b""

    try: # Try to connect to the server to complete handshake
        conn.connect((SERVER_HOST, SERVER_PORT))
        first_message, buffer = receive_line(conn, buffer)
        
        # If server sends nothing, print the message and exit
        if first_message is None:
            print("Server closed the connection.")
            return

        # If server is full, print the message and exit
        if first_message.startswith("FULL "):
            print(first_message[5:])
            return
        
        # If the server does not send a welcome message, print the message and exit
        if not first_message.startswith("WELCOME "):
            print(first_message)
            return

        client_name = first_message[8:]
        print("Connected as " + client_name)
        conn.sendall((client_name + "\n").encode("utf-8"))

        # Receive the ready message from the server
        ready_message, buffer = receive_line(conn, buffer)
        if ready_message is None:
            print("Server closed the connection.")
            return
        print(ready_message)

        print("Commands: list | GET filename | exit")
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
                    print("Server disconnected.")
                    break
                print(reply)
                continue

            # If the client wants to get a file from the server
            if message.startswith("GET "):
                requested_name = message[4:].strip()
            else:
                requested_name = message.strip()

            # Receive the server's response to the GET request
            reply, buffer = receive_line(conn, buffer)
            if reply is None:
                print("Server disconnected.")
                break

            # If the server responds with a file header, process the file transfer
            if reply.startswith("FILE "):
                fields = reply.split(" ", 2)
                if len(fields) != 3:
                    print("Invalid file header from server.")
                    break
                filename = fields[1]
                try:
                    file_size = int(fields[2])
                except ValueError:
                    print("Invalid file size from server.")
                    break

                # Receive the file data and save it
                file_data, buffer = receive_exactly(conn, file_size, buffer)
                save_received_file(filename, file_data)
            else:
                print(reply)

    # Handle connection errors
    except (OSError, ConnectionError) as error:
        print("Connection error: " + str(error))
    
    # If used CTRL + C to exit the client, print a message
    except KeyboardInterrupt:
        print("\nClient interrupted.")
    
    # Close the connection to the server
    finally:
        try:
            conn.close()
        except OSError:
            pass

if __name__ == "__main__":
    main()
