import gphoto2 as gp
import logging, time, os
import config
import threading

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class GPhotoCamera(threading.Thread):

    def __init__(self, args=(), kwargs=None, index=None, name=None, addr=None):
        super().__init__()
        self.q = args
        self.kwargs = kwargs
        self.index = index
        print(self.index)
        self.name = name
        if not os.path.exists(config.experiment_path):
            os.makedirs(config.experiment_path)
        self.init_gcam(index, name, addr)
        config.cameras[self.name+str(self.index)] = True

    def init_gcam(self, index, name, addr):
        self.camera = gp.Camera()
        port_info_list = gp.PortInfoList()
        port_info_list.load()
        idx = port_info_list.lookup_path(addr)
        self.camera.set_port_info(port_info_list[idx])
        self.camera.init()

    def run(self):
        self.plugged = True
        logging.debug('Camera running')
        while True:
            if config.run == False:
                self.stop()
                break
            if config.gtrigger == True:
                config.cameras[self.name+str(self.index)] = False
                logging.debug("Gphoto camera triggered")
                self.i2 = self.camera.capture(gp.GP_CAPTURE_IMAGE)
                self.t = time.time()
                self.f2 = self.camera.file_get(self.i2.folder,self.i2.name,gp.GP_FILE_TYPE_NORMAL)
                self.q.put( [self.t, self.i2.name] )
                self.empty_queue()
                self.save_photo()
                config.cameras[self.name+str(self.index)] = True
                config.gtrigger = False
                
    def save_photo(self):
        dest2 = os.path.join( config.experiment_path, str(self.t)+"g"+str(self.index)+self.i2.name)
        self.f2.save(dest2)
        logging.debug("Saved gPhoto camera image to '%s'" % dest2)

    def empty_queue(self):
        typ,data = self.camera.wait_for_event(200)
        while typ != gp.GP_EVENT_TIMEOUT:
            
            logging.debug("Event: %s, data: %s" % (self.event_text(typ),data))
            
            if typ == gp.GP_EVENT_FILE_ADDED:
                fn = os.path.join(data.folder,data.name)
                logging.debug("New file: %s" % fn)
            typ, data = self.camera.wait_for_event(1)

    def stop(self):
        self.empty_queue()
        self.camera.exit()
        print('Dropped connection with camera')

    def event_text(self, event_type):
        if event_type == gp.GP_EVENT_CAPTURE_COMPLETE: return "Capture Complete"
        elif event_type == gp.GP_EVENT_FILE_ADDED: return "File Added"
        elif event_type == gp.GP_EVENT_FOLDER_ADDED: return "Folder Added"
        elif event_type == gp.GP_EVENT_TIMEOUT: return "Timeout"
        else: return "Unknown Event"

    def __exit__(self, exc_type, exc_value, traceback) :
        self.stop()

class GPhotoUtils:

    def __init__(self):
        #callback_obj = gp.check_result(gp.use_python_logging())
        camera_list = list(gp.Camera.autodetect())
        if not camera_list:
            logging.warning('No GPHOTO2 camera detected')
            self.plugged = False
        self.plugged = True
        camera_list.sort(key=lambda x: x[0])
        for index, (name, addr) in enumerate(camera_list):
            logging.debug('{:d}:  {:s}  {:s}'.format(index, addr, name))
        self.camera_list = camera_list
        self.set_datetime()

    def set_datetime(self):
        for index, (name, addr) in enumerate(self.camera_list):
            camera = gp.Camera()
            port_info_list = gp.PortInfoList()
            port_info_list.load()
            idx = port_info_list.lookup_path(addr)
            camera.set_port_info(port_info_list[idx])
            camera.init()
            abilities = camera.get_abilities()
            config = camera.get_config()
            if self.gphoto_datetime(config, abilities.model, gp):
                camera.set_config(config)
                logging.debug("Synchronized datetime for : "+ '{:d}:  {:s}  {:s}'.format(index, addr, name) )
            else:
                logging.warning('Could not set date & time for '+ '{:d}:  {:s}  {:s}'.format(index, addr, name))
            camera.exit()

    def gphoto_datetime(self, config, model, gp):
        if model == 'Canon EOS 100D':
            OK, date_config = gp.gp_widget_get_child_by_name(config, 'datetimeutc')
            if OK >= gp.GP_OK:
                now = int(time.time())
                date_config.set_value(now)
                return True
        OK, sync_config = gp.gp_widget_get_child_by_name(config, 'syncdatetime')
        if OK >= gp.GP_OK:
            sync_config.set_value(1)
            return True
        OK, date_config = gp.gp_widget_get_child_by_name(config, 'datetime')
        if OK >= gp.GP_OK:
            widget_type = date_config.get_type()
            if widget_type == gp.GP_WIDGET_DATE:
                now = int(time.time())
                date_config.set_value(now)
            else:
                now = time.strftime('%Y-%m-%d %H:%M:%S')
                date_config.set_value(now)
            return True
        return False
            