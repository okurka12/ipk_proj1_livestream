/**************/
/* IPK stream */
/* 2024-03-08 */
/**************/

/* getaddrinfo, strdup (see man 7 feature_test_macros) */
#define _POSIX_C_SOURCE 200809L

#include <assert.h>
#include <stdio.h>
#include <string.h>  // memcpy, strdup
#include <stdlib.h>  // free
#include <netinet/in.h>  // struct sockaddr_in
#include <netdb.h>  // getaddrinfo
#include <arpa/inet.h>  // inet_ntoa

/**
 * @note output pointer needs to be freed
*/
char *resolve_hostname(char *hostname) {
    int rval;

    /* stuff */
    struct sockaddr_in address;
    struct addrinfo hints = {
        .ai_family = AF_INET,
        .ai_socktype = SOCK_DGRAM
    };
    struct addrinfo *result;

    /* call getaddrinfo */
    rval = getaddrinfo(hostname, NULL, &hints, &result);
    assert(rval == 0);

    /* use the first address (result is a linked list) */
    memcpy(&address, result->ai_addr, result->ai_addrlen);

    /* convert to a dotted decimal */
    char *address_dd = inet_ntoa(address.sin_addr);

    /**
     * copy inet_ntoa output - why is this necessary?
     *
     * from man 3 inet_ntoa:
     * The  inet_ntoa()  function  converts the Internet host address in,
     * given in network byte order, to a string in IPv4 dotted-decimal
     * notation.  The string is returned in a statically allocated buffer,
     * which subsequent calls will overwrite.
     */
    char *address_dd_copied = strdup(address_dd);
    assert(address_dd_copied != NULL);

    freeaddrinfo(result);

    return address_dd_copied;
}

int main(int argc, char *argv[]) {

    /* check arguments */
    if (argc < 2) {
        fprintf(stderr, "Usage: ./%s HOSTNAME\n", argv[0]);
        return 1;
    }

    /* call resolve_hostname */
    char *resolved = resolve_hostname(argv[1]);
    printf("resolved %s to %s\n", argv[1], resolved);
    free(resolved);
}
