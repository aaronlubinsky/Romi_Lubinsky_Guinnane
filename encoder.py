import pyb
from time import ticks_us, ticks_diff # Use to get dt value in update()
from pyb import Timer, Pin

class Encoder:
 '''A quadrature encoder decoding interface encapsulated in a Python class'''

 def __init__(self, tim, chA_pin, chB_pin):
     '''Initializes an Encoder object'''

     self.position = 0 # Total accumulated position of the encoder
     self.prev_count = 0 # Counter value from the most recent update
     self.delta = 0 # Change in count between last two updates
     self.dt = 0 # Amount of time between last two updates
     self.prev_ticks = ticks_us() #Initializes previous ticks
     
     self.del_min1 = 0
     self.del_min2 = 0
     
     self.dt_min1 = 0
     self.dt_min2 = 0
     
     #Initialize encoder timer and channels
     self.timer = pyb.Timer(tim, period = 0xFFFF, prescaler = 0)
     self.chA = self.timer.channel(2, pin = chA_pin, mode = pyb.Timer.ENC_AB )
     self.chB = self.timer.channel(1, pin = chB_pin, mode = pyb.Timer.ENC_AB )
     
    
     
 def update(self):
     '''Runs one update step on the encoder's timer counter to keep
     track of the change in count and check for counter reload'''
     
     AR = 65_535 #Auto Reload Value
     
     self.now = ticks_us()
     self.dt = ticks_diff(self.now,self.prev_ticks)
     self.delta = self.timer.counter() - self.prev_count
     
     #Deal with delta over/underflow
     if self.delta > (AR+1)/2:
         self.delta = self.delta - (AR + 1)
     elif self.delta < -(AR+1)/2:
         self.delta = self.delta + (AR + 1)
     try:         
        self.del_min2 = self.del_min1     #if past second data collection. average 
        self.del_min1 = self.delta
        
        self.dt_min2 = self.dt_min1
        self.dt_min1 = self.dt

        self.position = self.position + self.delta
        
        self.vel = (self.del_min2 + self.del_min1 +self.delta)/(self.dt_min1 + self.dt_min2+ self.dt) 
        
        self.prev_count = self.timer.counter()
        self.prev_ticks = ticks_us()
        
     except (ZeroDivisionError, AttributeError):
        self.position = self.position + self.delta
        self.vel = self.position/self.dt
        self.prev_ticks = ticks_us()
        self.prev_count = self.timer.counter()
        
        
 def get_position(self):
     
     '''Returns the most recently updated value of position as determined
     within the update() method'''
     return self.position

 def get_velocity(self):
     '''Returns a measure of velocity using the the most recently updated
     value of delta as determined within the update() method'''
     try:
        return self.vel
     except AttributeError:
        print('No velocity data in encoder driver')
     

 def zero(self):
     '''Sets the present encoder position to zero and causes future updates
     to measure with respect to the new zero position'''
     self.position = 0
     self.prev_count = self.timer.counter()
     self.delta = 0
     self.del_min2 = 0
     self.del_min1 = 0
     
pass