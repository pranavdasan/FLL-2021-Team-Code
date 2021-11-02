#!/usr/bin/env python3

from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, OUTPUT_B,MoveTank, SpeedPercent, follow_for_ms, MoveSteering
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
import Line_Following
from time import sleep
from ev3dev2.motor import OUTPUT_B, MediumMotor

def Printy_Printy():
    # init Motors
    tank = MoveTank(OUTPUT_D, OUTPUT_A) 

    # Init Color Sensors
    colorRight = ColorSensor(INPUT_2)
    colorLeft = ColorSensor(INPUT_3)

    # init Gyro Sensor
    tank.gyro = GyroSensor(INPUT_1)
    tank.gyro.mode='GYRO-ANG'
    tank.gyro.reset() 

    while True:
        init.debug_print("Gyro Values "+gyro.angle) 
        init.debug_print("ColorLeft values "+colorLeft.reflected_light_intensity) 
        init.debug_print("ColorRight values "+colorRight.reflected_light_intensity)

if __name__ == "__main__":
    Printy_Printy()