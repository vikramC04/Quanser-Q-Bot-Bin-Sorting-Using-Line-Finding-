# Quanser-Q-Bot-Bin-Sorting-Using-Line-Finding
This project leverages Quanser Simulation Lab in an environment that uses a ultrasonic and colour sensors mounted on a Q-Bot to accurately sort recyclables and waste into their appropriate bins

## How It Works

### Q-Bot Simulation (Q-Labs Python Files/Student_Files/P3_Simulation_Template.py)

The core functionality of this project revolves around loading containers from a bottle dispensary into the Q-Bot using a Q-arm and having the Q-Bot travel around a line-track and dispense the containers into appropriate bins. 
The Q-Bot follows the line using an IR sensor and a set of calls that determine how to adjust the wheel position and speed based on the input from the IR sensor. In order to dump the bottles into the appropriate bins, the robot uses an
ultrasonic sensor to determine whether a bin is a 90% degree angle to the robot and a colour sensor to determine if it is the right bin. If a bin is present and the right colour, the robot stops and uses linear acutators to dump the
bottles and cans into their respect bins. The robot then follows the same line and returns to its original location. 

![image](https://github.com/vikramC04/Quanser-Q-Bot-Bin-Sorting-Using-Line-Finding-/assets/139662459/e78cc373-e18b-4c6e-b0fb-1da222e71d5f)



