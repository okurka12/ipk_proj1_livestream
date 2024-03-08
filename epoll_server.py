##############
# IPK stream #
# 2024-03-08 #
##############

# works with python 3.12.2

from time import sleep
import socket

# AF_INET -> adress family internet -> IPv4
ADDRESS_FAMILY = socket.AF_INET

# DGRAM -> datagram -> UDP (user datagram protocol)
SOCKET_KIND = socket.SOCK_DGRAM

# bind on 0.0.0.0 -> listen on all available interfaces
BIND_ADDRESS = "0.0.0.0"
BIND_PORT = 6969

# number of seconds to wait before sending reply
N = 4

# create the socket
sock = socket.socket(ADDRESS_FAMILY, SOCKET_KIND)

# bind the socket (note that address is a tuple of address and port)
sock.bind((BIND_ADDRESS, BIND_PORT))
print(f"started server on {BIND_ADDRESS}:{BIND_PORT}")

# blocking
print("waiting for data...")
data, response_address = sock.recvfrom(65535)

# after receiving data, wait for N s
print(f"received data: {data}, sleeping for {N} s")
sleep(N)

reply_str = "this is a reply from server"

# possible ways of transforming a string into bytes
reply_data = b"this is a reply"
reply_data = bytes(reply_str, "utf-8")
reply_data = reply_str.encode("utf-8")

# send the reply
sock.sendto(reply_data, response_address)
print("sent reply, i am done...")
