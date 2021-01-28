import logging, os, time
import config
from FBpyGIF import fb

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class FrameBuffer(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, path = None):
        super().__init__(group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
        self.BIT_DEPTH = 8
        self.FRAME_BUFFER = 1
        config.framebuffer = path

    def run(self):
        fb.ready_fb(self.BIT_DEPTH, self.FRAME_BUFFER)
        fb.ready_img(config.path)
        fb.show_img(fb.ready_img(config.path))


fb = FrameBuffer(path = "./images/areyareadykids.gif")
fb.start()

time.sleep(5)

fb.join()
