import gimbalusb
import time as t
import numpy as np
import pylab as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from random import randint
from mayavi import mlab 

# Set parameters for servo commands
MAX_VAL = 2**16 - 1 # 16 bit unsigned int
MIN_VAL = 0

NUM_STEPS = 25
INC_VAL = int(MAX_VAL/NUM_STEPS)

# Range of motion of servos (deg)
PAN_RANGE = 180
TILT_RANGE = 180

# Create list of distances for calibration (cm)
dists = [10, 20, 30, 40, 50]

def main():

    # Initialize servo position
    PAN = 0
    TILT = 0

    # Initialize gimbal usb object
    # gusb = gimbalusb.gimbalusb()

    # Start servos at 0 position
    # gusb.set_vals(PAN, TILT)

    # Run calibration routine
    # speed = calibrate(dists)

    # Initialize data array
    arr = np.zeros([NUM_STEPS, NUM_STEPS, 3])

    # Create plot for data visualization
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # ax.autoscale(True)

    # ax.scatter(arr[:,0], arr[:,1], arr[:,2])

    # # plt.show()

    # plt.interactive(True)

    # plt.xlabel('Time (s)')
    # plt.ylabel()


    # Iterate each servo position
    for pan_ind in range(NUM_STEPS):
        for tilt_ind in range(NUM_STEPS):
            # Send servo position command
            # gusb.set_vals(PAN, TILT)


            # Send ping, measure TOF
            # tof = gusb.ping_ultrasonic()

            # Use calibrated speed to find dist to object
            # dist = calc_dist(tof, speed)
            dist = randint(5,50)

            # Convert spherical coordinates to cartesian
            [x, y, z] = sphr2cart(PAN, TILT, dist)

            # Store cartestion positions
            arr[pan_ind,tilt_ind] = [x, y, z]
            mlab.points3d(arr[:,0], arr[:,1], arr[:,2])
            mlab.show()

            # Increment tilt value
            TILT += INC_VAL

        # Increment pan value
        PAN += INC_VAL

    # ax.scatter(arr[:,0], arr[:,1], arr[:,2])

    # plt.show()

    # plt.show()

    # while 1:
    #     temp = gusb.ping_ultrasonic()
    #     t.sleep(0.25)

def calibrate(dists):

    # Calibration routine to calculate distance to object
    arr = np.zeros([len(dists),3])
    i = 0

    for dist in dists:
        res = raw_input("Place sensor %d cm from wall and press ENTER" %dist)
        t = gusb.ping_ultrasonic()
        arr[i,:] = [dist,t, dist/t]
        i += 1

    return np.average(arr[:,2])

def calc_dist(t,speed):

    # Calculate distance to object using TOF and calibrated speed
    return t * speed


def sphr2cart(pan, tilt, dist):

    # Convert position of servos and object distance to cartesian pos of object

    # Convert servo positions to angles (in rad)
    theta = np.deg2rad(mapServo2Ang(pan,PAN_RANGE))
    phi = np.deg2rad(mapServo2Ang(tilt,TILT_RANGE))

    # Convert spherical coordinates to cartesian
    x = dist * np.cos(theta) * np.sin(phi)
    y = dist * np.sin(theta) * np.sin(phi)
    z = dist * np.cos(phi)

    return x, y, z

def mapServo2Ang(servo_val,total_ang):

    # Convert servo command to angle of servo
    return servo_val / 2**16 * total_ang

if __name__ == '__main__':
    main()

