import pyb
from pyb import Pin, Timer

class Motor:
    '''A motor driver interface encapsulated in a Python class. Works with
    motor drivers using separate PWM and direction inputs such as the DRV8838
    drivers present on the Romi chassis from Pololu.'''
    '''Motor should accept queue and shares from user task, then implement direction'''
    def __init__(self, chan, PWM, DIR, nSLP):
        tim_3 = pyb.Timer(3, freq=100, prescaler=0)  # PWM Timer
        '''Initializes a Motor object'''
        # Init SLP pins
        self.SLP_pin = Pin(nSLP, mode=Pin.OUT_PP)
        # Init DIR pins
        self.DIR_pin = Pin(DIR, mode=Pin.OUT_PP)  
        # Init PWM pins  
        self.PWM_pin = tim_3.channel(chan, pin=Pin(PWM), mode=Timer.PWM)

    def setEffort(self, effort):
        '''Sets the present effort requested from the motor based on an input value
        between -100 and 100'''
        #print(f"setting effort at {effort}")
        if effort >= 0:              
            self.DIR_pin.low()
        else:
            self.DIR_pin.high()
        self.PWM_pin.pulse_width_percent(abs(effort)) 
        self.SLP_pin.high()

    def enable(self):
        '''Enables the motor driver by taking it out of sleep mode into brake mode'''
        self.setEffort(0)
        
    def disable(self):
        '''Disables the motor driver by taking it into sleep mode'''
        self.SLP_pin.low()

