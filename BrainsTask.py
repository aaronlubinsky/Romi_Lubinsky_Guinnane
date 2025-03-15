import time
import pyb
from bump import Bump


class Brains:

    def __init__(self, task_label):
        '''this Task will act as a PID for the Romi as a whole. Recieving centroid data, bump sensor data, and speed from UI.
        Will decouple desired v and psi_dot '''

        #Define States for Type of Movement
        self.BrainState = 0
        self.linefollow = 1
        self.driveStraight = 2

        #Declare Battery Level & Initial PID consts
        PB0 = pyb.ADC(pyb.Pin.cpu.B0)
        BatteryLevel = PB0.read()*3.3/4095*14.7/4.7
        print(f"Battery Level:  {BatteryLevel}V " )


        #self.Kp = 1 - 0.075*BatteryLevel
        self.Kp = 0.50 #Orig 0.55
        self.Kp = float(input("Enter Kp"))
        self.checkDdist = float(input("Enter D dist (0.602)"))
        #From testing, I've foudn KP = 0.48 works pretty consistently for 
        #BV = 7.26648 V
        #KP 4.5 WORKS AT 7.3V
        
        
        self.Ki = 0
        self.Kd = 0

        #init bump
        self.bump = Bump(pyb.Pin.cpu.C11,pyb.Pin.cpu.C9)
    

    def track(self, shares):
        L_vel_set, R_vel_set , UI_stop, the_queue, IR_centroid, IRSum, romiSetSpeed, Heading, AngularVelo, distTraveled = shares
        self.angularVelo = AngularVelo.get()
        self.IRsum = IRSum.get()
        self.checkpoint = '0' #initialize
        UI_stop.put(True) #UI task doesnt always run before this
        distanceDatum = 0
        
        while True:
            if self.checkpoint == '0':
                print('CHECKPOINT 0')
                #print(UI_stop.get())
                if (UI_stop.get() == 0):
                    self.checkpoint = 'A'
                    self.headingDatum = Heading.get()/16 #what is original heading when enter is pressed
                    print(f" Heading Datum: {self.headingDatum}")

            if self.checkpoint == 'A': #LINE FOLLOW FROM BEGINNING TO DIAMOND
                print('CHECKPOINT A')
                self.BrainState = self.linefollow
                romiSetSpeed.put(22)  # GUESS
                # Compute the heading change correctly considering wraparound
                current_heading = Heading.get() / 16  # Convert raw value to degrees
                # Compute the shortest angular difference (corrected for 360° wraparound)
                delta_Heading = (current_heading - self.headingDatum + 180) % 360 - 180
                

                print(delta_Heading)
                print(f"Heading difference is: {abs(delta_Heading)} degrees")

                # Ensure the threshold is also scaled
                if (abs(delta_Heading) > (80)): 
                    self.checkpoint = 'B' #TODO CHECKPOINT SKIP, RESTORE TO B WHEN DONE
                    #self.headingDatum = Heading.get()  # Set new datum to 90 degrees CW from start
                    self.headingDatum += (90)  # Set new datum to 90 degrees CW from start
                    distanceDatum = distTraveled.get()  # Reset distance traveled datum
                    self.errorSum = 0
                    self.error_min1 = 0

            elif self.checkpoint == 'B': #DRIVE STRAIGHT THROUGH DIAMOND
                print(f" CHECKPOINT B   dist traveled: {distTraveled.get() - distanceDatum}")
                self.BrainState = self.driveStraight
                romiSetSpeed.put(27) #GEUSS
                if (distTraveled.get()  - distanceDatum) >= 0.6:
                    print('moving to checkpoint C')
                    self.checkpoint = 'C' #SKIP C and D
                    self.errorSum = 0
                    distanceDatum = distTraveled.get()
                    self.headingDatum = Heading.get()/16 
                
            elif self.checkpoint == 'C': #FOLLOW LINE AROUND 180* BEND
                print('CHECKPOINT C')
                self.BrainState = self.linefollow
                romiSetSpeed.put(20)
                #print(IRSum.get())

                # Compute the heading change correctly considering wraparound
                current_heading = Heading.get() / 16  # Convert raw value to degrees
                # Compute the shortest angular difference (corrected for 360° wraparound)
                delta_Heading = (current_heading - self.headingDatum + 180) % 360 - 180

                print(delta_Heading)
                if abs(delta_Heading) > (178): #TODO TWEAK ME
                    self.checkpoint = 'D'
                    self.headingDatum += (-180) #recallibrate heading datum ##TODO NORM 180
                    distanceDatum = distTraveled.get()
                    self.error = 0
                    self.errorSum = 0
                    #self.Ki += 0.01
                    self.Kp += 0.05
                
            elif self.checkpoint == 'D': #STRAIGHT THROUGH DASHED LINE
                print('CHECKPOINT D')
                print(f"DISTANCE DELTA: {distTraveled.get()  - distanceDatum}")
                self.BrainState = self.linefollow
                romiSetSpeed.put(20) #GEUSS 
                if (distTraveled.get() - distanceDatum) > self.checkDdist: #GUESS
                    self.checkpoint = 'E'
                    self.error = 0
                    self.errorSum = 0   
                    self.headingDatum += (-90) #change heading datum to CP4 tangent
                    #self.Ki -= 0.01 #TODO TWEAK PI TO HELP RELIABILITY THRU DASHED
                    self.Kp -= 0.05 
                    
            elif self.checkpoint == 'E':#AROUND BIG TURN THROUGH CROSSHATCH
                print('CHECKPOINT E')
                self.BrainState = self.linefollow
                #print(f" IRSUM: {IRSum.get()}")
                print(f"DISTANCE DELTA: {distTraveled.get()  - distanceDatum}")
                romiSetSpeed.put(20) 
                
                # Compute the heading change correctly considering wraparound
                current_heading = Heading.get() / 16  # Convert raw value to degrees
                # Compute the shortest angular difference (corrected for 360° wraparound)
                delta_Heading = (current_heading - self.headingDatum + 180) % 360 - 180

                print (delta_Heading)

                if (delta_Heading < 5)  and (distTraveled.get()  - distanceDatum) >= 10.5   : #when traveled near CP4 and facing correct dir
                    self.checkpoint = 'H' #skip checkpoint F and G
                    distanceDatum = distTraveled.get()
                    #self.headingDatum -= self.headingDatum - (90*16)
                '''
            elif self.checkpoint == 'F': #DRIVE STRAIGHT THROUGH CROSS 
                print('CHECKPOINT F')
                self.BrainState = self.driveStraight
                romiSetSpeed.put(50)
                if (self.distanceTraveled - distanceDatum) > 100: #GEUSS
                    self.checkpoint = 'G'
                
            elif self.checkpoint == 'G':
                print('CHECKPOINT G')
                self.BrainState = self.linefollow
                romiSetSpeed.put(50)
                if (self.IRsum) < 1000: #GEUSS
                    self.centroid = 'H'
                    headingDatum = Heading.get() #recallibrate heading datum
                    distanceDatum = 0
                ''' 
            elif self.checkpoint == 'H': #DRIVE STRAIGHT THROUGH GRID
                # Compute the heading change correctly considering wraparound
                current_heading = Heading.get() / 16  # Convert raw value to degrees
                # Compute the shortest angular difference (corrected for 360° wraparound)
                delta_Heading = (current_heading - self.headingDatum + 180) % 360 - 180
                print('CHECKPOINT H')
                print (f" heading: {delta_Heading}")
                self.BrainState = self.driveStraight
                romiSetSpeed.put(30)

                print(f"dist traveled: {abs(distTraveled.get()  - distanceDatum)}")
                #print(f"Heading difference is: {(Heading.get - self.headingDatum)/16} degrees")
                if (abs(distTraveled.get()  - distanceDatum)) > 2.5: #GEUSS
                    self.headingDatum = Heading.get()/16 + (90)
                    self.checkpoint = 'I'  
                    checkpointIcount = 0
                    self.errorSum = 0         
            elif self.checkpoint == 'I': #PIVOT
                print('CHECKPOINT I')
                romiSetSpeed.put(0)
                self.BrainState = self.driveStraight
                checkpointIcount += 1
                if checkpointIcount > 14:
                    self.checkpoint = 'J'  
                    distanceDatum = distTraveled.get()
                    self.bump.reset() #Reset Bump sensor in case it was triggered before
            elif self.checkpoint == 'J': #EXIT GRID
                print('CHECKPOINT J')
                romiSetSpeed.put(20)
                self.BrainState = self.driveStraight 
                if (distTraveled.get()  - distanceDatum) > 0.5: #GEUSS 
                    self.checkpoint = 'K'
            elif self.checkpoint == 'K': #Drive into wall
                print('CHECKPOINT K')
                self.BrainState = self.linefollow
                self.bump.update()
                romiSetSpeed.put(25)
                if self.bump.bstate() == 1:
                    self.checkpoint = 'L'
                    self.error = 0
                    self.errorSum = 0 
                    distanceDatum = distTraveled.get()
                    
            elif self.checkpoint == 'L': #DRIVE BACKWARDS WHEN WALL IS HIT   
                print('CHECKPOINT L')
                self.BrainState = self.driveStraight
                romiSetSpeed.put(-20)
                print(f"REVERSE DIST {distTraveled.get()  - distanceDatum}")
                if (distTraveled.get()  - distanceDatum) < -0.3: #GEUSS
                    self.headingDatum = Heading.get()/16 + (90)
                    self.checkpoint = 'M'
                    checkpointIcount = 0
            
            elif self.checkpoint == 'M': #PIVOT 90 DEG CW
                print('CHECKPOINT M')
                romiSetSpeed.put(0) 
                self.BrainState = self.driveStraight
                checkpointIcount += 1
                if checkpointIcount > 14:
                    self.checkpoint = 'N'  
                    distanceDatum = distTraveled.get()   ##TODO END OF CURRENT PATH          
                
            
            elif self.checkpoint == 'N': #DRIVE STRAIGHT, HIT CUP MAYBE
                print('CHECKPOINT N')
                self.BrainState = self.driveStraight
                romiSetSpeed.put(30)
                if (distTraveled.get()  - distanceDatum) > 1.6: #GEUSS
                    self.headingDatum = Heading.get()/16 - (90)
                    self.checkpoint = 'O'
                    checkpointIcount = 0                
            
            elif self.checkpoint == 'O': #PIVOT 90 DEG CCW
                print('CHECKPOINT O')
                romiSetSpeed.put(0) 
                self.BrainState = self.driveStraight
                checkpointIcount += 1
                self.brainState = self.driveStraight
                if checkpointIcount > 14:
                    self.checkpoint = 'P'  
                    distanceDatum = distTraveled.get()    
                    
            elif self.checkpoint == 'P': #DRIVE STRAIGHT TOWARDS LINE
                print('CHECKPOINT P')
                romiSetSpeed.put(30)
                self.BrainState = self.driveStraight
                if (distTraveled.get()  - distanceDatum) > 1.2: #GEUSS
                    self.headingDatum = Heading.get()/16 - (90)
                    self.checkpoint = 'Q'
                    checkpointIcount = 0                
            
            elif self.checkpoint == 'Q': #PIVOT 90 DEG CCW
                print('CHECKPOINT Q')
                romiSetSpeed.put(0) 
                self.BrainState = self.driveStraight
                checkpointIcount += 1
                if checkpointIcount > 16:
                    self.checkpoint = 'R' ##TODO SKIP TO STOP 
                    distanceDatum = distTraveled.get()
                    self.error = 0
                    self.errorSum = 0

            elif self.checkpoint == 'R': #FOLLOW LINE TOWARDS START
                print('CHECKPOINT R')
                self.BrainState = self.driveStraight
                romiSetSpeed.put(20)
                if (distTraveled.get()  - distanceDatum) > 1.7: #GEUSS
                    self.checkpoint = 'Z'
                    self.error = 0
                    self.errorSum = 0

            elif self.checkpoint == 'Z': #STOP(FOR NOW)
                print('CHECKPOINT Z')
                UI_stop.put(True)
                    
                    

            yield





    def run(self, shares):
        L_vel_set, R_vel_set , UI_stop, the_queue, IR_centroid, IRSum, romiSetSpeed, Heading, AngularVelo, distTraveled = shares
        self.centroid = IR_centroid
        self.errorSum = 0
        self.error_min1 = 0
        self.ticks_last = 0
        self.romiSetSpeed = romiSetSpeed
        self.Heading = Heading
       
        while True:
            if self.BrainState == 1:#FOLLOW LINE
                #print('brainState')
                #print(romiSetSpeed)
                #print('IN LINE FOLLOWING MODE')
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


                #print(f"Yaw Rate: {self.yawRate}  Centroid: {self.centroid.get()}")
                if UI_stop.get() == True:
                  #print('L_vel/R_vel = 0')
                  L_vel_set.put(0)
                  R_vel_set.put(0)      
                else:
                    #print('L_vel/R_vel SET')
                    L_vel_set.put(int(self.romiSetSpeed.get() - 0.5*self.yawRate))
                    R_vel_set.put(int(self.romiSetSpeed.get() + 0.5*self.yawRate))
            
            
            
            elif self.BrainState == 2: #Drive Straight
                #print('brainState')
                #print(romiSetSpeed)
                '''This state is the 'simple, line following PID loop' for the Romi's YAW RATE as a whole'''
                current_heading = Heading.get() / 16  # Convert raw value to degrees
                # Compute the shortest angular difference (corrected for 360° wraparound)
                delta_Heading = (current_heading - self.headingDatum + 180) % 360 - 180
                self.error = (delta_Heading)#in degrees
                print(self.error)
                if self.error > 180:
                    self.error = self.error-360
                #print(f" ERRROR: {self.error}  ERRORSUM: {self.errorSum}")
                
                #Proportional
                self.P = self.error*1 
       
                #Integral
                self.errorSum += self.error 
                if abs(self.errorSum) > 1000:
                    
                    self.errorSum = 1000 * (self.errorSum/abs(self.errorSum))
                self.I = 0  * self.errorSum ##TODO PI TWEAK
                
                #Derivative
                self.ticks_now = time.ticks_us()
                self.errorDer = (self.error_min1 - self.error)/(time.ticks_diff(self.ticks_last, self.ticks_now))
                self.error_min1 = self.error
                self.ticks_last = self.ticks_now
                self.D = self.errorDer * self.Kd
            
                #Sum PID
                self.yawRate = int(self.P + self.I + self.D)

                if UI_stop.get() == True:
                  #print('L_vel/R_vel = 0')
                  L_vel_set.put(0)
                  R_vel_set.put(0)      
                else:
                    #print('L_vel/R_vel SET')
                    L_vel_set.put(int(self.romiSetSpeed.get() - 0.5*self.yawRate))
                    R_vel_set.put(int(self.romiSetSpeed.get() + 0.5*self.yawRate))
            yield