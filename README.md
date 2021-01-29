# camera_toolkit

This package is designed to capture images from two different kinds of camera sources (webcams compatible with `opencv` and DSLRs compatible with `gphoto2`) while simultaneously recording the value of a voltage captured using the ADC channels of an Arduino Uno. The packages uses threading to try as much as possible to grab data from all sources at the same time.

# Install

First, start by installing the necessary system dependencies.

## Dependencies

Dependencies necessary to run the package (tested on Debian and Ubuntu):

`sudo apt install build-essential pkg-config git python3-dev python3-venv gnuplot libgphoto2-dev`

## Clone the repo

Then clone the repo:

`git clone https://github.com/ilyasst/camera_toolkit.git`

Enter the cloned folder:

`cd camera_toolkit`

## Python package dependencies

Then install the necessary python packages, we'd recommend that you do that in a virtual environment.

### Virtual environment

Create your virtual environment:

`python3 -m venv .env`

Then load it:

`source .env/bin/activate`

Then install the python dependecies using:

`pip install -r requirements.txt`

# Run the code

You should be ready to run the code, but before doing do, you might want to edit the content of the `config.py` file:

```python
import os

status = "experiment" # Can be 'experiment' or 'calibration'
serial = False # Will you be using an Arduino for ADC acquisition ?
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
```

And finally, use `python3 camcontroller.py` to run the code.


# Arduino for ADC measurements

This is an example of the kind of code that can be used on the Arduino Uno to measure the voltage (between 0 and 5V) using the A0 channel of the ADC.

```c                                       
void setup() {
        Serial.begin(115200); // use the same baud-rate as the python side
}
void loop() {

  // read value from analog pin
  int sensorValue0 = analogRead(A0);
  float voltage0 = sensorValue0 * ( 5.0 / 1023.0 );

  Serial.println("1:"); // This is using as a marker to recognize the channel
  Serial.println(voltage0);
}
```