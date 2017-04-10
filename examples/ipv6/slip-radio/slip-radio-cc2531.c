/*
 * Copyright (c) 2011, Swedish Institute of Computer Science.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

/**
 * \file
 *         Slip-radio driver
 * \author
 *         Niclas Finne <nfi@sics.se>
 *         Joakim Eriksson <joakime@sics.se>
 */
#include "contiki.h"
#include "contiki-net.h"
#include "cc2530-rf.h"
#include "dev/leds.h"
#include "cmd.h"
#include <string.h>
#include <stdint.h>
#include "net/mac/frame802154.h"

#define DEBUG DEBUG_NONE
#include "debug.h"

/*---------------------------------------------------------------------------*/
/*
 * Blink one LED on RF TX commands. Blink the second LED on reception of all
 * other commands
 */
#define CC2531_SLIP_RADIO_CMD_RFTX_LED  LEDS_GREEN
#define CC2531_SLIP_RADIO_CMD_MGMT_LED  LEDS_RED
/*---------------------------------------------------------------------------*/

int
cmd_handler_cc2531(const uint8_t *data, int len)
{
  leds_on(CC2531_SLIP_RADIO_CMD_MGMT_LED);

  if(data[0] == '!') {
    if(data[1] == 'C' && len == 3) {
      putstring("cc2531: Setting RF channel 0x");
      puthex(data[2]);
      putstring("\n");

      if(NETSTACK_RADIO.set_value(RADIO_PARAM_CHANNEL, data[2])
         != RADIO_RESULT_OK) {
        putstring("cc2531: Error\n");
      }

      leds_off(CC2531_SLIP_RADIO_CMD_MGMT_LED);

      return 1;
    } else if(data[1] == 'M' && len == 10) {

      /* Update RF registers and Contiki's data structures with the new MAC */
      memcpy(uip_lladdr.addr, data+2, sizeof(uip_lladdr.addr));
      linkaddr_set_node_addr((linkaddr_t *) uip_lladdr.addr);
      if(NETSTACK_RADIO.set_object(RADIO_PARAM_64BIT_ADDR, data+2, 8)
         != RADIO_RESULT_OK) {
        putstring("cc2531: Error updating MAC.\n");
        putstring("cc2531: You may have to manually reboot the dongle.\n");
      }

      leds_off(CC2531_SLIP_RADIO_CMD_MGMT_LED);

      return 1;
    }
  } else if(data[0] == '?') {
    if(data[1] == 'C' && len == 2) {
      uint8_t buf[4];
      radio_value_t chan;

      if(NETSTACK_RADIO.get_value(RADIO_PARAM_CHANNEL, &chan)
         == RADIO_RESULT_OK) {
        buf[0] = '!';
        buf[1] = 'C';
        buf[2] = (uint8_t)chan;

        cmd_send(buf, 3);
      } else {
        putstring("cc2531: Read RF channel error\n");
      }

      leds_off(CC2531_SLIP_RADIO_CMD_MGMT_LED);

      return 1;
    }
  }
  leds_off(CC2531_SLIP_RADIO_CMD_MGMT_LED);
  return 0;
}
