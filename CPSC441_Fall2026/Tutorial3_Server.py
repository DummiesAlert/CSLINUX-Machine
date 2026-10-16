import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 6767
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "exit"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
print(f"[LISTENING] Server is listening on {ADDR}")

conn, addr = server.accept()
print(f"[NEW CONNECTION] {addr} connected.")

connected = True
while connected:
    data = conn.recv(2048).decode(FORMAT)
    
    if data == DISCONNECT_MESSAGE:
        connected = False
        conn.send("Goodbye!".encode(FORMAT))
    else:
        response = f"Received: {data.upper()}"
        print(f"[SERVER RESPONSE] Recieved From Client: {response}")
        conn.send(response.encode(FORMAT))

conn.close()
server.close()