#Main.py

import gc
import pyb
import cotask
import task_share
import motor
import encoder
import time
import UITask
import MotorTask
import IRDriver
import IRTask
import BrainsTask
import IMUTask
#import BT_configurator


if __name__ == "__main__":
    '''Introduction Console'''
    print("Press Ctrl-C to stop and show diagnostics.")
    '''Task Declarations and Scheduler'''
    #Share & Queues----------
    Left_Vel_instr = task_share.Share('h', thread_protect=False, name="Left Vel")
    Right_Vel_instr = task_share.Share('h', thread_protect=False, name="Right Vel")
    UI_stop = task_share.Share('h', thread_protect=False, name="Hard Stop")
    romiState = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Romi State")
    IR_Centroid = task_share.Share('h', thread_protect=False, name="IR centroid")
    IR_sum = task_share.Share('f', thread_protect=False, name="IR sum")
    romiSetSpeed = task_share.Share('h', thread_protect=False, name="Romi Set Speed")
    Heading = task_share.Share('h', thread_protect=False, name="Heading")
    AngularVelo = task_share.Share('h', thread_protect=False, name="Angular Velocity")
    distTraveled = task_share.Share('f', thread_protect=False, name="Distance Share")
    #---------set parameter for testing
    speed = 15
    #speed = int(input('Press enter for speed'))

        
    #Task Objects------------
    UITaskObj = UITask.UITask("Task1 - UI", speed)
    LeftMotorTaskObj = MotorTask.MotorTask("Left Motor", chan=1, PWM=pyb.Pin.cpu.B4, DIR=pyb.Pin.cpu.B3,
                                            nSLP=pyb.Pin.cpu.C1, tim=1, chA_pin=pyb.Pin.cpu.A9, chB_pin=pyb.Pin.cpu.A8,
                                            Kp = 1, Ki = 0, Kd = 0)  
    RightMotorTaskObj = MotorTask.MotorTask("Right Motor", chan=2, PWM=pyb.Pin.cpu.B5, DIR=pyb.Pin.cpu.A10, 
                                            nSLP=pyb.Pin.cpu.C0, tim=2, chA_pin=pyb.Pin.cpu.A1, chB_pin=pyb.Pin.cpu.A0,
                                            Kp = 1, Ki = 0, Kd = 0)  
    IRTaskObj = IRTask.IRTask("Task4 - IR")
    IMUTaskObj =IMUTask.IMUTask("Task 6 - IMU")


    BrainsTaskObj = BrainsTask.Brains("Task 5 - Brains")
    #cotask objects----------L_vel_set, R_vel_set , UI_stop, the_queue, IR_centroid, IRSum, romiSetSpeed, Heading, AngularVelo, distTraveled
    task1 = cotask.Task(UITaskObj.UI, name="Task_1", priority=1, period=200,
                        profile=True, trace=False, shares=(Left_Vel_instr, Right_Vel_instr,
                                                           UI_stop, romiState, IR_Centroid, IR_sum,
                                                            romiSetSpeed, Heading, AngularVelo, distTraveled))
    task2 = cotask.Task(LeftMotorTaskObj.drive, name="Task_2", priority=4, period=10,
                        profile=True, trace=False, shares=(Left_Vel_instr, Right_Vel_instr,
                                                           UI_stop, romiState, IR_Centroid, IR_sum,
                                                            romiSetSpeed, Heading, AngularVelo, distTraveled))
    task3 = cotask.Task(RightMotorTaskObj.drive, name="Task_3", priority=5, period=10,
                        profile=True, trace=False, shares=(Left_Vel_instr, Right_Vel_instr,
                                                           UI_stop, romiState, IR_Centroid, IR_sum,
                                                            romiSetSpeed, Heading, AngularVelo, distTraveled))
    task4 = cotask.Task(IRTaskObj.getIRArray, name="Task_4", priority=2, period=50,
                        profile=True, trace=False, shares=(Left_Vel_instr, Right_Vel_instr,
                                                           UI_stop, romiState, IR_Centroid, IR_sum,
                                                            romiSetSpeed, Heading, AngularVelo, distTraveled))
    task5 = cotask.Task(BrainsTaskObj.run, name="Task_5", priority=3, period=50,
                        profile=True, trace=False, shares=(Left_Vel_instr, Right_Vel_instr,
                                                           UI_stop, romiState, IR_Centroid, IR_sum,
                                                            romiSetSpeed, Heading, AngularVelo, distTraveled))
    task6 = cotask.Task(BrainsTaskObj.track, name="Task_6", priority=3, period=50,
                        profile=True, trace=False, shares=(Left_Vel_instr, Right_Vel_instr,
                                                           UI_stop, romiState, IR_Centroid, IR_sum,
                                                            romiSetSpeed, Heading, AngularVelo, distTraveled))
    task7 = cotask.Task(IMUTaskObj.EulerAngle, name="Task_7", priority=3, period=50,
                        profile=True, trace=False, shares=(Left_Vel_instr, Right_Vel_instr,
                                                           UI_stop, romiState, IR_Centroid, IR_sum,
                                                            romiSetSpeed, Heading, AngularVelo, distTraveled))
    task8 = cotask.Task(IMUTaskObj.AngularVelo, name="Task_8", priority=3, period=50,
                        profile=True, trace=False, shares=(Left_Vel_instr, Right_Vel_instr,
                                                           UI_stop, romiState, IR_Centroid, IR_sum,
                                                            romiSetSpeed, Heading, AngularVelo, distTraveled))  
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)
    cotask.task_list.append(task4)
    cotask.task_list.append(task5)
    cotask.task_list.append(task6)
    cotask.task_list.append(task7)
    cotask.task_list.append(task8)


    # If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed

    '''Garbade Collector'''
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()


   

    #-------------------------------Executing Code---------------------------------------
    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    '''IR1 = IRDriver.IRDriver(1, pyb.Pin.cpu.C5)
    while True:
        print(IR1.getValue())
        time.sleep_us(10000)
    '''
    




    while True:
        try:
            #print('scheduler looped')
            cotask.task_list.pri_sched()
            
        except KeyboardInterrupt:
            LeftMotorTaskObj.disable()
            RightMotorTaskObj.disable()
            break
    #--------------------------------Execute after Quit-----------------------------------
    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')