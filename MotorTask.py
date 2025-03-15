import motor
import encoder
import time
import pyb

class MotorTask:

    def __init__(self, task_label, chan, PWM, DIR, nSLP, tim, chA_pin, chB_pin, Kp, Ki, Kd):
        self.task_label = task_label
        self.chan = chan
        self.PWM = PWM
        self.DIR = DIR
        self.nSLP = nSLP
        self.tim = tim
        self.chA_pin = chA_pin
        self.chB_pin = chB_pin
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.T2state = 0
        

    def drive(self, shares):

         # Main control loop for the motor.
        # Implements a PID loop to adjust motor effort based on desired and actual velocity.
        
        L_vel_set, R_vel_set , the_queue, IR_centroid, romiSetSpeed, dist_travelled, Heading = shares
        while True:
            if self.T2state == 0: #run once. create the motor and encoder objects

                
                
                #Create driver objects
                self.Motor = motor.Motor(self.chan, self.PWM, self.DIR, self.nSLP)
                self.Encoder = encoder.Encoder(self.tim, self.chA_pin, self.chB_pin)

                self.T2state = 1 #always move to next state
                self.errorSum = 0
                self.error_min1 = 0
                self.ticks_last = 0
                self.wheel_rotations = 0

            elif self.T2state == 1:
                #update set velocity with correct share
                if self.task_label in {'L', 'Left', 'Left Motor'}:
                    self.vel_set = float(L_vel_set.get())
                    #print(f"left motor set velo: {self.vel_set}")
                elif self.task_label in {'R', 'Right', 'Right Motor' }:
                    self.vel_set = float(R_vel_set.get())
                else:
                    print("Motor Task not Assosciated with L or R motor")

                '''This is the operating state of the motor task. PID loop'''
                #Read encoder
                self.Encoder.update()
                try:
                    
                    self.pos = self.Encoder.get_position()
                    
                    if self.task_label in {'L', 'Left', 'Left Motor'}:
                        dist_travelled.put(int(self.pos/1440))
                    
                    #print(self.pos)
                    self.vel = float(self.Encoder.get_velocity())
                    self.error = float(self.vel_set - self.vel)
                    

                    #Proportional
                    self.P = self.error*self.Kp
                    
                    #Integral
                    self.errorSum += self.error
                    self.I = self.Ki * self.errorSum
                    
                    #Derivative
                    self.ticks_now = time.ticks_us()
                    self.errorDer = (self.error_min1 - self.error)/(time.ticks_diff(self.ticks_last, self.ticks_now))
                    self.error_min1 = self.error
                    self.ticks_last = self.ticks_now
                    self.D = self.errorDer * self.Kd
                
                    #Sum PID
                    self.PWM = int(self.P + self.I + self.D)
                    #print(self.PWM)
                    self.Motor.setEffort(self.PWM)

                except AttributeError:
                    print('Motor Task is missing data')


            yield #all of T2 states should flow to this yield

    def disable(self):
        self.Motor.disable()
