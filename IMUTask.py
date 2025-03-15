from imudriver import IMUDriver
from pyb import Pin

class IMUTask:
  
    def __init__(self, task_label):
        #RUM CALIBRATION LOGIC HERE
        self.IMU = IMUDriver()
         #create IMU object
        


    def EulerAngle(self, shares):
        #from IMU driver, capable of more functions that used, collect only Euler Angle
        while True:
            L_vel_set, R_vel_set , the_queue, IRcentroid, romiSetSpeed, Heading = shares
            Heading.put(self.IMU.get_eangle()) #thisreturns on z-component as other Euler angles do not apply to our planar movement
            #print(Heading.get())
            yield
