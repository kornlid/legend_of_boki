from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QMovie
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QLabel, QWidget

app = QApplication([])
window = QWidget()

# 영상 파일 경로 지정
file_path = "boki_prologue.wmv"

# MediaPlayer 생성 후 영상 재생
media_player = QMediaPlayer()
media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
media_player.play()

# 영상 크기에 맞게 라벨 크기 조절
label = QLabel(window)
movie = QMovie(file_path)
label.setMovie(movie)
movie.start()
label.resize(movie.frameRect().size())

# 화면 종료
media_player.stateChanged.connect(lambda state: window.close())
window.show()
app.exec_()
