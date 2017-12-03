#!/usr/bin/python

from motor import getMotors, turnOffMotors, moveForward, moveBackward, turnLeftInPlace, turnRightInPlace

import atexit

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer

leftMotors = []
rightMotors = []

maxSpeed = 50
turnSpeed = 50

class SocketReceiver(WebSocket):
    def handleMessage(self):
        print(self.data)
        if (self.data == "w"):
            moveForward(leftMotors, rightMotors, maxSpeed)
        elif (self.data == "s"):
            moveBackward(leftMotors, rightMotors, maxSpeed)
        elif (self.data == "a"):
            turnLeftInPlace(leftMotors, rightMotors, turnSpeed)
        elif (self.data == "d"):
            turnRightInPlace(leftMotors, rightMotors, turnSpeed)

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

    cls = SocketReceiver
    server = SimpleWebSocketServer('0.0.0.0', 8000, cls)
    server.serveforever()


if __name__ == '__main__':
    main()