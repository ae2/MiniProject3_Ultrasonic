/*
	Elecanisms Mini-Project III using a PIC18F
	
	Shivam Desai and Asa Eckert-Erdheim
	September 23, 2013
	
	Questions? 		   [Shivam@students.olin.edu; Asa@students.olin.edu]
*/

/***************************************************** 
		Includes
**************************************************** */

// Include files
#include <p24FJ128GB206.h> // PIC
#include "config.h"
#include "common.h"
#include "oc.h"			   // output compare
#include "pin.h"
#include "timer.h"
#include "uart.h"
#include "ui.h"
#include "usb.h"
#include <stdio.h>

// Define vendor requests
#define SET_VALS            1   // Vendor request that receives 2 unsigned integer values
#define GET_VALS            2   // Vendor request that returns  2 unsigned integer values
#define PRINT_VALS          3   // Vendor request that prints   2 unsigned integer values 
#define PING_ULTRASONIC     4   // Vendor request that prints 	1 unsigned integer value

// Define names for pins
#define SERVO_PAN		&D[0] // servo pin
#define SERVO_TILT		&D[1] // servo pin
#define ULTRASONIC_TX	&D[2] // us_tx pin

// Define names for timers
#define BLINKY_TIMER		&timer1 // blinky light
#define PAN_TIMER			&timer2 // pan servo
#define TILT_TIMER			&timer3 // tilt servo
#define ULTRASONIC_TIMER	&timer4 // ultrasonic transmission
#define TOF_TIMER			&timer5 // time of flight

// Define constants
#define interval	20e-3
#define min_width	.8e-3
#define max_width	2.2e-3
#define pos			0
#define freq		40000
#define duty_init	0
#define timeout		0 		// seconds

/***************************************************** 
		Function Prototypes & Variables
**************************************************** */ 

void initChip(void);

uint16_t PAN_VAL  = 0;
uint16_t TILT_VAL = 0;

uint16_t LED_VAL  = 0;

uint16_t DUTY_VAL = 32768; // 50% duty cycle

uint16_t TOF_VAL = 0;

/*************************************************
			Initialize the PIC
**************************************************/

void initChip(){
	
    init_clock();
    init_uart();
    init_pin(); 	// initialize the pins for ULTRASONIC
    init_ui();		// initialize the user interface for BLINKY LIGHT
    init_timer();	// initialize the timer for BLINKY LIGHT
    init_oc(); 		// initialize the output compare module for SERVO

	pin_digitalOut(SERVO_PAN);		// configure SERVO as output
	pin_digitalOut(SERVO_TILT);		// configure SERVO as output
	pin_digitalOut(ULTRASONIC_TX);	// configure US_TX as output

    oc_servo(&oc1, SERVO_PAN,     PAN_TIMER, 		interval, min_width, max_width, pos); // configure servo control
	oc_servo(&oc2, SERVO_TILT,    TILT_TIMER, 		interval, min_width, max_width, pos); // configure servo control
	oc_pwm  (&oc3, ULTRASONIC_TX, ULTRASONIC_TIMER, freq,	 duty_init);				 // configure ultrasonic transmission pulse

}

/*************************************************
			Vendor Requests
**************************************************/

void VendorRequests(void) {
    WORD temp;

    switch (USB_setup.bRequest) {
        case SET_VALS:
            PAN_VAL = USB_setup.wValue.w;
            TILT_VAL = USB_setup.wIndex.w;
            BD[EP0IN].bytecount = 0;    // set EP0 IN byte count to 0 
            BD[EP0IN].status = 0xC8;    // send packet as DATA1, set UOWN bit
            break;
        case GET_VALS:
            temp.w = PAN_VAL;
            BD[EP0IN].address[0] = temp.b[0];
            BD[EP0IN].address[1] = temp.b[1];
            temp.w = TILT_VAL;
            BD[EP0IN].address[2] = temp.b[0];
            BD[EP0IN].address[3] = temp.b[1];
            BD[EP0IN].bytecount = 4;    // set EP0 IN byte count to 4
            BD[EP0IN].status = 0xC8;    // send packet as DATA1, set UOWN bit
            break;            
        case PRINT_VALS:
            printf("PAN_VAL = %u, TILT_VAL = %u\n", PAN_VAL, TILT_VAL);
            BD[EP0IN].bytecount = 0;    // set EP0 IN byte count to 0
            BD[EP0IN].status = 0xC8;    // send packet as DATA1, set UOWN bit
            break;
        case PING_ULTRASONIC:
			pin_write(ULTRASONIC_TX, DUTY_VAL);  // send the transmit pulse
			timer_start(TOF_TIMER);
			while(!timer_flag(TOF_TIMER)) {	// wait until the timer trips
				if (timer_time(TOF_TIMER) >= timeout) { // timeout
					break;
					}
				}
			TOF_VAL = timer_time(TOF_TIMER);
            timer_lower(TOF_TIMER);
            BD[EP0IN].bytecount = 0;    // set EP0 IN byte count to 0
            BD[EP0IN].status = 0xC8;    // send packet as DATA1, set UOWN bit
            break;
        default:
            USB_error_flags |= 0x01;    // set Request Error Flag
    }
}

void VendorRequestsIn(void) {
    switch (USB_request.setup.bRequest) {
        default:
            USB_error_flags |= 0x01;                    // set Request Error Flag
    }
}

void VendorRequestsOut(void) {
    switch (USB_request.setup.bRequest) {
        default:
            USB_error_flags |= 0x01;                    // set Request Error Flag
    }
}

/******************************************************************************/
/* Main Program                                                               */
/******************************************************************************/

int16_t main(void) {
	
	initChip();						// initialize the PIC pins etc.
    InitUSB();                      // initialize the USB registers and serial interface engine

    led_on(&led1);					// initial state for BLINKY LIGHT
    timer_setPeriod(BLINKY_TIMER, 1);	// timer for BLINKY LIGHT
    timer_start(BLINKY_TIMER);

    timer_setPeriod(ULTRASONIC_TIMER, 5e-4);	// timer for transmission at 500 microseconds

    while (USB_USWSTAT!=CONFIG_STATE) {     // while the peripheral is not configured...
        
        ServiceUSB();                       // ...service USB requests
        
    }

    while (1) {
        
        ServiceUSB();               // service any pending USB requests

        if (timer_flag(BLINKY_TIMER)) {	// when the timer trips
            timer_lower(BLINKY_TIMER);
            led_toggle(&led1);			// toggle the BLINKY LIGHT
        }
        
        pin_write(SERVO_PAN,  PAN_VAL);  // control SERVO_PAN  with LEFT/RIGHT KEYS
        pin_write(SERVO_TILT, TILT_VAL); // control SERVO_TILT with UP/DOWN	 KEYS

    }
}
