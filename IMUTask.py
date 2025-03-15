from imudriver import IMUDriver
from pyb import Pin

class IMUTask:
    '''This class will contribute an array of current IR voltages (length  15)'''
    def __init__(self, task_label):
        #RUM CALIBRATION LOGIC HERE
        self.IMU = IMUDriver()

        


    def EulerAngle(self, shares):
        while True:
            L_vel_set, R_vel_set , the_queue, IRcentroid, romiSetSpeed, Heading = shares
            #print(self.IMU.calstatus())
            Heading.put(self.IMU.get_eangle())
            print(Heading.get())
            yield