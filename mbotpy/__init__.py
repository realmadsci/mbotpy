import contextlib
import time
import signal
import struct

import serial

class _mBot:
    def __init__(self, port, timeout=10):
        self._ser = serial.Serial(port,baudrate=115200,timeout=timeout)

    def close(self):
        self._ser.close()

    def _sendFrame(self, data):
        self._ser.write(data)

    def _readOk(self):
        '''Read an OK symbol'''
        ok = self._ser.read(4)
        if ok != bytes([0xff, 0x55, 0x0d, 0x0a]):
            raise RuntimeError('Got invalid OK symbol = ' + str(ok))

    def _readFrame(self):
        # First get a start delimiter of 0xFF55
        start = self._ser.read_until(bytes([0xFF, 0x55]))
        if (len(start) < 2) or (start[-2:] != bytes([0xFF, 0x55])):
            raise TimeoutError()

        # Next, read the header info (2 bytes)
        header = self._ser.read(2)
        if len(header) != 2:
            raise TimeoutError()

        extID = int(header[0])
        typeID = int(header[1])

        if typeID == 1:
            value = self._ser.read(1)[0]
        if typeID == 2:
            value = self.readFloat()
        if typeID == 3:
            value = self.readShort()
        if typeID == 4:
            value = self.readString()
        if typeID == 5:
            value = self.readDouble()

        # Now read the closing delimiter and verify that it is closed
        ending = self._ser.read_until(bytes([0x0D, 0x0A]))
        if (len(ending) != 2) or (ending[-2:] != bytes([0x0D, 0x0A])):
            raise TimeoutError()

        return value

    def readFloat(self):
        return struct.unpack('<f', self._ser.read(4))[0]

    def readShort(self, position):
        return struct.unpack('<h', self._ser.read(2))[0]

    def readString(self, position):
        l = int(self._ser.read(1))
        return self._ser.read(l).decode('ascii')

    def readDouble(self, position):
        return struct.unpack('<d', self._ser.read(8))[0]

    def float2bytes(self,fval):
        return struct.pack("<f",fval)

    def short2bytes(self,sval):
        return struct.pack("<h",sval)

    def doRGBLed(self,port,slot,index,red,green,blue):
        self._sendFrame(bytes([0xff,0x55,0x9,0x0,0x2,0x8,port,slot,index,red,green,blue]))
        self._readOk()

    def doRGBLedOnBoard(self,index,red,green,blue):
        self.doRGBLed(0x7,0x2,index,red,green,blue)
        self._readOk()

    def doMotor(self,port,speed):
        self._sendFrame(bytes([0xff,0x55,0x6,0x0,0x2,0xa,port]) + self.short2bytes(speed))
        self._readOk()

    def doMove(self,leftSpeed,rightSpeed):
        '''
        Set motor speed of both motors at once.
        Range is -1.0 to +1.0, positive is forward.
        '''
        # Note: Flip left motor backward so that they both move "together":
        leftBytes = self.short2bytes(-round(leftSpeed*255))
        rightBytes = self.short2bytes(round(rightSpeed*255))
        self._sendFrame(bytes([0xff,0x55,0x7,0x0,0x2,0x5]) + leftBytes + rightBytes)
        self._readOk()

    def doServo(self,port,slot,angle):
        self._sendFrame(bytes([0xff,0x55,0x6,0x0,0x2,0xb,port,slot,angle]))
        self._readOk()

    def doBuzzer(self,buzzer,time=0):
        '''
        Set frequency and duration of buzzer beep.
        buzzer = frequency in Hz
        time = time in seconds
        '''
        self._sendFrame(bytes([0xff,0x55,0x7,0x0,0x2,0x22]) + self.short2bytes(round(buzzer)) + self.short2bytes(round(time*1000)))
        self._readOk()

    def doSevSegDisplay(self,port,display):
        self._sendFrame(bytes([0xff,0x55,0x8,0x0,0x2,0x9,port]) + self.float2bytes(display))
        self._readOk()

    def doIROnBoard(self,message):
        self._sendFrame(bytes([0xff,0x55,len(message)+3,0x0,0x2,0xd,message]))
        self._readOk()

    def requestLight(self,port=6,extID=0):
        self._sendFrame(bytes([0xff,0x55,0x4,extID,0x1,0x3,port]))
        return self._readFrame()

    def requestButtonOnBoard(self,extID=0):
        self._sendFrame(bytes([0xff,0x55,0x4,extID,0x1,0x1f,0x7]))
        return self._readFrame()

    def requestIROnBoard(self,extID=0):
        self._sendFrame(bytes([0xff,0x55,0x3,extID,0x1,0xd]))
        return self._readFrame()

    def requestUltrasonicSensor(self,port=3,extID=0):
        self._sendFrame(bytes([0xff,0x55,0x4,extID,0x1,0x1,port]))
        return self._readFrame()

    def requestLineFollower(self,port=2,extID=0):
        '''Returns dictionary for "left" or "right" sees white'''
        self._sendFrame(bytes([0xff,0x55,0x4,extID,0x1,0x11,port]))
        v = int(self._readFrame())
        r = {
            "left" : (v & 0x2 != 0),
            "right" : (v & 0x1 != 0)
        }
        return r


@contextlib.contextmanager
def openSerial(port):
    mbot = _mBot(port)
    try:
        yield mbot
    finally:
        mbot.close()
