import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 6767
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

visitor_count = 0
counter_lock = threading.Lock()

def handle_client(conn, addr):
    global visitor_count
    
    with counter_lock:
        visitor_count += 1
        my_number = visitor_count
        
    conn.send(f"[Server] You are visitor #{my_number}".encode(FORMAT))
    print(f"[Server] Client number {my_number} just connected from {addr}.")
    conn.close()
    
def start():
    server.listen()
    print(f"Visitor Counter Server listening on {ADDR}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()

if __name__ == "__main__":
    start()