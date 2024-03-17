# Demo files for the IPK first project livestream

Here you'll find all the files shown on the livestream (https://www.youtube.com/watch?v=vyVJRc0kr6s)

# Contents

- `epoll_server.py`\
a python script that starts a UDP server on port `6969`
and when it receives a packet, prints it and waits for `N` (4 by default)
seconds and then sends a reply

- `epoll.c`\
a simple program that sends a UDP packet to port `6969` and then
waits until it either receives a reply to that packet OR receives input on
standard input. Then it prints either `stdin event happened first` or
`socket event happened first`.

- `udp_send.c`\
a module that demonstrates processing the dotted decimal
form of an IP address and a `sendto` call - used by `epoll.c`

- `resolve_hostname.c`\
a program demonstrates a `getaddrinfo` call to resolve
a hostname to a dotted decimal IP address

- `socket_timeout.c`\
a program that creates a socket, sets a timeout on
the socket, binds to port `55555`, and calls `recv`. If no UDP packet
comes to port `55555` in 1.25 s, returns.

- `capt.sh`\
a script that uses `tcpdump` to capture all UDP + ICMP packets
on either the default interface or loopback interface (choose by uncommenting)
one in the script. Saves all the captured packets to `tcpdump.log`, but only
prints those that are from/to `HOST` (a variable defined in the script)


# Mock server `ipk_server.py`

`ipk_server.py` is a mock server you can run on localhost (or anywhere else,
really) to test your IPK client implementation.

To sum it up, this server is completely stateless and therefore not very
smart. It just sends responses to anything the client the client sends it
at any time.

## Features

The server can't do much, but it:

- sends a CONFIRM message for every message from client
- prints every incoming message (except for `CONFIRM` messages), both the raw
binary content and parsed fields
- always responds to `AUTH` messages with a `REPLY` where `result=1`
(success) - this can be toggled with the `REPLY_SUCCESS` variable in the script
- sends responses from a dynamic port (it can be toggled with the
`REPLY_FROM_DYNAMIC_PORT` variable in the script)
  - `CONFIRM` responses to `AUTH` messages are always sent from the default
port though. This can be toggled with the `CONFIRM_AUTH_FROM_DEFAULT_PORT`
variable in the script. To see why this is necessary, see this
[change to the assignment](https://moodle.vut.cz/mod/forum/discuss.php?d=3834).
- for every `MSG` message from the client, it sends back a MSG with
display name `Server`
  - server's behavior can be configured to send this message more than once
(with the same ID), so you can test your client's behavior when UDP
packet duplication occurs. to do this, set the `MSG_REPLY_COUNT` variable
in the script to a value greater than 1.
- if the word `bye` is in the MSG message from client, server sends a BYE
message

## Notes

Here's basic information and limitation of the server

- The server only supports UDP.
- The server doesn't distribute messages between clients. It only sends some
responses it generates itself.
- The server does not care if its messages were confirmed or not
- Python version shouldn't really matter, but I run it using 3.12.2

## Example communication

Here's the client side:
```
vita@abakus:~/ipk$ ./ipk24chat-client -t udp -s localhost
/auth user123 secret123 joe
Success: Hi, joe, this is a successful REPLY message to your AUTH message id=69. You wanted to authenticate under the username user123
hi there
Server: Hi, joe! This is a reply MSG to your MSG id=70 content='hi there...' :)
/rename donald
i am now renamed
Server: Hi, donald! This is a reply MSG to your MSG id=71 content='i am now rename...' :)
/join channel123
Success: Hi, donald, this is a successful REPLY message to your JOIN message id=72. You wanted to join the channel channel123
ok, bye
Server: Hi, donald! This is a reply MSG to your MSG id=72 content='ok, bye...' :) since the word 'bye' was in your message, the server will also send you a BYE message.
vita@abakus:~/ipk$
```

Here's the server side:
```
vita@abakus:~/ipk$ py server.py
started server on 0.0.0.0 port 4567

Message from 127.0.0.1:55803 came to port 4567:
TYPE: AUTH
ID: 69
USERNAME: 'user123'
DISPLAY NAME: 'joe'
SECRET: 'secret123'
b'\x02\x00Euser123\x00joe\x00secret123\x00'
Confirming AUTH message id=69
sending REPLY with result=1 to AUTH msg id=69

Message from 127.0.0.1:55803 came to port dyn2:
TYPE: MSG
ID: 70
DISPLAY NAME: 'joe'
'hi there'
b'\x04\x00Fjoe\x00hi there\x00'
Confirming MSG message id=70

Message from 127.0.0.1:55803 came to port dyn2:
TYPE: MSG
ID: 71
DISPLAY NAME: 'donald'
'i am now renamed'
b'\x04\x00Gdonald\x00i am now renamed\x00'
Confirming MSG message id=71

Message from 127.0.0.1:55803 came to port dyn2:
TYPE: JOIN
ID: 72
DISPLAY NAME: 'donald'
CHANNEL ID: 'channel123'
b'\x03\x00Hchannel123\x00donald\x00'
Confirming JOIN message id=72

sending REPLY with result=1 to JOIN msg id=72
Message from 127.0.0.1:55803 came to port dyn2:
TYPE: MSG
ID: 72
DISPLAY NAME: 'donald'
'ok, bye'
b'\x04\x00Hdonald\x00ok, bye\x00'
Confirming MSG message id=72
sending BYE...
```

# Build process
Running `make` will build:
- `epl.bin` - compiled `epoll.c`
- `rh.bin` - compiled `resolve_hostname.c`
- `so.bin` - compiled `socket_timeout.c`

# Usage
Here are the ways to use the demos:

## epoll demo
In one terminal, run `python3 epoll_server.py`. Then, in a second terminal,
run `./epl.bin`. You can either wait and see that the server sent a reply
or press enter and see that stdin was processed.

## resolve_hostname demo
Run `./rh.bin HOSTNAME`, where `HOSTNAME` can be a hostname of your choice,
eg. `localhost`, `antont5.fit.vutbr.cz`...

## socket_timeout demo
Run `./so.bin`. If nothing comes to port `55555` in 1.25 s, which it probably
won't, the program returns. You can verify this by running
`time ./so.bin`

# Useful links
- [project 1 assignment](https://git.fit.vutbr.cz/NESFIT/IPK-Projects-2024/src/branch/master/Project%201)
- [general project specifications](https://git.fit.vutbr.cz/NESFIT/IPK-Projects-2024/src/branch/master/README.md)
- [development environments](https://git.fit.vutbr.cz/NESFIT/dev-envs)
- [C socket UDP client - IBM z/OS doc](https://www.ibm.com/docs/en/zos/3.1.0?topic=programs-c-socket-udp-client)
