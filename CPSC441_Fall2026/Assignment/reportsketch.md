# CPSC 441 – Fall 2026 Programming Assignment 1
## TCP Client-Server Communication Application

### 1. Brief Description of the Code Operation

This assignment implements a client-server communication application using TCP sockets in Python. The application supports multiple simultaneous clients, message acknowledgements, client connection tracking, repository file listing, and file downloads.

The server listens on TCP port 5000 and uses a separate thread to handle each accepted client. A maximum of three clients can be connected simultaneously. When a client connects, the server assigns a sequential name in the format `Client01`, `Client02`, and so on. The client sends its assigned name back to the server to complete identification.

The server maintains an in-memory connection history containing each client's name, network address, connection acceptance time, and disconnection time. The history is kept for the duration of the server process and displayed when the server shuts down.

After connecting, a client automatically requests a list of files in the server's `repository` directory. The user can subsequently send ordinary text messages, request the file list again, download a file, or disconnect by entering `exit`. For ordinary messages, the server returns the original message with ` ACK` appended. If a requested file does not exist or its name is invalid, the server sends an error response.

The application uses newline-delimited JSON for control messages. Since TCP is a byte stream and does not preserve message boundaries, the code buffers incoming data until a complete control message is available. File transfers use a metadata message containing the filename and file size, followed by the file's raw bytes. The client reads exactly the announced number of bytes, allowing both text and binary files to be transferred without interpreting their contents as text.

The server restricts file requests to regular files directly inside the repository directory. This prevents clients from requesting arbitrary paths outside the repository. Downloaded files are saved in a local `downloads` directory.

### 2. Steps to Run the Code

1. Install Python 3 on the computer.
2. Save `server.py` and `client.py` in the same directory.
3. Run `python server.py` in a terminal to start the server.
4. Open additional terminals and run `python client.py` to connect clients.
5. Add files to the server's `repository` directory to make them available for download.
6. Use the client commands `list`, `get <filename>`, and `exit`. Any other input is treated as a chat message.
7. Stop the server with Ctrl+C after testing.

The default configuration assumes that the client and server run on the same computer. The client connects to `127.0.0.1` on port `5000`. For computers on different networks, the client address and firewall configuration must be adjusted.

### How to run the application
You need Python 3 installed. No external libraries are required.
Step 1 — Start the server
Open a terminal in the assignment directory and run:
python server.py


On some systems, use python3 server.py instead.
The server should display its listening address, port, client limit, and repository location.
Step 2 — Start clients
Open up to three additional terminal windows in the same directory. In each terminal, run:
python client.py


Each client receives an automatically assigned name, such as Client01, Client02, and Client03.
The client automatically requests the server's file listing after connecting.
Step 3 — Use the client commands
Input	Expected behavior
Hello server	Server replies Hello server ACK
list	Displays the available repository files
get example.txt	Downloads the file into downloads/
get missing.txt	Displays an error if the file does not exist
exit	Closes the client connection cleanly
To stop the server, press Ctrl+C in its terminal.
Important: This example assumes the client and server run on the same computer. To connect from another computer, change SERVER_HOST in client.py to the server computer's reachable IP address and ensure TCP port 5000 is allowed through the firewall.

### 3. Assumptions and Design Considerations

TCP is used for all application communication, as required. No external networking packages are necessary.

The maximum number of simultaneous clients is configured as three. The server uses a lock to protect shared state when allocating client names, checking the connection limit, and updating the connection history. Client names increment during the server session and are not reset when a client disconnects.

Connection history is stored in memory rather than a database or file. Consequently, it is not retained after the server process terminates. The server exposes only files in the repository's top-level directory; subdirectories are not included in listings or file requests.

Control messages use JSON terminated by a newline. File contents are transmitted as raw bytes after a header specifies their size. This design avoids relying on individual TCP reads to correspond to complete application messages.

The client saves downloaded files in its local `downloads` directory. If a file with the same name already exists, the download overwrites it. The server handles a missing or invalid filename by returning an error rather than terminating the client connection.

### 4. Difficulties Faced and How They Were Handled

Potential implementation challenges include handling TCP message boundaries, coordinating concurrent client threads, enforcing the simultaneous-client limit, and transferring files of arbitrary size.

TCP can deliver a message in multiple reads or deliver parts of successive messages together. The implementation addresses this by buffering incoming data and extracting complete newline-delimited JSON messages. During file transfers, the receiver reads the exact number of bytes specified by the server, preventing file data from being mistaken for a subsequent control message.

Concurrency is handled with a separate thread for each client. A lock protects shared connection information and the active-client counter so that concurrent connections do not incorrectly exceed the configured limit. Cleanup code closes client sockets and records their disconnection times.

Before submitting, this section should be updated to describe the actual issues encountered while implementing and testing the program, along with any changes made to resolve them.

### 5. Possible Improvements

With additional development time, the application could be improved by adding persistent connection logs, configurable server settings, authentication, and encrypted communication. The server could also support file uploads, directory browsing, and resumable downloads.

Additional robustness could be achieved through explicit file-transfer checksums, limits on message sizes and file sizes, automated integration tests, and more comprehensive error handling. A graphical user interface could make the application easier to use, while a more advanced chat design could broadcast messages between connected clients instead of only acknowledging messages through the server.

Overall, this implementation demonstrates TCP socket communication, multithreading, connection management, message framing, and file streaming in a simple client-server application.



[ ] Server and client startup
Start server.py and connect a client.py instance.

[ ] Automatic client naming
Connect clients sequentially and verify Client01, Client02, Client03.

[ ] Multithreading
Keep multiple clients connected and send messages from each.

[ ] Three-client limit
Connect three clients, then try connecting a fourth. The fourth should be rejected.

[ ] Message acknowledgement
Send several strings and verify each response contains the original string followed by ACK.

[ ] Clean exit and slot reuse
Send exit from one client, then connect a replacement client.

[ ] Connection history
Disconnect clients and check the server's accepted and finished timestamps when it stops.

[ ] File listing
Add multiple files to repository/ and check the list command.

[ ] File streaming
Download a text file and a binary file, then compare the downloaded files with the originals.

[ ] Invalid file request
Request a nonexistent filename and verify the client receives an error without disconnecting.