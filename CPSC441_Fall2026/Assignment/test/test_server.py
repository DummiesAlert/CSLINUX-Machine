import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 6667
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'exit'

visitor_counter = 0
counter_lock = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    global visitor_counter

    # Assign a unique visitor number
    with counter_lock:
        visitor_counter += 1
        my_number = visitor_counter

    conn.send(
        f"Welcome! You are visitor number {my_number}".encode(FORMAT)
    )

    print(f"Visitor {my_number} connected from {addr}")

    connected = True

    try:
        while connected:
            data = conn.recv(2048).decode(FORMAT)

            # Client disconnected unexpectedly
            if not data:
                break

            if data == DISCONNECT_MESSAGE:
                connected = False
                conn.send("Server says: Goodbye!".encode(FORMAT))

            else:
                response = "Server says: " + data.upper()

                print(
                    f"Received from client: {data}\n"
                    f"Send: {response}"
                )

                conn.send(response.encode(FORMAT))

    finally:
        conn.close()
        print(f"Visitor {my_number} disconnected")


def start():
    server.listen()
    print(f"Shout Server listening on {ADDR} ...")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr)
        )

        thread.start()


try:
    start()
except KeyboardInterrupt:
    print("\nServer shutting down...")
finally:
    server.close()