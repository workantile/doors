
import os
import sys
#######################################################
#                                                     #
# Add simulator/ directory to the module search path. #
#                                                     #
#######################################################
sys.path.insert(0, os.path.join(os.getcwd(), "simulator"))



print("Welcome to the Workantile Door System Simulator!")
import doors
from doors import *
