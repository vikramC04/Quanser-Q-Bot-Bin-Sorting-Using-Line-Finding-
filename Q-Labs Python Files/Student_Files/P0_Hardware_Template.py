ip_address = '172.17.42.73' # Enter your IP Address here
project_identifier = 'P0'
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.hardware_project_library import *

hardware = True
speed = 0.1 # in m/s
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
bot = qbot(speed,ip_address,QLabs,project_identifier,hardware)
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------











#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

