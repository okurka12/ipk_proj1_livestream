/**************/
/* IPK stream */
/* 2024-03-08 */
/**************/

#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>  // close
#include <time.h>  // nanosleep
#include <sys/epoll.h>
#include <sys/socket.h>

#include "udp_send.h"

const struct timespec one_second = { .tv_sec = 1 };

/* pointer to one second struct timespec */
const struct timespec *s = &one_second;

/* localhost address (loopback interface) */
const char *localhost = "127.0.0.1";

const uint16_t port = 6969;

const unsigned int MAX_EVENTS = 1;

const int stdin_fd = 0;

const unsigned int LINEBUF = 100;
const unsigned int RESPONSEBUF = 100;

int main() {

    const int flags = 0;

    /* return value */
    int rval;

    /* create IPv4 UDP socket */
    int sock_fd = socket(AF_INET, SOCK_DGRAM, 0);
    assert(sock_fd != -1);

    /* create epoll instance */
    int epoll_fd = epoll_create1(flags);
    assert(epoll_fd != -1);


    struct epoll_event sock_event;
    struct epoll_event stdin_event;

    /* watch for input events (see man 2 epoll_ctl) */
    sock_event.events = EPOLLIN;
    stdin_event.events = EPOLLIN;

    sock_event.data.fd = sock_fd;
    stdin_event.data.fd = stdin_fd;

    /* int epoll_ctl(int epfd, int op, int fd,
                     struct epoll_event *_Nullable event); */
    rval = epoll_ctl(epoll_fd, EPOLL_CTL_ADD, sock_fd, &sock_event);
    assert(rval == 0);
    rval = epoll_ctl(epoll_fd, EPOLL_CTL_ADD, stdin_fd, &stdin_event);
    assert(rval == 0);

    /* buffer for the events */
    struct epoll_event events[MAX_EVENTS];

    /* send datagram to localhost:port */
    char *msg = "this is a message from client";
    udp_send(sock_fd, localhost, port, msg, strlen(msg) + 1);


    /* wait for an event */
    /* int epoll_wait(int epfd, struct epoll_event *events,
                      int maxevents, int timeout); */
    int even_count = epoll_wait(epoll_fd, events, MAX_EVENTS, -1);
    assert(even_count != -1);

    if (events[0].data.fd == stdin_fd) {
        char line[LINEBUF];
        fgets(line, LINEBUF, stdin);
        line[strcspn(line, "\n")] = '\0';
        printf("stdin event happened first: '%s'\n", line);
    } else {
        char response[RESPONSEBUF];
        rval = recv(sock_fd, response, RESPONSEBUF, 0);
        assert(rval != -1);
        assert((unsigned int)rval <= RESPONSEBUF);
        printf("socket event happened first: '%s'\n", response);
    }


    /* close file descriptors and check for success */
    int epoll_close_success = close(epoll_fd);
    int sock_close_success = close(sock_fd);
    assert(epoll_close_success == 0);
    assert(sock_close_success == 0);

}

