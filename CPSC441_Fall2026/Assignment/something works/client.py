import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
BUFFER_SIZE = 4096


def receive_line(conn, buffer):
    while b"\n" not in buffer:
        chunk = conn.recv(BUFFER_SIZE)
        if not chunk:
            return None, buffer
        buffer += chunk
    line, buffer = buffer.split(b"\n", 1)
    return line.decode("utf-8", errors="replace").rstrip("\r"), buffer


def receive_exactly(conn, count, buffer):
    while len(buffer) < count:
        chunk = conn.recv(min(BUFFER_SIZE, count - len(buffer)))
        if not chunk:
            raise ConnectionError("Connection closed during file transfer.")
        buffer += chunk
    return buffer[:count], buffer[count:]


def save_received_file(filename, data):
    # Save the file in the current working directory.
    with open("downloaded_" + filename, "wb") as file_handle:
        file_handle.write(data)
    print("Saved as downloaded_" + filename)


def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    buffer = b""

    try:
        conn.connect((SERVER_HOST, SERVER_PORT))
        first_message, buffer = receive_line(conn, buffer)
        if first_message is None:
            print("Server closed the connection.")
            return

        if first_message.startswith("FULL "):
            print(first_message[5:])
            return
        if not first_message.startswith("WELCOME "):
            print(first_message)
            return

        client_name = first_message[8:]
        print("Connected as " + client_name)
        conn.sendall((client_name + "\n").encode("utf-8"))

        ready_message, buffer = receive_line(conn, buffer)
        if ready_message is None:
            print("Server closed the connection.")
            return
        print(ready_message)

        print("Commands: list | filename | GET filename | exit")
        while True:
            message = input(client_name + "> ")
            conn.sendall((message + "\n").encode("utf-8"))

            if message.strip().lower() == "exit":
                reply, buffer = receive_line(conn, buffer)
                if reply:
                    print(reply)
                break

            if message.strip().lower() == "list":
                reply, buffer = receive_line(conn, buffer)
                if reply is None:
                    print("Server disconnected.")
                    break
                print(reply)
                continue

            if message.startswith("GET "):
                requested_name = message[4:].strip()
            else:
                requested_name = message.strip()

            # A file response is either FILE <name> <byte-count> or a
            # normal text response such as ACK ... or ERROR ...
            reply, buffer = receive_line(conn, buffer)
            if reply is None:
                print("Server disconnected.")
                break

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

                file_data, buffer = receive_exactly(conn, file_size, buffer)
                save_received_file(filename, file_data)
            else:
                print(reply)

    except (OSError, ConnectionError) as error:
        print("Connection error: " + str(error))
    except KeyboardInterrupt:
        print("\nClient interrupted.")
    finally:
        try:
            conn.close()
        except OSError:
            pass


if __name__ == "__main__":
    main()
