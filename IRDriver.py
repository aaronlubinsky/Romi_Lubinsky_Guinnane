from pyb import Pin, Timer, ADC

'''IR Driver'''
class IRDriver:
    '''this class is converned with driving a single IR sensor to simplify the task that collects an array of IR data'''
    def __init__(self, SensorPin):
        #self.pin = Pin(SensorPin, mode = Pin.IN)
        self.pinADC = ADC(SensorPin)

    def getValue(self):
        return self.pinADC.read()                  # read an analog value