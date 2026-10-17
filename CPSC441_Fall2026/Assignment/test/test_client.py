import socket

PORT = 6667
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "exit"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

connected = True
while connected:
    message = input("Enter message (type 'exit' to disconnect): ")
    client.send(message.encode(FORMAT))
    
    if message == DISCONNECT_MESSAGE:
        connected = False
        
    response =client.recv(2048).decode(FORMAT)
    print(f"Server response: {response}")
    
client.close()