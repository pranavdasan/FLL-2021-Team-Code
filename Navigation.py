#!/usr/bin/env python3

'''
Imports:
'''

from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C, OUTPUT_D, OUTPUT_A, SpeedPercent, follow_for_ms, SpeedRPM, LargeMotor, MoveSteering
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from ev3dev2.button import Button
from time import sleep
from ev3dev2.sound import Sound
import init 

'''
Variables:
'''

# constant to control speed increment
rotation = 0.2

def move_in_cm(tank, distance_cm, choose_program, direction):
   #Distance for robot to go (in centimeters   )
    distance  = distance_cm

    #Current rotation number variable
    rotationnumber = 0

    inital_angle = tank.gyro.angle
           
    #Number of wheel rotations needed to get there
    number_of_wheel_rotations = distance / 25.13

    init.debug_print(number_of_wheel_rotations)
    
    if choose_program == "Line Follower":
        Line_Following(tank, number_of_wheel_rotations, rotationnumber)
    
    if choose_program == "Distance To Object":
        distance_to_object(tank, number_of_wheel_rotations, direction,rotationnumber, inital_angle)


#Goes to certain distance        
def distance_to_object(tank, number_of_wheel_rotations, direction, rotationnumber, inital_angle):
    #Saying to use the global variables, and not def variables
    global speed 
    
    distance_not_reached = True

    while distance_not_reached==True:
        if direction == "Forward":
            tank.on_for_rotations(20, 20, rotation)
        if direction == "Backward":
            tank.on_for_rotations(-20, -20, rotation)

          
        #Add rotation number
        rotationnumber += rotation

        degrees_off = inital_angle

        if degrees_off < 0: 
         tank.turn_right(20, abs(degrees_off))
        if degrees_off > 0: 
            tank.turn_left(20, abs(degrees_off))

        #Checks if robot has reached destination
        if number_of_wheel_rotations < rotationnumber:
            #Stops the line following program
            distance_not_reached = False
        
        degrees_off = tank.gyro.angle

        if degrees_off < 0: 
         tank.turn_right(20, abs(degrees_off))
        if degrees_off > 0: 
            tank.turn_left(20, abs(degrees_off))


'''
Line Following Program:
'''
def Line_Following(tank, number_of_wheel_rotations, rotationnumber):
      #Saying to use the global variables, and not def variables
    distance_not_reached = True

    while distance_not_reached == True:
        difference = colorLeft.reflected_light_intensity - colorRight.reflected_light_intensity


        tank.on_for_rotations(20, 20, rotation)

        if difference < 0: 
            #Left is closer to black, We have to turn left
            if difference > -4:
                tank.turn_right(20, 1)
            elif difference < -30:
                tank.turn_right(20, 4)
            elif difference < -20:
                tank.turn_right(20, 3)
            elif difference > - 10:
                tank.turn_right(20, 2)
                        

        if difference > 0:
            #Right is closer to black, we have to turn right
            if difference < 4:
                tank.turn_left(20, 1)
            elif difference > 30:
                tank.turn_left(20, 4)
            elif difference > 20:
                tank.turn_left(20, 3)
            elif difference < 10:
                tank.turn_left(20, 2)


        #Add rotation number
        rotationnumber += rotation

        #Checks if robot has reached destination
        if number_of_wheel_rotations < rotationnumber:
            #Stops the line following program
            distance_not_reached == False
