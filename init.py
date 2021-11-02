#!/usr/bin/env python3
"""
  Define all the default values and common functions in this file

"""
import os, sys
from ev3dev2.motor import LargeMotor, MoveSteering, MoveTank, OUTPUT_A, OUTPUT_D, OUTPUT_B, OUTPUT_C, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor, UltrasonicSensor
from time import sleep


# state constants
ON = True
OFF = False

#debug print on or off. Use this to print debug messages and try different I/O values
DEBUG_PRINT_ON = True
DEBUG_TREADMILL_ON = True
DEBUG_INNOVATION_ON = False
DEBUG_STEPCOUNTER_ON = False
DEBUG_BENCH_ON = False

#Robot screen height
#Note- only 8 lines are visible at a time
screen_length = 8

#mission names
mission_list = [
    "Bench"
    "Innovation",
    "Treadmill",
    "Step counter",
    "Slide",
    "Basketball",
    "Row",
    "Final Lap"]

#menu items
main_menu = [
    "Bench",
    "Calibrate Sensors",
    "Scripts",
    "Sensor Values",
    "Remote Control",
    "South Side Missions",
    "Innovation",
    "Treadmill",
    "Step counter",
    "Slide",
    "Basketball",
    "Remote control",
    "Row",
    "Final Lap",
    "SSm1"]

# menu items and assosiated .py file
menu_file = {
    "Bench": "bench",
    "Calibrate Sensors": "calibrate",
    "Scripts": "scripts",
    "Sensor Values": "values",
    "Remote Control": "remote_control",
    "South Side Missions": "south_side_missions",
    "Innovation": "innovation",
    "Treadmill":"treadmill",
    "Step counter":"stepcounter",
    "Slide":"slide",
    "Basketball" :"basketball",
    "Remote control" :"remote_control",
    "Row" : "row",
    "Final Lap": "final_lap",
    "SSm1": "PenultimateRunSouthside"
    }

# menu font
menu_font_regular = "Lat15-Terminus14"
menu_font_bold = "Lat15-TerminusBold14"


# treadmill
treadmill = {
    "run_speed" : 30,
    "run_rotations" : 2,
    "ultrasonic": 5
}

# step counter
stepcounter_values = {
    "speed" : 20,
    "time" : 1000
}


""" Console Output Messaging functions """

# Print debug messages in VS Code.
#Only thing we need 
def debug_print(*args, **kwargs):
    if DEBUG_PRINT_ON:
        print(*args, **kwargs, file=sys.stderr)

# Reset console to default state
def reset_console():
    print('\x1Bc', end='')

# Cursor turned off or on
def set_cursor(state):
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')

# Set the console font
def set_font(name):
    os.system('setfont ' + name)


# Print the menu in the console with the selected item highlighted
# menu: list of items to be displayed in the menu
# s: the index of the item selected in the menu list.
def load_menu(menu, s):

    reset_console()
    set_cursor(OFF)
    debug_print( s, " ", menu[s])

    #get the length of the menu
    menu_length = len(menu)

    #check if the list is longer than screen length and if scrolling is required
    if menu_length <= screen_length:
        start = 0
        end = menu_length
    else:
        #scrolling logic using start and end values for range
        if s < screen_length:
            start  = 0
            end = screen_length
        else:
            start  = s - screen_length + 1
            end = s + 1
        debug_print ("start ", start, " end ", end, " selected ", s, "screen len", screen_length)

    # print each menu item and show > next to the selected item
    print(" ")
    for y in range(start, end):
        if (y == s):
            print(" > ", menu[y])
        else:
            print("   ", menu[y])
        y = y + 1


def safe_gyro_reading(sleep_time):
    r1 = gyro.angle
    sleep(sleep_time)
    r2 = gyro.angle
    sleep(sleep_time)
    r3 = gyro.angle
    sleep(sleep_time)

    #average of three readings
    avg_r = ((r1 + r2 + r3) / 3)
    error_margin = 3
    dif12 = abs(r1 - r2)
    dif13 = abs(r1 - r3)
    dif23 = abs(r2 - r3)

    if r1 == r2:
        init.debug_print("Safe reading... returned " + str(r2))
        return r2

    elif dif12 < error_margin:
        avg12 = (r1 + r2) / 2
        init.debug_print("Safe reading... returned " + str(avg12))
        return avg12

    elif dif12 >= error_margin:
        # use r3 as tie breaker
        if r3 == r1 or dif13 < error_margin:
            init.debug_print("Safe reading... returned " + str(r1))
            return r1
        elif r3 == r2 or dif23 < error_margin:
            init.debug_print("Safe reading... returned " + str(r2))
            return r2
        else:
            # all 3 readings are diffrent. Restarting readings
            init.debug_print("Safe reading restarting/failed: Read again"+ str(r1) + " " +str(r2) + " " +str(r3))
            safe_sonic_reading(sleep_time)



