#GUI module
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt

#YOLO module
from ultralytics import YOLO
from collections import Counter

#OpenCV module
import cv2
import supervision as sv

#DB module
from trfdb import insertdb

#Arduino Communication module
from arduino_communication import to_Arduino

#etc
import datetime
import time
import threading
import sys

#UI load
form_class = uic.loadUiType("main.ui")[0]

running = False

#Main Window
class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        now = QDate.currentDate()
        current_date = now.toString('yyyy MMMM dd')
        current_time = datetime.datetime.now().strftime("%I:%M %p")

        self.date_lb.setText(current_date)
        self.time_lb.setText(current_time)
        self.start_btn.clicked.connect(self.start_btn_clicked)
        self.stop_btn.clicked.connect(self.stop_btn_clicked)

    def start_btn_clicked(self):
        QMessageBox.about(self, "message", "Start Detecting...")
        global running
        running = True

        #threading
        th = threading.Thread(target=self.run)
        th.start()
        print("started..")

    def stop_btn_clicked(self):
        QMessageBox.about(self, "message", "Stop Detecting...")
        global running
        running = False
        print("stoped..")


    def run(self):
        global running

        #Assign Camera Adress
        camera_id = "/dev/video0"

        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

        #screen size setting
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_lb.resize(width, height)

        #YOLO model load
        model = YOLO("trained.pt")

        #annotation box setting
        box_annotator = sv.BoxAnnotator(
            thickness=2,
            text_thickness=2,
            text_scale=1
        )

        labels_buffer = []  # label buffer
        start_time = time.time()  

        #start detecting
        while running:
            ret, frame = self.cap.read() #read frame from camera
            result = model(frame, agnostic_nms=True)[0]
            detections = sv.Detections.from_ultralytics(result) #detection result

            #set label information
            labels = [
                f"{model.model.names[class_id]} {confidence:0.2f}"
                for _, _, confidence, class_id, _ in detections
            ]

            labels_buffer.extend(labels)  # label add to buffer
            elapsed_time = time.time() - start_time

            if labels:
                if elapsed_time >= 1.0: # unless 1 seconds, do not insert to DB
                    if labels_buffer:
                        counter = Counter(labels_buffer) # count labels
                        most_common_label = counter.most_common(1)[0][0] # select representative class
                        split_labels = most_common_label.split()

                        print(f"Detector : {split_labels}")

                        insertdb(split_labels) # insert to DB
                        to_Arduino(split_labels) # send to Arduino

                        #set label information for GUI
                        self.classid_lb.setText(split_labels[0])
                        self.confidence_lb.setText(split_labels[1])

                        labels_buffer.clear()  # refresh buffer
                        start_time = time.time()  # refresh time
            else:
                print(labels)

            #show video
            frame = box_annotator.annotate(
                scene=frame, 
                detections=detections, 
                labels=labels
            )

            if ret: #if frame read success
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert color
                h,w,c = frame.shape #get frame size
                qImg = QtGui.QImage(frame.data, w, h, w*c, QtGui.QImage.Format_RGB888) #convert to QImage
                pixmap = QtGui.QPixmap.fromImage(qImg) #convert to QPixmap
                self.video_lb.setPixmap(pixmap) #set video
                self.video_lb.setScaledContents(True) #show video with original size
            else:
                QMessageBox.about(self, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break
            
            cv2.waitKey(1) #wait 1ms
        self.cap.release() #release camera
        print("Thread end.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()