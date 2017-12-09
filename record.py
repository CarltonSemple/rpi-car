import RPi.GPIO as GPIO
import datetime
import time
import json
import os

from util import save_dictionary_to_csv

def finish_encoder_motion_recording(filename):
    global _record_now
    _record_now = False
    print(json.dumps(_motor_movement_events))

    recording_dir = './saved_recordings'
    if os.path.isdir(recording_dir) is not True:
        os.mkdir(recording_dir)
    save_dictionary_to_csv(_motor_movement_events, recording_dir+'/'+filename)

def record_encoder_motion(encoder_pins_mapped_to_motor_nums):
    global _encoder_pins_motor_nums
    global _record_now
    global _motor_movement_events
    for i in range(1,5):
        _motor_movement_events[i] = []
    #_encoder_pins_motor_nums = encoder_pins_mapped_to_motor_nums # not reliable method of copying.. inconsistent results
    for key, value in encoder_pins_mapped_to_motor_nums.items():
        _encoder_pins_motor_nums[key] = value
    _setup_encoder_pins_with_callback(_encoder_pins_motor_nums)
    _record_now = True
    while _record_now:
        time.sleep(1)

_record_now = False    
_encoder_pins_motor_nums = {} # map of encoder pins -> motor numbers
_motor_movement_events = {} # map of motor numbers (Adafruit HAT) -> time of movements

def _movement_callback(encoder_gpio_pin):
    global _motor_movement_events
    #print(encoder_gpio_pin)
    motor_number = _encoder_pins_motor_nums[encoder_gpio_pin]
    #print(motor_number)
    _motor_movement_events[motor_number].append(str(datetime.datetime.now()))


def _setup_encoder_pins_with_callback(encoder_pins_as_keys_map):
    for key, value in encoder_pins_as_keys_map.items():
        GPIO.setup(key, GPIO.IN)
        GPIO.remove_event_detect(key)
        GPIO.add_event_detect(key, GPIO.RISING, callback=_movement_callback)
