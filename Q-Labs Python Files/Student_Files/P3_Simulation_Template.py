ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P3B' # Enter the project identifier i.e. P3A or P3B

# SERVO TABLE CONFIGURATION
short_tower_angle = 270 # enter the value in degrees for the identification tower 
tall_tower_angle = 0 # enter the value in degrees for the classification tower
drop_tube_angle = 180 # enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# BIN CONFIGURATION
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.13 # offset in meters
bin1_color = [1,0,0] # e.g. [1,0,0] for red
bin1_metallic = False

bin2_offset = 0.13
bin2_color = [0,1,0] #Green
bin2_metallic = False

bin3_offset = 0.13
bin3_color = [0,0,1] #Blue
bin3_metallic = False

bin4_offset = 0.13
bin4_color = [2,0,0] #Black
bin4_metallic = False
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
if project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
else:
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color],[bin1_metallic,bin2_metallic, bin3_metallic,bin4_metallic]]
    configuration_information = [table_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bot = qbot(0.1,ip_address,QLabs,project_identifier,hardware)
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
import random
import time

#List that stores every container dispensed. 
container_list = []

#Ethan
def get_home_position():
    #Meant to store initial position of QBot
    home_position = bot.position()
    return home_position

#Ethan
def dispense_container():
    rand_int = random.randint(1, 6)

    #Storing all container attributes of randomly dispensed container 
    container_attributes = table.dispense_container(rand_int,True)

    #Returning list containing the attributes
    return container_attributes

#Ethan
def pick_up_drop_off(counter):
    #Moving arm to initial bottle position and gripping the bottle
    arm.move_arm(0.64, 0.0, 0.23)
    time.sleep(3)
    arm.control_gripper(40)
    time.sleep(3)

    #Moving arm to neutral position where the bottle will not clip the Qbot
    arm.move_arm(0.012,-0.376,0.621)
    time.sleep(3)

    '''
    Depending on the number of bottles dispensed, there is a different location on the Qbot
    the bottle is dropped in. The counter variable is a parameter which represents the bottles dispensed
    with 0 being 1, 1 being 2 etc. 
    '''
    if counter == 0:
        #Moving the Q-arm to the Q-Bot and dropping the container
        arm.move_arm(0.012, -0.637, 0.531)
        time.sleep(3)
        arm.control_gripper(-40)
        time.sleep(3)
        arm.rotate_shoulder(-20)
        time.sleep(1)
        arm.home()
    elif counter == 1:
        arm.move_arm(0.017, -0.521, 0.498)
        time.sleep(3)
        arm.control_gripper(-40)
        time.sleep(3)
        arm.rotate_shoulder(-20)
        time.sleep(1)
        arm.home()
    else:
        arm.move_arm(0, -0.462, 0.478)
        time.sleep(3)
        arm.control_gripper(-40)
        time.sleep(3)
        arm.rotate_shoulder(-20)
        time.sleep(1)
        arm.home()
    
    return None

#Vikram
def load_container(cycle_count):
    #Intializing variables
    total_mass = 0
    counter = 0

    #Mass of any bottles on table before any bottles are dispensed
    table_mass = table.load_cell_sensor(0.2)[0]

    #Iterating till three bottles are dropped or conditions are met
    while counter < 3:

        '''
        Cycle count represents, the number of cycles that have been completed. If one cycle
        has already been completed and there is a bottle on the table and no bottles have been dispensed
        The bottle that is already on the table is loaded onto the Qbot. 
        This conditional is designed to acommodate for extra containers that were dispensed but could not be loaded.
        '''
        if cycle_count != 1 and table_mass != 0.0 and counter == 0:

            #Loading container and incrementing the mass
            pick_up_drop_off(counter)
            total_mass += table_mass

            '''
            During the first cycle, a list stores the bin locations of all the container that were dispensed. The last
            bin location of the bottles that were dispensed is stored and then added to a new list to mark the start
            of the second cycle
            '''
            temp = container_list[-1]
            container_list.clear()
            container_list.append(temp)
            counter += 1

            #This counts as a load iteration so the remaining code does not need to be run
            continue

        #Clearing the container list if there is no containers left on the servo table to prevent bin mixup
        if counter == 0:
            container_list.clear()

        #Dispensing the storing it's attributes and incrementing mass
        container_attributes = dispense_container()
        container_list.append(container_attributes[2])
        total_mass += container_attributes[1]
        print("Total mass: ", total_mass)

        if total_mass < 90:
            if counter == 0:
                #When first bottle is dispensed, bin location is stored
                print(container_attributes[2])
                #Container is moved to Q-Bot
                pick_up_drop_off(counter)
                counter += 1
                time.sleep(3)
            elif counter != 0 and container_list[counter -1] == container_attributes[2]:
                '''
                When the second or third bottles are dispensed, they are only loaded if the previous bottle
                has the same bin destination
                '''
                pick_up_drop_off(counter)
                counter += 1
                time.sleep(3)
            else:
                #If the bottle dispensed does not have the same bin location, loop stops and function ends
                break
        else:
            break

        
    #Returns all containers in Q-Bot
    return container_list

#Vikram
def unload_container():
    '''
    In order to make sure the containers do not go flying when they are being transferred to the bins,
    The hopper is incremented slowly with pauses in between to allow for a smooth transfer. 
    '''
    bot.stop()
    time.sleep(1)
    bot.activate_linear_actuator()
    time.sleep(2)
    bot.rotate_hopper(20)
    time.sleep(2)
    bot.rotate_hopper(40)
    time.sleep(2)
    bot.rotate_hopper(60)
    time.sleep(2)
    bot.rotate_hopper(90)
    time.sleep(3)
    bot.deactivate_linear_actuator()
    bot.deactivate_color_sensor()

#Vikram   
def transfer_container(cycle_count): 
    #Dispensing and loading container
    container_list = load_container(cycle_count)
    print(container_list)

    bot.activate_line_following_sensor()
    time.sleep(0.3)
    bot.activate_color_sensor()

    #Two boolean variables used to indicate sensors active
    ultrasonic_active = False
    coulour_turned_off = False
    
    x = True
    while x:
        '''
        When both IR sensors are located on the line, the Qbot is straight and therefore bot wheels are set to the same speed.
        When the left reading of the IR sensor is 0, which means it's off the line, the Qbot pivots on it's right wheel to straighten it out.
        When the right reading of the IR sensor is 0, it similarly pivotes on the left wheel. When the bot is off the line, it will spin faster on it's
        left than it's right to attempt to straighten itself out and allign itself with the line. 
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

        '''
        This protocol was put in place to only read the colour sensor if the ultrasonic sensor is not active.
        It's done to make sure the Qbot does not overload and tumble of the line. The colour sensor is also
        deactivated once the ultrasonic sensor is turned on
        '''
        if ultrasonic_active == False:
            colour_readings = bot.read_color_sensor()
        elif ultrasonic_active == True and coulour_turned_off == False :
            bot.deactivate_color_sensor()
            coulour_turned_off = True

        '''
        If the bin deposit location matches the colour readings for the bin, the ultrasonic sensor is activated. The following is also
        executed if the ultrasonic sensor is turned on and the designated bin location matches the Qbot position. 
        '''
        if ultrasonic_active == True and container_list[0] == 'Bin01' or container_list[0] == 'Bin01' and colour_readings[0][0] == 1:
            '''
            The first time this code will be executed is when the colour readings match the bin drop off as the ultrasonic_active is False on default
            and cannot be True until inside the conditional. The first instance of the bot being close to the correct bin, the ultrasonic sensor will turn on.
            '''
            if ultrasonic_active == False:
                bot.activate_ultrasonic_sensor()
                ultrasonic_active = True

            '''
            The ultrasonic readings are stored and once it's underneath a certain threshold, the method that unloads the container is called. This is the same
            for all the if statements in this particular conditional
            '''
            ultrasonic_readings = bot.read_ultrasonic_sensor()
            print(ultrasonic_readings) 
            if ultrasonic_readings < 0.065:
                unload_container()
                x= False;
        elif ultrasonic_active == True and container_list[0] == 'Bin02' or container_list[0] == 'Bin02' and colour_readings[0][1] == 1:
            if ultrasonic_active == False:
                bot.activate_ultrasonic_sensor()
                ultrasonic_active = True
                
            ultrasonic_readings = bot.read_ultrasonic_sensor()
            print(ultrasonic_readings)
            if ultrasonic_readings <= 0.02:
                unload_container()
                x= False;
        elif ultrasonic_active == True and container_list[0] == 'Bin03' or container_list[0] == 'Bin03' and colour_readings[0][2] == 1:
            if ultrasonic_active == False:
                bot.activate_ultrasonic_sensor()
                ultrasonic_active = True
                
            ultrasonic_readings = bot.read_ultrasonic_sensor()
            print(ultrasonic_readings) 
            if ultrasonic_readings <= 0.038:
                unload_container()
                x= False;
        elif ultrasonic_active == True and container_list[0] == 'Bin04' or container_list[0] == 'Bin04' and colour_readings[0][0] == 2:
            if ultrasonic_active == False:
                bot.activate_ultrasonic_sensor()
                ultrasonic_active = True
                
            ultrasonic_readings = bot.read_ultrasonic_sensor()
            print(ultrasonic_readings) 
            if ultrasonic_readings <= 0.025:
                unload_container()
                x= False;
    return None

#Vikram
def return_home(initial_home_position):

    #Storing home coordinates 
    home_position = initial_home_position
    position = []
    bot.activate_line_following_sensor()
    x = True
    while x:
        IR_readings = bot.line_following_sensors()
        left_ir = IR_readings[0]
        right_ir = IR_readings[1]
        position = bot.position()
        '''Home position is passed as a parameter and
        if current position is within a 5% difference on the x and y coordinates, bot stops.
        The bot must also be oriented straightly to stop. 
        '''
        if position[0]/home_position[0] >= 0.95 and position[1]/home_position[1] >= 0.95 and IR_readings[0] == 1 and IR_readings[1] == 1:
            bot.stop()
            break;
        
        '''
        When both IR sensors are located on the line, the Qbot is straight and therefore bot wheels are set to the same speed.
        When the left reading of the IR sensor is 0, which means it's off the line, the Qbot pivots on it's right wheel to straighten it out.
        When the right reading of the IR sensor is 0, it similarly pivotes on the left wheel. When the bot is off the line, it will spin faster on it's
        left than it's right to attempt to straighten itself out and allign itself with the line. 
        '''
        if left_ir == 1 and right_ir == 1:
            bot.set_wheel_speed([0.1,0.1])
        elif left_ir == 1 and right_ir == 0:
            bot.set_wheel_speed([0,0.03])
        elif left_ir == 0 and right_ir == 1:
            bot.set_wheel_speed([0.03,0])
        else:
            bot.set_wheel_speed([0.5,0.2])

    #Rotating Qbot to straight position as the Qbot when stopped is slanted 15 degrees off 180 degrees
    time.sleep(3)
    bot.rotate(-15)
    time.sleep(3)

    #Moving Qbot forward to correct home position and then rotating bot to face the wall and again moving forward to reach the right depth from the wall
    bot.forward_time(2.5)
    time.sleep(3)
    bot.rotate(100)
    time.sleep(3)
    bot.forward_time(0.9)
    time.sleep(3)

    #Rotating Qbot to correct orientation
    bot.rotate(-100)
    return None

#Vikram
def execute():
    #Calling all functions
    initial_home_position = get_home_position()
    time.sleep(3)
    transfer_container(1)
    time.sleep(3)
    return_home(initial_home_position)
    time.sleep(3)
    transfer_container(2)
    time.sleep(2)
    return_home(initial_home_position)
    return None

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

