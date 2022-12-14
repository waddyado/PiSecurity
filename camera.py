import cv2
import numpy as np
import os
from twilio.rest import Client

class VideoCamera(object):
    video = cv2.VideoCapture(0)
    def __init__(self, source = 0):
        
        self.num = 0
        self.text = False
        self.out = cv2.VideoWriter(
        'detected.avi',
        cv2.VideoWriter_fourcc(*'MJPG'),
        15.,
        (640,480))
    def __del__(self):
        video.release()        
    
    def text_alert():
        account_sid = 'account SID'
        auth_token = 'account token'
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                body='Person Detected on camera',
                
                from_='twilionumber',
                to='your number'
            )
            
    def get_frame(self):
        
        ret, frame = VideoCamera.video.read()
        
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_detect = face_cascade.detectMultiScale(imgGray, 1.3, 5)
        boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
        # Here is where we can put things like overlays or cropping
        frame = frame[:, :, :]
        
            
        for (x, y, w, h) in face_detect:
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
            cv2.putText(img, 'face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            self.out.write(frame.astype('uint8'))

        for (xA, yA, xB, yB) in boxes:
            img2 = cv2.rectangle(frame, (xA, yA), (xB, yB),
                              (0, 255, 0), 2)
            cv2.putText(img2, 'person', (xA, yA-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            self.num += 1
            
            filename = 'static/image' + str(self.num) + '.jpg'
            cv2.imwrite(filename, frame)
            print('Person Detected')
            if self.num % 2 == 1:
                if self.text == True:
                    VideoCamera.text_alert()
            
            
            
        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()


