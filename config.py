import os

status = "experiment" # Can be 'experiment' or 'calibration'
serial = True # Will you be using an Arduino for ADC acquisition ?
serial_port = "/dev/ttyACM0"
serial_baudrate = 115200
opencv = True # Will you be using a webcam ?
DSLR = False # Will you be using a gphoto2 compatible camera ?
timestep = 2 # Must be higher than 1 at least
experiment_path = os.getcwd()+"/Dummy_experiment/"


# No need to change these variables
run = True
preview = False
trigger = False
framebuffer = None
devices = {}
count = 0