def safe_sonic_reading(sleep_time):
    r1 = ultrasonic.distance_centimeters
    sleep(sleep_time)
    r2 = ultrasonic.distance_centimeters

    #average of three readings
    error_margin = 3
    dif12 = abs(r1 - r2)

    if r1 == r2:
        #init.debug_print("Safe reading... returned " + str(r2))
        return r2

    elif dif12 < error_margin:
        avg12 = (r1 + r2) / 2
        #init.debug_print("Safe reading... returned " + str(avg12) + " avg:" + str(r1)  + str(r2))
        return avg12

    sleep(sleep_time)
    r3 = ultrasonic.distance_centimeters
    dif13 = abs(r1 - r3)
    dif23 = abs(r2 - r3)

    # use r3 as tie breaker
    if r3 == r1 or dif13 < error_margin:
        #init.debug_print("Safe reading... returned " , str(r1))
        return r1
    elif r3 == r2 or dif23 < error_margin:
        #init.debug_print("Safe reading... returned " , str(r2))
        return r2
    else:
        # all 3 readings are diffrent. Restarting readings
        init.debug_print("Safe reading restarting/failed: Restart. ", str(r1) , " " ,str(r2) ," ", str(r3))
        safe_sonic_reading(sleep_time)

def straighting_up(rm, lm, r, lower, upper):
    gyro.reset()
    init.debug_print("Straighting up")
    stop = 0
    while stop == 0:
        sleep(0.5)
        gyro_sensor = gyro.angle
        init.debug_print(' Gyro   : ' + str(gyro.angle))

        # Ultra sonic is greater than
        if gyro_sensor > upper:
            tank.on_for_rotations(rm, lm, r)
        # Ultra sonic is less than
        elif gyro_sensor < lower:
            tank.on_for_rotations(lm, rm, r)
        else:
            stop = 1

def moving_with_sonic(rm, lm, r, lower, upper, far):
    init.debug_print("Moving with sonic", rm, lm, r, lower, upper, far)
    stop = 0
    while stop == 0:
        sonic_sensor = float(safe_sonic_reading(0.2))

        # Ultra sonic is greater than upper then move forward
        if sonic_sensor > upper:
            tank.on_for_rotations(rm, lm, r)

        # Ultra sonic is less than lower then move backward
        elif sonic_sensor < lower:
            rm1= rm*-1
            lm1= lm*-1
            tank.on_for_rotations(rm1, lm1, r)

        # If sensor is too far then stop program
        elif sonic_sensor > far:
            init.debug_print("Too far. Sonic reader failed!!!")
            sys.exit()

        # exit while loop
        else:
            stop = 1

def move_straight_sonic_reading(speed, svalue):
    # this is how far the robot is from the wall
    current_dist_wall = safe_sonic_reading(0.2)
    # this is how far it needs to move to get to the destination.
    dist_to_dest = current_dist_wall - svalue
    # If destionation is positive move robot forward else backwards
    direction = 1
    seconds = abs(dist_to_dest / speed)
    if dist_to_dest < 0:
        direction = -1
    elif dist_to_dest > 0:
        direction = 1
    else:
        init.debug_print("Destination reached" + str(svalue))
        return
    speed = speed * direction
    tank.on_for_seconds(speed, speed, seconds)

    current_dist_wall = safe_sonic_reading(0.2)
    if current_dist_wall == svalue:
        init.debug_print("Destination reached")
        return
    else:
         moving_with_sonic(rm = 5, lm = 5, r = 0.05, upper = svalue + 2, lower = svalue - 1, far = svalue + 30)

