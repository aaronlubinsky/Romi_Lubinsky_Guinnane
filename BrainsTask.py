import time



class Brains:

    def __init__(self, task_label, Kp, Ki, Kd):
        '''
        Constructor for the Brains class.
        This class is intended to act as a PID controller for the Romi robot. It delcares two tasks seperately
        It receives sensor data (centroid, bump sensors, speed, heading) and decouples 
        the desired linear velocity and yaw rate for the robot.
        
        Parameters:
          task_label: A label identifying the task (not used further in the code).
          Kp, Ki, Kd: PID constants for proportional, integral, and derivative terms.
        '''
        self.BrainState = 0
        self.Kp = Kp #defined in main
        self.Ki = Ki
        self.Kd = Kd
        self.linefollow == 0 


    def track(self, shares):
        L_vel_set, R_vel_set , the_queue, IR_centroid, romiSetSpeed, Heading = shares

        self.checkpoint = 'A'
        headingDatum = Heading.get() #what is original heading
        distanceDatum = 0
        while True:
            
            if self.checkpoint == 'A':
                self.BrainState == self.linefollow
                self.speed == 50 #
                if (Heading.get() - headingDatum) > 100: 
                    self.checkpoint == 'B'

            if self.checkpoint == 'B':
                self.BrainState == self.linefollow
                self.speed == 15 
                if (yawRaw < 10): 
                    self.checkpoint == 'C'

            if self.checkpoint == 'C':
                self.BrainState == self.linefollow
                self.speed == 50
                if (IR_array_total) < 1000
                    self.checkpoint == 'D'
                    headingDatum = Heading.get #recallibrate heading datum
                    distanceDatum = 0

            if self.checkpoint == 'D':
                self.BrainState == self.driveStraight
                self.speed == 50 #GEUSS
                if (distanceTraveled - distanceDatum) > 100: #GUSS
                    self.checkpoint == 'E'

            if self.checkpoint == 'E':
                self.BrainState == self.linefollow
                self.speed == 50 #GEUSS
                if (IR_array_total) > 2000:
                    self.checkpoint == 'F'
                    headingDatum = Heading.get()
                    distanceDatum = 0

            if self.checkpoint == 'F':
                self.BrainState == self.driveStraight
                self.speed == 50
                if (distanceTraveled - distanceDatum) > 100: #GEUSS
                    self.checkpoint == 'G'

            if self.checkpoint == 'G':
                self.BrainState == self.linefollow
                self.speed == 50
                if (IR_array_total) < 1000: #GEUSS
                    self.centroid == 'H'
                    headingDatum = Heading.get #recallibrate heading datum
                    distanceDatum = 0

            if self.checkpoint == 'H':
                self.BrainState == self.driveStraight
                self.speed == 50
                if (distanceTraveled - distanceDatum) > 100: #GEUSS
                    self.checkpoint == 'I'

            if self.checkpoint == 'I':
                self.BrainState == self.linefollow
                self.speed == 50
                    



    def run(self, shares):
        '''
        Main PID control loop for the robot.
        
        Functionality:
          - If the robot is in the line-following initialization state, set up sensor references and reset PID errors.
          - When in BrainState 1 (line following), compute PID control based on the centroid sensor input.
          - When in BrainState 2 (orientation control, "Go North"), compute PID control based on the heading.
          - Adjust left and right motor speeds based on the computed yaw rate.
        '''
        L_vel_set, R_vel_set , the_queue, IR_centroid, romiSetSpeed, Heading = shares
        while True:
            if self.BrainState == self.linefollow: #Run once, like init state
               self.centroid = IR_centroid
               self.errorSum = 0
               self.error_min1 = 0
               self.ticks_last = 0
               self.BrainState = 1 #manually set mode by default
               self.romiSetSpeed = romiSetSpeed
               self.Heading = Heading

            elif self.BrainState == 1:#FOLLOW LINE
                
                self.error = -1*(self.centroid.get())
                

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
                self.yawRate = int(self.P + self.I + self.D)


                if romiSetSpeed.get() == 0:
                  print('L_vel/R_vel = 0')
                  L_vel_set.put(0)
                  R_vel_set.put(0)      
                else:
                    print('L_vel/R_vel SET')
                    L_vel_set.put(int(self.romiSetSpeed.get() - 0.5*self.yawRate))
                    R_vel_set.put(int(self.romiSetSpeed.get() + 0.5*self.yawRate))
            
            
            
            elif self.BrainState == 2: #Adjust heading to match HeadingDatum
               
                '''This state is the 'simple, line following PID loop' for the Romi's YAW RATE as a whole'''
                self.error = ((self.Heading.get())/16)#in degrees
                if self.error > 180:
                    self.error = self.error-360
                print(f" ERRROR: {self.error}  ERRORSUM: {self.errorSum}")
                
                #Proportional
                self.P = self.error*1 
       
                #Integral
                self.errorSum += self.error 
                if abs(self.errorSum) > 1000:
                    self.errorSum = 1000 * (self.errorSum/abs(self.errorSum))
                self.I = 0  * self.errorSum
                
                #Derivative
                self.ticks_now = time.ticks_us()
                self.errorDer = (self.error_min1 - self.error)/(time.ticks_diff(self.ticks_last, self.ticks_now))
                self.error_min1 = self.error
                self.ticks_last = self.ticks_now
                self.D = self.errorDer * self.Kd
            
                #Sum PID
                self.yawRate = int(self.P + self.I + self.D)

                if romiSetSpeed.get() == 0:
                  L_vel_set.put(0)
                  R_vel_set.put(0)      
                else:
                    L_vel_set.put(int(self.romiSetSpeed.get() - 0.5*self.yawRate))
                    R_vel_set.put(int(self.romiSetSpeed.get() + 0.5*self.yawRate))
            yield
