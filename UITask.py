from pyb import USB_VCP, UART, repl_uart
from nb_input import NB_Input
from imudriver import IMUDriver

class UITask:

    def __init__(self, task_label,speed):
            self.state = 0
            
            # A counter variable used to track runs through
            # state 2
            self.count = 0
            
            # A label for the task to distinguish it's print statements
            self.task_label = task_label

            self.serial_stream = USB_VCP ()
            self.nb_in = NB_Input (self.serial_stream, echo=True)
            
            UART1obj = UART(1, 115200)
            
            self.bt_in = UART1obj #Bluetooth input
            
            repl_uart(UART1obj)
            self.speed = speed
            self.yawRate = 0
            self.IMU = IMUDriver()


    def UI(self, shares):
        
        # Get references to the share and queue which have been passed to this task
        L_vel_set, R_vel_set , the_queue, IR_centroid, romiSetSpeed, Heading = shares
        T1state = 0
        
        while True:
            
            '''Init State does nothing. Use later in init is neccesasary'''
            if T1state == 0:
                T1state = 1
                toggle = 0
                #print('T1S0')  
            elif T1state == 1:
                '''should (nonblocking) check bluetooth and console for inputs. act accordingly'''
                #print('T1S1')
                #self.ser.write("Testing") THIS WILL TRIGGLE nb_in
                #print('cp1')
                if toggle == 0: #if romi is currently off
                    if self.nb_in.any () or self.bt_in.any ():#and button is hit

                        romiSetSpeed.put(self.speed)
                        print('speed set to 30')                        
                        self.nb_in.get()
                        self.bt_in.read()
    
                        toggle = 1
                elif self.nb_in.any () or self.bt_in.any (): #if romi is currently on and button is hit
                    #self.IMU.get_calcoef()   
                    romiSetSpeed.put(0)
                    print('SPEED ---> 0')
                    self.nb_in.get()
                    self.bt_in.read()
                    toggle = 0
                    
            yield #communal yield. All Task 1 states should share this yield