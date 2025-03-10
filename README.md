# Romi_Lubinsky_Guinane
ME405 Term Project


W25 Cal Poly ME405

## Table of Contents
[Romi Design](#romi-design)<br>
    [Romi Design](#romi-design)<br>
[Program Design and Structure](#program-design-and-structure)<br>
[Video Demonstration](#video-demonstration)<br>

## Romi Design

To complete the obstacle course, we outfitted our Romi bot with an IR reflectance sensor to follow the lines on the track, a BNO055 to help the Romi drive straight in its current heading or turn to face a new heading, and a bump sensor to detect when the Romi has hit the wall.

### Bill of Materials
| Item | Quantity | Source|
| --- | --- | --- |
| QTR-MD-08A Reflectance Sensor Array: 8-Channel, 8mm Pitch, Analog Output | 1 | [Pololu Store](https://www.pololu.com/product/4248)<br> |
| Right Bumper Switch Assembly for Romi/TI-RSLK MAX | 1 | [Pololu Store](https://www.pololu.com/product/3674)<br> |
| Left Bumper Switch Assembly for Romi/TI-RSLK MAX | 1 | [Pololu Store](https://www.pololu.com/product/3673)<br> |
| Adafruit BNO055 Absolute Orientation Sensor | 1 | Instructor Provided |
| HC-05 Wirelesss Bluetooth Module | 1 | [Amazon](https://www.amazon.com/dp/B01MQKX7VP)<br> |


## Program Design and Structure
Our Romi utilizes cooperative multitasking to cycle between relevant tasks at assigned intervals, with priorities assigned to each Task. The tasks are executed using JR Ridgley's task scheduler, cotask.py, and share module, task_share.py. Our final Romi program is the result of 9 weeks of growing complexity. Though, when it was first implemented six weeks ago, it was much simpler. In this early stage, only three tasks existed: Left Motor, Right Motor, and UI tasks. However as more difficult challenges were attempted, Romi's multitasking routine grew to include an IR task for tracking lines, IMU tasks for orienting and tracking the robot, and two tasks for navigating the course and commanding its movement. The following outlines the tasks Romi is executing.
[
[
[
[
]]]]
It should be noted that improvements to this program structure such as combining tasks or altering priorities and frequencies have been discussed. However, with the expedited timeline of this project, we have attempted to optimize Romi on Track Speed and Reliability. Improvements to Microcontroller efficiency or negligible improvements on track speed a program restructure may have are deemed out of our scope.





## Video Demonstration
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
