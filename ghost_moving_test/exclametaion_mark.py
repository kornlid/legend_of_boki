import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 600, 400)
        self.setStyleSheet('background-color: black')


        self.character_img_right = QPixmap('character_right.png')
        self.character_img_left = QPixmap('character_left.png')
        self.mark_img = QPixmap('mark.png')

        #캐릭터 담을 라벨 만들어주기
        self.character = QLabel(self)
        self.character.setFixedSize(40, 80)
        self.character.setStyleSheet('background-color: transparent')
        self.character.setPixmap(self.character_img_right.scaled(QSize(30, 50), aspectRatioMode=Qt.IgnoreAspectRatio))
        self.character.move(10, 30)

        self.character.show()


        #느낌표 담을 라벨 만들어주기
        self.mark_label = QLabel(self)
        self.mark_label.setPixmap(self.mark_img.scaled(QSize(50, 50), aspectRatioMode=Qt.IgnoreAspectRatio))
        self.mark_label.setStyleSheet('background-color: transparent')
        self.mark_label.hide()

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
        self.ghost_label.setStyleSheet('background-color: transparent')

        self.random_num = 1

        # 방향 타이머
        self.position = QTimer()
        self.position.setInterval(3000)
        self.position.timeout.connect(self.direction)
        self.position.start()

        # 유령 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_label)
        self.timer.start(30)  # 라벨을 40마다 움직이게 함

        #응답 상태
        self.reply_state = False

        #이스터에그 리스트
        self.msg_sample_list = {
            1:"그거 아시나요? 우리반에는 점심시간만 되면 배드민턴을 하는 사람들이 있다고 합니다.",
            2:"그거아시나요? 개발원 식당에서 나오는 라면은 물 70퍼 스프 30퍼로 구성되어있습니다.",
            3:"그거 아시나요? 옆팀 팀장님 >시연< 은 가위손 스킬을 지녔습니다.",
            4:"아이템 Hp(소)는 Hp(소) 만큼의 회복량을 가지고있습니다",
            5:"Tip. 그거 아시나요? 스킬 버튼을 누르면 스킬창이 뜹니다",
            6:"사실 미하일은 이혼 전적이 있습니다...",
            7:" 그거 아시나요? 게임 제작자도 엔딩을 못 봤습니다",
            8:"그거 아시나요?? 랜슬롯은 남자를..",
            9:"우리 낭만코더 리보키의 팀장은 커피를 한번에 세잔을 마실 수 있습니다.",
            10:"Tip. 깡깡.... 깡 (파스락)",
            11:"그거 아시나요? 우리반에는 매일 달리는 경주마가 있습니다.",
            12:"그거 아시나요? 이동녀크는 1층의 보스입니다."
        }

    def keyPressEvent(self, event):
        self.x_positon = self.character.pos().x()
        self.y_position = self.character.pos().y()

        # self.mark_label.move(self.x_positon+10, self.y_position)

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

        if self.reply_state == False and self.checkCollision(self.character, self.ghost_label):
            self.mark_label.move(self.character.x()+10, self.character.y())
            self.mark_label.show()
            self.show_messagebox()

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

        # 움직임 계산
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

        # if self.checkCollision(self.ghost_label, self.character):
        #     self.show_messagebox()

    def checkCollision(self, obj1, obj2):
        """겹치면 true반환"""
        x1, y1, w1, h1 = abs(obj1.x()), abs(obj1.y()), abs(obj1.width()), abs(obj1.height())
        x2, y2, w2, h2 = abs(obj2.x()), abs(obj2.y()), abs(obj2.width()), abs(obj2.height())
        if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
            return True
        return False

    def show_messagebox(self):
        self.reply_state = True
        # paper_img = QPixmap('구겨진_종이조각-removebg-preview.png')

        msg_box = QMessageBox()
        msg_box.setIconPixmap(QPixmap("구겨진_종이조각-removebg-preview.png"))
        msg_box.setText("구겨진 종이조각을 유령이 주었습니다... 보시겠습니까?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec_()

        if result == QMessageBox.Yes:
            self.show_second_messagebox()
        else:
            self.mark_label.hide()
            pass

        self.reply_state = False

    def show_second_messagebox(self):
        ranodm_num = random.randint(1, len(self.msg_sample_list.keys()))
        msg_box = QMessageBox()
        msg_box.setWindowFlags(Qt.FramelessWindowHint)
        msg_box.setStyleSheet('background-color: rgb(242, 238, 203)')
        if ranodm_num == 3:
            msg_box.setIconPixmap(QPixmap('모야.jpg'))
        msg_box.setText(f"쪽지에 작성된 내용은...\n{self.msg_sample_list[ranodm_num]}")
        msg_box.exec_()
        self.mark_label.hide()


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
