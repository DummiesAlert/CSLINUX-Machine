Socket Programming 2

IP Address: IPv4 (32-bits) and IPv6
    In this course, Sockets will use IPv4 for the Assignments. Since IPv6 does not really work on CloudLabs

    Examples: 
        IPV4: 127.0.0.1, 
                each 8-bits (2^8 numbers, 0 - 255), _ _ _ _ _ _ _ _ . _ _ _ _ _ _ _ _ . _ _ _ _ _ _ _ _ . _ _ _ _ _ _ _ _
                meaning lowest of 0.0.0.0 - highest 255.255.255.255, Universal Network Address - Universal Broadcast Address

Protocols: Some set of rules, different layers uses different Protocols
    Transport layer uses: 
        [1] Transmission Control Protocols: want to have secure data communications, such as sending messages
            Three Way Handshaking: Client - Service - Client
                [a] Establish Stable/Secure Connection (End-user/Client sends signal bits/flags/ping-(for now) to Server)
                    [ai] What happens when a third party is interferring? 
                        it can throw error
                        it can try again
                        it can give up connection
                        depending on configuration, TCP waits/attempts for three times
                [b] Server sends a signal for connection, End-user needs to establish avaliable connection
                [c] Client sends information, addresses, and respond to for secure connection

                [!] When terminating, the same process, but Server - Client - Server
        [2] User Datagram Protocol: want to transfer data in the most efficient and fastest way such as video streaming, speed over security
            Direct Handshaking:
                [a] Client directly sends data and connection to Server
                [b] Server sends available connection and requested data 

                [c] Example: Imagine you are filming in 1 minute increments, with delays
                    [ci] But client knows how many segments, but server does not neccessarily. 
                        [i1] Then how could the server know how many segments left?
                        [i2] How can the client knows it was successful to the Server?
        [3] SYN FLAGS:
            [a] Sequence Number: can be anything
                [ai] imagine SN:5, Client sends 10 bytes
                    [i1] 5th 
                    [i2] 6th
                    [i3] 7th
                    [i4] 8th
                    [i5] 9th
                    [i6] 10th
                    [i7] 11th
                    [i8] 12th
                    [i9] 13th
                    [i10] 14th
                    [i11] of a total of 10 bytes, 2 bytes each increment

            [b] Acknowledging Number: ending sequence number
                [bi] Then client would recieve the next data AN:15, and a new SN for the client
                [bii] depending on the AN, client can tell if all the bits are transferred