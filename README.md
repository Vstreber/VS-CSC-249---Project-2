# YOU WOULDN'T DOWNLOAD A CAT

> This is a demo of a basic VPN, which mask's a client and their request to receive either a cat or a dog from a black market pet server. 


### Client->VPN Server Message Format + Network interactions
1. Client parses user input, and takes VPN IP and port to send a string containing server IP/Port and the intended message to the VPN
    - Each data point in this string is separated by " || " so that the VPN knows where to split the information
    - A user can attempt to send any message, and the client won't complain -- only IP information and port information errors are corrected
      - Unusable messages are dealt with at the server level. 
2. VPN splits apart message into necessary data points: the server IP, the server port, and the client's message. It then attempts to open a connection with the server, and if successful, sends the client's message to it. It waits for a response.

### VPN Server->Client Message Format + Network interactions
1. Once VPN receives response from server (can be any message under a certain size) it passes it back to the client. Once the message is sent, the VPN closes connection with both the client and server.
    - The server I used will only take in messages "CAT" and "DOG", which it will warn the user about if something else is inputted. However, this server could be replaced with any other server and should work the same -- unlike my Project 1, this client doesn't do anything to police the user's input, and instead relies on the server informing the user of its purpose.
2. When the client receives the message, it displays it for the user, and then closes.

### Example Output

CLIENT:
```
$ python client.py --VPN_IP  127.0.0.1 --VPN_port 55554 --server_IP 127.0.0.1 --server_port 65432 --message CAT
client starting - connecting to VPN at IP 127.0.0.1 and port 55554
Connection established, sending message 'CAT' and IP/port data.
Message sent, waiting for reply.
Received response:
                   _ |\_
                   \` ..\
              __,.- =__Y=
            .        )
      _    /   ,    \/\_
     ((____|    )_-\ \_-`
     `-----'`-----` `--`
[178 bytes]
client is done!
```

VPN:
```
$ python VPN.py --VPN_IP 127.0.0.1 --VPN_port 55554
VPN starting - connecting to client. listening for connections at IP 127.0.0.1 and port 55554
Connected established with ('127.0.0.1', 65321)
Received client message: ''127.0.0.1 || 65432 || CAT'' [25 bytes]
Sending message to specified server address, IP: '127.0.0.1 and PORT: '65432
Connection established, sending message 'CAT' to server.
Message sent, waiting for reply.
Following message received from server:
                   _ |\_
                   \` ..\
              __,.- =__Y=
            .        )
      _    /   ,    \/\_
     ((____|    )_-\ \_-`
     `-----'`-----` `--`
 Sending to client.
VPN is done!
```

SERVER:
```
$ python server.py     
server starting - listening for connections at IP 127.0.0.1 and port 65432
Connected established with ('127.0.0.1', 65277)
Received client message: 'b'CAT'' [3 bytes]
Client requested a cat. Sending.
server is done!
```

### Acknowledgements
Cat and Dog ASCII art is by Joan Stark, and was found in the ASCII Art Archive (https://www.asciiart.eu/)
