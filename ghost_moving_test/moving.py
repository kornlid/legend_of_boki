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
        self.speed = 10

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

        self.setWindowTitle("Avoidance Game")
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
        # Move player
        self.update()

        # Move obstacles
        for obstacle in self.obstacles:
            obstacle.move()

            # Check collision with player
            if self.checkCollision(obstacle, self.player):
                self.lives -= 1
                self.obstacles.remove(obstacle)
                if self.lives == 0:
                    self.timer.stop()
                    self.showGameOverDialog()

        # Generate new obstacle randomly
        if random.random() < 0.05:
            y = random.randint(0, self.height() - 20)
            obstacle = Obstacle(self.width(), y, 20)
            self.obstacles.append(obstacle)

    def checkCollision(self, obj1, obj2):
        if (abs(obj1.x - obj2.x) < obj1.size and abs(obj1.y - obj2.y) < obj1.size) or \
                (abs(obj1.x - obj2.x) < obj2.size and abs(obj1.y - obj2.y) < obj2.size):
            return True
        return False

    def showGameOverDialog(self):
        message = f"Game Over!\nScore: {self.score}"
        QMessageBox.information(self, "Game Over", message, QMessageBox.Ok)
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = GameWindow()
    game.show()
    sys.exit(app.exec_())
