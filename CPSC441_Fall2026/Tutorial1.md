Socket Programming

Review TCP/IP Internet Layered Architecture, ____________ Layers
    [5] Physical, Binary numbers
    [4] Data Link, think of Nodes, header has MAC addresses
    [3] Network, think of Nodes, header has the IP/Logical addresses and how to get to the destination (HOPS between routers)
    [2] Transport, think of Nodes, header has the Port numbers
    [1] Application, Google.com -> port numbers

Port Numbers - Processes
Logical Address - Internet Protocol Address
Physical Address - MAC Address
Protocol - Wake up, make something, make public, this a protocol/ Binary Numbers 0/1's 

LAN vs WLAN
    LAN - Local Area Nework, has network and broadcast network
    WLAN - Wireless Local Area Network, 

Socket Address
    A socket is a combination of Physical/Hardware IP Address:Port Number

Question: We have Transport and Network Layer, why have Sockets?
    Is it used to differentiate unique socket address, when having duplicate tabs? Not really?!
    
    HERE: **Socket Programming** is just connecting Network system and Transport System together, think HDMI cable, PC to monitor!

Server vs Client: Think simple system, how many servers, compared to clients? 
    Server active first
    Ideally try to host max clients to servers

Ports
    Well-known Ports: 0 - 1023, Public/Commonly Used
    Registered Ports: 1024 - 49151, Private, For Rich People, Companies use
    Dynamic Ports: 49152 - 65535, Private, temporary and non-reserved ports
        technically used to unique tabs of the same process and protocol!

    Try to Memorize:
        HTTP: 80
        HTTPS: 443
