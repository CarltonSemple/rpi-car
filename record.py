from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import RPi.GPIO as GPIO
import datetime
import time
import json
import os

from motor import accelerateToSpeed, decelerateFromSpeed, getMotor
from util import save_dictionary_to_csv

def finish_encoder_motion_recording(filename):
    global _record_now
    _record_now = False
    print(json.dumps(_motor_movement_events))

    recording_dir = './saved_encoder_recordings'
    if os.path.isdir(recording_dir) is not True:
        os.mkdir(recording_dir)
    save_dictionary_to_csv(_motor_movement_events, recording_dir+'/'+filename)

def record_encoder_motion(encoder_pins_mapped_to_motor_nums):
    global _encoder_pins_motor_nums
    global _record_now
    global _motor_movement_events
    if _record_now is True:
        print('system is already recording')
        return
    for i in range(1,5):
        _motor_movement_events[i] = []
    #_encoder_pins_motor_nums = encoder_pins_mapped_to_motor_nums # not reliable method of copying.. inconsistent results
    for key, value in encoder_pins_mapped_to_motor_nums.items():
        _encoder_pins_motor_nums[key] = value
    _setup_encoder_pins_with_callback(_encoder_pins_motor_nums)
    _record_now = True
    while _record_now:
        time.sleep(1)

'''
Iterates through all of the speeds, 0-255, recording the average encoder activations per
'''
def record_encoder_movements_per_speed(encoder_gpio_pin, motor_number):
    global _speed
    global _recording_motor_number
    global _movements_per_speed
    GPIO.setup(encoder_gpio_pin, GPIO.IN)
    GPIO.remove_event_detect(encoder_gpio_pin)
    GPIO.add_event_detect(encoder_gpio_pin, GPIO.RISING, callback=_callback_record_encoder_movements_per_speed)
    _recording_motor_number = motor_number
    _movements_per_speed = []

    getMotor(motor_number).run(Adafruit_MotorHAT.FORWARD)

    for i in range(255):
        _movements_per_speed.append(0)
    
    if _record_now is True:
        print('system is already recording')
        return
    for i in range(0,255):
        _speed = i
        print('speed: ', _speed)
        print(json.dumps(_movements_per_speed))
        accelerateToSpeed(_speed, _speed + 1, [getMotor(motor_number)], [])
        time.sleep(15)
    print('finishing up')
    decelerateFromSpeed(_speed, 0, [getMotor(motor_number)], [])
    getMotor(motor_number).run(Adafruit_MotorHAT.RELEASE)
    print(_movements_per_speed)

_record_now = False    
_encoder_pins_motor_nums = {} # map of encoder pins -> motor numbers
_motor_movement_events = {} # map of motor numbers (Adafruit HAT) -> time of movements

# variables for record_encoder_movements_per_speed
_speed = 0
_movements_per_speed = []

def _callback_record_encoder_movements_per_speed(encoder_gpio_pin):
    global _movements_per_speed
    if _speed >= len(_movements_per_speed):
        print('_movements_per_speed does not have enough array values for speed ', _speed)
        print('_movements_per_speed is of size ', len(_motor_movement_events), ' elements')
        return
    _movements_per_speed[_speed] = _movements_per_speed[_speed] + 1

def _callback_record_encoder_motion(encoder_gpio_pin):
    global _motor_movement_events
    #print(encoder_gpio_pin)
    motor_number = _encoder_pins_motor_nums[encoder_gpio_pin]
    #print(motor_number)
    _motor_movement_events[motor_number].append(str(datetime.datetime.now()))

def _setup_encoder_pins_with_callback(encoder_pins_as_keys_map):
    for key, value in encoder_pins_as_keys_map.items():
        GPIO.setup(key, GPIO.IN)
        GPIO.remove_event_detect(key)
        GPIO.add_event_detect(key, GPIO.RISING, callback=_callback_record_encoder_motion)
