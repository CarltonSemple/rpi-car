#!/usr/bin/python

from motor import getMotors, turnOffMotors, moveForward, moveBackward, turnLeftInPlace, turnRightInPlace

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

def motorFunctionExecutor():
    while True:
        if (len(motorFunctionQueue) > 0):
            motorFunctionQueue[0]
            motorFunctionQueue.pop(0)
            turnOffMotors()
            time.sleep(15) # make thread wait for the timing of the called function
        else:
            time.sleep(0.01)

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

def start_recording():
    print('start recording - not implemented')

def stop_recording():
    print('stop recording - not implemented')

def is_record_command(command):
    return command['command_type'] == 'record_begin' or command['command_type'] == 'record_stop'

def handle_record_command(command):
    if (command['command_type'] == 'record_begin'):
        start_recording()
    elif (command['command_type'] == 'record_stop'):
        stop_recording()
    else:
        print('invalid record command')


class CarCommandReceiver(WebSocket):
    def handleMessage(self):
        print('received:')
        print(self.data)
        #self.sendMessage(self.data)

        command = json.loads(self.data)

        if (is_motor_command(command)):
            handle_motor_command(command)
        elif (is_record_command(command)):
            handle_record_command(command)
            
        self.sendMessage('ok')

    def handleConnected(self):
        print (self.address, 'connected')

    def handleClose(self):
        print (self.address, 'closed')

def main():
    atexit.register(turnOffMotors)
    
    lMotors, rMotors = getMotors()
    leftMotors.extend(lMotors)
    rightMotors.extend(rMotors)

    #turnOffMotors()

    executor = Thread(target=motorFunctionExecutor)
    #executor.daemon = True
    executor.start()

    cls = CarCommandReceiver
    server = SimpleWebSocketServer('0.0.0.0', 8000, cls)
    server.serveforever()


if __name__ == '__main__':
    main()