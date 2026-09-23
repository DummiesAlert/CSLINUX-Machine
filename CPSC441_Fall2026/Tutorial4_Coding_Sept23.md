**Connection Oriented TCP 2**

# Activity 2: The “Visitor Counter”

Your server accepts multiple clients at the same time, using threads.
Keep one shared counter. Every time a new client connects, increment it.
Send that client a message like “You are visitor #3”, then close the connection.
No need to track who's currently connected — just count how many have connected in
total.

## Using Threading 
    [1] accept() blocks until client connects
    [2] revc() blocks until data arrives
    [3] A server must accept-then-serve loop, so the second client must wait
        [a] we can fix this: as soon as a connection is accpted, hand it off to its own thread and immediately go back to accpet() for the next one

### Python

import socket
import threading 

def handle_client(conn, addr):
...                                                                 # everything this client needs

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()
...

MAX_CLIENTS = 3

lock = threading.Lock()
active = 0

with lock:
    if active >= MAX_CLIENTS:
        conn.close() # politely refuse -- server is full
    else:
        active += 1

...

### Java

import java.io.*;
import java.net.*;

ServerSocket serverSocket = new ServerSocket(PORT);

while (true) {
    Socket conn = serverSocket.accept();
    new Thread(() -> handleClient(conn)).start();
}

...

final int MAX_CLIENTS = 3;

static int active = 0;
static final int MAX_CLIENTS = 3;
static final Object lock = new Object();

synchronized (lock) {
    if (active >= MAX_CLIENTS) {
        conn.close(); // politely refuse -- server is full
    } else {
        active++;
    }
}

...

# Activity 2: The “Visitor Counter” CONTINUTED
    [1] Extend your server to accept multiple clients at the same time, using a thread per connection.
    [2]Keep one shared counter, starting at 0.
    [3] Every time a new client connects, increment the counter.
    [4] Send that client a message such as “You are visitor #3”, using its new counter value.
    [5] Close that connection — no need to keep talking, and no need to remember who's still
    connected.

    Since multiple threads touch the counter, make sure the increment is protected (see the
    earlier slide).

# Extra Content - Streaming files, and Common Bugs
    [1] The server keeps repo/ folder of files it is willing to share
    [2] The client sends a "list" command, the server repies with the file names
    [3] The client asks for one file by name, the server streams that file's bytes back
    [4] The client saves incoming bytes to a local file
    
    TIP: Don't forget to implement error handling

## Python 

import os
REPO_DIR = "repo"                                                   # where the server's shareable files live
DOWNLOAD_DIR = "downloads"                                          # where the client saves what it receives

if not os.path.exists("repo"):
    os.makedirs("repo")

files = os.listdir("repo")
conn.send("\n".join(files).encode(FORMAT)) # reply to "list"
filename = conn.recv(1024).decode(FORMAT)

if filename in files:
    with open(os.path.join("repo", filename), "rb") as f:
        conn.sendall(f.read())
else:
    conn.send("ERROR: File not found".encode(FORMAT))

client.send("list".encode(FORMAT))
print(client.recv(1024).decode(FORMAT))

filename = input("Enter file: ")
client.send(filename.encode(FORMAT))

with open(os.path.join("downloads", filename), "wb") as f:
    # write the incoming bytes here
    # (chunked streaming pattern -- see Extra Content)
    pass

## Java

import java.io.*;                                                   // File, FileInputStream, FileOutputStream, etc.
String REPO_DIR = "repo";                                           // where the server's shareable files
live
String DOWNLOAD_DIR = "downloads";                                  // where the client saves what it
receives

File repo = new File("repo");
String[] files = repo.list();
out.println(String.join("\n", files));                              // reply to "list"

String filename = in.readLine();
File requested = new File(repo, filename);

if (requested.exists()) {
    // stream requested's bytes to the client
    // (chunked streaming pattern -- see Extra Content)
} else {
    out.println("ERROR: File not found");
}

out.println("list");
System.out.println(in.readLine());

String filename = console.readLine("Enter file: ");
out.println(filename);

// write the incoming bytes to downloads/<filename>
// (chunked streaming pattern -- see Extra Content)

## Streaming a File in Chunks
    [1] A file can be larger that one revc() call returns, so you continute the loop, until the full message is recieved
    [2] Strategies to know when to stop
        [a] Have the server send the file's size first
        [b] Close the connection after sending, and let client read until the stream ends
        [c] Send a small marker/sentinel after the file signal "done"
    [3] Note: "rb" to read and "wb" to write.

## Debugging Tips
    [1] "Address already in use" - Often refers to you restarting the server too quickly after closing it, give it a moment or set SO_REUSEADDR before setting a bind()
    [2] revc() hanging forever - usually means the other side actually never sent anything, or been waiting on more bytes than were sent, Check both sides agree on the protocol
    [3] TypeError mixing up str and bytes - you forgot to encode() before send() or a decode()
    [4] Sockets piling up — close every socket you open, especially while restarting the server often during testing.
    [5] Testing multiple clients — open several terminal windows and run the client separately in each.
    [6] Shared counters/caches without a lock — two threads updating the same variable at once can silently lose updates.