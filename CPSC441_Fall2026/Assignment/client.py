import socket
import json
from pathlib import Path

# ---------------- Configuration ----------------

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 6667
BUFFER_SIZE = 4096
FORMAT = "utf-8"

DOWNLOAD_DIRECTORY = Path(__file__).resolve().parent / "downloads"

# ---------------- TCP Message Handling ----------------

class MessageReader:
    """
    Read newline-delimited JSON messages from TCP.

    Extra bytes are preserved because TCP may deliver multiple messages
    or part of a file transfer in a single recv() call.
    """

    def __init__(self, conn):
        self.conn = conn
        self.buffer = bytearray()

    def receive_more(self):
        """Receive more bytes or report a closed connection."""
        chunk = self.conn.recv(BUFFER_SIZE)

        if not chunk:
            raise ConnectionError("Server disconnected.")

        self.buffer.extend(chunk)

    def receive_json(self):
        """Read one complete JSON control message."""
        while b"\n" not in self.buffer:
            self.receive_more()

            if len(self.buffer) > 1024 * 1024:
                raise ValueError("Control message too large.")

        line, _, remaining = self.buffer.partition(b"\n")
        self.buffer = bytearray(remaining)

        return json.loads(line.decode(FORMAT))

    def receive_exact(self, size):
        """Read exactly size bytes, preserving any extra bytes."""
        while len(self.buffer) < size:
            self.receive_more()

        result = bytes(self.buffer[:size])
        del self.buffer[:size]

        return result


def send_json(conn, message):
    """Send a JSON control message terminated by a newline."""
    data = json.dumps(message).encode(FORMAT) + b"\n"
    conn.sendall(data)


# ---------------- File Operations ----------------

def show_files(response):
    """Display the list of files received from the server."""
    files = response.get("files", [])

    print("\nFiles available on the server:")

    if not files:
        print("  No files available.")
    else:
        for filename in files:
            print(f"  - {filename}")

    print()


def download_file(conn, reader, filename):
    """Request a file and save its contents locally."""
    send_json(conn, {
        "type": "get",
        "filename": filename
    })

    response = reader.receive_json()

    if response.get("type") == "error":
        print("Download failed:", response.get("message"))
        return

    if response.get("type") != "file":
        print("Download failed: unexpected server response.")
        return

    size = response.get("size")
    server_filename = response.get("filename")

    if (
        not isinstance(size, int)
        or isinstance(size, bool)
        or size < 0
    ):
        raise ValueError("Invalid file size received from server.")

    if (
        not isinstance(server_filename, str)
        or not server_filename
        or Path(server_filename).name != server_filename
        or server_filename in (".", "..")
    ):
        raise ValueError("Invalid filename received from server.")

    DOWNLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    destination = DOWNLOAD_DIRECTORY / server_filename

    # File contents are binary data. Do not decode them as UTF-8.
    remaining = size

    with destination.open("wb") as output:
        while remaining > 0:
            chunk_size = min(BUFFER_SIZE, remaining)
            chunk = reader.receive_exact(chunk_size)
            output.write(chunk)
            remaining -= len(chunk)

    print(
        f"Downloaded {server_filename} ({size} bytes).\n"
        f"Saved to: {destination}\n"
    )


# ---------------- Client Program ----------------

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"Connecting to {SERVER_HOST}:{SERVER_PORT}...")
        conn.connect((SERVER_HOST, SERVER_PORT))

        reader = MessageReader(conn)

        # Receive the assigned client name or a server-full response.
        welcome = reader.receive_json()

        if welcome.get("type") == "busy":
            print(welcome.get("message", "Server is full."))
            return

        if welcome.get("type") != "welcome":
            print("Unexpected response from server.")
            return

        client_name = welcome.get("name")
        print(welcome.get("message", f"Connected as {client_name}"))

        # Send the assigned name back to the server.
        send_json(conn, {
            "type": "hello",
            "name": client_name
        })

        ready = reader.receive_json()

        if ready.get("type") != "ready":
            print(ready.get("message", "Could not establish connection."))
            return

        print(ready.get("message", "Connection established."))

        # Automatically request the file listing after connecting.
        send_json(conn, {"type": "list"})
        response = reader.receive_json()

        if response.get("type") == "list":
            show_files(response)
        else:
            print(response.get("message", "Could not list files."))

        print("Available commands:")
        print("  Any text       - send a message")
        print("  list           - list repository files")
        print("  get <filename> - download a file")
        print("  exit           - disconnect")
        print()

        while True:
            try:
                user_input = input(f"{client_name}> ")
            except EOFError:
                user_input = "exit"

            command = user_input.strip()

            if command.lower() == "exit":
                send_json(conn, {"type": "exit"})

                try:
                    response = reader.receive_json()
                    print(response.get("message", "Disconnected."))
                except (ConnectionError, OSError):
                    print("Server disconnected.")

                break

            elif command.lower() == "list":
                send_json(conn, {"type": "list"})
                response = reader.receive_json()

                if response.get("type") == "list":
                    show_files(response)
                else:
                    print(response.get("message", "Could not list files."))

            elif command.lower().startswith("get "):
                filename = command[4:].strip()

                if not filename:
                    print("Usage: get <filename>")
                    continue

                download_file(conn, reader, filename)

            else:
                # The server echoes the message with ACK appended.
                send_json(conn, {
                    "type": "message",
                    "text": user_input
                })

                response = reader.receive_json()

                if response.get("type") == "ack":
                    print("Server:", response.get("text", ""))
                else:
                    print(response.get("message", "Unexpected response."))

    except ConnectionRefusedError:
        print(
            "Could not connect. Check that server.py is running "
            "and that the host and port match."
        )

    except (ConnectionError, OSError) as exc:
        print(f"Network error: {exc}")

    except (ValueError, json.JSONDecodeError) as exc:
        print(f"Protocol error: {exc}")

    except KeyboardInterrupt:
        print("\nClient interrupted.")

    finally:
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        conn.close()
        print("Client stopped.")


if __name__ == "__main__":
    main()
