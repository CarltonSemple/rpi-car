#!/usr/bin/python

import RPi.GPIO as GPIO
from motor import getMotors, turnOffMotors, moveForward, moveBackward, turnLeftInPlace, turnRightInPlace, get_motor_number_for_encoder_pin
from record import record_encoder_motion, finish_encoder_motion_recording
from ultrasonic import setup_ultrasonic_pin, send_ultrasonic_pulse, get_detected_edge_arrays
from util import save_2d_array_to_csv, json_file_to_dictionary, save_json_to_file

import atexit

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer

import json
from threading import Thread
import time

leftMotors = []
rightMotors = []

maxSpeed = 50
turnSpeed = 50

motorFunctionQueue = []

_encoder_pins_motor_nums = {}

_ultrasonic_record = False
ultrasonic_pin = 23
ultrasonic_pulse_period = 1

def motorFunctionExecutor():
    while True:
        if (len(motorFunctionQueue) > 0):
            motorFunctionQueue[0]
            motorFunctionQueue.pop(0)
            turnOffMotors()
            time.sleep(15) # make thread wait for the timing of the called function
        else:
            time.sleep(0.01)

def is_encoder_config_command(command):
    return command['command_type'] == 'encoder_config'

def handle_encoder_config_command(command):
    global _encoder_pins_motor_nums
    if is_encoder_config_command(command) is False:
        print('called handle_encoder_config_command with invalid command_type')
        return

    if command['action'] == 'new_encoder_motor_calibration':
        '''
        TODO - call script to export pins
        '''
        if 'encoder_gpio_pins' not in command:
            print('command is missing encoder pin array')
            return
        pins = command['encoder_gpio_pins']
        if len(pins) != 4:
            print('encoder pin array does not have 4 pins')
            return
        print('starting calibration')
        GPIO.setmode(GPIO.BCM)
        _encoder_pins_motor_nums = get_motor_number_for_encoder_pin(pins[0], pins[1], pins[2], pins[3])
        print('saving to disk')
        save_json_to_file(json.dumps(_encoder_pins_motor_nums), './config', 'encoder_pins_to_motors.json', True)
    elif command['action'] == 'load_encoder_motor_calibration':
        print('loading encoder-motor pairs')
        _encoder_pins_motor_nums = json_file_to_dictionary('./config', 'encoder_pins_to_motors.json')
    else:
        print('no valid action present for handle_encoder_config_command')
        return
    print(json.dumps(_encoder_pins_motor_nums))

def is_motor_command(command):
    return command['command_type'] == 'turn' or command['command_type'] == 'move'

def handle_motor_command(command):
    if (command['command_type'] == 'turn'):
        if command['turnDirection'] == 'left':
            motorFunctionQueue.append(turnLeftInPlace(leftMotors, rightMotors, command['speed']))
        elif command['turnDirection'] == 'right':
            motorFunctionQueue.append(turnRightInPlace(leftMotors, rightMotors, command['speed']))
    elif (command['command_type'] == 'move'):
        if command['moveDirection'] == 'forward':
            motorFunctionQueue.append(moveForward(leftMotors, rightMotors, command['speed']))
        elif command['moveDirection'] == 'backward':
            motorFunctionQueue.append(moveBackward(leftMotors, rightMotors, command['speed']))
    else:
        print('invalid motor command')

def start_recording_encoder_movement(run_name):
    print('starting encoder recording')
    t = Thread(target=record_encoder_motion, kwargs={'encoder_pins_mapped_to_motor_nums': _encoder_pins_motor_nums})
    t.daemon = True
    print('about to start encoder thread')
    t.start()
    print('encoder thread started')

def start_ultrasonic_recording():
    print('starting ultrasonic recording')
    while _ultrasonic_record is True:
        print('pulse')
        send_ultrasonic_pulse(ultrasonic_pin)
        time.sleep(ultrasonic_pulse_period)

def stop_recording_encoder_movement(run_name):
    print('stop recording')
    finish_encoder_motion_recording(run_name+'.csv')

def is_record_command(command):
    return command['command_type'] == 'record_begin' or command['command_type'] == 'record_stop'

def handle_record_command(command):
    global _ultrasonic_record
    if ('filename' not in command):
        print('no filename given')
        return -1 # todo - throw an error...

    if (command['command_type'] == 'record_begin'):
        start_recording_encoder_movement(command['filename'])
        _ultrasonic_record = True
        setup_ultrasonic_pin(ultrasonic_pin)
        t = Thread(target=start_ultrasonic_recording)
        t.daemon = True
        t.start()
    elif (command['command_type'] == 'record_stop'):
        stop_recording_encoder_movement(command['filename'])
        print('stopping ultrasonic')
        _ultrasonic_record = False
        ultrasonic_edge_sets = get_detected_edge_arrays()
        save_2d_array_to_csv(ultrasonic_edge_sets, './saved_ultrasonic_recordings', command['filename'])
    else:
        print('invalid record command')


class CarCommandReceiver(WebSocket):
    def handleMessage(self):
        print('received:')
        print(self.data)
        #self.sendMessage(self.data)

        command = json.loads(self.data)

        if (is_encoder_config_command(command)):
            handle_encoder_config_command(command)
        elif (is_motor_command(command)):
            handle_motor_command(command)
        elif (is_record_command(command)):
            handle_record_command(command)
            
        self.sendMessage('ok')

    def handleConnected(self):
        print (self.address, 'connected')

    def handleClose(self):
        print (self.address, 'closed')

def main():
    GPIO.setmode(GPIO.BCM)
    atexit.register(turnOffMotors)
    
    lMotors, rMotors = getMotors()
    leftMotors.extend(lMotors)
    rightMotors.extend(rMotors)

    #turnOffMotors()

    executor = Thread(target=motorFunctionExecutor)
    executor.daemon = True
    executor.start()

    cls = CarCommandReceiver
    server = SimpleWebSocketServer('0.0.0.0', 8000, cls)
    server.serveforever()


if __name__ == '__main__':
    main()