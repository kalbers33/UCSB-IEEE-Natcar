/*
 * NatcarUART.c
 *
 *  Created on: Apr 27, 2014
 *      Author: Kevin
 */

#include "inc/lm4f120h5qr.h"
#include "inc/hw_types.h"
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/pin_map.h"
#include "driverlib/uart.h"
#include "uartstdio.h"
#include "stdlib.h"
#include "string.h"
#include "stdio.h"

#define LISTEN 0
#define ACTIVE 1

/*
 * Quick dynamic linked list for resizable buffers
 */
typedef struct NU_Byte {
  char data;
  struct NU_Byte* next;
} NU_Byte;

unsigned int NUB_Len(NU_Byte* head) {
  NU_Byte* runner = head;
  unsigned int result = 0;
  for ( ; runner; runner = runner->next)
    result++;
  return result;
}

/*
 * appends to list and returns new head
 */
NU_Byte* NUB_Append(NU_Byte* head, char data) {
  NU_Byte* result = (NU_Byte*)malloc(sizeof(NU_Byte));
  result->data = data;
  result->next = NULL;
  
  // passed NULL as head, return new object
  if (!head)
    return result;
  
  // otherwise append to list
  // go to right before end
  NU_Byte* runner = head;
  for ( ; runner->next; runner = runner->next) {}
  // append
  runner->next = result;
  return head;
}

/*
 * pops the head of the list and writes the byte into data
 * returns new head and removes the appropriate NU_Byte
 */
NU_Byte* NUB_PopFront(NU_Byte* head, char *data) {
  NU_Byte* newHead = head->next;
  *data = head->data;
  free(head);
  return newHead;
}

/*
 * free()s all elements in the list.
 */
void NUB_Free(NU_Byte* head) {
  NU_Byte* runner = head;
  while (runner) {
    NU_Byte* victim = runner;
    runner = runner->next;
    free(victim);
  }
}
/*************************************************/

unsigned char Enabled;
unsigned char CurrentState;
char CurrentCommand[3];
NU_Byte* NU_Buffer = NULL;
int NU_MessageLength = -1;

float NU_kPID[3];

void NU_GetPID(float *kp, float *ki, float *kd) {
  *kp = NU_kPID[0];
  *ki = NU_kPID[1];
  *kd = NU_kPID[2];
}

void NatcarUartInit(void)
{
    // Enable GPIO port A which is used for UART0 pins.
    // TODO: change this to whichever GPIO port you are using.
    //
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOC);

    //
    // Configure the pin muxing for UART0 functions on port A0 and A1.
    // This step is not necessary if your part does not support pin muxing.
    // TODO: change this to select the port/pin you are using.
    //
    GPIOPinConfigure(GPIO_PC4_U1RX);
    GPIOPinConfigure(GPIO_PC5_U1TX);

    //
    // Enable UART1 so that we can configure the clock.
    //
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART1);

    //
    // Use the internal 16MHz oscillator as the UART clock source.
    //
    UARTClockSourceSet(UART1_BASE, UART_CLOCK_PIOSC);

    //
    // Select the alternate (UART) function for these pins.
    // TODO: change this to select the port/pin you are using.
    //
    GPIOPinTypeUART(GPIO_PORTC_BASE, GPIO_PIN_4 | GPIO_PIN_5);

    //
    // Initialize the UART for console I/O.
    //
    UARTStdioConfig(1, 115200, 16000000);

    UARTEchoSet(false);

    //DEBUG

    GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_2, 0xFF);
	Enabled = true;
	CurrentState = LISTEN;

//    UARTprintf("+++");
//
//    int timeout;
//    for(timeout = 10000000; timeout > 0; timeout--)
//    {
//    	if(UARTRxBytesAvail() > 1)
//		{
//			char CurrentChar[3];
//			UARTgets(CurrentChar,3);
//			if(CurrentChar[0] == 'O' && CurrentChar[1] == 'K' )
//			{
//				GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_2, 0xFF);
//				Enabled = true;
//				CurrentState = LISTEN;
//			}else
//			{
//				GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_2, 0x00);
//				Enabled = false;
//			}
//			return;
//		}
//    }
    //UARTprintf("Natcar Test\n");
}

void NatcarUartUpdate(void)
{
	if(!Enabled) return;

	if (CurrentState == LISTEN) {
		// listen for the command chars
		if(UARTRxBytesAvail() >= 3) {
			CurrentCommand[0] = UARTgetc();
			CurrentCommand[1] = UARTgetc();
			CurrentCommand[2] = UARTgetc();

			// MAYBE? check the commands?
			CurrentState = ACTIVE;
		}
	} else if (CurrentState == ACTIVE) {
		// process commands
		// if..else handle each command
		if (strcmp(CurrentCommand, "HAI") == 0) {
			// write back "AOK"
			UARTwrite("AOK", 3);
			UARTFlushRx();
			CurrentState = LISTEN;
		} else if (strcmp(CurrentCommand, "PID") == 0) {
			// write in pid values ->
      for ( ; UARTRxBytesAvail() > 0; )
        NU_Buffer = NUB_Append(NU_Buffer, UARTgetc());
      
      // if we have sufficient data in NU_Buffer and we haven't
      // actually processed any data yet
      if (NUB_Len(NU_Buffer) >= 4 && NU_MessageLength == -1) {
        // read message length
        char msgLen[4];
        NU_Buffer = NUB_PopFront(NU_Buffer, &msgLen[0]);
        NU_Buffer = NUB_PopFront(NU_Buffer, &msgLen[1]);
        NU_Buffer = NUB_PopFront(NU_Buffer, &msgLen[2]);
        NU_Buffer = NUB_PopFront(NU_Buffer, &msgLen[3]);
        
        // do something with newfound data
        NU_MessageLength = atoi(msgLen);
      }

      // if buffer has enough data
      if (NUB_Len(NU_Buffer) >= NU_MessageLength) {
        // set variables accordingly
      }
		} else {
			// comamnd not recognized.. done with command and restart
			UARTFlushRx();
			CurrentState = LISTEN;
		}

		// if (done with command) then
		// clear buffers
		// CurrentState = LISTEN;
	} else {
		// shouldn't be here...
		// flush buffer and set to LISTEN
	}

}
