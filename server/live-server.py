from BaseHTTPServer import BaseHTTPRequestHandler
import cv2

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

# define web server handler
class liveHTTPServer_Handler(BaseHTTPRequestHandler):
    # when access come
    def do_GET(self):
        print("path=", self.path)
        # send pict.
        if self.path[0:7] == "/camera":
            # headers
            self.send_response(200)
            self.send_header('Content-Type', 'image/jpeg')
            self.end_headers()
            # send frame
            _, frame = camera.read()

            #
            # recognize faces
            #
            img = cv2.resize(frame, (600, 400))
            # transform gray scale
            igray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # face recognize
            faces = cascade.detectMultiScale(igray, minSize=MIN_SIZE)
            if len(faces) == 0:
                a = 0
            # mark on the area recognized
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
                f = open('live2.html', 'r')
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
