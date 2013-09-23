import gimbalusb
import time as t
import numpy as np

# Set parameters for servo commands
MAX_VAL = 2**16 - 1 # 16 bit unsigned int
MIN_VAL = 0

NUM_STEPS = 25
INC_VAL = int(MAX_VAL/NUM_STEPS) 

# Initialize servo position
PAN_VAL = 0
TILT_VAL = 0

# Initialize instance of usb device
gusb = gimbalusb.gimbalusb()

# Initialize storage array
arr = np.zeros([NUM_STEPS, NUM_STEPS, 3])

for pan_ind in range(NUM_STEPS):
    for tilt_ind in range(NUM_STEPS):
        arr[pan_ind,tilt_ind] = [PAN_VAL, TILT_VAL, 999]
        TILT_VAL += INC_VAL

        # Send command to board over USB
        gusb.set_vals(PAN_VAL, TILT_VAL)

        gusb.ping_ultrasonic()

        # Wait briefly
        t.sleep(0.5)

        gusb.ping_ultrasonic()

        t.sleep(0.5)

    PAN_VAL += INC_VAL


