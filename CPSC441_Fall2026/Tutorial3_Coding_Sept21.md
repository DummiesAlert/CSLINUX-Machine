**Connection Oriented TCP**
    Sockets = import a library, then program a socket class

    For the purpose of the demo, consider this: 

    Server-Side
    [1] Create Circuit
    [2] Assign IP Address and Port Number
    [3] Start Server
    [4] Establish Connection/Accept Connection

    Simulaniously Client-Side
    [1] Have a socket
    [2] Assign a socket address
    [3] connect a socket from the server-side

    Note: 
    [1] Let us set a buffer to analyze this
    [2] This is only one-to-one connection

**Python:**

# Section 1
import socket

HOST = socket.gethostbyname (socket.gethost())          # or 127.0.0.1 to test locally
PORT = 6666
ADDR = (HOST, PORT)                                     # create a tuple

FORMAT = 'utf-8'                                        # optional, up to you
DISCONNECT_MESSAGE = 'exit'                             # or whatever keyword you choose

# Section 2
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
conn, addr = server.accept()                            # blocks until a client connects

# Section 3
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, PORT))

# Section 4
FORMAT = 'utf-8'

#client side
client.send(message.encode(FORMAT))
reply = client.recv(2048).decode(FORMAT)

#server side
data = conn.recv(2048).decode(FORMAT)
conn.send(response.encode(FORMAT))

# Section 5

#inside the server, right after accept()
client_counter += 1
client_name = f"Client{client_counter:02d}"             # Client01, Client02,
...
conn.send(client_name.encode(FORMAT))

# Section 6
clients = {} # name -> connection info
clients[client_name] = addr

DISCONNECT_MESSAGE = "exit"                             # you choose the exact keyword
if data == DISCONNECT_MESSAGE:
connected = False
conn.close()

The process:
    [1] Select IP address
    [2] Select the port number for host and server
    [3] Bind a socket ADDR = (HOST, PORT)
    [4] Make sure when you are done, close client-sides and server-sides

**Java:**

# Section 1
import java.io.*;
import java.net.*;
String HOST = "127.0.0.1";                              // or
inetAddress.getLocalHost().getHostAddress()
int PORT = 6666;                                        // pick any free port number

# Section 2
ServerSocket serverSocket = new ServerSocket(PORT);
Socket conn = serverSocket.accept();                    // blocks until a client
connects

# Section 3
Socket socket = new Socket(SERVER_HOST, PORT);          // the connection is already established here

# Section 4
BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
out.println(message);                                   // send
String reply = in.readLine();                           // receive

# Java-Tip
The same idea - break out of the read loop, then call conn.close()

## The process:
    [1] import libraries
    [2] create IP address and port number
    [3] create a socket
    [4] bind the socket
    [5] then start the server, listen

**Activity: Your Task - Python**
    [1] Build a TCP client and server (a single client is enough).
    [2] The client reads a line of text from the user and sends it to the server.
    [3] The server receives the message, converts it to UPPERCASE, and sends that back — nothing else added.
    [4] The client prints whatever the server sends back, then asks for the next message.
    [5] Pick a keyword (e.g. “exit”) that tells both sides to close the connection cleanly. Use only what's on today's slides: creating a socket, sending/receiving, and a loop.

# Client File
## Section 1
import socket

HOST = socket.gethostbyname (socket.gethost())          
PORT = 6666
ADDR = (HOST, PORT)                                     

FORMAT = 'utf-8'                                        
DISCONNECT_MESSAGE = 'exit'                             

## Section 2
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
conn, addr = server.accept()                            

## Section 3
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, PORT))

## Section 4
FORMAT = 'utf-8'

#client side
message = "whatever"                                    # Added Message
client.send(message.encode(FORMAT))
reply = client.recv(2048).decode(FORMAT)

#server side
data = conn.recv(2048).decode(FORMAT)
conn.send(response.encode(FORMAT))

## Section 5

#inside the server, right after accept()
client_counter += 1
client_name = f"Client{client_counter:02d}"             # Client01, Client02,
...
conn.send(client_name.encode(FORMAT))

## Section 6
clients = {} # name -> connection info
clients[client_name] = addr

DISCONNECT_MESSAGE = "exit"
if data == DISCONNECT_MESSAGE:
connected = False
conn.close()

# Server File