import pyb
from pyb import Pin, Timer
from bump import Bump


#Initialize Sleep Pins (White)
SLP_L = Pin(Pin.cpu.C1, mode = Pin.OUT_PP)
SLP_R = Pin(Pin.cpu.C0, mode = Pin.OUT_PP)
SLP_L.low()
SLP_R.low()

#bumpR = Bump(Pin.cpu.C11)
#bumpL = Bump(Pin.cpu.C9)

#bump = Bump(Pin.cpu.C11,Pin.cpu.C9)

