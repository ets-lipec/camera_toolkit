import os

status = "experiment" # Can be 'experiment' or 'calibration'

serial = False # Will you be using an Arduino for ADC acquisition ?
continuous_serial = False #If True, Arduino data will be constantly logged as well as when a picture is grabbed
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
data_export_script = os.getcwd()+"/export_data.py"