import threading
import serial, time
import logging
import config

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)


class DAQReader(threading.Thread):

    def __init__(self, args=(), kwargs=None, baudrate=115200, port="/dev/ttyACM0"):
        super().__init__()
        self.q = args
        self.args = args
        self.port = port
        self.baudrate = baudrate
        self.kwargs = kwargs
        self.test_arduino()

    def run(self):
        last_update = time.time()
        while True:
            if config.run == False:
                self.stop()
                break
            if self.plugged == True:
                channels = self.read_all_channels()
                self.q.put( [time.time(), channels] )
                if time.time() - last_update > 10:
                    logging.debug("Arduino reader is currently running with no issues: " + str(channels))
                    last_update = time.time()
            elif self.plugged == False:
                self.test_arduino()

    def stop(self):
        self.arduino.close()

    def test_arduino(self):
        try:
            self.arduino = serial.Serial(self.port, self.baudrate, timeout = None)
            self.plugged = True
            logging.debug("Successfully connected to the Arduino port.")
        except serial.serialutil.SerialException as e:
            logging.warning("An ADC channel is specified in the deck, but I can't access it: " + str(e))
            self.plugged = False

    def read_all_channels(self):
        channels = ["1:", "2:"]
        results = []
        save_next = False
        while True:
            try:
                data = (self.arduino.readline().strip())
                data_d = data.decode("utf-8")
            except UnicodeDecodeError:
                data_d = ""
                save_next = False 
            if len(results) == len(channels):
                return results
            if save_next == True:
                results.append( data_d )
                save_next = False
            if data_d in channels:
                save_next = True

    def __exit__(self, exc_type, exc_value, traceback) :
        self.arduino.close()