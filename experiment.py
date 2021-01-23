import config
import queue
import time
import logging
from modules import *

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

config.status = "experiment"
buffers = {}
threads = {}
i = 0

setup_DSLRs = GPhotoUtils()
for gcamera in setup_DSLRs.camera_list:
    name = gcamera[0]
    addr = gcamera[1]
    buffers["gcamera"+str(i)] = queue.Queue(maxsize=0)
    threads["gcamera"+str(i)] = GPhotoCamera(args =(buffers["gcamera"+str(i)]), index=i, name=gcamera[0], addr=gcamera[1]) 
    i += 1
    
opencv_cameras = CV2Utils.returnCameraIndexes()
opencv_best_res = CV2Utils.returnCameraResolutions( opencv_cameras )
for cvcamera in opencv_cameras:
    buffers["ocamera"+str(cvcamera)] = queue.Queue(maxsize=0)
    threads["ocamera"+str(cvcamera)] = WebcamVideoStream( q = buffers["ocamera"+str(cvcamera)], src = int(cvcamera), width = opencv_best_res[0], height = opencv_best_res[1])


config.run = True
logging.debug("Config.run is True")

"""
serial_buffer = queue.Queue(maxsize=0)
arduino = DAQReader(args = (serial_buffer))
buffers["arduino"] = serial_buffer
threads["arduino"] = arduino
"""
clips = Clipboard(args =(buffers))
threads["clips"] = clips

for key, thread in threads.items():
    logging.debug("Starting thread: " + key)
    thread.start()

time.sleep(20)

config.run = False  
logging.debug("Config.run is False")
time.sleep(2)

for key, thread in threads.items():
    thread.stop()
    thread.join()