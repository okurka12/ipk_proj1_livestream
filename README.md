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
form of an IP address and a `sendto` call

# Soon
I want to add:
- a module that demonstrates the use of `getaddrinfo`
- a demo of `threads.h`
- my implementation of the python mock server
- `capture.sh` script that uses various `tcpdump` commands

# Build process
Running `make` will build `epl.bin`

# Usage
In one terminal, run `python3 epoll_server.py`. Then, in a second terminal,
run `./epl.bin`. You can either wait and see that the server sent a reply
or press enter and see that stdin was processed.

# Useful links
- [project 1 assignment](https://git.fit.vutbr.cz/NESFIT/IPK-Projects-2024/src/branch/master/Project%201)
- [general project specifications](https://git.fit.vutbr.cz/NESFIT/IPK-Projects-2024/src/branch/master/README.md)
- [development environments](https://git.fit.vutbr.cz/NESFIT/dev-envs)
- [C socket UDP client - IBM z/OS doc](https://www.ibm.com/docs/en/zos/3.1.0?topic=programs-c-socket-udp-client)
