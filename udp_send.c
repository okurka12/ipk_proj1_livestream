/**************/
/* IPK stream */
/* 2024-03-08 */
/**************/

#include <assert.h>
#include <stdint.h>
#include <netinet/in.h>  // struct sockaddr_in
#include <arpa/inet.h>  // inet_pton, htons
#include "udp_send.h"

/**
 * https://www.ibm.com/docs/en/zos/2.3.0?topic=programs-c-socket-udp-client
*/


void udp_send(int sock_fd, const char *address, uint16_t port,
              const char *data, unsigned int data_length) {

    int rval;

    struct sockaddr_in s;
    s.sin_family = AF_INET;
    s.sin_port = htons(port);

    /* we could use inet_addr here but nah */
    rval = inet_pton(AF_INET, address, &s.sin_addr);
    assert(rval > 0);

    ssize_t result = sendto(sock_fd, data, data_length, 0, (struct sockaddr *)(&s), sizeof(s));
    assert(result != -1);

}
