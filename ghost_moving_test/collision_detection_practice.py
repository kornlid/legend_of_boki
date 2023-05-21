
"""
1. x, y 좌표가 정확하게 동일한 경우
- 타일 게임에서 유용

2. x, y의 거리 확인
- 한 개체의 x, y 좌표에서 다른 객체의 x, y 좌표까지 거리 측정해서 비교

3. 경계 상차
- 각 개체의 주위에 가상의 상자를 그려 모서리를 비교하거나
- 각 상자의 측면을 다른 측면과 비교하는 것

4. 픽셀 완전 충돌 검사
- 실제로 이미지의 모든 단일 픽셀을 다른 이미지의 픽셀과 비교하는 것
- 많은 확인 과정이 있기 때문에 복잡하지만 정확하다.

"""


import turtle
import math

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Collision Detection by @TokyoEdtech")
wn.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

shapes = ["wizard.gif", "goblin.gif", "pacman.gif", "cherry.gif", "bar.gif", "ball.gif", "x.gif"]

for shape in shapes:
    wn.register_shape(shape)


# Create Sprite Class
class Sprite():
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    def is_overlapping_collision(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def is_distance_collision(self, other):
        distance = (((self.x - other.x) ** 2) + ((self.y - other.y) ** 2)) ** 0.5
        if distance < (self.width + other.width) / 2.0:
            return True
        else:
            return False

    def is_aabb_collision(self, other):
        # Axis Aligned Bounding Box
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)


wizard = Sprite(-128, 200, 128, 128, "wizard.gif")
goblin = Sprite(128, 200, 108, 128, "goblin.gif")

pacman = Sprite(-128, 0, 128, 128, "pacman.gif")
cherry = Sprite(128, 0, 128, 128, "cherry.gif")

bar = Sprite(0, -400, 128, 24, "bar.gif")
ball = Sprite(0, -200, 32, 32, "ball.gif")

sprites = [wizard, goblin, pacman, cherry, bar, ball]


def move_goblin():
    goblin.x -= 64


def move_pacman():
    pacman.x += 30


def move_ball():
    ball.y -= 24


wn.listen()
wn.onkeypress(move_goblin, "Left")
wn.onkeypress(move_pacman, "Right")
wn.onkeypress(move_ball, "Down")

while True:

    for sprite in sprites:
        sprite.render(pen)

    # Collision detection
    if wizard.is_overlapping_collision(goblin):
        wizard.image = "x.gif"

    if pacman.is_overlapping_collision(cherry):
        cherry.image = "x.gif"

    if bar.is_overlapping_collision(ball):
        ball.image = "x.gif"

    wn.update()
    pen.clear()
