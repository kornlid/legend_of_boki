import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.move(200, 200)
        self.setFixedSize(700, 800)
        self.setStyleSheet("background-color:black")

        # Create a label
        # 이미지 불러오기
        self.ghost_img_top = QPixmap('./ghost_img/ghost_top.png')  # 귀신 이미지 상
        self.ghost_img_right = QPixmap('./ghost_img/ghost_right.png')  # 우
        self.ghost_img_left = QPixmap('./ghost_img/ghost_left.png')  # 좌
        self.ghost_img_bottom = QPixmap('./ghost_img/ghost_bottom.png')  # 하
        self.ghost_img_right_top = QPixmap('./ghost_img/ghost_right_top.png')  # 우상
        self.ghost_img_left_top = QPixmap('./ghost_img/ghost_left_top.png')  # 좌상
        self.ghost_img_left_bottom = QPixmap('./ghost_img/ghost_left_bottom.png')  # 좌하
        self.ghost_img_right_bottom = QPixmap('./ghost_img/ghost_right_bottom.png')  # 좌하

        self.label = QLabel(self)
        self.label.setPixmap(self.ghost_img_right.scaled(QSize(200, 200), aspectRatioMode=Qt.IgnoreAspectRatio))
        self.label.setGeometry(300, 300, 300, 300)

        self.character = QLabel(self)
        self.character.setStyleSheet('background-color: yellow')
        self.character.setFixedSize(30, 50)
        self.character.show()

        self.random_num = None
        # 방향 타이머
        self.position = QTimer()
        self.position.setInterval(3000)
        self.position.timeout.connect(self.direction)
        self.position.start()

        # 유령 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_label)
        self.timer.start(40)  # Move the label every 100 milliseconds

    def direction(self):
        random_num = random.randint(1, 8)
        self.random_num = random_num

    def move_label(self):
        # Get the current position of the label
        current_pos = self.label.pos()
        if not self.current_pos.x()

        # Calculate the new position
        if self.random_num == 1:  # 우하
            self.label.setPixmap(
                self.ghost_img_right_bottom.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = current_pos.x() + 1  # 오른쪽으로 1 움직이게 하기
            new_y = current_pos.y() + 1  # 아래로 1 움직이게 하기
        elif self.random_num == 2:  # 우상
            self.label.setPixmap(
                self.ghost_img_right_top.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = current_pos.x() + 1  # 오른쪽으로 1 움직이게 하기
            new_y = current_pos.y() - 1  # 위로 1 움직이게 하기
        elif self.random_num == 3:  # 좌상
            self.label.setPixmap(
                self.ghost_img_left_top.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = current_pos.x() - 1  # 오른쪽으로 1 움직이게 하기
            new_y = current_pos.y() - 1  # 아래로 1 움직이게 하기
        elif self.random_num == 4:  # 좌상
            self.label.setPixmap(
                self.ghost_img_left_bottom.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = current_pos.x() - 1  # 오른쪽으로 1 움직이게 하기
            new_y = current_pos.y() + 1  # 아래로 1 움직이게 하기
        elif self.random_num == 5:  # 왼쪽
            self.label.setPixmap(
                self.ghost_img_left.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = current_pos.x() - 1  # 왼쪽으로만 움직이게 하기
            new_y = current_pos.y()
        elif self.random_num == 6:
            self.label.setPixmap(
                self.ghost_img_right.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = current_pos.x() + 1  # 오른쪽으로만 움직이게 하기
            new_y = current_pos.y()
        elif self.random_num == 7:
            self.label.setPixmap(
                self.ghost_img_top.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = current_pos.x()
            new_y = current_pos.y() - 1
        else:
            self.label.setPixmap(
                self.ghost_img_bottom.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = current_pos.x()
            new_y = current_pos.y() + 1
        # Set the new position of the label
        self.label.move(new_x, new_y)

    def keyPressEvent(self, event):
        x_positon = self.character.pos().x()
        y_position = self.character.pos().y()

        label_x_positon = self.label.pos().x()
        label_y_positoin = self.label.pos().y()

        if event.key() == Qt.Key_Right:
            self.character.move(x_positon + 20, y_position)
        if event.key() == Qt.Key_Left:
            self.character.move(x_positon - 20, y_position)
        if event.key() == Qt.Key_Up:
            self.character.move(x_positon, y_position - 20)
        if event.key() == Qt.Key_Down:
            self.character.move(x_positon, y_position + 20)
        # if self.character.geometry().intersects(self.label.geometry()):
        #     reply = QMessageBox()
        #     reply.setText("만났습니다!")
        #     reply.exec_()
        # # 충돌을 구현을 해야 한다.. -> 객체와 객체
        # if label_x_positon
        if label_x_positon - 70 < x_positon < label_x_positon + 70 and label_y_positoin - 70 < y_position < label_y_positoin + 70:
            reply = QMessageBox()
            reply.setText("만났습니다!")
            reply.exec_()


# Create an instance of QApplication and your MainWindow class:
app = QApplication([])
window = MainWindow()
window.show()
app.exec()
