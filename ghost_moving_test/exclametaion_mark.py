import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 600, 400)


        self.character_img_right = QPixmap('character_right.png')
        self.character_img_left = QPixmap('character_left.png')
        self.mark_img = QPixmap('mark.png')

        #캐릭터 담을 라벨 만들어주기
        self.character = QLabel(self)
        self.character.setFixedSize(80, 120)
        # self.character.setStyleSheet('background-color: yellow')
        self.character.setPixmap(self.character_img_right.scaled(QSize(30, 50), aspectRatioMode=Qt.IgnoreAspectRatio))
        self.character.move(10, 30)
        self.character.show()


        #느낌표 담을 라벨 만들어주기
        self.mark_label = QLabel(self)
        self.mark_label.setPixmap(self.mark_img.scaled(QSize(50, 50), aspectRatioMode=Qt.IgnoreAspectRatio))

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


        # 유령 담길 라벨 만들어주기
        self.ghost_label = QLabel(self)
        self.ghost_label.setPixmap(self.ghost_img_right.scaled(QSize(self.ghost_fixed_size, self.ghost_fixed_size),
                                                               aspectRatioMode=Qt.IgnoreAspectRatio))
        self.ghost_label.move(random.randint(0, self.width()), random.randint(0, self.height()))
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

        # self.mark_label.show()

    def keyPressEvent(self, event):
        self.x_positon = self.character.pos().x()
        self.y_position = self.character.pos().y()

        label_x_positon = self.ghost_label.pos().x()
        label_y_positoin = self.ghost_label.pos().y()

        self.mark_label.move(self.x_positon+10, self.y_position)

        if event.key() == Qt.Key_Right:
            self.character.setPixmap(self.character_img_right.scaled(QSize(30, 50), aspectRatioMode=Qt.IgnoreAspectRatio))
            self.character.move(self.x_positon + 20, self.y_position)
        if event.key() == Qt.Key_Left:
            self.character.setPixmap(self.character_img_left.scaled(QSize(30, 50), aspectRatioMode=Qt.IgnoreAspectRatio))
            self.character.move(self.x_positon - 20, self.y_position)
        if event.key() == Qt.Key_Up:
            self.character.move(self.x_positon, self.y_position - 20)
        if event.key() == Qt.Key_Down:
            self.character.move(self.x_positon, self.y_position + 20)

        if label_x_positon - 50 < self.x_positon < label_x_positon + 50 and label_y_positoin - 50 < self.y_position < label_y_positoin + 50:
            reply = QMessageBox()
            reply.setIconPixmap(QPixmap('음미탐미.jpg'))
            reply.setText("만났습니다!")
            reply.exec_()

    def direction(self):
        """유령 방향 랜덤값 반환"""
        random_num = random.randint(1, 8)
        self.random_num = random_num

    def move_label(self):
        """유령 움직임 조정 함수"""
        current_pos = self.ghost_label.pos()

        # x, y 값 고정
        x_start = 0  # 시작 x 값
        x_end = self.width() - self.ghost_label.width()  # 끝 x 값
        y_start = 0  # 시작 y 값
        y_end = self.height() - self.ghost_label.height()  # 끝 y 값

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
            self.ghost_label.setPixmap(
                self.ghost_img_left.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
            new_x = max(current_pos.x() - 1, x_start)
            new_y = current_pos.y()
        elif self.random_num == 6:  # 오른쪽
            self.ghost_label.setPixmap(
                self.ghost_img_right.scaled(QSize(100, 100), aspectRatioMode=Qt.IgnoreAspectRatio))
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

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
