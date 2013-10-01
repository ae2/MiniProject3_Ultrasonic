import gimbalusb
import time as t
import numpy as np

# Set parameters for servo commands
MAX_VAL = 2**16 - 1 # 16 bit unsigned int
MIN_VAL = 0

NUM_STEPS = 25
INC_VAL = int(MAX_VAL/NUM_STEPS) 

# Create list of distances for calibration (cm)
dists = [10, 20, 30, 40, 50]

def main():

    # Initialize servo position
    PAN = 0
    TILT = 0

    gusb = gimbalusb.gimbalusb()

    arr = np.zeros([NUM_STEPS, NUM_STEPS, 3])

    # speed = calibrate(dists)

    # for pan_ind in range(NUM_STEPS):
    #     for tilt_ind in range(NUM_STEPS):
    #         # Send command to board over USB
    #         gusb.set_vals(PAN, TILT)

    #         t = gusb.ping_ultrasonic()
    #         # d = calc_dist(t, speed)
    #         d = 555

    #         arr[pan_ind,tilt_ind] = [PAN, TILT, d]

    #         TILT += 1

    #     PAN += 1

    while 1:
        temp = gusb.ping_ultrasonic()
        t.sleep(0.25)


def calc_dist(t,speed):
    return t * speed

def calibrate(dists):

    arr = np.zeros([len(dists),3])
    i = 0

    for dist in dists:
        res = raw_input("Place sensor %d cm from wall and press ENTER" %dist)
        t = gusb.ping_ultrasonic()
        arr[i,:] = [dist,t, dist/t]
        i += 1

    return np.average(arr[:,2])

if __name__ == '__main__':
    main()

