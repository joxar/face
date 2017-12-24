from BaseHTTPServer import BaseHTTPRequestHandler
import cv2
import voice
import subprocess
import random

# open camera device
camera = cv2.VideoCapture(0)

# on Mac OS
#CASCADE_DIR = "/usr/local/share/OpenCV/haarcascades/"
# on raspberryPi
CASCADE_DIR = "/usr/share/opencv/haarcascades/"

CASCADE_FILE = CASCADE_DIR + "haarcascade_frontalface_alt.xml"
# don't recognize too small face
MIN_SIZE = (150, 150)
# generate recognizer
cascade = cv2.CascadeClassifier(CASCADE_FILE)

# mp3 directory
MP3_DIR = "mp3"
# chat interval
GAP = 50
# for getting interval of chat
count = 100
prev_count = 0
# html file
HTML_FILE = "live.html"

# get mp3 resource list
def res_cmd_lfeed(cmd):
  return subprocess.Popen(
      cmd, stdout=subprocess.PIPE,
      shell=True).stdout.readlines()
def res_cmd_no_lfeed(cmd):
  return [str(x).rstrip("\n") for x in res_cmd_lfeed(cmd)]

lsResultList = res_cmd_no_lfeed("ls -1 " + MP3_DIR)

# define web server handler
class liveHTTPServer_Handler(BaseHTTPRequestHandler):
    # when access come
    def do_GET(self):

        global count
        global prev_count
        global lsResultList
        count += 1

        print("path=", self.path)
        # send pict.
        if self.path[0:7] == "/camera":
            # headers
            self.send_response(200)
            self.send_header('Content-Type', 'image/jpeg')
            self.end_headers()
            # send frame
            _, frame = camera.read()

            # recognize faces
            ###################
            img = cv2.resize(frame, (600, 400))
            # transform gray scale
            igray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # face recognize
            faces = cascade.detectMultiScale(igray, minSize=MIN_SIZE)
            if len(faces) == 0:
                a = 0
            # mark on the area recognized
            if len(faces) and count-prev_count > GAP:
                voice.voiceFunc(random.choice(lsResultList))
                prev_count = count
            for (x, y, w, h) in faces:
                color = (255, 0, 0)
                cv2.rectangle(img, (x,y), (x+w, y+h), color, thickness=2)

            # encode to JPEG
            param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
            _, encimg = cv2.imencode('.jpg', img, param)
            self.wfile.write(bytearray(encimg))
        # send HTML
        elif self.path == "/":
            # headers
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            # output HTML
            try:
                f = open('live.html', 'r')
                s = f.read()
            except:
                s = "file not found"
            self.wfile.write(s.encode('utf-8'))
        else:
            self.send_response(404)
            self.wfile.write("file not found".encode('utf-8'))
try:
    # start web server
    addr = ('', 8081)
    from BaseHTTPServer import HTTPServer
    httpd = HTTPServer(addr, liveHTTPServer_Handler)
    print('server started...', addr)
    httpd.serve_forever()

except KeyboardInterrupt:
    httpd.socket.close()
