import os
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QMovie

scriptDir = os.path.dirname(os.path.realpath(__file__))
gifFile = (scriptDir + os.path.sep + 'egg.gif')


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Resize main window to be 600px / 400px
        self.resize(600, 400)
        self.MovieLabel = QLabel(self)
        # Set gif content to be same size as window (600px / 400px)
        self.MovieLabel.setGeometry(QtCore.QRect(0, 0, 600, 400))
        # self.movie = QMovie(gifFile)
        # self.MovieLabel.setMovie(self.movie)
        # self.movie.start()

        self.movie = QMovie('greet.gif', bytearray(), self)
        self.MovieLabel.setMovie(self.movie)
        self.movie.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())