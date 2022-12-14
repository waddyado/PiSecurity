from flask import Flask, render_template, Response, jsonify, request, send_file
from camera import VideoCamera
import cv2
import requests
import json
import numpy as np
from flask import send_from_directory
import os


app = Flask(__name__, static_url_path='/static')

video_stream1 = VideoCamera()
#video_stream2 = VideoCamera("http://192.168.68.102:8080/video")



@app.route('/')
def index():
    #return render_template('index.html')
    return render_template('demo.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
        
@app.route('/video_feed')
def video_feed():
     return Response(gen(video_stream1),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/download')
def downloadFile():
    path = "static/image1.jpg"
    return send_file(path, as_attachment=True)


@app.route('/light')
def triggerlight():
    os.system('python light.py')
    #return render_template('index.html')
    return render_template('demo.html')


@app.route('/nolight')
def deactivatelight():
    os.system('python deactivatelight.py')
    return render_template('demo.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,port="5001")


