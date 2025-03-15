# Romi_Lubinsky_Guinane
ME405 Term Project


W25 Cal Poly ME405
Rev. Mar 13, 2025

## Table of Contents
[Romi Design](#romi-design)<br>
[Program Design and Structure](#program-design-and-structure)<br>
[Video Demonstration](#video-demonstration)<br>

## Romi Design

To complete the obstacle course, we outfitted our Romi bot with a Pololu IR reflectance sensor to follow the lines on the track, an Adafruit BNO055 IMU to help the Romi drive straight in its current heading or turn to face a new heading, and a Pololu bump sensor to detect when the Romi has hit the wall. In addition to these sensors, the Romi was equipped with a HC-05 Bluetooth module to enable wireless operation of the Romi bot. Later on in the project, a circuit was added to the Romi to read the robot's battery voltage.
To implement our

![20250314_120230](https://github.com/user-attachments/assets/d6e9c733-55c5-4a1c-8662-09e5068ae85e)

All of the sensors are mounted on the front of the Romi using standoffs due to compatible mounting points between the IR and bump sensors, making 3D-printing a custom adapter unnecessary.


### Bill of Materials
| Item | Quantity | Source|
| --- | --- | --- |
|Romi Chassis Kit | 1 | Instructor Provided |
|Romi Ball Caster Kit | 1 | Instructor Provided |
|Romi Power Distribution Board| 1 | Instructor Provided |
|Romi Encoder Pair Kit | 1 | Instructor Provided |
|Nucleo L476RG| 1 | Instructor Provided |
|BNO055 IMU | 1 | Instructor Provided |
| QTR-MD-08A Reflectance Sensor Array: 8-Channel, 8mm Pitch, Analog Output | 1 | [Pololu Store](https://www.pololu.com/product/4248)<br> |
| Right Bumper Switch Assembly for Romi/TI-RSLK MAX | 1 | [Pololu Store](https://www.pololu.com/product/3674)<br> |
| Left Bumper Switch Assembly for Romi/TI-RSLK MAX | 1 | [Pololu Store](https://www.pololu.com/product/3673)<br> |
| Adafruit BNO055 Absolute Orientation Sensor | 1 | Instructor Provided |
| HC-05 Wirelesss Bluetooth Module | 1 | [Amazon](https://www.amazon.com/dp/B01MQKX7VP)<br> |




### IR Reflectance Sensor
![image](https://a.pololu-files.com/picture/0J9136.600x480.jpg?21d47be8d4bfa4f6d290741354a839ba)

To follow the lines on the obstacle course, we used the Pololu QTR-MD-08A Reflectance Sensor Array. We chose this sensor 
While it can easily keep track of wide turns on the obstacle course, testing revealed that the small size of the sensor was limiting how fast we could take sharp corners, especially at the start of the course.


### Bump Sensor
![image](https://a.pololu-files.com/picture/0J10203.600x480.jpg?793c0b893bd0ac5f64733eee603cd0fd)
To allow our robot to detect bumping the wall at the end of the course, a pair of pololu bump sensors were utilized.

### BNO055 IMU


### Wiring Diagram
Below is the final revision of our wiring diagram of our Nucleo Board.
![image](https://github.com/user-attachments/assets/8ae91c52-fd46-442b-8d40-f865ef19f9c3)

To detect the Battery Level, the following circuit is constructed and read through ADC on PB0
![image](https://github.com/user-attachments/assets/5dc78c35-1b31-4a9f-9368-63c8d1c1bc0d)



## Program Design and Structure
Our Romi utilizes cooperative multitasking to cycle between relevant tasks at assigned intervals, with priorities assigned to each Task. The tasks are executed using JR Ridgley's task scheduler, cotask.py, and share module, task_share.py. Our final Romi program is the result of 9 weeks of growing complexity. Though, when it was first implemented six weeks ago, it was much simpler. In this early stage, only three tasks existed: Left Motor, Right Motor, and UI tasks. However as more difficult challenges were attempted, Romi's multitasking routine grew to include an IR task for tracking lines, IMU tasks for orienting and tracking the robot, and two tasks for navigating the course and commanding its movement. The following outlines the tasks Romi is executing.

| Task | Number | Priority | Period | Description |
|---|---|---| --- | --- |
| UITaskObj.UI |1|1|200|Handles UI functionality of Romi| 
| LeftMotorTaskObj.drive |2| 4 |10 |Handles Effort input to the left motor|
| RightMotorTaskObj.drive |3| 4 |10 |Handles Effort input to the right motor|
| IRTaskObj.getIRArray | 4| 5 |50 |Frequently returns data from the IR sensor array |
| BrainsTaskObj.run |5 | 2 |50 |Handles the driving mode PID loops driving the |
|BrainsTaskObj.track | 6 | 3 |50 | Handles important track logic that sets speed and driving mode of the Romi |
|IMUTaskObj.EulerAngle| 7 | 3 |50 | Frequently returns Euler angle data from the IMU |
|IMUTaskObj.AngularVelo| 8 | 3 |50 | Frequently returns Angular velocity data from the IMU|

It should be noted that improvements to this program structure such as combining tasks or altering priorities and frequencies have been discussed. However, with the expedited timeline of this project, we have attempted to optimize Romi on Track Speed and Reliability. Improvements to Microcontroller efficiency or negligible improvements on track speed a program restructure may have are deemed out of our scope.

The task diagram for these tasks is shown below.
![image](https://github.com/user-attachments/assets/94ed56c8-0b22-479b-9822-d6769d87d905)

## Classes

*Bump

*Motor

*Encoder

*IMUDriver

## Tasks

* UITask.py
This task is responsibe for handling all REPL input for the romi as well as initializing the UART protocol for the HC-05 Bluetooth module. In our final implementation of our obstacle course

* MotorTask.py
This task class is initialized twice within main.py: one for the left motor and again for the right. Within the task, a PID loop is cycled to match the motor speed, as detected by an encoder, to the desired motor velocity communicated via a task share variable. The need for this PID loop arises from the difference between the physical motors. While indistinguishable at first, the difference became evident when sending identical PWM to both motors. The right motor had a repeatable tendency to outpace the left. With the PID implemented, each PWM is adjusted so that Romi drives straight when desired left and right motor speeds are equal.
* IRTask.py

[* BrainsTask.py]([url](https://github.com/aaronlubinsky/Romi_Lubinsky_Guinnane/blob/main/BrainsTask.py))
This task is responsible for handling all of the important track logic as well as switching between driving modes.
Track logic is handled by breaking the track up into 16 sections


For ease of reference, a diagram of the obstacle course and corresponding checkpoints are shown below.
![layer-MC0](https://github.com/user-attachments/assets/362de588-184d-4373-a530-dd08862760d2)

* IMUTask.py


## Conclusion

While we are satisfied with the Romi's performance on the track, we 


## Video Demonstration
Below is a video of the Romi's final trial run. Our final raw running time was 38.10 seconds. Including the single cup hit at the end, the final processed time of our Romi bot is 33.10 seconds.

Click the thumbnail to watch the video

[![Video of Trial Run](https://img.youtube.com/vi/gykSGYLJhhQ/0.jpg)](https://www.youtube.com/watch?v=gykSGYLJhhQ)

