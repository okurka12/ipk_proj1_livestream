##############
# IPK stream #
# 2024-03-08 #
##############
CC=gcc
CFLAGS=-Wall -Wextra -pedantic

EPOLL_BINARY=epl.bin

all: $(EPOLL_BINARY)

$(EPOLL_BINARY): udp_send.c udp_send.h epoll.c
	$(CC) $(CFLAGS) -o $@ $^

.PHONY: clean
clean:
	rm -f $(EPOLL_BINARY)
