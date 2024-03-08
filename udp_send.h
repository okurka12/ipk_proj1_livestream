/**************/
/* IPK stream */
/* 2024-03-08 */
/**************/

#include <stdint.h>
#ifndef QWERTYUIOP_ASDFGHJKL_ZXCVBNM
#define QWERTYUIOP_ASDFGHJKL_ZXCVBNM

void udp_send(int sock_fd, const char *address, uint16_t port,
              const char *data, unsigned int data_length);

#endif  // ifndef QWERTYUIOP_ASDFGHJKL_ZXCVBNM
