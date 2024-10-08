#!/usr/bin/env python3

import socket
import arguments
import argparse

# Run 'python3 echo-server.py --help' to see what these lines do
parser = argparse.ArgumentParser('Starts a server that returns the data sent to it unmodified')
parser.add_argument('--server_IP', help='IP address at which to host the server', **arguments.ip_addr_arg)
parser.add_argument('--server_port', help='Port number at which to host the server', **arguments.server_port_arg)
args = parser.parse_args()

SERVER_IP = args.server_IP  # Address to listen on
SERVER_PORT = args.server_port  # Port to listen on (non-privileged ports are > 1023)
PET = "Sorry, we don't have the requested animal, OR perhaps you mistyped. Please message one of the following terms: 'CAT' or 'DOG'"

print("server starting - listening for connections at IP", SERVER_IP, "and port", SERVER_PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected established with {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received client message: '{data!r}' [{len(data)} bytes]")

            dataString = str(data)
            dataString = dataString[2:-1]

            if dataString == "CAT":
                print("Client requested a cat. Sending ASCII art.")
                PET = "\n                   _ |\_\n                   \` ..\ \n              __,.- =__Y=\n            .        )\n      _    /   ,    \/\_\n     ((____|    )_-\ \_-`\n     `-----'`-----` `--`\n"
            elif dataString == "DOG":
                print("Client requested a dog. Sending ASCII art.")
                PET ="/n             ,\n            |`-.__\n            / ' _/\n           ****` \n          /    }\n         /  \ /\n     \ /`   \\\ \n      `\    /_\\ \n       `~~~~~``~` \n"

            conn.sendall(bytes(PET, 'utf-8'))

print("server is done!")
