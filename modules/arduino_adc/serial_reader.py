import threading
import serial, time
import logging
import config
import asciiplotlib as apl

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
        self.update = 200
        self.last_values = []

    def run(self):
        while True:
            if config.run == False:
                self.stop()
                break
            if self.plugged == True:
                channels = self.read_all_channels()
                with self.q.mutex:
                    self.q.queue.clear()
                self.q.put( [self.t, channels] )
                self.last_values.append( [self.t, channels] )
                if len(self.last_values) > self.update:
                    self.preview_plot()
                    self.last_values = []
                self.arduino.flushInput()
            elif self.plugged == False:
                self.test_arduino()

    def preview_plot(self):
        x = []
        y = []
        for count, event in enumerate(self.last_values):
            x.append(float(count))
            y.append(float(event[1][0]))
        fig = apl.figure()
        fig.plot(x, y, label="ch0", width=25, height=6)
        fig.show() 

    def join(self):
        self.stop()

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
        channels = ["1:"]
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
                self.t = time.time()
                return results
            if save_next == True:
                results.append( data_d )
                save_next = False
            if data_d in channels:
                save_next = True

    def __exit__(self, exc_type, exc_value, traceback) :
        self.arduino.close()