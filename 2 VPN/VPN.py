#!/usr/bin/env python3

### INSTRUCTIONS ###
# The VPN, like the server, must listen for connections from the client on IP address
# VPN_IP and port VPN_port. Then, once a connection is established and a message recieved,
# the VPN must parse the message to obtain the server IP address and port, and, without
# disconnecting from the client, establish a connection with the server the same way the
# client does, send the message from the client to the server, and wait for a reply.
# Upon receiving a reply from the server, it must forward the reply along its connection
# to the client. Then the VPN is free to close both connections and exit.

# The VPN server must additionally print appropriate trace messages and send back to the
# client appropriate error messages.


import socket
import arguments
import argparse

# Run 'python3 VPN.py --help' to see what these lines do
parser = argparse.ArgumentParser('Send a message to a server at the given address and prints the response')
parser.add_argument('--VPN_IP', help='IP address at which to host the VPN', **arguments.ip_addr_arg)
parser.add_argument('--VPN_port', help='Port number at which to host the VPN', **arguments.vpn_port_arg)
args = parser.parse_args()

VPN_IP = args.VPN_IP  # Address to listen on
VPN_PORT = args.VPN_port  # Port to listen on (non-privileged ports are > 1023)


def parse_message(message):
    message = message.decode("utf-8")
    splitMessage = message.split(' || ')

    SERVER_IP = splitMessage[0]
    SERVER_PORT = int(splitMessage[1])

    message = splitMessage[2]

    return SERVER_IP, SERVER_PORT, message

print("VPN starting - connecting to client. listening for connections at IP", VPN_IP, "and port", VPN_PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((VPN_IP, VPN_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected established with {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break

            dataString = str(data)
            dataString = dataString[2:-1]

            print(f"Received client message: '{dataString!r}' [{len(data)} bytes]")
            server_ip, server_port, message = parse_message(data)

            print(f"Sending message to specified server address, IP: '{server_ip} and PORT: '{server_port}")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((server_ip, server_port))
                print(f"Connection established, sending message '{message}' to server.")
                s.sendall(bytes(message, 'utf-8'))
                print("Message sent, waiting for reply.")
                data = s.recv(1024).decode("utf-8")

                dataString = str(data)

                print(f"Following message received from server: {dataString} Sending to client.")
                conn.sendall(bytes(data, 'utf-8'))

print("VPN is done!")