from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class BlinkingLabel(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 400)

        self.character_img_right = QPixmap('character_right.png')
        self.character_img_left = QPixmap('character_left.png')

        self.label = QLabel(self)
        self.label.setFixedSize(100, 150)
        self.label.move(0, 0)
        # self.label.setGeometry(50, 50, 30, 50)
        self.label.setPixmap(self.character_img_right)
        self.label.setStyleSheet("background-color: transparent")
        self.label.show()

        self.button = QPushButton('Start Blinking', self)
        self.button.clicked.connect(self.start_blinking)

        self.label_ = QLabel(self)
        self.label_.setFixedSize(300, 300)


        layout = QVBoxLayout()
        layout.addWidget(self.label_)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.toggle_background)

    def start_blinking(self):
        """버튼을 누르면 비활성화 및 깜빡임 함수호출, 2초뒤에 멈추게"""
        self.button.setEnabled(False)
        self.timer.start(500)  # 0.5초마다 toggle_background() 호출
        QTimer.singleShot(2000, self.stop_blinking)  # 2초 후에 stop_blinking() 호출

    def toggle_background(self):
        if self.label.palette().color(self.label.backgroundRole()) == QColor("transparent"):
            self.label.setStyleSheet("background-color: red")
        else:
            self.label.setStyleSheet("background-color: transparent")

    def stop_blinking(self):
        self.timer.stop()
        self.label.setStyleSheet("background-color: transparent")
        self.button.setEnabled(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.label.setPixmap(self.character_img_left)
            self.label.move(self.label.x() - 20, self.label.y())
        if event.key() == Qt.Key_D:
            self.label.setPixmap(self.character_img_right)
            self.label.move(self.label.x() + 20, self.label.y())
        else:
            return

if __name__ == '__main__':
    app = QApplication([])
    window = BlinkingLabel()
    window.show()
    app.exec()
