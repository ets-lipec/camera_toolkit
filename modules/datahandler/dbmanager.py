import threading
import logging
from tinydb import TinyDB, where
import os
import config

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class Entry(threading.Thread):

    def __init__(self, args=(), kwargs=None, index=None, name=None, addr=None):
        super().__init__()
        self.q = args
        self.kwargs = kwargs
        self.index = index
        if not os.path.exists(config.experiment_path):
            os.makedirs(config.experiment_path)
        self.db = TinyDB(config.experiment_path + "/" + "data.json")
        logging.debug("TinyDB is up and running.")

    def run(self):
        last_value = ""
        while True:
            qvalue = self.q.get() 
            if qvalue != last_value:
                logging.debug("New entry saved to database: " + str(qvalue))
                last_value = qvalue
                self.prepare_doc(qvalue)

    def prepare_doc(self, qvalue):
        for key, value in qvalue.items():
            doc = {}
            doc["type"] = key
            doc["timestamp"] = value[0]
            doc["value"] = value[1]
            doc["count"] = config.count
            doc["status"] = config.status
            self.db.insert( doc )
