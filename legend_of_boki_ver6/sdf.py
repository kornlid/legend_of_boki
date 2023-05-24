import sys

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class WindowClass(QWidget):
    def __init__(self):
        super().__init__()
        self.initui()
    def initui(self):
        self.a = QWidget(self)
        self.a.resize(500, 500)
        self.label = QLabel("라벨", self)
        self.label.setGeometry(200,200,100,100)
        self.label.setPixmap(QPixmap("./MonsterImage/fire_1.png"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
