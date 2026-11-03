import sys
import time

import face_recognition
import mediapipe as mp
import cv2
import dlib
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from threading import Thread
from mouth_function import *

import pyshine as ps


class MouthDetection(QDialog):
    def __init__(self):
        super(MouthDetection, self).__init__()
        loadUi('Mouth.ui', self)
        self.image = QLabel(self)
        self.image.setPixmap(QPixmap('logo (9).png'))
        self.image.move(750, 70)
        self.show()
        
        self.image = None
        self.img = None
        self.startButton.clicked.connect(self.start_webcam)
        self.stopButton.clicked.connect(self.stop_webcam)
        self.detectButton.setCheckable(True)
        self.detectButton.toggled.connect(self.detect_face)
        self.face_Enabled = False

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(max_num_faces=1)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=2, circle_radius=1)

        self.playButton.clicked.connect(self.startWorker)
        self.resetButton.clicked.connect(self.reset_score)

        self.fps = 0
        self.COUNTER_A = 0
        self.COUNTER_E = 0
        self.COUNTER_C = 0
        self.FRAMES = 1
        self.FRAMES_C = 2
        self.TOTAL_A = 0
        self.TOTAL_E = 0
        self.TOTAL_C = 0
        self.TIMER = 3
        self.ret_mouth_open = False
        self.ret_mouth_smile = False
        self.ret_left_cheek = False
        self.ret_right_cheek = False
        self.detect = False
        self.waktu_timer1 = 3
        self.prev1 = time.time()
        self.cur1 = time.time()
        self.waktu_timer2 = 3
        self.prev2 = time.time()
        self.cur2 = time.time()
        self.waktu_timer3 = 3
        self.prev3 = time.time()
        self.cur3 = time.time()
        self.waktu_timer4 = 3
        self.prev4= time.time()
        self.cur4 = time.time()

    def startWorker(self):
        if self.instruction1.isChecked():
            self.Worker1 = Worker1()
            self.Worker1.start()
            self.Worker1.videoUpdate.connect(self.VideoUpdateSlot)

        elif self.instruction2.isChecked():
            self.Worker2= Worker2()
            self.Worker2.start()
            self.Worker2.videoUpdate.connect(self.VideoUpdateSlot)

        elif self.instruction3.isChecked():
            self.Worker3 = Worker3()
            self.Worker3.start()
            self.Worker3.videoUpdate.connect(self.VideoUpdateSlot)

    def VideoUpdateSlot(self,img):
        self.vidLabel.setPixmap(QPixmap.fromImage(img))
        self.vidLabel.setScaledContents(True)
        key = cv2.waitKey(125)

    def detect_face(self, status):
        if status:
            self.detectButton.setText('Stop Detection')
            self.face_Enabled = True
        else:
            self.detectButton.setText('Start Detection')
            self.face_Enabled = False

    def start_webcam(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

    def detect_mouth(self, img):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.faceMesh.process(imgRGB)

        for faceLms in results.multi_face_landmarks:
            self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_LIPS,
                                       None, self.drawSpec)
        return img

    def start_rehab(self,img):
        self.img = img
        face_landmarks_list = face_recognition.face_landmarks(self.img)
        for face_landmarks in face_landmarks_list:
            self.ret_mouth_open = is_mouth_open(face_landmarks)
            self.ret_mouth_smile = check_horizontal(face_landmarks)
            self.ret_left_cheek = cheek_left_distance(face_landmarks)
            self.ret_right_cheek = cheek_right_distance(face_landmarks)

        if self.ret_mouth_open is True:
            self.img = self.detect_mouth(self.img)
            self.cur1 = time.time()
            self.img = ps.putBText(self.img, str(self.waktu_timer1), text_offset_x=25, text_offset_y=100, vspace=20,
                                   hspace=20, font_scale=5,
                                   background_RGB=(10, 20, 222), text_RGB=(255, 255, 255))

            self.displayImage(self.img)

            if self.cur1 - self.prev1 >= 1:
                self.prev1 = time.time()
                self.waktu_timer1 = self.waktu_timer1 - 1
            if self.waktu_timer1 == -1:
                self.waktu_timer1 = 3
                self.COUNTER_A += 1

            if self.COUNTER_A >= self.FRAMES:
                self.TOTAL_A += 1
                self.COUNTER_A = 0



        if self.ret_mouth_smile is True:
            self.img = self.detect_mouth(self.img)
            self.cur2 = time.time()
            self.img = ps.putBText(self.img, str(self.waktu_timer2), text_offset_x=25, text_offset_y=100, vspace=20,
                                   hspace=20, font_scale=5,
                                   background_RGB=(10, 20, 222), text_RGB=(255, 255, 255))

            self.displayImage(self.img)

            if self.cur2 - self.prev2 >= 1:
                self.prev2 = time.time()
                self.waktu_timer2 = self.waktu_timer2 - 1
            if self.waktu_timer2 == -1:
                self.waktu_timer2 = 3
                self.COUNTER_E += 1

            if self.COUNTER_E >= self.FRAMES:
                self.TOTAL_E += 1
                self.COUNTER_E = 0

        if self.ret_left_cheek is True:
            self.img = self.detect_mouth(self.img)
            self.cur4 = time.time()
            self.img = ps.putBText(self.img, str(self.waktu_timer4), text_offset_x=25, text_offset_y=100, vspace=20,
                                   hspace=20, font_scale=5,
                                   background_RGB=(10, 20, 222), text_RGB=(255, 255, 255))

            self.displayImage(self.img)

            if self.cur4 - self.prev4 >= 1:
                self.prev4 = time.time()
                self.waktu_timer4 = self.waktu_timer4 - 1
            if self.waktu_timer4 == -1:
                self.waktu_timer4 = 3
                self.COUNTER_C += 1

        #
        elif self.ret_right_cheek is True:
            self.img = self.detect_mouth(self.img)

            self.cur3 = time.time()

            self.img = ps.putBText(self.img, str(self.waktu_timer3), text_offset_x=25, text_offset_y=100, vspace=20,
                                   hspace=20, font_scale=5,
                                   background_RGB=(10, 20, 222), text_RGB=(255, 255, 255))

            self.displayImage(self.img)

            if self.cur3 - self.prev3 >= 1:
                self.prev3 = time.time()
                self.waktu_timer3 = self.waktu_timer3 - 1

            if self.waktu_timer3 == -1:
                self.waktu_timer3 = 3
                self.COUNTER_C += 1

        if self.COUNTER_C == self.FRAMES_C:
                self.TOTAL_C += 1
                self.COUNTER_C = 0

        return self.img


    def update_frame(self):
        ret, self.image = self.capture.read()
        image = cv2.flip(self.image, 1)

        if self.face_Enabled:
            detected_image = self.detect_mouth(image)
            self.displayImage(detected_image, 1)
            image = self.start_rehab(image)


        else:
            self.displayImage(self.image, 1)


        text = 'Score A : ' + str(self.TOTAL_A)
        img = ps.putBText(image, text, text_offset_x=25, text_offset_y=30, vspace=20, hspace=10, font_scale=0.80,
                          background_RGB=(10, 20, 222), text_RGB=(255, 255, 255))
        text = 'Score E : ' + str(self.TOTAL_E)
        img = ps.putBText(img, text, text_offset_x=image.shape[1] - 425, text_offset_y=30, vspace=20, hspace=10,
                          font_scale=0.80, background_RGB=(228, 20, 222), text_RGB=(255, 255, 255))

        text = 'Score Cheek : ' + str(self.TOTAL_C)
        img = ps.putBText(img, text, text_offset_x=image.shape[1] - 235, text_offset_y=30, vspace=20, hspace=10,
                          font_scale=0.80, background_RGB=(20, 210, 4), text_RGB=(255, 255, 255))
        self.displayImage(img)

    def stop_webcam(self):
        self.timer.stop()

    def reset_score(self):
        self.TOTAL_A = 0
        self.TOTAL_E = 0
        self.TOTAL_C = 0

    def displayImage(self, img, window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)

        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)

class Worker1(QThread):
    videoUpdate = pyqtSignal(QImage)

    def run(self):
        self.ThreadActive = True
        capture1 = cv2.VideoCapture("1.mov")
        while self.ThreadActive:
            ret, img = capture1.read()
            if ret:
                Image = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
                Image = Image.rgbSwapped()
                self.videoUpdate.emit(Image)

class Worker2(QThread):
    videoUpdate = pyqtSignal(QImage)

    def run(self):
        self.ThreadActive = True
        capture1 = cv2.VideoCapture("2.mov")
        while self.ThreadActive:
            ret, img = capture1.read()
            if ret:
                Image = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
                Image = Image.rgbSwapped()
                self.videoUpdate.emit(Image)

class Worker3(QThread):
    videoUpdate = pyqtSignal(QImage)

    def run(self):
        self.ThreadActive = True
        capture1 = cv2.VideoCapture("3.mp4")
        while self.ThreadActive:
            ret, img = capture1.read()
            if ret:
                Image = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
                Image = Image.rgbSwapped()
                self.videoUpdate.emit(Image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MouthDetection()
    window.setWindowTitle('ORAL UP')
    window.show()
    sys.exit(app.exec_())
