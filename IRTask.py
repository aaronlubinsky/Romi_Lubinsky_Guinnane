from IRDriver import IRDriver
from pyb import Pin

class IRTask:
    '''This class will contribute an array of current IR voltages (length  15)'''
    def __init__(self, task_label):


        self.IRPinOut = [Pin.cpu.C4, Pin.cpu.C4, Pin.cpu.B1, Pin.cpu.C5, Pin.cpu.A6, Pin.cpu.A7, Pin.cpu.C2, Pin.cpu.C3] #List of nucleo pins for each sensor from index 1 - 15 (odd only used)
        self.IR_Array_Object = [] #Empty list to be filled with IR objects
        for pin in self.IRPinOut:
            self.IR_Array_Object.append(IRDriver(pin)) #Fill list object with objects of individual IR sensors

        cal_IR_question = input('Recalibrate IR Sensor? (Y/N)?') #do we want to recalibrate IR or use hardcoded value?
        if cal_IR_question == 'N':
            self.IRblack = [3010, 3005, 2766, 2722, 2735, 2703, 2891, 2979]
            self.IRwhite = [489, 490, 275, 265, 265, 261, 280, 308]
            #taken on a clear sky day @8:30AM Feb 25. Classroom lights on 
        else:
          pass  

        


    def getIRArray(self, shares):
        while True:
            L_vel_set, R_vel_set , the_queue, IRcentroid, IRsum, romiSetSpeed, Heading = shares
            rawIRReadings = list(map(lambda x: x.getValue() , self.IR_Array_Object)) #use driver to make list of IR sensors
            IRReadings = [(x-Low)/(High-Low) for x, Low, High in zip(rawIRReadings, self.IRwhite, self.IRblack)]

            IR_spacing = [-56, -40, -24, -8, 8, 24, 40, 56]  #in mm
            IRsum = 0
            centroid_numer = 0
            centroid_den = 0
            for x in range(len(IR_spacing)):
                centroid_numer += (IR_spacing[x]*IRReadings[x]*8)
                centroid_den += (IRReadings[x]*8)
                IRsum += (IRReadings[x])
            centroid = centroid_numer/centroid_den
            IRcentroid.put(int(centroid))
            IRsum.put(int(IRsum))
            
            yield
             
    def callibrateIR(self): #call this function (blocking code) when user selects new calibration 
        input('Press ENTER to read BLACK')
        self.IRblack = list(map(lambda x: x.getValue() , self.IR_Array_Object))
        print(self.IRblack)
        input('Press ENTER to read WHITE')
        self.IRwhite = list(map(lambda x: x.getValue() , self.IR_Array_Object))
        print(self.IRwhite)


        
    