def move_straight_centimeters(speed, distance):

    # speed is the speed the user wants the robot to move at
    # distance is the centimeters that the user wants the robot to move forward
    # current_dist is the distance of the robot from the wall
    # seconds is the time it will take for the robot to move to the distance

    tire_circ = 6.9
    pi = 3.1416

    # calculate distance from the wall
    current_dist = safe_sonic_reading(0.2)
    init.debug_print("Current distance from wall: " + str(current_dist))

    # calculate the distance the robot should be from the wall
    new_distance = abs(current_dist - distance)
    init.debug_print("New distance from wall should be: ", new_distance)

    # calculate seconds = how long it will take the robot to move at speed
    seconds = distance/speed
    init.debug_print("Calculate time: ", seconds)

    # calculate the number of rotations needed to travel forward using formula pi*d = circumference
    # tire diameter = 6.8cm
    rotations_for_distance = (distance) / (tire_circ*pi)
    init.debug_print("Rotations : ", rotations_for_distance)

    # move the robot
    init.debug_print("Move robot forward...")
    #tank.on_for_seconds(speed, speed, seconds)
    tank.on_for_rotations(speed, speed, rotations_for_distance)

    # get the sonic reading of the robot from the wall
    current_dist = safe_sonic_reading(0.2)
    init.debug_print("Current distance from wall after moving: ", current_dist)

    diff = new_distance - current_dist

    # check if the sonic reader is equal to where the robot needs to be
    if diff == 0:
        init.debug_print("Tank moved to the right spot per sonic reader: " + str(distance)+"cm , Current distance" + str(current_dist) + " Needed" + str(new_distance) +" Difference" + str(diff))
        return
    else:
        # if the robot did not move to where it should be, then move slowly to get to that position
        init.debug_print("Not the right spot per sonic" + str(distance)+"cm , Current distance" + str(current_dist) + " Needed" + str(new_distance) +" Difference" + str(diff))
        #moving_with_sonic(rm = 5, lm = 5, r = 0.01, upper = new_distance+error_margin, lower = new_distance-error_margin, far = distance + 70)


def turn_to_angle(speed, angle):
    starting_angle = gyro.angle
    rotations = 0.1
    stop = 0
    init.debug_print(' Gyro from   : ' + str(starting_angle) + ' to: ' + str(angle))

    while stop == 0:
        sleep(0.2)
        current_angle = gyro.angle
        upper = angle + 1
        lower = angle - 1
        init.debug_print(' Gyro   : ' + str(current_angle))

        # if angle difference is small enough, go slower for accuracy
        diff = abs(current_angle - angle)
        if diff < 10:
            init.debug_print(' Slowing down   : ' + str(diff))
            speed = 2
            rotations = 0.05

        # determine direction
        if current_angle > upper:
            tank.on_for_rotations(speed, speed*-1, rotations)
        elif current_angle < lower:
            tank.on_for_rotations(speed*-1, speed, rotations)
        else:
            stop = 1

def unit_test():

    # unit test 1
    init.debug_print("Unit test 1: Read Gyro")
    g = safe_gyro_reading(0.2)
    init.debug_print("Gyro reading: ", g)

    # unit test 2
    init.debug_print("\n\nUnit test 2: Read Sonic")
    s = safe_sonic_reading(0.2)
    init.debug_print("Sonic reading: ", s)


    # unit test 3
    dist = 10.0
    init.debug_print("\n\nUnit test 3: Move straight ", str(dist))
    move_straight_centimeters(10,dist)
    s = safe_sonic_reading(0.2)
    init.debug_print("Sonic reading: ", s)

    # unit test 4
    angle = 0
    speed = 5
    init.debug_print("\n\nUnit test 4: Turn angle ", str(angle))
    turn_to_angle(speed,angle)
    g = safe_gyro_reading(0.2)
    init.debug_print("Gyro reading: ", g)

    angle = 90
    speed = 5
    init.debug_print("\n\nUnit test 4: Turn angle ", str(angle))
    turn_to_angle(speed,angle)
    g = safe_gyro_reading(0.2)
    init.debug_print("Gyro reading: ", g)

    angle = 70
    speed = 5
    init.debug_print("\n\nUnit test 4: Turn angle ", str(angle))
    turn_to_angle(speed,angle)
    g = safe_gyro_reading(0.2)
    init.debug_print("Gyro reading: ", g)
