/**************/
/* IPK stream */
/* 2024-03-08 */
/**************/

#include <assert.h>
#include <stdio.h>
#include <errno.h>
#include <sys/socket.h>  // socket, setsockopt
#include <sys/time.h>  // struct timeval
#include <netinet/in.h>  // struct sockaddr_in

const unsigned int BUFSIZE = 100;

const unsigned int timeout_s = 1;
const unsigned int timeout_ms = 250;

const struct sockaddr_in bind_addr = {
    .sin_addr.s_addr = 0,  // 0.0.0.0
    .sin_port = 55555
};


int main() {
    int rval;

    /* create socket */
    int sock_fd = socket(AF_INET, SOCK_DGRAM, 0);
    assert(sock_fd != -1);

    /* set timeout on socket */
    struct timeval t = { .tv_sec = timeout_s, .tv_usec = timeout_ms * 1000 };
    rval = setsockopt(sock_fd, SOL_SOCKET, SO_RCVTIMEO, &t, sizeof(t));
    assert(sock_fd != -1);

    /* bind socket */
    rval = bind(sock_fd, (struct sockaddr *)(&bind_addr), sizeof(bind_addr));
    assert(sock_fd != -1);

    /* recv */
    char *buf[BUFSIZE];
    rval = recv(sock_fd, buf, BUFSIZE, 0);
    if (rval == -1 && errno == EWOULDBLOCK) {
        printf("recv timed out...\n");
    }
}
