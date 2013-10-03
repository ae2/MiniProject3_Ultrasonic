import gimbalusb
import time as t
import numpy as np
import pylab as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from random import randint


# Set parameters for servo commands
MAX_VAL = 2**16 - 1 # 16 bit unsigned int
MIN_VAL = 0

NUM_STEPS = 5
INC_VAL = int(MAX_VAL/NUM_STEPS)

# Range of motion of servos (deg)
PAN_RANGE = 180
TILT_RANGE = 180

# Set constant axis limits for plot
PLOT_MIN = 0
PLOT_MAX = 50

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
    #Initiate 3D Plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #Set Axis Limits Here 
    ax.set_xlim3d(-25, 25)
    ax.set_ylim3d(PLOT_MIN, PLOT_MAX)   
    ax.set_zlim3d(PLOT_MIN, PLOT_MAX)  

    ax.autoscale(False)               
        
    #Set Axis Labels Here
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    #Open Plot with Animation Enabled
    plt.ion()
    plt.show()

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
            # print x, y, z

            # Store cartestion positions
            arr[pan_ind,tilt_ind] = [x, y, z]

            ax.scatter(x, y, z)
            plt.draw()

            # Increment tilt value
            TILT += INC_VAL

            t.sleep(0.5)

        # Reset tilt value
        TILT = 0

        # Increment pan value
        PAN += INC_VAL

    raw_input("Press any key to close plot and exit")

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

    # print theta, phi

    # Convert spherical coordinates to cartesian
    # x = dist * np.cos(theta) * np.sin(phi)
    # y = dist * np.sin(theta) * np.sin(phi)
    # z = dist * np.cos(phi)

    x = dist * np.cos(theta) * np.cos(phi)
    y = dist * np.sin(theta) * np.cos(phi)
    z = dist * np.sin(phi)

    return x, y, z

def mapServo2Ang(servo_val,total_ang):

    # Convert servo command to angle of servo
    return servo_val / 2.0**16 * total_ang

if __name__ == '__main__':
    main()

