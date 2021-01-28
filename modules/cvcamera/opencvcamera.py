from threading import Thread, Lock
import cv2, time
import pkg_resources
import logging
import config
import pandas as pd

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class WebcamVideoStream :
    def __init__(self, q = None, src = 0, width = 1280, height = 720) :
        self.q = q
        self.src = src
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()
        config.devices["opencv"+str(self.src)] = True
        logging.debug("OpenCV camera is __init__.")

    def start(self) :
        if self.started :
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        logging.debug("Started OpenCV stream in thread.")

    def update(self) :
        while self.started :
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.t = time.time()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()
            if config.trigger == True:
                config.devices["opencv"+str(self.src)] = False
                frame = self.get()
                logging.debug("Open CV camera triggered.")
                self.filename = config.experiment_path+config.status+"/"+str(self.t)+"ocv"+str(self.src)+".png"
                self.q.put( [self.t, self.filename] )
                self.save_image(frame)
                config.devices["opencv"+str(self.src)] = True
                config.trigger = False
            if config.preview == True:
                config.devices["opencv"+str(self.src)] = False
                frame = self.get()
                logging.debug("Open CV camera triggered.")
                self.filename = config.experiment_path+"preview"+"/"+"ocv"+str(self.src)+".png"
                print("FILENAME: ", self.filename)
                self.save_image(frame)
                config.devices["opencv"+str(self.src)] = True
                config.preview = False

    def save_image(self, frame):
        cv2.imwrite(self.filename, frame)
        logging.debug("Saved Open CV camera image to: "+ self.filename)

    def get(self) :
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame
        
    def stop(self):
        self.join()

    def join(self) :
        self.started = False
        if self.thread.is_alive():
            self.thread.join()
        self.stream.release()
        logging.debug("Closed connection with Open CV camera")

    def __exit__(self, exc_type, exc_value, traceback) :
        self.stream.release()


def returns_common_resolutions():
    stream = pkg_resources.resource_stream(__name__, 'data/common_resolutions.csv')
    return pd.read_csv(stream)

class CV2Utils:

    def __init__(self):
        pass


    @staticmethod
    def returnCameraIndexes():
        index = 0
        arr = []
        i = 20
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
            i -= 1
            time.sleep(0)
        if not arr: 
            arr = False
            logging.debug("No OpenCV webcams found ..." )
        else:
            arr = [str(i) for i in arr] 
            logging.debug("Found OpenCV cameras: " + str(arr))
        return arr

    @staticmethod
    def returnCameraResolutions( video_sources ):
        table = CV2Utils.returns_common_resolutions()
        resolutions = {}
        for video_source in video_sources:
            resolutions[str(video_source)] = []
            cap = cv2.VideoCapture(int(video_source))
            for index, row in table[["W", "H"]].iterrows():
                if index != 0:
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(row["W"]))
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(row["H"]))
                    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                    resolutions[str(video_source)].append( [ int(width), int(height)] )

        max_resolutions = []
        for camera, resolutions_list in resolutions.items():
            resolutions_set = set(tuple(i) for i in resolutions_list)
            best_res = max(resolutions_set)
            max_resolutions.append( best_res )
        best_compatible_res =min(max_resolutions)

        logging.debug("The best resolution for all OpenCV cameras is: " + str(best_compatible_res) )
        return best_compatible_res

    @staticmethod
    def returns_common_resolutions():
        stream = pkg_resources.resource_stream(__name__, 'data/common_resolutions.csv')
        return pd.read_csv(stream)