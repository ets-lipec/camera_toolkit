import threading, os, glob
from os import path
import logging
import config
import time
import queue
import cv2
import shutil
from .dbmanager import Entry

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class Clipboard(threading.Thread):

    def __init__(self, args=(), kwargs=None):
        super().__init__()
        self.queues = args
        self.kwargs = kwargs
        self.dbqueue = queue.Queue(maxsize=0)
        self.dbthread = Entry(args = (self.dbqueue))
        shutil.copy(config.data_export_script, config.experiment_path+"data_export.py")
        if not os.path.exists(config.experiment_path+config.status+"/"):
            os.makedirs(config.experiment_path+config.status+"/")
        if not os.path.exists(config.experiment_path+"preview"+"/"):
            os.makedirs(config.experiment_path+"preview"+"/")

    def run(self):
        self.dbthread.start()
        last_grab = time.time() - 99999
        while True:
            if config.run == False:
                break
            if config.status == "experiment":
                if time.time() - last_grab > config.timestep and all(value == True for value in config.devices.values()):
                    config.trigger = True
                    logging.debug("TIME FOR A SHOT " + str(time.time() - last_grab ))
                    last_grab = time.time()
                    logging.debug("config.trigger is TRUE")
                    logging.debug("The queue contains "+str(len(self.queues.items())) + " objects.")
                    cycle_results = {}
                    for device, q in self.queues.items():
                        qvalue = q.get()
                        cycle_results[device] = qvalue
                    logging.debug(cycle_results)
                    self.dbqueue.put(cycle_results)
                    config.trigger = False
                    logging.debug("config.trigger is FALSE")
                    config.count += 1
            elif config.status == "calibration":
                if config.trigger == True and all(value == True for value in config.devices.values()):
                    logging.debug("YOU ASKED FOR A SHOT")
                    logging.debug("The queue contains "+str(len(self.queues.items())) + " objects.")
                    last_grab = time.time()
                    cycle_results = {}
                    for device, q in self.queues.items():
                        qvalue = q.get()
                        cycle_results[device] = qvalue
                    logging.debug(cycle_results)
                    self.dbqueue.put(cycle_results)
                    config.trigger = False
                    logging.debug("config.trigger is FALSE")
                    config.count += 1
                elif config.trigger == False and all(value == True for value in config.devices.values()):
                    if time.time() - last_grab > 5:
                        config.preview = True
                        logging.debug("TIME FOR A PREVIEW SHOT " + str(time.time() - last_grab ))
                        last_grab = time.time()
                        config.count += 1
                        #for infile in glob.glob(config.experiment_path+"preview"+"/"+"*.png"):
                        #    pass
                        config.preview = False
                        logging.debug("config.preview is FALSE")

            else:
                if time.time() - last_grab > 15:
                    logging.debug("Standby in an unkown mode")

    def stop(self):
        pass