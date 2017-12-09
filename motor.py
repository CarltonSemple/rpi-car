#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import RPi.GPIO as GPIO
 
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
		time.sleep(0.001)

def decelerateFromSpeed(leftMotors, rightMotors, startSpeed):
	for i in range(startSpeed,0,-1): # decrease
		motorsSetSpeed(leftMotors,i)
		motorsSetSpeed(rightMotors,i)		
		time.sleep(0.001)

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

current_motor_num = 1
encoder_pin_nums = {}

def motor_calib_rising_callback(gpio_pin):
    #print(gpio_pin)
    encoder_pin_nums[gpio_pin] = current_motor_num

'''
note: wheels must be free for this, so car must be upside-down or suspended in the air
Returns a dictionary of encoder pins #s and motor #s, as visualized with the JSON:
{
	encoder_# : motor_#,
	encoder_# : motor_#
}
'''
def get_motor_number_for_encoder_pin(encoder_pin_1, encoder_pin_2, encoder_pin_3, encoder_pin_4):
    global current_motor_num
    global encoder_pin_nums
    encoder_pin_nums[encoder_pin_1] = 0
    encoder_pin_nums[encoder_pin_2] = 0
    encoder_pin_nums[encoder_pin_3] = 0
    encoder_pin_nums[encoder_pin_4] = 0
    for key, value in encoder_pin_nums.items():
        GPIO.setup(key, GPIO.IN)
        GPIO.add_event_detect(key, GPIO.RISING, callback=motor_calib_rising_callback)

    for m in range(1, 5):
        motor = mh.getMotor(m)
        current_motor_num = m
        motor.run(Adafruit_MotorHAT.FORWARD)
        target_speed = 100
        for i in range(target_speed):
            motor.setSpeed(i)
            time.sleep(0.001)
        for i in range(target_speed,0,-1): # decrease
            motor.setSpeed(i)		
            time.sleep(0.001)
        time.sleep(1)
    for m in range(1, 5):
        mh.getMotor(m).run(Adafruit_MotorHAT.RELEASE)
    #print('calibration finished')
    #print(json.dumps(encoder_pin_nums))
    return encoder_pin_nums