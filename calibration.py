from modules import *
import queue, time


def read_kbd_input(inputQueue):
    print('Ready for keyboard input:')
    while (True):
        input_str = input()
        inputQueue.put(input_str)

config.status = "calibration"

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

clips = Clipboard(args =(buffers))
threads["clips"] = clips

for key, thread in threads.items():
    logging.debug("Starting thread: " + key)
    thread.start()


inputQueue = queue.Queue()
inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue,), daemon=True)
inputThread.start()

logging.debug("Press 'Q' or 'C' to exit")
while (True):
    if (inputQueue.qsize() > 0):
        input_str = inputQueue.get()
        print("input_str = {}".format(input_str))
        if (input_str == "quit"):
            config.run = False
            logging.debug("Exiting serial terminal.")
            break 
        elif (input_str == "s"):
            config.trigger = True
            logging.debug("Triggered caliration shot.")

        time.sleep(0.01) 


config.run = False  
logging.debug("Config.run is False")
time.sleep(2)

for key, thread in threads.items():
    thread.stop()
    thread.join()