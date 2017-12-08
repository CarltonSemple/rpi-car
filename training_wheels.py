import RPi.GPIO as GPIO
import motor

import time
import json

count = 0

def falling_callback(channel):
    global count
    print('Falling edge {} detected on channel {}'.format(count, channel))
    count = count + 1

def rising_callback(channel):
    global count
    print('Rising edge {} detected on channel {}'.format(count, channel))
    count = count + 1

def main():    
    GPIO.setmode(GPIO.BCM)
    print(json.dumps(motor.get_motor_number_for_encoder_pin(4,18,13,19)))
    
    '''GPIO.setup(20, GPIO.IN)
    print(GPIO.input(20))
    GPIO.add_event_detect(20, GPIO.BOTH, callback=rising_callback)
    #GPIO.add_event_detect(20, GPIO.FALLING, callback=falling_callback)
    while True:
        time.sleep(60)
    '''

if __name__ == '__main__':
    main()