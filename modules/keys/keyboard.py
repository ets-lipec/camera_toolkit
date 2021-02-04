import threading
import logging
import config

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)


class KeyMonitor(threading.Thread):

    def __init__(self, args=(), kwargs=None):
        super().__init__()
        self.q = args
        self.args = args
        logging.debug('Ready for keyboard input:')

    def run(self):
        while (True):
            input_str = input()
            self.q.put(input_str)
