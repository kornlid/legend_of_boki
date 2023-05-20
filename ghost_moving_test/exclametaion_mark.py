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


        self.character = QLabel(self)
        self.character.setFixedSize(80, 120)
        self.character.setStyleSheet('background-color: yellow')
        self.character.setPixmap(self.character_img_right)
        self.character.move(10, 30)
        self.character.show()

        self.mark_label = QLabel(self)
        self.mark_label.setPixmap(self.mark_img.scaled(QSize(50, 50), aspectRatioMode=Qt.IgnoreAspectRatio))

        # self.mark_label.show()

    def keyPressEvent(self, event):
        self.x_positon = self.character.pos().x()
        self.y_position = self.character.pos().y()

        self.mark_label.move(self.x_positon+10, self.y_position)

        if event.key() == Qt.Key_Right:
            self.character.setPixmap(self.character_img_right)
            self.character.move(self.x_positon + 20, self.y_position)
        if event.key() == Qt.Key_Left:
            self.character.setPixmap(self.character_img_left)
            self.character.move(self.x_positon - 20, self.y_position)
        if event.key() == Qt.Key_Up:
            self.character.move(self.x_positon, self.y_position - 20)
        if event.key() == Qt.Key_Down:
            self.character.move(self.x_positon, self.y_position + 20)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
