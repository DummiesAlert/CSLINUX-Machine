import socket

PORT = 6767
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "exit"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

connected = True
while connected:
    message = input("Enter message: ")
    client.send(message.encode(FORMAT))
    
    if message == DISCONNECT_MESSAGE:
        connected = False
        
    response = client.recv(2048).decode(FORMAT)
    print(f"[SERVER RESPONSE] {response}")
    
client.close()