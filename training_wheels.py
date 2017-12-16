import RPi.GPIO as GPIO
import motor
from record import record_encoder_motion, finish_encoder_motion_recording, record_encoder_movements_per_speed, finish_encoder_movements_per_speed_recording
from ultrasonic import setup_ultrasonic_pin, send_ultrasonic_pulse, get_detected_edge_arrays
from util import save_2d_array_to_csv

import time
import json
import threading

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
    ultrasonic_pin = 23
    setup_ultrasonic_pin(ultrasonic_pin)
    for i in range(10):
        send_ultrasonic_pulse(ultrasonic_pin)
        time.sleep(1)
    
    edge_sets = get_detected_edge_arrays()
    print(json.dumps(edge_sets))
    save_2d_array_to_csv(edge_sets, 'saved_ultrasonic_recordings', 'test')
    print('finishing')

    '''
    print('suspend wheels in the air...')
    time.sleep(5)
    print('starting calibration')
    GPIO.setmode(GPIO.BCM)
    encoder_pins_motor_nums = motor.get_motor_number_for_encoder_pin(4,18,13,19)
    print(json.dumps(encoder_pins_motor_nums))
    print('calibration finished')
    time.sleep(3)

    print('beginning to record motion')

    filename = 'test.csv'
    t = threading.Thread(target=record_encoder_motion, kwargs={'encoder_pins_mapped_to_motor_nums': encoder_pins_motor_nums})
    t.daemon = True
    t.start()

    time.sleep(10)

    print('stopping motion recording')
    finish_encoder_motion_recording(filename)

    print('recording movements per speed')
    speed_motor_encoder = 13
    record_encoder_movements_per_speed(speed_motor_encoder, encoder_pins_motor_nums[speed_motor_encoder], 20)
    finish_encoder_movements_per_speed_recording('test')
    '''

    '''GPIO.setup(20, GPIO.IN)
    print(GPIO.input(20))
    GPIO.add_event_detect(20, GPIO.BOTH, callback=rising_callback)
    #GPIO.add_event_detect(20, GPIO.FALLING, callback=falling_callback)
    while True:
        time.sleep(60)
    '''

if __name__ == '__main__':
    main()