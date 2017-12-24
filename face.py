import cv2
from datetime import datetime
from time import sleep
import voice

# file for recognizing face
# on Mac OS
#CASCADE_DIR = "/usr/local/share/OpenCV/haarcascades/"
# on raspberryPi
CASCADE_DIR = "/usr/share/opencv/haarcascades/"

CASCADE_FILE = CASCADE_DIR + "haarcascade_frontalface_alt.xml"
OUTPUT_DIR = "output"

# don't recognize too small face
MIN_SIZE = (150, 150)

# generate recognizer
cascade = cv2.CascadeClassifier(CASCADE_FILE)

# open camera
camera = cv2.VideoCapture(0)

# judge pict.
try:
    while True:
        # input pict. from camera
        _, img = camera.read()
        # transform gray scale
        igray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # face recognize
        faces = cascade.detectMultiScale(igray, minSize=MIN_SIZE)
        if len(faces) == 0:
            continue # no faces
        # mark on the area recognized
        for (x, y, w, h) in faces:
            voice.voiceFunc("Hello")
            color = (255, 0, 0)
            cv2.rectangle(img, (x,y), (x+w, y+h), color, thickness=8)
        # save image
        s = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        fname = OUTPUT_DIR + "/" + "face" + s + ".jpg"
        cv2.imwrite(fname, img)
        print("recognize!")
        sleep(3)

except KeyboardInterrupt:
    print("ok.")
