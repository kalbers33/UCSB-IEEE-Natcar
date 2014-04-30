/*
 * NatcarUART.h
 *
 *  Created on: Apr 27, 2014
 *      Author: Kevin
 */

#ifndef NATCARUART_H_
#define NATCARUART_H_

/*
 * Interface functions
 */
void NU_GetPID(float *kp, float *ki, float *kd);

void NatcarUartInit(void);

void NatcarUartUpdate(void);

#endif /* NATCARUART_H_ */
