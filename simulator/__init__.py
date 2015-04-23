
import importlib
import os
import sys
#######################################################
#                                                     #
# Add simulator/ directory to the module search path. #
#                                                     #
#######################################################
sys.path.insert(0, os.path.join(os.getcwd(), "simulator"))


import doors
from doors import *


def reload_sim(namespace):
    importlib.reload(GPIO)
    importlib.reload(request)
    importlib.reload(serial)
    importlib.reload(doors)
    namespace.update(doors.__dict__)


print("")
print("Welcome to the Workantile Door System Simulator!")
print("Hint: call reload() to reload the simulator with updated code.")
