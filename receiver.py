#!/usr/bin/python

from motor import getMotors, turnOffMotors, moveForward, moveBackward, turnLeftInPlace, turnRightInPlace

import atexit

leftMotors = []
rightMotors = []

def main():
    atexit.register(turnOffMotors)
    
    lMotors, rMotors = getMotors()
    leftMotors.extend(lMotors)
    rightMotors.extend(rMotors)

    maxSpeed = 70
    turnSpeed = 100

    print("move forward")
    moveForward(leftMotors, rightMotors, maxSpeed)

    print("turn left")
    turnLeftInPlace(leftMotors, rightMotors, turnSpeed)

    print("turn right")
    turnRightInPlace(leftMotors, rightMotors, turnSpeed)

    print("move backwards")
    moveBackward(leftMotors, rightMotors, maxSpeed)

if __name__ == '__main__':
    main()