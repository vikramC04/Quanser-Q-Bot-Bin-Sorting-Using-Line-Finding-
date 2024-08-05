ip_address = '172.17.42.73' # Enter your IP Address here
project_identifier = 'P3B' # Enter the project identifier i.e. P3A or P3B
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.hardware_project_library import *

hardware = True
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
if project_identifier == 'P3A':
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    table = servo_table(ip_address,QLabs,None,hardware)
else:
    speed = 0.1 # in m/s
    bot = qbot(speed,ip_address,QLabs,project_identifier,hardware)
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
import time

def transfer_container(time_taken, container):
    bot_dropped = False
    bot.activate_line_following_sensor()
    bot.activate_color_sensor()

    #Taking time from epoch at the start of the function
    initial_time= time.time()

    x =True
    while x:
        #Taking time from epoch every time loop iterates
        program_running_time = time.time()

        #If the time the Qbot has been moving is greater than the time passed as a parameter, the bot is stopped
        time_difference= program_running_time - initial_time
        if time_difference >= time_taken:
            bot.stop()
            break;

        '''
        The colour readings are read and if the RGB values from the readings match
        the correct values for the specific colour and also matches the container that was grabbed from input, the containers are deposited
        '''
        try:
            #Red
            colour_readings = bot.read_color_sensor()
            rgb_values = colour_readings[1]
            if rgb_values[0] > 140 and container == 2 or rgb_values[0] > 140 and container == 5:
                bot.stop()
                time.sleep(3)
                unload_container()
                break
            elif rgb_values[1] > 140 and container == 3:
                #Green
                bot.stop()
                time.sleep(3)
                unload_container()
                break
            elif rgb_values[2] > 140 and container == 1:
                #Blue
                bot.stop()
                time.sleep(3)
                unload_container()
                break
            elif rgb_values[0] == 0 and rgb_values[1] == 0 and rgb_values[2] == 0 and container == 4 or rgb_values[0] == 0 and rgb_values[1] == 0 and rgb_values[2] == 0 and container == 6:
                #Black
                bot.stop()
                time.sleep(3)
                unload_container()
                break
                
        except:
            #If there is an error thrown such as the double list not being created, the program is paused
            time.sleep(2)
            
        '''
        When both IR sensors are located on the line, the Qbot is straight and therefore bot wheels are set to the same speed.
        When the left reading of the IR sensor is 0, which means it's off the line, the Qbot pivots on it's right wheel to straighten it out.
        When the right reading of the IR sensor is 0, it similarly pivotes on the left wheel. When the bot is off the line, it will spin faster on it's
        left than it's right to       attempt to straighten itself out and allign itself with the line. 
        '''
        IR_readings = bot.line_following_sensors()
        left_ir = IR_readings[0]
        right_ir = IR_readings[1]
        if left_ir == 1 and right_ir == 1:
            bot.set_wheel_speed([0.1,0.1])
        elif left_ir == 1 and right_ir == 0:
            bot.set_wheel_speed([0,0.03])
        elif left_ir == 0 and right_ir == 1:
            bot.set_wheel_speed([0.03,0])
        else:
            bot.set_wheel_speed([0.5,0.2])
    return None


def unload_container():
    #Function in which the hopper transfers the container
    bot.activate_linear_actuator()
    bot.linear_actuator_out(4)
    time.sleep(8)
    bot.linear_actuator_in(4)
    time.sleep(1)

def execute():
    #Calling all functions and getting user input for containers
    container = input("Enter container being transferred: ")
    transfer_container(400,container)
    time.sleep(5)
    transfer_container(45,container)
    return None

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

