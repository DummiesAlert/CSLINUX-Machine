import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 6767
ADDR = (HOST, PORT)
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(ADDR)
    message = client.recv(2048).decode(FORMAT)
    print(message)

except ConnectionRefusedError:
    print("Could not connect to the server.")

except Exception as e:
    print(f"Error: {e}")

finally:
    client.close()
    
# IF WAS ON THE SAME PC

import socket

HOST = socket.gethostbyname(socket.gethostname()) # or "127.0.0.1"
PORT = 6767
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))
    print(client.recv(2048).decode(FORMAT))
    
    # OR THIS
    # message = client.rev(2048).decode(FORMAT)
    # print(message)

except ConnectionRefusedError:
    print("Could not connect to the server.")

except Exception as e:
    print(f"Error: {e}")

finally:
    client.close()