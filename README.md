# Romi_Lubinsky_Guinane
ME405 Term Project

Aaron Lubinsky
Owen Guinane

W25 Cal Poly ME405

Rev. Mar 15, 2025

## Table of Contents
[Romi Design](#romi-design)<br>
[Program Design and Structure](#program-design-and-structure)<br>
&nbsp;&nbsp;&nbsp;&nbsp;[Tasks](#tasks)<br>
&nbsp;&nbsp;&nbsp;&nbsp;[Classes](#classes)<br>
[Conclusion](#conclusion)
[Video Demonstration](#video-demonstration)<br>

## Romi Design

To complete the obstacle course, we outfitted our Romi bot with a Pololu IR reflectance sensor to follow the lines on the track, an Adafruit BNO055 IMU to help the Romi drive straight in its current heading or turn to face a new heading, and a Pololu bump sensor to detect when the Romi has hit the wall. In addition to these sensors, the Romi was equipped with a HC-05 Bluetooth module to enable wireless operation of the Romi bot. Later on in the project, a circuit was added to the Romi to read the robot's battery voltage. Pictures of the Romi's final configuration are shown below.

![20250314_120230](https://github.com/user-attachments/assets/d6e9c733-55c5-4a1c-8662-09e5068ae85e)
![romi_top](https://github.com/user-attachments/assets/308f10cb-2911-44a5-9b0c-88326dceb7a5)
![romi_bottom](https://github.com/user-attachments/assets/451f89cc-94a4-4813-94c3-e40be3c8701d)
![romi_back](https://github.com/user-attachments/assets/2e60e1f5-4f2f-4981-bcc5-2caad98fa46d)

![RomiTopAngle](https://github.com/user-attachments/assets/e2cdfcc9-a27a-4bcd-bf52-43aaf9b9fd85)
![RomiBottomAngle](https://github.com/user-attachments/assets/68cf7f2e-1061-4f6f-8f93-5fc685c556da)


All of the sensors are mounted on the front of the Romi using standoffs due to compatible mounting points on the chassis between the IR and bump sensors, making 3D-printing a custom adapter unnecessary. CAD Files of the robot have been included with accurate sensor placement.


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
![image](https://a.pololu-files.com/picture/0J9136.600x480.jpg?21d47be8d4bfa4f6d290741354a839ba)

To follow the lines on the obstacle course, we used the Pololu QTR-MD-08A Reflectance Sensor Array. We chose this sensor because it had a sensible amount of IR Sensors and was long, but not long enough to require a custom adapter to mount on the Romi.
While it can easily keep track of wide turns on the obstacle course, testing revealed that the small size of the sensor was limiting how fast we could take sharp corners, especially at the start of the course.


### Bump Sensor
![image](https://a.pololu-files.com/picture/0J10203.600x480.jpg?793c0b893bd0ac5f64733eee603cd0fd)

To allow our robot to detect bumping the wall at the end of the course as well as protect the IR array from impacts, a pair of Pololu bump sensors were utilized. While all 3 sensors on each units were originally planned to be implemented, testing found that having the front sensor working worked just fine as it was.

### BNO055 IMU
![image](https://cdn-learn.adafruit.com/assets/assets/000/024/585/medium800/sensors_2472_top_ORIG.jpg?1429638074)

To allow our robot to use heading data to aid in navigation, we used the Adafruit BNO055 IMU.

### Wiring Diagram
Below is the final revision of our wiring diagram of our Nucleo Board.
![image](https://github.com/user-attachments/assets/8ae91c52-fd46-442b-8d40-f865ef19f9c3)

To detect the Battery Level, the following circuit is constructed and read through ADC on PB0.
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

## Tasks

* **UITask.py**

This task is responsibe for handling all REPL input for the romi as well as initializing the UART protocol for the HC-05 Bluetooth module. In our final implementation of our obstacle course, we use UITask to start the robot at the start of the course and to pause the robot if necessary.

* **MotorTask.py**

This task class is initialized twice within main.py: one for the left motor and again for the right. Within the task, a PID loop is cycled to match the motor speed, as detected by an encoder, to the desired motor velocity communicated via a task share variable. The need for this PID loop arises from the difference between the physical motors. While indistinguishable at first, the difference became evident when sending identical PWM to both motors. The right motor had a repeatable tendency to outpace the left. With the PID implemented, each PWM is adjusted so that Romi drives straight when desired left and right motor speeds are equal.


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![MotorTask_FSM](https://github.com/user-attachments/assets/6ceb8a18-f858-4d7c-9366-ad0111710b1b)
&nbsp;&nbsp;&nbsp;&nbsp;


* **IRTask.py**

This task class is responsible for reading data from the IR array, calculating the centroid and sum of the IR array, and putting these values into the share on a regular basis.

* **BrainsTask.py**
[BrainsTask.py]([url](https://github.com/aaronlubinsky/Romi_Lubinsky_Guinnane/blob/main/BrainsTask.py))

This task is responsible for handling all of the important track logic as well as switching between driving modes.
The two different driving modes handled by this task are line following and driving straight. 
Line following uses centroid data from the IR task and a PID loop to control the Romi as it follows lines throughout the track. This is the driving mode utilized throughout the majority of the obstacle course, mostly up to checkpoint 4.
Driving straight uses Euler angle data from the IMU task and a PID loop to have the romi face a desired heading and drive straight. This driving mode is used primarily in the second half of the course to the finish line. Additionally, the drive straight driving mode is also used to pivot in place by setting the Romi's forward speed to 0 and updating the desired heading. 

Track logic is handled by breaking the track up into 16 sections (checkpoints), labeled alphabetically. Each of these checkpoints has criteria to determine if it has crossed into a new checkpoint or not. for For ease of reference, a diagram of the obstacle course and corresponding checkpoints are shown below.

![layer-MC0](https://github.com/user-attachments/assets/362de588-184d-4373-a530-dd08862760d2)

|Checkpoint|Driving Mode|Criterion|
|---|---|---|
|0|N/A|UI_stop.get == 0|
|A|Line follow|abs(delta_Heading) > 80|
|B|Drive straight|(distTraveled.get)/
|C
|D
|E

|H
|I
|J
|K
|L
|M
|N
|O

* **IMUTask.py**

This task is responsible for regularly putting the Euler heading of the romi bot into the share.


## Classes

* **Bump**

  This class handles bump sensor functionality. It initializes the pins used for both left and right sensors and toggles bstate if the bump sensor is pressed during an update.
  
* **Motor**

   This class acts as a motor driver for the Romi bot. It initializes the timer of the PWM channels as well as the pins for SLP,DIR, and PWM, as well as setting the effort of the motor based on an input between -100 and 100.

* **Encoder**

  This class acts as a driver and quadrature decoder for the encoders on the Romi motor. It initializes the encoder timer and pins for channels A and B, and calculates current velocity and position every update step.

* **IMUDriver**

  This class acts as the driver for the BNO055 IMU. It initializes the IMU using the I2C protocol, and sets its operation mode to NDOF_FMC_OFF_MODE upon startup. It returns the system calibration status bytes, Euler heading, and angular velocity about the Z axis.

## Conclusion

While we are satisfied with the Romi's performance on the track, there are still a lot of improvements that can be made to help the robot run more reliably. For instance, A major issue with the Romi bot was that performance was very dependent on battery charge. While we were able to construct a circuit to read of the Romi's voltage,


## Video Demonstration
Below is a video of the Romi's final trial run. Our final raw running time was 38.10 seconds. Including the single cup hit at the end, the final processed time of our Romi bot is 33.10 seconds.

Click the thumbnail to watch the video

[![Video of Trial Run](https://img.youtube.com/vi/gykSGYLJhhQ/0.jpg)](https://www.youtube.com/watch?v=gykSGYLJhhQ)

