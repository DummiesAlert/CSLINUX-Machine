import socket
import threading
import json
from datetime import datetime
from pathlib import Path

# ---------------- Configuration ----------------

HOST = socket.gethostbyname(socket.gethostname())
PORT = 6667
ADDR = (HOST, PORT)
FORMAT = "utf-8"
BUFFER_SIZE = 4096
MAX_CLIENTS = 3
DISCONNECT_MESSAGE = "exit"

# Store shared server state safely across threads.
counter_lock = threading.Lock()
active_clients = 0
visitor_counter = 0
client_history = []

# Files available for download are stored here.
REPOSITORY = Path(__file__).resolve().parent / "aaa"
REPOSITORY.mkdir(parents=True, exist_ok=True)

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(ADDR)

# ---------------- TCP Message Handling ----------------

def send_json(conn, message):
    """JSON control message followed by a newline."""
    data = json.dumps(message).encode(FORMAT) + b"\n"
    conn.sendall(data)


class MessageReader:
    """Read complete JSON messages from a TCP byte stream."""

    def __init__(self, conn):
        self.conn = conn
        self.buffer = bytearray()

    def receive_json(self):
        """Read one newline-terminated JSON message."""
        while b"\n" not in self.buffer:
            chunk = self.conn.recv(BUFFER_SIZE)

            if not chunk:
                return None

            self.buffer.extend(chunk)

            if len(self.buffer) > 1024 * 1024:
                raise ValueError("Control message too large.")

        line, _, remaining = self.buffer.partition(b"\n")
        self.buffer = bytearray(remaining)
        return json.loads(line.decode(FORMAT))


# ---------------- Repository Operations ----------------

def list_files():
    """Return regular files directly inside the repository."""
    return sorted(
        [
            item.name
            for item in REPOSITORY.iterdir()
            if item.is_file() and not item.is_symlink()
        ],
        key=str.lower
    )


def find_file(filename):
    """Reject invalid filenames and paths outside the repository."""
    if not isinstance(filename, str):
        return None

    if not filename or filename in (".", ".."):
        return None

    if Path(filename).name != filename:
        return None

    path = REPOSITORY / filename

    if path.is_symlink() or not path.is_file():
        return None

    try:
        path.resolve().relative_to(REPOSITORY.resolve())
    except ValueError:
        return None

    return path

# ---------------- Client Handler ----------------

def handle_client(conn, addr, client_name, history_entry):
    """Handle one client in its own thread."""
    global active_clients

    reader = MessageReader(conn)

    try:
        # Assign the client name and send it to the client.
        send_json(conn, {
            "type": "welcome",
            "name": client_name,
            "message": f"Welcome! You are {client_name}."
        })

        # The client sends its assigned name back to the server.
        identification = reader.receive_json()

        if (
            not isinstance(identification, dict)
            or identification.get("type") != "hello"
            or identification.get("name") != client_name
        ):
            send_json(conn, {
                "type": "error",
                "message": "Invalid client identification."
            })
            return

        send_json(conn, {
            "type": "ready",
            "message": "Connection established."
        })

        print(f"{client_name} connected from {addr}")

        while True:
            request = reader.receive_json()

            # Handle an unexpected disconnection.
            if request is None:
                break

            if not isinstance(request, dict):
                send_json(conn, {
                    "type": "error",
                    "message": "Invalid request."
                })
                continue

            command = request.get("type")

            # Echo the original message with ACK appended.
            if command == "message":
                message = request.get("text")

                if not isinstance(message, str):
                    send_json(conn, {
                        "type": "error",
                        "message": "Message must be a string."
                    })
                    continue

                response = message + " ACK"

                print(f"Received from {client_name}: {message}")
                print(f"Sending: {response}")

                send_json(conn, {
                    "type": "ack",
                    "text": response
                })

            # Return the files available in the repository.
            elif command == "list":
                send_json(conn, {
                    "type": "list",
                    "files": list_files()
                })

            # Stream the requested file.
            elif command == "get":
                path = find_file(request.get("filename"))

                if path is None:
                    send_json(conn, {
                        "type": "error",
                        "message": "File does not exist or filename is invalid."
                    })
                    continue

                try:
                    file_size = path.stat().st_size

                    # Send file metadata before sending raw bytes.
                    send_json(conn, {
                        "type": "file",
                        "filename": path.name,
                        "size": file_size
                    })

                    with path.open("rb") as file_handle:
                        while True:
                            chunk = file_handle.read(BUFFER_SIZE)

                            if not chunk:
                                break

                            conn.sendall(chunk)

                    print(
                        f"{client_name} downloaded {path.name} "
                        f"({file_size} bytes)"
                    )

                except OSError as exc:
                    print(f"File transfer error: {exc}")
                    break

            # Close the connection when the client sends exit.
            elif command == "exit":
                send_json(conn, {
                    "type": "bye",
                    "message": "Server says: Goodbye!"
                })
                break

            else:
                send_json(conn, {
                    "type": "error",
                    "message": "Unknown command."
                })

    except (OSError, ConnectionError) as exc:
        print(f"Connection error for {client_name}: {exc}")

    except (ValueError, json.JSONDecodeError) as exc:
        print(f"Protocol error for {client_name}: {exc}")

    finally:
        # Close the connection and record the finish time.
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        conn.close()

        history_entry["finished"] = datetime.now().astimezone().isoformat(
            timespec="seconds"
        )

        with counter_lock:
            active_clients -= 1

        print(f"{client_name} disconnected.")
        print(f"Active clients: {active_clients}")


# ---------------- Server Startup ----------------

def print_history():
    """Print all client connection records stored in memory."""
    print("\n========== CLIENT HISTORY ==========")

    for entry in client_history:
        print(
            f"Name: {entry['name']} | "
            f"Address: {entry['address']} | "
            f"Accepted: {entry['accepted']} | "
            f"Finished: {entry['finished'] or 'Still connected'}"
        )

    print("====================================")


def start():
    global active_clients, visitor_counter

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind(ADDR)
        server.listen()

        print(f"Server listening on port {PORT}")
        print(f"Maximum simultaneous clients: {MAX_CLIENTS}")
        print(f"File repository: {REPOSITORY}")
        print("Press Ctrl+C to stop the server.")

        while True:
            conn, addr = server.accept()

            # Check the limit and assign names while holding the lock.
            with counter_lock:
                if active_clients >= MAX_CLIENTS:
                    accepted = False
                else:
                    accepted = True
                    active_clients += 1
                    visitor_counter += 1

                    client_name = f"Client{visitor_counter:02d}"

                    history_entry = {
                        "name": client_name,
                        "address": f"{addr[0]}:{addr[1]}",
                        "accepted": datetime.now().astimezone().isoformat(
                            timespec="seconds"
                        ),
                        "finished": None
                    }

                    client_history.append(history_entry)

            if not accepted:
                print(f"Rejected connection from {addr}: server is full.")

                try:
                    send_json(conn, {
                        "type": "busy",
                        "message": "Server is full. Maximum 3 clients."
                    })
                except OSError:
                    pass
                finally:
                    conn.close()

                continue

            thread = threading.Thread(
                target=handle_client,
                args=(conn, addr, client_name, history_entry),
                daemon=True
            )
            thread.start()

    finally:
        server.close()
        print_history()
        print("Server stopped.")


if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
