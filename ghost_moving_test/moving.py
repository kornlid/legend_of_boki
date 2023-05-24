import sys
import random
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.speed = 5

    def move(self, direction):
        if direction == 'W':
            self.y -= self.speed
        elif direction == 'A':
            self.x -= self.speed
        elif direction == 'S':
            self.y += self.speed
        elif direction == 'D':
            self.x += self.speed

    def draw(self, painter):
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)


class Obstacle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.speed = 3

    def move(self):
        self.x -= self.speed

    def draw(self, painter):
        painter.setBrush(QColor(0, 0, 255))
        painter.drawRect(self.x, self.y, self.size, self.size)


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("피하기 게임")
        self.setGeometry(100, 100, 600, 400)

        self.player = Player(50, 200, 20)
        self.obstacles = []
        self.lives = 3
        self.score = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateGame)
        self.timer.start(20)  # 20 milliseconds

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_W:
            self.player.move('W')
        elif key == Qt.Key_A:
            self.player.move('A')
        elif key == Qt.Key_S:
            self.player.move('S')
        elif key == Qt.Key_D:
            self.player.move('D')

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw player
        self.player.draw(painter)

        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(painter)

    def updateGame(self):
        # 플레이어 움직이게 하기
        self.update()

        # 장애물 움직이게 하기
        for obstacle in self.obstacles:
            obstacle.move()

            # 겹치는지 확인
            if self.checkCollision(obstacle, self.player):
                self.lives -= 1
                self.obstacles.remove(obstacle)
                if self.lives == 0:
                    self.timer.stop()
                    self.showGameOverDialog()

        # 장애물 랜덤으로 생성
        if random.random() < 0.05:
            y = random.randint(0, self.height() - 20)
            obstacle = Obstacle(self.width(), y, 20)
            self.obstacles.append(obstacle)

    def checkCollision(self, a, b):
        """겹치면 True값 반환하는 함수"""
        if (abs(a.x - b.x) < a.size and abs(a.y - b.y) < a.size) or \
                (abs(a.x - b.x) < b.size and abs(a.y - b.y) < b.size):
            return True
        return False

    def showGameOverDialog(self):
        """게임 오버되면 메세지 출력"""
        message = f"Game Over!\nScore: {self.score}"
        QMessageBox.information(self, "Game Over", message, QMessageBox.Ok)
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = GameWindow()
    game.show()
    sys.exit(app.exec_())
