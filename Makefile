##############
# IPK stream #
# 2024-03-08 #
##############
CC=gcc
CFLAGS=-Wall -Wextra -pedantic

EPOLL_BINARY=epl.bin

RESOLVE_HOSTNAME_BINARY=rh.bin

SOCKET_TIMEOUT_BINARY=so.bin

BINARIES=$(EPOLL_BINARY) $(RESOLVE_HOSTNAME_BINARY) $(SOCKET_TIMEOUT_BINARY)

all: $(BINARIES)

$(EPOLL_BINARY): udp_send.c udp_send.h epoll.c
	$(CC) $(CFLAGS) -o $@ $^

$(RESOLVE_HOSTNAME_BINARY): resolve_hostname.c
	$(CC) $(CFLAGS) -o $@ $^

$(SOCKET_TIMEOUT_BINARY): socket_timeout.c
	$(CC) $(CFLAGS) -o $@ $^


.PHONY: clean
clean:
	rm -f $(BINARIES)
