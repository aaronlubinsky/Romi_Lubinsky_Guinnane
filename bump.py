#bump.py

import pyb
from pyb import Pin,ExtInt
import MotorTask

class Bump():
    '''This Class initalizes the bump sensor'''
    def __init__(self,RBPin,LBPin):
        #
        '''This initializes the bump sensor on the selected pin and enables
        external interrupts.'''
        
        self.rbPin = Pin(RBPin, mode=Pin.IN, pull = Pin.PULL_UP)
        self.lbPin = Pin(LBPin, mode=Pin.IN, pull = Pin.PULL_UP)
        self.rbPin.high()
        self.lbPin.high()
        #extint = ExtInt(self.bPin, ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, self.callback)
        #extint.enable
        self.btoggle = 0
        
    def callback(self,extint):
        '''This is the callback function for the bump sensor interrupt. When
        the interrupt is triggered, it will disable both motors.''' 
        LeftMotorTaskObj = MotorTask.MotorTask("Left Motor", chan=1, PWM=pyb.Pin.cpu.B4, DIR=pyb.Pin.cpu.B3,
                                            nSLP=pyb.Pin.cpu.C1, tim=1, chA_pin=pyb.Pin.cpu.A9, chB_pin=pyb.Pin.cpu.A8,
                                            Kp = 1, Ki = 0, Kd = 0)  
        RightMotorTaskObj = MotorTask.MotorTask("Right Motor", chan=2, PWM=pyb.Pin.cpu.B5, DIR=pyb.Pin.cpu.A10, 
                                            nSLP=pyb.Pin.cpu.C0, tim=2, chA_pin=pyb.Pin.cpu.A1, chB_pin=pyb.Pin.cpu.A0,
                                            Kp = 1, Ki = 0, Kd = 0)  
        #raise KeyboardInterrupt("Bump Sensor Activated!")
        LeftMotorTaskObj.disable()
        RightMotorTaskObj.disable()
        
    def update(self):
        '''Updates bumper toggle when bumper pin is low'''
        if self.rbPin.value() == 0 or self.lbPin.value() == 0:
            print("Bump!")
            self.btoggle = 1
            
    def bstate(self):
        '''Returns if bumper has been hit or not'''
        return self.btoggle        
            
    def reset(self):
        '''Resets bumper toggle'''
        self.btoggle = 0
    