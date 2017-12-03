#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
 
import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

def motorsSetSpeed(motors, speed):
	for i in range(len(motors)): 
		motors[i].setSpeed(speed)

def motorsSetDirection(motors, direction):
	for i in range(len(motors)):
		motors[i].run(direction)

def accelerateToSpeed(leftMotors, rightMotors, targetSpeed): 
	for i in range(targetSpeed):
		motorsSetSpeed(leftMotors,i)
		motorsSetSpeed(rightMotors,i)		
		time.sleep(0.01)

def decelerateFromSpeed(leftMotors, rightMotors, startSpeed):
	for i in range(startSpeed,0,-1): # decrease
		motorsSetSpeed(leftMotors,i)
		motorsSetSpeed(rightMotors,i)		
		time.sleep(0.01)

def moveForward(leftMotors, rightMotors, maxSpeed):
	motorsSetDirection(leftMotors,Adafruit_MotorHAT.FORWARD)
	motorsSetDirection(rightMotors,Adafruit_MotorHAT.BACKWARD)
	accelerateToSpeed(leftMotors, rightMotors, maxSpeed)
	decelerateFromSpeed(leftMotors, rightMotors, maxSpeed)

def moveBackward(leftMotors, rightMotors, maxSpeed):
	motorsSetDirection(leftMotors,Adafruit_MotorHAT.BACKWARD)
	motorsSetDirection(rightMotors,Adafruit_MotorHAT.FORWARD)
	accelerateToSpeed(leftMotors, rightMotors, maxSpeed)
	decelerateFromSpeed(leftMotors, rightMotors, maxSpeed)

def turnLeftInPlace(leftMotors, rightMotors, maxSpeed):
	motorsSetDirection(leftMotors,Adafruit_MotorHAT.BACKWARD)
	motorsSetDirection(rightMotors,Adafruit_MotorHAT.BACKWARD)
	accelerateToSpeed(leftMotors, rightMotors, maxSpeed)
	decelerateFromSpeed(leftMotors, rightMotors, maxSpeed)

def turnRightInPlace(leftMotors, rightMotors, maxSpeed):
	motorsSetDirection(leftMotors,Adafruit_MotorHAT.FORWARD)
	motorsSetDirection(rightMotors,Adafruit_MotorHAT.FORWARD)
	accelerateToSpeed(leftMotors, rightMotors, maxSpeed)
	decelerateFromSpeed(leftMotors, rightMotors, maxSpeed)

def getMotors():
	leftMotors = []
	rightMotors = []
	for i in range(1,3):
		cMotor = mh.getMotor(i)
		cMotor.setSpeed(150)
		leftMotors.append(cMotor)

	for i in range(3,5):
		cMotor = mh.getMotor(i)
		cMotor.setSpeed(150)
		rightMotors.append(cMotor)
	return leftMotors, rightMotors