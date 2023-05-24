import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.move(200, 200)
        self.setGeometry(200, 200, 300, 300)
        self.setStyleSheet("background-color:black")

        # Create a label
        # 유령 이미지 불러오기
        self.ghost_img_top = QPixmap('./ghost_img/ghost_top.png')  # 귀신 이미지 상
        self.ghost_img_right = QPixmap('./ghost_img/ghost_right.png')  # 우
        self.ghost_img_left = QPixmap('./ghost_img/ghost_left.png')  # 좌
        self.ghost_img_bottom = QPixmap('./ghost_img/ghost_bottom.png')  # 하
        self.ghost_img_right_top = QPixmap('./ghost_img/ghost_right_top.png')  # 우상
        self.ghost_img_left_top = QPixmap('./ghost_img/ghost_left_top.png')  # 좌상
        self.ghost_img_left_bottom = QPixmap('./ghost_img/ghost_left_bottom.png')  # 좌하
        self.ghost_img_right_bottom = QPixmap('./ghost_img/ghost_right_bottom.png')  # 좌하

        # 유령 크기 고정해주기
        self.ghost_fixed_size = 100

        #캐릭터 만들어주기
        self.character = QLabel(self)
        self.character.setStyleSheet('border: 4px solid yellow')
        self.character.setFixedSize(300, 300)
        self.character.move(0, 0)
        self.character.show()

        # 유령 담길 라벨 만들어주기
        self.ghost_label = QLabel(self)
        self.ghost_label.setPixmap(self.ghost_img_right.scaled(QSize(self.ghost_fixed_size, self.ghost_fixed_size), aspectRatioMode=Qt.IgnoreAspectRatio))
        self.ghost_label.move(10, 10)
        self.ghost_label.setFixedSize(100, 100)

        self.random_num = 1

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
        """유령 방향 랜덤값 반환"""
        random_num = random.randint(1, 8)
        self.random_num = random_num


    def checkCollision(self, obj1, obj2):
        """라벨끼리 겹치면 true반환"""
        x1, y1, w1, h1 = abs(obj1.x()), abs(obj1.y()), abs(obj1.width()), abs(obj1.height())
        x2, y2, w2, h2 = abs(obj2.x()), abs(obj2.y()), abs(obj2.width()), abs(obj2.height())
        if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
            return True
        return False

    def check_ghost_moving(self):
        if self.checkCollision(self.ghost_label, self.character):
            reply = QMessageBox()
            reply.setText("만났습니다.")
            reply.exec_()
    def move_label(self):
        """유령 움직임 조정 함수"""


        # Get the current position of the label
        current_pos = self.ghost_label.pos()

        # Define the range of x and y positions
        x_start = 0  # 시작 x 값
        x_end = 300  # self.width() - self.label.width()  # 끝 x 값
        y_start = 0  # 시작 y 값
        y_end = 300  # self.height() - self.label.height()  # 끝 y 값

        # Calculate the new position
        if self.random_num == 1:  # 우하
            self.ghost_label.setPixmap(
                self.ghost_img_right_bottom.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = min(current_pos.x() + 1, x_end)
            new_y = min(current_pos.y() + 1, y_end)
        elif self.random_num == 2:  # 우상
            self.ghost_label.setPixmap(
                self.ghost_img_right_top.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = min(current_pos.x() + 1, x_end)
            new_y = max(current_pos.y() - 1, y_start)
        elif self.random_num == 3:  # 좌상
            self.ghost_label.setPixmap(
                self.ghost_img_left_top.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = max(current_pos.x() - 1, x_start)
            new_y = max(current_pos.y() - 1, y_start)
        elif self.random_num == 4:  # 좌하
            self.ghost_label.setPixmap(
                self.ghost_img_left_bottom.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = max(current_pos.x() - 1, x_start)
            new_y = min(current_pos.y() + 1, y_end)
        elif self.random_num == 5:  # 왼쪽
            self.ghost_label.setPixmap(self.ghost_img_left.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = max(current_pos.x() - 1, x_start)
            new_y = current_pos.y()
        elif self.random_num == 6:  # 오른쪽
            self.ghost_label.setPixmap(self.ghost_img_right.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = min(current_pos.x() + 1, x_end)
            new_y = current_pos.y()
        elif self.random_num == 7:  # 상
            self.ghost_label.setPixmap(self.ghost_img_top.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = current_pos.x()
            new_y = max(current_pos.y() - 1, y_start)
        else:  # 하
            self.ghost_label.setPixmap(
                self.ghost_img_bottom.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = current_pos.x()
            new_y = min(current_pos.y() + 1, y_end)

        # Set the new position of the label
        self.ghost_label.move(new_x, new_y)

    def keyPressEvent(self, event):
        x_positon = self.character.pos().x()
        y_position = self.character.pos().y()

        label_x_positon = self.ghost_label.pos().x()
        label_y_positoin = self.ghost_label.pos().y()

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
        # if label_x_positon - 70 < x_positon < label_x_positon + 70 and label_y_positoin - 70 < y_position < label_y_positoin + 70:
        #     reply = QMessageBox()
        #     reply.setText("만났습니다!")
        #     reply.exec_()

        self.check_ghost_moving()



# Create an instance of QApplication and your MainWindow class:
app = QApplication([])
window = MainWindow()
window.show()
app.exec()
