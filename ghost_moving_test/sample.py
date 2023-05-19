from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.w_width = 500
        self.w_height = 500
        self.setGeometry(100, 100, self.w_width, self.w_height)

        #메서드 부르기
        self.UiComponets()

        self.show()

        self.speed = 5
        self.mass = 1
        self.jump = False

        #positon



    def UiComponets(self):

        self.label = QLabel(self)
        self.l_width = 40
        self.l_height = 40



        self.label.setGeometry(self.positon[0], self.positon[1], self.l_width, self.l_height)

        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "border: 4px solid darkgreen;"
                                 "background: lightgreen;"
                                 "}")
        timer = QTimer(self)
        timer.start(50)
        timer.timeout.connect(self.show_time)

    def show_time(self):

        if self.jump:
            y = self.label.y()

            #힘 = 1/2 * 질량 * 속도 ** 2
            #1/2는 사용하지 않음
            Force = self.mass * (self.speed ** 2)

            #y 위치 변경
            y -= Force

            # 올라갈수록 속도를 줄인다
            self.label.move(200, y)
            self.speed = self.speed - 1

            #개체의 최고 높이 설정
            if self.speed < 0:
                self.mass = -1

            if self.speed == -6:
                self.jump = False

                self.speed = 5
                self.mass = 1
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.jump = True
        if event.key() == Qt.Key_Right:
            self.positon = self.label.x() + 20, self.label.y()
            self.label.move(self.label.x() + 20, self.label.y())
        if event.key() == Qt.Key_Left:
            self.positon = self.label.x() - 20, self.label.y()
            self.label.move(self.label.x() - 20, self.label.y())


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec())


