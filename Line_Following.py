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


'''
Variables:
'''
# init Motors
tank = MoveTank(OUTPUT_D, OUTPUT_A) 

# Init Color Sensors
colorRight = ColorSensor(INPUT_2)
colorLeft = ColorSensor(INPUT_3)

# init Gyro Sensor
tank.gyro = GyroSensor(INPUT_1)
tank.gyro.mode='GYRO-ANG'
tank.gyro.reset() 


#Current rotation number variable
rotationnumber = 0

#True/False variable to start and stop line following program
distance_not_reached = True

#Distance for robot to go (in centimeters)
distance  = 63
        
#Number of wheel rotations needed to get there
number_of_wheel_rotations = distance / 20.48


'''
Distance Functions:
'''
#Function to add wheel rotation and see if we have reached our distance
def check_if_reach_distance(rotation, end_angle, number_of_wheel_rotations):
    #Saying to use the global variables, and not def variables
    global rotationnumber
    global distance_not_reached

    #Add rotation number
    rotationnumber += rotation

    #Checks if robot has reached destination
    if number_of_wheel_rotations < rotationnumber:

        #Stops the line following program
        distance_not_reached = False

        
        

'''
Line Following Program:
'''
while distance_not_reached == True:
    difference = colorLeft.reflected_light_intensity - colorRight.reflected_light_intensity


    tank.on_for_rotations(20, 20, 0.2)
    check_if_reach_distance(0.2, 0, number_of_wheel_rotations)

    sleep(1)



    if difference < 0: 
        #Left is closer to black, We have to turn left
        if difference > -10:
            pass
        elif difference < -30:
            tank.turn_right(20, 5)
        elif difference < -20:
            tank.turn_right(20, 2.5)
        elif difference > - 20:
            tank.turn_right(20, 1.25)
                    

    if difference > 0:
        #Right is closer to black, we have to turn right
        if difference < 10:
            pass
        elif difference > 30:
            tank.turn_left(20, 5)
        elif difference > 20:
            tank.turn_left(20, 2.5)
        elif difference < 20:
            tank.turn_left(20, 1.25)