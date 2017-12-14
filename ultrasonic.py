import RPi.GPIO as GPIO
import datetime
import time

_ready_to_send_pulse = True
_start_time = 0
_send_count = 0
_receive_count = 0
_valid = True


def setup_ultrasonic_pin(ultrasonic_pin_number):
    GPIO.setup(ultrasonic_pin_number, GPIO.IN)
    GPIO.remove_event_detect(ultrasonic_pin_number)
    GPIO.add_event_detect(ultrasonic_pin_number, GPIO.BOTH, callback=_callback_falling)

def send_ultrasonic_pulse(ultrasonic_pin_number):
    global _ready_to_send_pulse
    global _start_time
    global _send_count
    global _valid
    if _ready_to_send_pulse is not True:
        print('cannot send pulse')
        return
    _send_count += 1
    print('sending pulse ', _send_count)
    #_ready_to_send_pulse = False
    _valid = False
    GPIO.setup(ultrasonic_pin_number, GPIO.OUT)
    GPIO.output(ultrasonic_pin_number, GPIO.LOW)
    time.sleep(.000002)
    GPIO.output(ultrasonic_pin_number, GPIO.HIGH)
    time.sleep(.000005)
    GPIO.output(ultrasonic_pin_number, GPIO.LOW)
    time.sleep(.000002)
    GPIO.setup(ultrasonic_pin_number, GPIO.IN)
    _start_time = datetime.datetime.now() #time.time()
    _valid = True
    print('sent ', _send_count)
    #print('_start_time: ', _start_time)
    '''GPIO.setup(ultrasonic_pin_number, GPIO.IN)
    GPIO.remove_event_detect(ultrasonic_pin_number)
    GPIO.add_event_detect(ultrasonic_pin_number, GPIO.BOTH, callback=_callback_falling)
    '''

'''
speed of sound: 343 meters/second
34300 centimeters
'''

_edges = []

'''
to be set to activate on the high signal
'''
def _callback_falling(ultrasonic_gpio_pin):
    global _ready_to_send_pulse
    global _receive_count
    #_receive_count += 1
    #if _ready_to_send_pulse is True:
    #    return
    #end_time = time.time()
    #local_start_time = _start_time
    #print('end time: ', end_time)

    #_ready_to_send_pulse = True

    '''
    seconds = end_time - local_start_time
    #print(seconds, ' seconds, ', _receive_count) # already in seconds
    cm = (34500 * seconds)
    print(cm, _receive_count)
    '''
    if _valid is True:
        _ready_to_send_pulse = True
        present = datetime.datetime.now()
        difference = (present - _start_time).total_seconds() * 1000000.0
        difference = (difference / 58.0) + 7
        print(difference, ' cm')
        #print(str(datetime.datetime.now()), 'falling')

    #print('signal received after ', time.time() - _start_time)
    #GPIO.setup(ultrasonic_gpio_pin, GPIO.OUT)
    
    '''GPIO.setup(ultrasonic_gpio_pin, GPIO.IN)
    GPIO.remove_event_detect(ultrasonic_gpio_pin)
    GPIO.add_event_detect(ultrasonic_gpio_pin, GPIO.RISING, callback=_callback_rising)
    '''

def _callback_rising(ultrasonic_gpio_pin):
    global _ready_to_send_pulse
    global _receive_count
    _receive_count += 1
    #if _ready_to_send_pulse is True:
    #    return
    end_time = time.time()
    local_start_time = _start_time
    #print('end time: ', end_time)

    _ready_to_send_pulse = True

    seconds = end_time - local_start_time
    #print(seconds, ' seconds, ', _receive_count) # already in seconds
    #cm = (34500 * seconds)
    #print(cm, _receive_count)
    
    print(str(datetime.datetime.now()), 'rising')

    #print('signal received after ', time.time() - _start_time)
    #GPIO.setup(ultrasonic_gpio_pin, GPIO.OUT)
    GPIO.setup(ultrasonic_gpio_pin, GPIO.IN)
    GPIO.remove_event_detect(ultrasonic_gpio_pin)
    #GPIO.add_event_detect(ultrasonic_gpio_pin, GPIO.FALLING, callback=_callback_falling)
    


_epoch = datetime.datetime.utcfromtimestamp(0)

def _unix_time_millis(dt):
    return (dt - _epoch).total_seconds() * 1000.0