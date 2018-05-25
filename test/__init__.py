import sys

import os


# make importing stuff from autoweeklyemail work
root_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_folder)
sys.path.append(os.path.join(root_folder, "autoweeklyemail"))

print(sys.path)