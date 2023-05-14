import os
import random
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic, Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
# 더 추가할 필요가 있다면 추가하시면 됩니다. 예: (from PyQt5.QtGui import QIcon)

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('maingame.ui')
form_class = uic.loadUiType(form)[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        # self.exitAction.triggered.connect(qApp.closeAllWindows) # 게임 종료 이벤트
        # TODO 캐릭터 움직일 때 마다 x, y 좌표 반영하기
        ## 임시 캐릭터 설정]
        self.character_left_img = QPixmap('character_left.png')
        self.character_right_img = QPixmap('character_right.png')
        self.back_ground_label.setPixmap(QtGui.QPixmap("용암.png"))
        self.widget.move(826,-1)
        self.back_ground_label.move(0,-1)
        self.Status1_1_Class.setText("close")

    #캐릭터 방향키로 움직이기===============================================================================================
    def keyPressEvent(self, event):
        rand_event = random.randrange(4)
        if event.key() == Qt.Key_A and self.label.x() > 0:
            self.label.setPixmap(self.character_left_img)
            self.label.move(self.label.x() - 20, self.label.y())
        elif event.key() == Qt.Key_D and self.label.x() < 1580:
            self.label.setPixmap(self.character_right_img)
            self.label.move(self.label.x() + 20, self.label.y())
        elif event.key() == Qt.Key_W and self.label.y() > 0:
            self.label.move(self.label.x(), self.label.y() - 20)
        elif event.key() == Qt.Key_S and self.label.y() < 760:
            self.label.move(self.label.x(), self.label.y() + 20)
        lab_x_ = self.label.pos().x()
        lab_y_ = self.label.pos().y()
        if rand_event == 1 and self.label.x() > 0 and self.label.x() < 1580 and self.label.y() > 0 and self.label.y() < 760:
            self.Log_textEdit.append("1칸 이동하였습니다.")
        elif rand_event == 2 and self.label.x() > 0 and self.label.x() < 1580 and self.label.y() > 0 and self.label.y() < 760:
            enemy_rand = random.randrange(4)
            if enemy_rand >= 3:
                self.Log_textEdit.append("적을 만났습니다.")
            elif enemy_rand == 4:
                self.Log_textEdit.append("타 수호대를 만났습니다.")
        elif rand_event == 3 and self.label.x() > 0 and self.label.x() < 1580 and self.label.y() > 0 and self.label.y() < 760:
            self.Log_textEdit.append("아이템을 획득하였습니다.")
        self.TopUI_Coordinate_Label.setText(f"x좌표: {lab_x_} y좌표: {lab_y_}")

# ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    # 게임 종료 이벤트
    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'EXIT', '정말 게임을 종료하시겠습니까?',
    #                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()
# └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
        # 여기에 시그널, 설정
    #여기에 함수 설정

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass( )
    myWindow.show( )
    app.exec_( )