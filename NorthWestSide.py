#!/usr/bin/env python3

'''
Imports:
'''
from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, OUTPUT_B,MoveTank, SpeedPercent, follow_for_ms, MoveSteering
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
import Navigation
from time import sleep
from ev3dev2.motor import OUTPUT_B, MediumMotor
import init

def Sahana_And_Pranav_Code():
    tank = MoveTank(OUTPUT_D, OUTPUT_A)
   
    mnm=LargeMotor(OUTPUT_B)

    # Init Color Sensors
    colorRight = ColorSensor(INPUT_2)
    colorLeft = ColorSensor(INPUT_3)


    # init Gyro Sensor
    tank.gyro = GyroSensor(INPUT_1)
    tank.gyro.mode='GYRO-ANG'
    tank.gyro.reset() 
   

    '''
    Unused Capacity 
    '''
    
    '''
    #Testy Objected by Cody PythonJava
    tank.on_for_rotations(50, 50, 4)
    return
    '''
    

    tank.turn_left(5, 40)    
    Navigation.move_in_cm(tank, 15, "Distance To Object", "Forward")

    return

    '''
    Unload Cargo Plane
    '''

    Navigation.move_in_cm(tank, 5, "Distance To Object", "Forward")

    mnm.on_for_rotations(-50, 0.2)

    Navigation.move_in_cm(tank, 7, "Distance To Object", "Forward")

    mnm.on_for_rotations(50, 0.2)

    Navigation.move_in_cm(tank, 20, "Distance To Object", "Backward")

    Navigation.move_in_cm(tank, colorRight, colorLeft,20, "Line Follower", "")



#Execute Northide Missions
if __name__ == "__main__":
    Sahana_And_Pranav_Code()
