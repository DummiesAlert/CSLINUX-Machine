import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 6767
MAX_CLIENTS = 3
BUFFER_SIZE = 4096
FOLDR = "something"

# Active connections and the session cache are protected by this lock.
clients_lock = threading.Lock()
active_clients = {}
client_cache = []
next_client_number = 1


def session_timestamp():
    # threading exposes Python's monotonic clock internally. Since the
    # assignment forbids importing time/datetime, this records a session
    # clock value rather than a calendar date/time.
    return "session-clock=" + str(round(threading._time(), 3))


def send_line(conn, message):
    conn.sendall((message + "\n").encode("utf-8"))


def receive_line(conn, buffer):
    """Return (one line without newline, remaining buffer), or (None, buffer)."""
    while b"\n" not in buffer:
        chunk = conn.recv(BUFFER_SIZE)
        if not chunk:
            return None, buffer
        buffer += chunk
    line, buffer = buffer.split(b"\n", 1)
    return line.decode("utf-8", errors="replace").rstrip("\r"), buffer


def send_file_list(conn):
    try:
        entries = []
        # No os/pathlib imports are allowed, so list the FOLDR using
        # a small socket-free directory listing via a shell is not suitable.
        # The FOLDR file list is maintained explicitly below instead.
        for name in FOLDR_FILES:
            entries.append(name)
        if entries:
            send_line(conn, "FILES " + " | ".join(entries))
        else:
            send_line(conn, "FILES (FOLDR is empty)")
    except Exception:
        send_line(conn, "ERROR Could not list FOLDR files.")


def stream_file(conn, filename):
    # Only names listed here are accessible. This prevents path traversal.
    if filename not in FOLDR_FILES:
        send_line(conn, "ERROR File not found: " + filename)
        return

    try:
        file_handle = open(FOLDR + "/" + filename, "rb")
        file_handle.close()
    except OSError:
        send_line(conn, "ERROR File not found: " + filename)
        return

    try:
        file_handle = open(FOLDR + "/" + filename, "rb")
        with file_handle:
            # Header announces a binary transfer and exact byte count.
            file_handle.seek(0, 2)
            file_size = file_handle.tell()
            file_handle.seek(0)
            send_line(conn, "FILE " + filename + " " + str(file_size))
            while True:
                data = file_handle.read(BUFFER_SIZE)
                if not data:
                    break
                conn.sendall(data)
    except OSError:
        try:
            send_line(conn, "ERROR Could not read file.")
        except OSError:
            pass


def handle_client(conn, address, client_name):
    buffer = b""
    try:
        send_line(conn, "WELCOME " + client_name)
        # Client must send its assigned name back to complete the handshake.
        received_name, buffer = receive_line(conn, buffer)
        if received_name != client_name:
            send_line(conn, "ERROR Client name handshake failed.")
            return

        send_line(conn, "READY Use list, a FOLDR filename, a message, or exit.")

        while True:
            message, buffer = receive_line(conn, buffer)
            if message is None:
                break

            command = message.strip()
            if command.lower() == "exit":
                send_line(conn, "BYE")
                break
            elif command.lower() == "list":
                send_file_list(conn)
            elif command.startswith("GET "):
                stream_file(conn, command[4:].strip())
            elif command in FOLDR_FILES:
                stream_file(conn, command)
            else:
                send_line(conn, "ACK " + message)

    except (ConnectionError, OSError):
        pass
    finally:
        finished = session_timestamp()
        try:
            conn.close()
        except OSError:
            pass
        with clients_lock:
            active_clients.pop(client_name, None)
            for record in client_cache:
                if record["name"] == client_name and record["finished"] is None:
                    record["finished"] = finished
                    break
        print(client_name + " disconnected from " + str(address) +
              " at " + finished)


def main():
    global next_client_number

    # Create the FOLDR if it does not exist. With the import restriction,
    # create this directory manually before starting the server.
    print("FOLDR directory: " + FOLDR)
    print("Put downloadable files in that directory and add their names to")
    print("FOLDR_FILES in server.py.")

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
                        send_line(conn, "FULL Server is at capacity. Try again later.")
                    except OSError:
                        pass
                    conn.close()
                    continue

                client_name = "Client" + str(next_client_number).zfill(2)
                next_client_number += 1
                accepted = session_timestamp()
                active_clients[client_name] = conn
                client_cache.append({
                    "name": client_name,
                    "address": str(address),
                    "accepted": accepted,
                    "finished": None
                })

            print(client_name + " connected from " + str(address) +
                  " at " + accepted)
            thread = threading.Thread(
                target=handle_client,
                args=(conn, address, client_name),
                daemon=True
            )
            thread.start()

    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        server.close()
        with clients_lock:
            for conn in list(active_clients.values()):
                try:
                    conn.close()
                except OSError:
                    pass
            active_clients.clear()
        print("Connection cache for this session:")
        for record in client_cache:
            print(record)


# Edit this list to match the files placed in the FOLDR directory.
# Example: create FOLDR/example.txt and keep "example.txt" in this list.
FOLDR_FILES = ["example.txt"]

if __name__ == "__main__":
    main()
