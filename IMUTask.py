from imudriver import IMUDriver
from pyb import Pin

class IMUTask:
    '''This class will contribute Euler angles and angular velocities'''
    def __init__(self, task_label):
        #RUM CALIBRATION LOGIC HERE
        self.IMU = IMUDriver()

        


    def EulerAngle(self, shares):
        '''Puts Euler angle associated with heading from IMU 
        into the share, and returns the value.'''
        while True:
            L_vel_set, R_vel_set , UI_stop, the_queue, IR_centroid, IRSum, romiSetSpeed, Heading, AngularVelo, distTraveled = shares
            #print(self.IMU.calstatus())
            Heading.put(self.IMU.get_eangle())
            #print(Heading.get())
            yield

    def AngularVelo(self, shares):
        '''Puts angular velocity associated with heading from IMU 
        into the share, and returns the value.'''
        while True:
            L_vel_set, R_vel_set , UI_stop, the_queue, IR_centroid, IRSum, romiSetSpeed, Heading, AngularVelo, distTraveled = shares
            #print(self.IMU.calstatus())
            gyro_z = self.IMU.get_angvelocity()
            #print(f" GYRO FROM IMU TASK: {gyro_z} ")
            AngularVelo.put(gyro_z)
            #print(AngularVelo.get())
            yield