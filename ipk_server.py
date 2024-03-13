##############
# IPK stream #
# 2024-03-08 #
##############

#
# author: okurka12 (https://github.com/okurka12)
#
# python version: 3.12.2
#
# see README.md for more information
# https://github.com/okurka12/ipk_proj1_livestream/blob/main/README.md
#

# inspiration
# https://wiki.python.org/moin/UdpCommunication

import socket
from random import randint

# what address to listen on
# BIND_IP = "127.0.0.1"  # localhost (loopback only)
BIND_IP = "0.0.0.0"  # listen on every available network interface
UDP_PORT = 4567  # default IPK24-CHAT port

# timeout for recv-loop
RECV_TIMEOUT = 0.01

REPLY_FROM_DYNAMIC_PORT = True

FAMILY = socket.AF_INET

# do we want to prin bloat?
VERBOSE = False

# https://stackoverflow.com/questions/5815675/what-is-sock-dgram-and-sock-stream
TYPE = socket.SOCK_DGRAM

MSG_TYPES: dict[str] = {
    0x00: "CONFIRM",
    0x01: "REPLY",
    0x02: "AUTH",
    0x03: "JOIN",
    0x04: "MSG",
    0xFE: "ERR",
    0xFF: "BYE",
}

MSG_INV_TYPES = {value: key for key, value in MSG_TYPES.items()}


class Message:
    def __init__(self, msg: bytes) -> None:
        # parse message header
        self.type = int(msg[0])
        self.type = \
            MSG_TYPES[self.type] if self.type in MSG_TYPES else "unknown"
        self.id = int.from_bytes(msg[1:3], byteorder="big")

        # binary form
        self.binary = msg

        # message type
        msgt = self.type

        if   msgt == "CONFIRM":
            self.ref_msgid = self.id
            del self.id
        elif msgt == "REPLY":
            self.result = int(msg[3])
            self.ref_msgid = int.from_bytes(msg[4:6], byteorder="big")
            self.content = str_from_bytes(6, msg)
        elif msgt == "AUTH":
            self.username = str_from_bytes(3, msg)
            self.dname = str_from_bytes(3 + len(self.username) + 1, msg)
            self.secret = str_from_bytes(3 + len(self.username) + 1 +
                                         len(self.dname) + 1, msg)
        elif msgt == "JOIN":
            self.chid = str_from_bytes(3, msg)
            self.dname = str_from_bytes(3 + len(self.chid) + 1, msg)
        elif msgt == "MSG" or msgt == "ERR":
            self.dname = str_from_bytes(3, msg)
            self.content = str_from_bytes(3 + len(self.dname) + 1, msg)
        elif msgt == "BYE":
            pass

    def __repr__(self) -> str:

        delim: str = "\n"
        output_list = []

        if self.type is not None:
            output_list.append(f"TYPE: {self.type}")
        if self.id is not None:
            output_list.append(f"ID: {self.id}")
        if self.ref_msgid is not None:
            output_list.append(f"REF ID: {self.ref_msgid}")
        if self.username is not None:
            output_list.append(f"USERNAME: '{no_lf(self.username)}'")
        if self.dname is not None:
            output_list.append(f"DISPLAY NAME: '{no_lf(self.dname)}'")
        if self.secret is not None:
            output_list.append(f"SECRET: '{no_lf(self.secret)}'")
        if self.chid is not None:
            output_list.append(f"CHANNEL ID: '{no_lf(self.chid)}'")
        if self.result is not None:
            output_list.append(f"RESULT: {self.result}")
        if self.content is not None:
            output_list.append(f"'{no_lf(self.content)}'")

        output_list.append(str(self.binary))

        return delim.join(output_list)

    def __getattr__(self, attr) -> None:
        if VERBOSE:
            print(f"ERROR: MSG:{hex(id(self))} has no attribute '{attr}' "
                f"(mtype: {self.type})")


def str_from_bytes(startpos: int, b: bytes) -> str:
    """
    reads a null terminated string beginning at `startpos` in `b`.
    returns the string
    o k u r k a 1 2
    """
    output = ""
    i = startpos
    while b[i] != 0 and i < len(b) - 1:
        output += chr(b[i])
        i += 1
    return output



def no_lf(s: str) -> str:
    r"""replaces (CR)LF with \n"""
    o = s.replace("\r", "")
    return o.replace("\n", "\\n")


def recv_loop(sock: socket.socket) -> None:

    # socket to send replies from
    sock_dynport = socket.socket(FAMILY, TYPE)
    sock_dynport.settimeout(RECV_TIMEOUT)

    while True:
        came_to_default_port = False
        came_to_dynamic_port = False

        # wait for the message
        try:
            response, retaddr = sock.recvfrom(2048)
            came_to_default_port = True
        except TimeoutError:
            pass
        if not came_to_default_port:
            try:
                response, retaddr = sock_dynport.recvfrom(2048)
                came_to_dynamic_port = True
            except TimeoutError:
                pass

        if not came_to_default_port and not came_to_dynamic_port:
            continue

        msg = Message(response)

        # print on stdout
        if msg.type != "CONFIRM":
            print("\nMessage came to port "
                  + ("dyn2" if came_to_dynamic_port else str(UDP_PORT)))
            print(f"MESSAGE from {retaddr[0]}:{retaddr[1]}:")
            print(msg)

        # sleep for 50 ms
        # time.sleep(0.1)

        reply_socket = sock_dynport if REPLY_FROM_DYNAMIC_PORT else sock

        # send CONFIRM and REPLY
        if msg.type != "CONFIRM":
            print(f"confirming msg id={msg.id}")
            reply = bytearray(3)
            reply[0] = MSG_INV_TYPES["CONFIRM"]
            reply[1] = response[1]
            reply[2] = response[2]
            reply_socket.sendto(reply, retaddr)

        if msg.type == "AUTH" or msg.type == "JOIN":
            id_lb = randint(0, 255)
            id_mb = randint(0, 255)
            auth_success: int = 1  # 1 - success, 0 - failure
            print(f"sending REPLY for AUTH msg id={msg.id}")
            arr = [MSG_INV_TYPES["REPLY"], id_mb, id_lb, auth_success, response[1], response[2]]
            reply_text = f"Hi, {msg.dname}! is a REPLY for msgid={msg.id}"
            arr.extend([ord(c) for c in reply_text])
            reply = bytearray(arr)
            reply_socket.sendto(reply, retaddr)

        if msg.type == "MSG":
            reply_text = f"this is a reply MSG to " \
            f"message '{msg.content[:20]}...' :)"
            id_lb = randint(0, 255)
            id_mb = randint(0, 255)
            arr = [MSG_INV_TYPES["MSG"], id_mb, id_lb]
            arr.extend([ord(c) for c in "Server"])
            arr.append(0)
            arr.extend([ord(c) for c in reply_text])
            arr.append(0)
            reply = bytearray(arr)
            reply_socket.sendto(reply, retaddr)

        if msg.type == "MSG" and "bye" in msg.content:
            print("sending BYE...")
            reply = bytearray([MSG_INV_TYPES["BYE"], 255, 255])
            reply_socket.sendto(reply, retaddr)



def main():

    # create socket and bind
    sock = socket.socket(FAMILY, TYPE)
    sock.bind((BIND_IP, UDP_PORT))
    sock.settimeout(RECV_TIMEOUT)
    print(f"started server on {BIND_IP} port {UDP_PORT}")

    try:
        recv_loop(sock)
    except KeyboardInterrupt:
        print()


    print("exiting...")


if __name__ == "__main__":
    main()
