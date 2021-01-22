import threading
import logging
import config
import time
import cv2

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class Clipboard(threading.Thread):

    def __init__(self, args=(), kwargs=None):
        super().__init__()
        self.queues = args
        self.kwargs = kwargs

    def run(self):
        last_grab = time.time() - 99999
        while True:
            if config.run == False:
                break
            if time.time() - last_grab > 1.0 and all(value == True for value in config.cameras.values()):
                logging.debug("TIME FOR A SHOT " + str(time.time() - last_grab ))
                last_grab = time.time()
                config.gtrigger = True
                logging.debug("config.trigger is TRUE")
                logging.debug("The queue contains "+str(len(self.queues.items())) + " objects.")
                logging.debug(self.queues)
                for device, q in self.queues.items():
                    value = q.get()
                    logging.debug("Retrieved "+device+" from the queue.")
                config.gtrigger = False
                logging.debug("config.trigger is FALSE")


    def stop(self):
        pass