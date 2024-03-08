# Demo files for the IPK first project livestream

Here you'll find all the files shown on the livestream (link? 🤔)

# Contents

- `epoll_server.py` a python script that starts a UDP server on port `6969`
and when it receives a packet, prints it and waits for `N` (4 by default)
seconds and then sends a reply

- `epoll.c` a simple program that sends a UDP packet to port `6969` and then
waits until it either receives a reply to that packet OR receives input on
standard input. Then it prints either `stdin event happened first` or
`socket event happened first`.

- `udp_send.c` a module that demonstrates processing the dotted decimal
form of an IP address and a `sendto` call - used by `epoll.c`

- `resolve_hostname.c` a program demonstrates a `getaddrinfo` call to resolve
a hostname to a dotted decimal IP address

- `socket_timeout.c` a program that creates a socket, sets a timeout on
the socket, binds to port `55555`, and calls `recv`. If no UDP packet
comes to port `55555` in 1.25 s, returns.


# Soon
I want to add:
- a module that demonstrates the use of `getaddrinfo`
- a demo of `threads.h`
- my implementation of the python mock server
- `capture.sh` script that uses various `tcpdump` commands

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
