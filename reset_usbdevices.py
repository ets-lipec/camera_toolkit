"""
    Example code for resetting the USB port that a Teensy microcontroller is
    attached to. There are a lot of situations where a Teensy or Arduino can
    end up in a bad state and need resetting, this code is useful for 
"""

import os
import fcntl
import subprocess


# Equivalent of the _IO('U', 20) constant in the linux kernel.
USBDEVFS_RESET = ord('U') << (4*2) | 20

devices = ["arduino", "canon", "camera"]

def get_teensy():
    """
        Gets the devfs path to a Teensy microcontroller by scraping the output
        of the lsusb command
        
        The lsusb command outputs a list of USB devices attached to a computer
        in the format:
            Bus 002 Device 009: ID 16c0:0483 Van Ooijen Technische Informatica Teensyduino Serial
        The devfs path to these devices is:
            /dev/bus/usb/<busnum>/<devnum>
        So for the above device, it would be:
            /dev/bus/usb/002/009
        This function generates that path.
    """
    devs = []
    proc = subprocess.Popen(['lsusb'], stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    lines = out.decode("utf-8").split('\n')
    print(lines)
    for line in lines:
        for device in devices:
            if device in line.lower():
                parts = line.split()
                bus = parts[1]
                dev = parts[3][:3]
                print(line)
                devs.append('/dev/bus/usb/%s/%s' % (bus, dev))
    return devs


def send_reset(dev_path):
    """
        Sends the USBDEVFS_RESET IOCTL to a USB device.
        
        dev_path - The devfs path to the USB device (under /dev/bus/usb/)
                   See get_teensy for example of how to obtain this.
    """
    fd = os.open(dev_path, os.O_WRONLY)
    try:
        fcntl.ioctl(fd, USBDEVFS_RESET, 0)
    finally:
        os.close(fd)


def reset_teensy():
    """
        Finds a teensy and reset it.
    """
    devs = get_teensy()
    for dev in devs:
        send_reset(dev)

reset_teensy()