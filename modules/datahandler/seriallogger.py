import threading
import logging
from tinydb import TinyDB, where
import os
import config
from datetime import datetime

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class DAQLogger(threading.Thread):

    def __init__(self, args=(), kwargs=None, index=None, name=None, addr=None):
        super().__init__()
        self.q = args
        self.kwargs = kwargs
        self.index = index
        if not os.path.exists(config.experiment_path):
            os.makedirs(config.experiment_path)
        self.db = TinyDB(config.experiment_path + "/" + "arduino_data.json")
        logging.debug("TinyDB is up and running.")

    def run(self):
        while True:
            qvalue = self.q.get()
            self.prepare_doc(qvalue)
            

    def prepare_doc(self, qvalue):
        doc = {}
        doc["type"] = "arduino"
        doc["timestamp"] = qvalue[0]
        doc["value"] = qvalue[1][0]
        doc["count"] = config.count
        doc["status"] = config.status
        self.db.insert( doc )