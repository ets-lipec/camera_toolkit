#https://raw.githubusercontent.com/miguelgrinberg/flask-video-streaming/master/base_camera.py
from importlib import import_module
import PIL
import os
from flask import Flask, render_template, Response
import cv2
import getpass

# uncomment below to use Raspberry Pi camera instead
# from camera_pi import Camera

# comment this out if you're not using USB webcam
from camera_opencv import Camera

app = Flask(__name__)

path= '/Users/stephanehu/Repositories/camera_experiments/image.jpg'
@app.route('/')
def index():
    return("API is up and running, images are being served at /image.jpg")

def gen2(camera):
    """Returns a single image frame"""
    frame = camera.get_frame()
    yield frame

@app.route('/image.jpg')
def image():
    """Returns a single current image for the webcam"""
    frame = gen2( Camera() )
    resp = Response( frame , mimetype='image/jpeg' )
    open('frame.jpg', 'wb').write(resp.data)
    return resp
    
    #cv2.imwrite(os.path.join(path , 'image1.jpg'), imfile)
    return imfile

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)