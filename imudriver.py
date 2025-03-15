#IMUDriver.py

from pyb import Pin,Timer,ADC,I2C
from time import ticks_us, ticks_diff,sleep
from os import listdir
import struct

BNO055_I2C_ADDR = 0x28 
# BNO055 Registers
BNO055_CHIP_ID = 0x00
BNO055_CALSTATUS = 0x35    
BNO055_MAG_Z_LB = 0x12
BNO055_OP_MODE_REG = 0x3D  
MAG_OFFSET_Z_LB = 0x59  # Low byte of magnetometer Z offset
MAG_OFFSET_Z_HB = 0x5A  # High byte of magnetometer Z offset
EUL_DATA_LSB = 0x1A
ACC_OFFSET_X_LSB = 0x55
GYR_DATA_Z_LSB = 0x18


class IMUDriver:
    '''This Class initializes the BNO055 IMU, sets its operating mode, and reads data from the device.'''
    
    def __init__(self):  
        '''Initializes IMU with I2C Protocol'''
        #filelist =listdir()
        self.I2C = I2C(2, I2C.CONTROLLER, baudrate = 400000)
        sleep(1) #allow time to create I2C      

        print(self.I2C.scan()) #search for any periphrals
        chip_id = self.I2C.mem_read(1, BNO055_I2C_ADDR, BNO055_CHIP_ID)[0] #needs [0] to return byte not bytearray
        if chip_id != 0xA0:  # BNO055 chip ID should be 0xA0
            print("Error: BNO055 not detected!")
        else:
            print("BNO055 detected successfully!")
    
        self.delta = 0 # Change in count between last two updates
        self.dt = 0 # Amount of time between last two updates
        self.prev_ticks = ticks_us() #Initializes previous ticks
        self.prevop = 0 #Tracks previous opmode for quick switching between modes


        #------------Calibration Logic-------
        self.opmode(4)
        self.prevop = 4
        '''
        while True:
            self.get_eangle()
            self.get_calcoef()
            self.calstatus()
            time.sleep_ms(500)
        
        if "IMU_CAL.txt" in self.filelist:
            print("Calibration found!, Skipping Calibration...")
            with open("IR_cal.txt","r") as file:
        
        '''
       
    def opmode(self,mode):
        '''Sets the operating mode of the IMU'''
        try:
            if mode == 0:
                self.I2C.mem_write(0b0000, BNO055_I2C_ADDR, BNO055_OP_MODE_REG)
            elif mode == 1:
                #IMUPLUS_MODE
                self.I2C.mem_write(0b1000, BNO055_I2C_ADDR, BNO055_OP_MODE_REG)
                self.prevop = 1
            elif mode == 2:
                #COMPASS_MODE
                self.I2C.mem_write(0b1001   , BNO055_I2C_ADDR, BNO055_OP_MODE_REG)
                print('IN COMPASS MODE')
                self.prevop = 2
            elif mode == 3:
                #M4G_MODE
                self.I2C.mem_write(0b1010, BNO055_I2C_ADDR, BNO055_OP_MODE_REG)
                self.prevop = 3
            elif mode == 4:
                #NDOF_FMC_OFF_MODE
                self.I2C.mem_write(0b1011, BNO055_I2C_ADDR, BNO055_OP_MODE_REG)
                self.prevop = 4
            elif mode == 5:
                #NDOF_MODE
                self.I2C.mem_write(0b1100, BNO055_I2C_ADDR, BNO055_OP_MODE_REG)
                self.prevop = 5
        except:
            print("Error: Invalid BNO055 Mode!")
            
    def calstatus(self):
        '''Reads the calibration bits for System, Gyrometer, Accelerometer, 
        and Magnetometer'''
        buf = bytes(self.I2C.mem_read(1,BNO055_I2C_ADDR, BNO055_CALSTATUS))#read the cal status byte
        buf_int = int.from_bytes(buf, 'little')  # Convert bytes to integer
        print(f"Calibration Status: {buf_int:08b}")  # Print as 8-bit binary
        calstatus = struct.unpack("B",buf)[0] #why do we want integer?
        print(calstatus)
        sys_stat = (calstatus >> 6) & 0b11  
        gyr_stat = (calstatus >> 4) & 0b11
        acc_stat = (calstatus >> 2) & 0b11
        mag_stat = (calstatus) & 0b11
        
        calstatus = [sys_stat,gyr_stat,acc_stat,mag_stat]
        print("Sys, Gyr, Acc, mag",calstatus) #,end="\r"
        #self.write_calcoef()
        if sys_stat == 3:
            return 1
        else:
            return 0

    def get_calcoef(self):
        '''Reads the calibration constants for all 3 sensors in the IMU'''
        self.opmode(0)
        self.offset_data = bytes(self.I2C.mem_read(18,BNO055_I2C_ADDR, ACC_OFFSET_X_LSB))
        #extract values from offset register
        print(self.offset_data[0:2])
        acc_offset_x = int.from_bytes(self.offset_data[0:2], 'little', True)
        acc_offset_y = int.from_bytes(self.offset_data[2:4], 'little', True)
        acc_offset_z = int.from_bytes(self.offset_data[4:6], 'little', True)
        mag_offset_x = int.from_bytes(self.offset_data[6:8], 'little', True)
        mag_offset_y = int.from_bytes(self.offset_data[8:10], 'little', True)
        mag_offset_z = int.from_bytes(self.offset_data[10:12], 'little', True)
        gyr_offset_x = int.from_bytes(self.offset_data[12:14], 'little', True)
        gyr_offset_y = int.from_bytes(self.offset_data[14:16], 'little', True)
        gyr_offset_z = int.from_bytes(self.offset_data[16:18], 'little', True)

        # Print the extracted values
        print(f"opmode init{self.I2C.mem_read(1, BNO055_I2C_ADDR, BNO055_OP_MODE_REG)}")
        print(f"Accelerometer Offsets: X={acc_offset_x}, Y={acc_offset_y}, Z={acc_offset_z}")
        print(f"Magnetometer Offsets: X={mag_offset_x}, Y={mag_offset_y}, Z={mag_offset_z}")
        print(f"Gyroscope Offsets: X={gyr_offset_x}, Y={gyr_offset_y}, Z={gyr_offset_z}")
        
        self.opmode(self.prevop)
        print(f"opmode after{self.I2C.mem_read(1, BNO055_I2C_ADDR, BNO055_OP_MODE_REG)}")
        #calcoef = self.read_register(0x3D) & 0b00001111
        #print(f"Accel. Cal Constants: {calcoef}")
        

    
    def write_calcoef(self):
        '''Writes new calibration coefficient to accociated register'''
        self.get_calcoef()
        if len(self.offset_data) != 18:
            raise ValueError("Offset data must be exactly 18 bytes")
            # Write the 18-byte offset data to the BNO055 offset registers
        self.I2C.mem_write(self.offset_data, BNO055_I2C_ADDR, ACC_OFFSET_X_LSB)
        print(f"OFFSETDATA: {self.offset_data}")
        '''
        with open("IMU_cal.txt", "w") as file:
            print("HI!!!")
            file.write(str(self.offset_data))
        '''    

        

    def get_eangle(self):
        '''Returns Euler angles from corresponding register in IMU'''
        EUL_Data= bytes(self.I2C.mem_read(6, BNO055_I2C_ADDR, EUL_DATA_LSB)) #just z of euler angle
        EULER_Heading = int.from_bytes(EUL_Data[0:2], 'little', True)
        # EULER_Roll =    int.from_bytes(EUL_Data[2:4], 'little', True)
        # EULER_Pitch =   int.from_bytes(EUL_Data[4:6], 'little', True)
        EULER_Heading = struct.unpack('<hhh', EUL_Data)[0]  
        #print(f" Heading={EULER_Heading}, Roll={EULER_Roll}, Pitch={EULER_Pitch}")
        return EULER_Heading
    
    def get_angvelocity(self):
        '''Returns angular velocity from corresponding register in IMU'''
        GYR_DATA = self.I2C.mem_read(2, BNO055_I2C_ADDR, GYR_DATA_Z_LSB)  # Read 2 byte
        #Unpack as a signed 16-bit little-endian integer
        GYRO_Z = struct.unpack('<h', GYR_DATA)[0]  
        #print(f"Gyro Z: {GYRO_Z}")
        return GYRO_Z
      

  