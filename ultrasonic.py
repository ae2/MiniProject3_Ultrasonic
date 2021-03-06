import gimbalusb
import time as t
import numpy as np
import pylab as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from random import randint
import msvcrt as ms

# Set parameters for servo commands
MAX_VAL = 2**16 - 1 # 16 bit unsigned int
MIN_VAL = 0

NUM_STEPS = 10
INC_VAL = int(MAX_VAL/NUM_STEPS)

# Range of motion of servos (deg)
PAN_RANGE = 180
TILT_RANGE = 180

# Set constant axis limits for plot
PLOT_MIN_XY = -200 
PLOT_MAX_XY = 200

PLOT_MIN_Z = 0 
PLOT_MAX_Z = 200

# Create list of distances for calibration (cm)
dists = np.logspace(np.log10(30.0), np.log10(200.0), 15)

def main():

    # Initialize servo position
    PAN = 0
    TILT = 0

    # Initialize gimbal usb object
    gusb = gimbalusb.gimbalusb()

    # Start servos at 0 position
    gusb.set_vals(PAN, TILT)

    # Run calibration routine

    run_cal = raw_input("Run calibration? (Y/N) ")
    if run_cal == "Y":
        speed = calibrate(gusb, dists)
    else:
        # Calibrated speed = 1.03283787E-03
        speed = raw_input("Enter speed: ")
        speed = float(speed)

    # Initialize data array
    arr = np.zeros([NUM_STEPS, NUM_STEPS, 3])

    # Create plot for data visualization
    #Initiate 3D Plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #Set Axis Limits Here 
    ax.set_xlim3d(PLOT_MIN_XY, PLOT_MAX_XY)
    ax.set_ylim3d(PLOT_MIN_XY, PLOT_MAX_XY)   
    ax.set_zlim3d(PLOT_MIN_Z, PLOT_MAX_Z)  

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
            gusb.set_vals(PAN, TILT)

            t.sleep(0.5)

            # Send ping, measure TOF
            [tof_count, overflow] = gusb.ping_ultrasonic()

            if overflow == 20:
                print "No object in range"
            else:
                tof = tof_count + overflow * 2**16

                # Use calibrated speed to find dist to object
                dist = calc_dist(tof, speed)
                # dist = 100

                # Convert spherical coordinates to cartesian
                [x, y, z] = sphr2cart(PAN, TILT, dist)
                # print x, y, z

                # Store cartestion positions
                arr[pan_ind,tilt_ind] = [x, y, z]

                ax.scatter(x, y, z)
                plt.draw()

            t.sleep(0.5)  

            # Increment tilt value
            TILT += INC_VAL

        # Reset tilt value
        TILT = 0

        # Increment pan value
        PAN += INC_VAL

    print  arr

    fig.set_size_inches(18.2,10, dpi=100)
    plt.savefig('point_cloud.pdf')
    plt.savefig('point_cloud.png')

    raw_input("Press any key to close plot and exit")

def calibrate(dev, dists):

    # Calibration routine to calculate distance to object
    arr = np.zeros([np.size(dists),3])
    i = 0

    for dist in dists:
        res = raw_input("Place sensor %f cm from wall and press ENTER" %dist)

        while 1:
            print "Press any key when satisfied with reading"

            if ms.kbhit():
                break

            [tof_count, overflow] = dev.ping_ultrasonic()
            tof = tof_count + overflow * 2**16
            print "TOF for %f cm is: %d" %(dist, tof)
            t.sleep(0.5)

        arr[i,:] = [dist,tof, dist/tof]
        i += 1

    avg_speed = np.average(arr[:,2])

    print arr

    print "Average Speed = %f cm/tick" %avg_speed
    appoval = raw_input("Is calibration good? (Y/N)")

    if appoval == "Y":
        return avg_speed
    else:
        calibrate(dev, dists)

def calc_dist(t,speed):

    # Calculate distance to object using TOF and calibrated speed
    return t * speed


def sphr2cart(pan, tilt, dist):

    # Convert position of servos and object distance to cartesian pos of object

    # Convert servo positions to angles (in rad)
    theta = np.deg2rad(mapServo2Ang(pan,PAN_RANGE))
    phi = np.deg2rad(mapServo2Ang(tilt,TILT_RANGE))

    # print "Theta = %f, Phi = %f" %(theta * 180/3.14159, phi * 180/3.14159)

    # print theta, phi

    # Convert spherical coordinates to cartesian
    # x = dist * np.cos(theta) * np.sin(phi)
    # y = dist * np.sin(theta) * np.sin(phi)
    # z = dist * np.cos(phi)

    x = dist * np.cos(theta) * np.cos(phi)
    y = dist * np.sin(theta) * np.cos(phi)
    z = dist * np.sin(phi)

    print y

    return x, y, z

def mapServo2Ang(servo_val,total_ang):

    # Convert servo command to angle of servo
    return servo_val / 2.0**16 * total_ang

def ping_const():
    gusb = gimbalusb.gimbalusb()

    while 1:
        [tof_count, overflow] = gusb.ping_ultrasonic()
        tof = tof_count + overflow * 2**16
        print "TOF = %d" %tof

        t.sleep(0.25)

if __name__ == '__main__':
    # main()
    ping_const()
