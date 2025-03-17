# Romi_Lubinsky_Guinane
ME405 Term Project

Aaron Lubinsky
Owen Guinane

W25 Cal Poly ME405

Rev. Mar 15, 2025

## Table of Contents
[Introduction](#introduction)<br>
[Romi Design](#romi-design)<br>
[Program Design and Structure](#program-design-and-structure)<br>
&nbsp;&nbsp;&nbsp;&nbsp;[Tasks](#tasks)<br>
&nbsp;&nbsp;&nbsp;&nbsp;[Classes](#classes)<br>
[Conclusion](#conclusion)<br>
[Video Demonstration](#video-demonstration)<br>

## Introduction
For our ME405 Term Project, we were tasked with constructing and programming a Romi robot to navigate an obstacle course. This obstacle course features sharp and gentle turns, dashed and crosshatched lines, diamonds, a grid, a wall to navigate around, and cups which can be knocked out of their areas for a time bonus. To accomplish this task, we outfitted our romi with an IR sensor array, an IMU, and a bump sensor to allow us to follow lines on the track, have the romi drive straight and pivot, and detect when it has bumped into the wall at the end of the course.


## Romi Design

To complete the obstacle course, we outfitted our Romi bot with a Pololu IR reflectance sensor to follow the lines on the track, an Adafruit BNO055 IMU to help the Romi drive straight in its current heading or turn to face a new heading, and a Pololu bump sensor to detect when the Romi has hit the wall. In addition to these sensors, the Romi was equipped with a HC-05 Bluetooth module to enable wireless operation of the Romi bot. Later on in the project, a circuit was added to the Romi to read the robot's battery voltage. Pictures of the Romi's final configuration are shown below.

<p align="center">
  <img src="https://github.com/user-attachments/assets/d6e9c733-55c5-4a1c-8662-09e5068ae85e" width="1000">
</p>


<p align="center">
  <img src="https://github.com/user-attachments/assets/451f89cc-94a4-4813-94c3-e40be3c8701d" width="475">
  <img src="https://github.com/user-attachments/assets/2e60e1f5-4f2f-4981-bcc5-2caad98fa46d" width="475">
</p>


<p align="center">
  <img src="https://github.com/user-attachments/assets/d948383d-464e-46e3-815b-8f34cd14e689" width="500">
</p>

**CAD Renders**
<p align="left">
  <img src="https://github.com/user-attachments/assets/e2cdfcc9-a27a-4bcd-bf52-43aaf9b9fd85" width="500">
  <img src="https://github.com/user-attachments/assets/68cf7f2e-1061-4f6f-8f93-5fc685c556da" width="500">
</p>

All of the sensors are mounted on the front of the Romi using standoffs due to compatible mounting points on the chassis between the IR and bump sensors, making 3D-printing a custom adapter unnecessary. Accessories such as the HC-05 Bluetooth Module and the Voltage reader circuit were taped on to the Romi. CAD Files of the robot have been included with accurate sensor placement.


### Bill of Materials
| Item | Quantity | Source|
| --- | --- | --- |
|Romi Chassis Kit | 1 | Instructor Provided |
|Romi Ball Caster Kit | 1 | Instructor Provided |
|Romi Power Distribution Board| 1 | Instructor Provided |
|Romi Encoder Pair Kit | 1 | Instructor Provided |
|Nucleo L476RG| 1 | Instructor Provided |
| Adafruit BNO055 Absolute Orientation Sensor | 1 | Instructor Provided |
| QTR-MD-08A Reflectance Sensor Array: 8-Channel, 8mm Pitch, Analog Output | 1 | [Pololu Store](https://www.pololu.com/product/4248)<br> |
| Right Bumper Switch Assembly for Romi/TI-RSLK MAX | 1 | [Pololu Store](https://www.pololu.com/product/3674)<br> |
| Left Bumper Switch Assembly for Romi/TI-RSLK MAX | 1 | [Pololu Store](https://www.pololu.com/product/3673)<br> |
| HC-05 Wirelesss Bluetooth Module | 1 | [Amazon](https://www.amazon.com/dp/B01MQKX7VP)<br> |



### IR Reflectance Sensor
<p align="center">
  <img src="https://a.pololu-files.com/picture/0J9136.600x480.jpg?21d47be8d4bfa4f6d290741354a839ba" width="500">
</p>

To follow the lines on the obstacle course, we used the Pololu QTR-MD-08A Reflectance Sensor Array. We chose this sensor because it had a sensible amount of IR Sensors and was long, but not long enough to require a custom adapter to mount on the Romi.
While it can easily keep track of wide turns on the obstacle course, testing revealed that the small size of the sensor was limiting how fast we could take sharp corners, especially at the start of the course.


### Bump Sensor
<p align="center">
  <img src="https://a.pololu-files.com/picture/0J10203.600x480.jpg?793c0b893bd0ac5f64733eee603cd0fd" width="500">
</p>


To allow our robot to detect bumping the wall at the end of the course as well as protect the IR array from impacts, a pair of Pololu bump sensors were utilized. While all 3 sensors on each units were originally planned to be implemented, testing found that having the front sensor working worked just fine as it was.

### BNO055 IMU
<p align="center">
  <img src="https://cdn-learn.adafruit.com/assets/assets/000/024/585/medium800/sensors_2472_top_ORIG.jpg?1429638074" width="500">
</p>
To allow our robot to use heading data to aid in navigation, we used the Adafruit BNO055 IMU. In the final iteration of our robot's program, it operates in NDOF_FMC_OFF_MODE, which provides absolute orientation data from the accelerometer, magnetometer, and gyrometer.

### Wiring Diagram
Below is the final revision of our wiring diagram of our Nucleo Board.
![image](https://github.com/user-attachments/assets/8ae91c52-fd46-442b-8d40-f865ef19f9c3)

To detect the Battery Level, the following circuit is constructed and read through ADC on PB0.

<p align="center">
  <img src="https://github.com/user-attachments/assets/5dc78c35-1b31-4a9f-9368-63c8d1c1bc0d" width="700">
</p>

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

## Tasks

* [**UITask.py**](https://github.com/aaronlubinsky/Romi_Lubinsky_Guinnane/blob/main/UITask.py)

This task is responsibe for handling all REPL input for the romi as well as initializing the UART protocol for the HC-05 Bluetooth module. In our final implementation of our obstacle course, we use UITask to start the robot at the start of the course and to pause the robot if necessary. Below is the state-transition diagram for this task.

<p align="center">
  <img src="https://github.com/user-attachments/assets/1dc6cc52-e5ec-42b0-8df0-d165758618ce" width="400">
</p>

* [**MotorTask.py**](https://github.com/aaronlubinsky/Romi_Lubinsky_Guinnane/blob/main/MotorTask.py)

This task class is initialized twice within main.py: one for the left motor and again for the right. Within the task, a PID loop is cycled to match the motor speed, as detected by an encoder, to the desired motor velocity communicated via a task share variable. The need for this PID loop arises from the difference between the physical motors. While indistinguishable at first, the difference became evident when sending identical PWM to both motors. The right motor had a repeatable tendency to outpace the left. With the PID implemented, each PWM is adjusted so that Romi drives straight when desired left and right motor speeds are equal. Below is the state-transition diagram for this task.

<p align="center">
  <img src="https://github.com/user-attachments/assets/9b9ac1f5-8cc1-4bc2-b94e-34fc743858a1" width="400">
</p>


* [**IRTask.py**](https://github.com/aaronlubinsky/Romi_Lubinsky_Guinnane/blob/main/IRTask.py)

This task class is responsible for reading data from the IR array, calculating the centroid and sum of the IR array, and putting these values into the share on a regular basis.

* [**BrainsTask.py**](https://github.com/aaronlubinsky/Romi_Lubinsky_Guinnane/blob/main/BrainsTask.py)

This task is responsible for handling all of the important track logic as well as switching between driving modes.
The two different driving modes handled by this task are line following and driving straight. 
Line following uses centroid data from the IR task and a PID loop to control the Romi as it follows lines throughout the track. This is the driving mode utilized throughout the majority of the obstacle course, mostly up to checkpoint 4.
Driving straight uses Euler angle data from the IMU task and a PID loop to have the romi face a desired heading and drive straight. This driving mode is used primarily in the second half of the course to the finish line. Additionally, the drive straight driving mode is also used to pivot in place by setting the Romi's forward speed to 0 and updating the desired heading. 

Track logic is handled by breaking the track up into 16 sections (checkpoints), labeled alphabetically. Each of these checkpoints has criteria to determine if it has crossed into a new checkpoint or not. Each checkpoint has four main functions:
1. Set the speed of the Romi bot
2. Set the driving mode
3. Check criterion for next checkpoint
4. If criterion is met, update parameters for next checkpoint.

An example of one checkpoint is shown below.

<p align="center">
  <img src="https://github.com/user-attachments/assets/04fd431c-7daa-4911-85b8-34022989204a" width="700">
</p>


For ease of reference, a diagram of the obstacle course and corresponding checkpoints, the task-state diagram, and a table of checkpoints and corresponding drivng mode and criterions are shown below.

![layer-MC0](https://github.com/user-attachments/assets/362de588-184d-4373-a530-dd08862760d2)

<p align="center">
  <img src="https://github.com/user-attachments/assets/66764854-aa4b-49ef-a120-cfaee3cd4d36" width="700">
</p>

|Checkpoint|Driving Mode|Criterion|
|---|---|---|
|0|N/A|UI_stop.get == 0|
|A|Line follow|abs(delta_Heading) > 80|
|B|Drive straight|(distTraveled.get) > 0.60 |
|C | Line follow | (delta_Heading) > 178|
|D | Drive straight | (distTraveled.get) > 0.60 |
|E | Line follow | (distTraveled.get) > 10.5 and (delta_Heading) < 5 |
|H | Drive straight | (distTraveled.get) > 2.50 |
|I | Pivot | yieldCount > 14 |
|J | Drive straight | (distTraveled.get) > 0.5 |
|K | Line Follow | bumpSensor TRUE |
|L | Drive Backwards | (distTraveled.get) < -0.3 |
|M | Pivot | yieldCount > 14 |
|N | Drive straight | (distTraveled.get) > 1.6 |
|O | Pivot | yieldCount > 14 |
|P | Drive straight | (distTraveled.get) > 1.2 |
|Q | Pivot | yieldCount > 16 |
|R | Line follow | (distTraveled.get) > 1.7 |
|Z | Stop | N/A |


* [**IMUTask.py**](https://github.com/aaronlubinsky/Romi_Lubinsky_Guinnane/blob/main/IMUTask.py)


This task is responsible for regularly putting the Euler heading of the romi bot into the share.


## Classes

* [**Bump**](https://github.com/aaronlubinsky/Romi_Lubinsky_Guinnane/blob/main/bump.py)

  This class handles bump sensor functionality. It initializes the pins used for both left and right sensors and toggles bstate if the bump sensor is pressed during an update.
  
* [**Motor**](https://github.com/aaronlubinsky/Romi_Lubinsky_Guinnane/blob/main/motor.py)

   This class acts as a motor driver for the Romi bot. It initializes the timer of the PWM channels as well as the pins for SLP,DIR, and PWM, as well as setting the effort of the motor based on an input between -100 and 100.

* [**Encoder**](https://github.com/aaronlubinsky/Romi_Lubinsky_Guinnane/blob/main/encoder.py)

  This class acts as a driver and quadrature decoder for the encoders on the Romi motor. It initializes the encoder timer and pins for channels A and B, and calculates current velocity and position every update step.

* [**IMUDriver**](https://github.com/aaronlubinsky/Romi_Lubinsky_Guinnane/blob/main/imudriver.py)

  This class acts as the driver for the BNO055 IMU. It initializes the IMU using the I2C protocol, and sets its operation mode to NDOF_FMC_OFF_MODE upon startup. It returns the system calibration status bytes, Euler heading, and angular velocity about the Z axis.

## Conclusion

While we are satisfied with the Romi's performance on the track, there are still a lot of improvements that can be made to help the robot run more reliably. For instance, A major issue with the Romi bot was that performance was very dependent on battery charge level. We we were able to construct a circuit to read of the Romi's voltage, we were not able to code in a way to compensate PID gains and motor effort for dropping battery voltage. Another issue that plagued our robot during testing was the dashed line section of the course, where the Romi would not correct itself enough to follow the dashes straight through. This ended up causing the Romi to veer to the left, outside of the range of the IR sensor array, causing it to lose the line and kill the run as a result. While measures were taken to remedy this by increasing Kp to be more aggressive during the line, it was not enough the morning of demonstration. This could be remedied by making Kp more agressive through that section, battery voltage compensation, or by switching back the drive straight mode for that checkpoint with some more tweaks to the desired heading. Apart from these two issues, the Romi performed consistently for most of the runs. We were able to have the Romi complete the obstacle course using proportional-only control, with a Kp of 0.45 driving the PID loops for both driving modes. In addition, the pivoting maneuvers of the Romi bot were performed by setting speed to zero and using the drive straight mode to have the romi face a desired heading. 


## Video Demonstration
Below is a video of the Romi's final trial run. Our final raw running time was 38.10 seconds. Including the single cup hit at the end, the final processed time of our Romi bot is 33.10 seconds.

Click the thumbnail to watch the video

[![Video of Trial Run](https://img.youtube.com/vi/gykSGYLJhhQ/0.jpg)](https://www.youtube.com/watch?v=gykSGYLJhhQ)

