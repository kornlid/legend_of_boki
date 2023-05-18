import os
import random
import sys
import time

from PyQt5.QtWidgets import *
from PyQt5 import uic, Qt
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

sys.setrecursionlimit(10 ** 7)  # 재귀함수 제한


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path('maingame_final.ui')
main_game = uic.loadUiType(form)[0]


class WindowClass(QMainWindow, main_game):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)  # 프레임 지우기
        self.showFullScreen()  # 풀스크린 화면 만들기
        # self.exitAction.triggered.connect(qApp.closeAllWindows) # 게임 종료 이벤트

        # 캐릭터 이미지 가져오기
        ## 일반필드에서 움직일 캐릭터
        self.character_right_img = QPixmap('character_right.png')
        self.character_left_img = QPixmap('character_left.png')

        # 유저는 보스를 이길 때까지 던전에 입장하지 못함
        self.user_can_enter_dungeon = False
        # 랜덤 던전 스팟 번호
        self.dungeon_number = 0

        # 처음 게임 시작했을 때 시작 화면 보여주기
        self.StackWidget_Field.setCurrentIndex(0)  # 일반필드로 이동

        # 포탈 생성                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 탈 생성하기
        # TODO 처음 게임 시작했을 때 시작 화면 보여주기
        self.StackWidget_Field.setCurrentIndex(0)  # 일반필드로 이동

        # TODO 랜덤확률로 수호대 위치 4군데 중 1군데로 설정시키기 (왼, 오, 위, 아래)
        # 포                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     탈 생성하기
        self.portal_sample = QLabel(self)
        self.portal_sample.setFixedSize(40, 40)
        self.portal_sample.setText("포탈")
        self.portal_sample.setStyleSheet('background-color: blue')
        self.portal_sample.show()

        # 캐릭터의 위치에 따라 포탈 위치 변경 / 유저의 x, y값 지정하기
        positions = {
            1: (790, 0),  # 상단
            2: (0, 390),  # 왼쪽 중앙
            3: (790, 780),  # 하단
            4: (1580, 390)  # 오른쪽 중앙
        }

        random_spot = random.randint(1, 4)  # 시작 캐릭터 위치 랜덤으로 위치시키기
        self.Character_QLabel.move(positions[random_spot][0], positions[random_spot][1])  # 캐릭터를 상하좌우로 위치시키기
        self.portal_sample.move(random.randint(1, 1580), random.randint(1, 780))  # 포탈 위치 랜덤으로 배정

        # 던전 맵 사이즈(크기별)
        self.map_size = {
            1: [529, 1087, 136, 695],  # 맵 1번 x시작, x끝, y시작, y끝
            2: [510, 1106, 120, 713],  # 맵 2번 x시작, x끝, y시작, y끝
            3: [488, 1127, 97, 736],  # 맵 3번 x시작, x끝, y시작, y끝
            4: [471, 1145, 80, 754],  # 맵 4번 x시작, x끝, y시작, y끝
        }

        # 던전필드에 있는 라벨 정보 가져오기
        self.label_list = self.Page_Dungeon_Field.findChildren(QLabel)
        # self.label_list_battlefield_2 = self.Page_Dungeon_Field_1.findChildren(QLabel)  # {던전 필드2}에 있는 라벨 정보 가져와서 리스트에 저장

        # for i in self.label_list:
        #     print(i.objectName()) # 던전에 있는 라벨 객체이름 확인용

    def keyPressEvent(self, event):
        """키값 입력받아 라벨 움직이는 함수"""

        # 현재 스택위젯 값 가져오기
        current_index = self.StackWidget_Field.currentIndex()

        # 랜덤값에 따라 얻는 부분
        user_item_get = ''  # 어떤 아이템을 얻을지 표시
        user_random_get = {1: "아이템을 획득했습니다.", 2: '전투로 이동합니다.', 3: '한칸 이동합니다.', }  # 랜덤분기에 따른 결과값
        # user_item_get = ['포션', '텐트'] / 포션에 대해 정확히 정하기(회의시간에)

        # 노말필드일 때
        if current_index == 0:
            # 노말필드일때 랜덤값에 따라 이동하기
            # 랜덤 값에 따라 이동 / 적 만남 / 수호대 만남 / 아이템 획득 (추가해야 함)
            user_motion_random_val = random.randint(1, 3)  # 사용자가 정해질 랜덤값
            if user_motion_random_val == 1:  # 아이템을 획득할 경우
                user_motion_random_potion_get = random.randint(1, 100)  # 아이템을 얻게 되었을 때 다시 랜덤값 추출하기
                print(user_motion_random_potion_get)
                if user_motion_random_val == 1 and 0 < user_motion_random_potion_get <= 10:  # 아이템 얻을 확률33% * 텐트얻을확률 10%
                    user_item_get = '텐트'
                if user_motion_random_val == 1 and 10 < user_motion_random_potion_get <= 100:  # 아이템 얻을 확률33% * 포션얻을확률 90%
                    user_item_get = '포션'

            if user_motion_random_val == 2:  # 전투할 경우
                """
                전투 매커니즘으로 연결 필요
                """

            self.Log_textEdit.append(f"{user_item_get}{user_random_get[user_motion_random_val]} ")  # 상태창에 추가하기

            previous_position = self.Character_QLabel.geometry()  # 움직이는 {라벨} 현재 위치 정보 가져옴 <= 이전위치
            if event.key() == Qt.Key_A:  # A 눌렀을 때
                self.Character_QLabel.setPixmap(self.character_left_img)
                self.Character_QLabel.move(self.Character_QLabel.x() - 20, self.Character_QLabel.y())  # 왼쪽으로 20  이동
            elif event.key() == Qt.Key_D:  # D 눌렀을 때
                self.Character_QLabel.setPixmap(self.character_right_img)
                self.Character_QLabel.move(self.Character_QLabel.x() + 20, self.Character_QLabel.y())  # 오른쪽으로 20  이동
            elif event.key() == Qt.Key_W:  # W눌렀을 때
                self.Character_QLabel.move(self.Character_QLabel.x(), self.Character_QLabel.y() - 20)  # 위로 20 이동
            elif event.key() == Qt.Key_S:  # S눌렀을 때
                self.Character_QLabel.move(self.Character_QLabel.x(), self.Character_QLabel.y() + 20)  # 위로 20 이동
            else:
                return

            # 현재위치 왼쪽 상단에 출력
            self.TopUI_Coordinate_Label.setText(
                f"x좌표: {self.Character_QLabel.pos().x()}, y좌표:{self.Character_QLabel.pos().y()}")  # 함수에서 구현되는지 확인하기

            # 일반필드에서 포탈 만났을 때
            if self.Character_QLabel.geometry().intersects(self.portal_sample.geometry()):  # 포탈 만나면
                self.move_to_dungeon()  # 랜덤으로 던전으로 이동

        # 던전입구1일 때
        elif current_index == 1:
            previous_position = self.Character_QLabel_2.geometry()  # 움직이는 {라벨} 현재 위치 정보 가져옴 <= 이전위치
            if event.key() == Qt.Key_A:  # A 눌렀을 때
                self.Character_QLabel_2.setPixmap(
                    self.character_left_img.scaled(QSize(30, 50), aspectRatioMode=Qt.IgnoreAspectRatio))
                new_position = self.Character_QLabel_2.geometry().translated(-20, 0)  # 새 포지션 값 저장
                self.Character_QLabel_2.move(self.Character_QLabel_2.x() - 20,
                                             self.Character_QLabel_2.y())  # 왼쪽으로 20  이동
            elif event.key() == Qt.Key_D:  # D 눌렀을 때
                self.Character_QLabel_2.setPixmap(
                    self.character_right_img.scaled(QSize(30, 50), aspectRatioMode=Qt.IgnoreAspectRatio))
                new_position = self.Character_QLabel_2.geometry().translated(20, 0)  # 이하동일
                self.Character_QLabel_2.move(self.Character_QLabel_2.x() + 20,
                                             self.Character_QLabel_2.y())  # 오른쪽으로 20 이동
            elif event.key() == Qt.Key_W:  # W눌렀을 때
                new_position = self.Character_QLabel_2.geometry().translated(0, -20)
                self.Character_QLabel_2.move(self.Character_QLabel_2.x(), self.Character_QLabel_2.y() - 20)  # 위로 20 이동
            elif event.key() == Qt.Key_S:  # S눌렀을 때
                new_position = self.Character_QLabel_2.geometry().translated(0, 20)
                self.Character_QLabel_2.move(self.Character_QLabel_2.x(), self.Character_QLabel_2.y() + 20)  # 아래로 20 이동
            else:
                return

            #좌표 위에 찍어주기
            self.TopUI_Coordinate_Label.setText(
                f"x좌표: {self.Character_QLabel_2.pos().x()}, y좌표:{self.Character_QLabel_2.pos().y()}")

            # 던전에서 몬스터 만났을 때 전투 이동
            if self.Character_QLabel_2.geometry().intersects(self.boss_monster.geometry()):
                self.show_messagebox("보스몬스터를 만났습니다!\n전투에 진입합니다.")
                # 전투로 스택위젯 이동
                # 전투함수로 이동
                self.user_can_enter_dungeon = True  # 전투에서 이기면 상태 True로 만들어주기

            # 던전에서 미궁 만났을 때 메세지 출력(임시) -> 코드 합치면 메세지 뜬 후 전투상황으로 이동하도록 하기
            if self.Character_QLabel_2.geometry().intersects(
                    self.entrance.geometry()) and self.user_can_enter_dungeon == True:
                self.show_messagebox("미궁을 만났습니다!")

            # 던전 벽 캐릭터가 벗어나지 못하게
            # 던전맵 벽 값 지정
            wall_list = {
                1: [(899, 908, 131, 338),  # 던전 맵 1
                    (522, 638, 412, 420),
                    (660, 680, 490, 700),
                    (829, 1091, 488, 496), ],
                2: [(800, 820, 117, 341),  # 던전 맵 2
                    (509, 962, 486, 500)],
                3: [(893, 909, 96, 327),  # 던전 맵 3
                    (898, 981, 317, 329),
                    (488, 718, 429, 443),
                    (690, 720, 431, 553),
                    (897, 910, 473, 741)],
                4: [(680, 967, 203, 233),  # 던전 맵 4
                    (663, 703, 224, 575),
                    (954, 969, 221, 577),
                    (683, 737, 557, 575),
                    (918, 969, 562, 578),
                    (950, 1157, 408, 424), ]
            }

            if self.dungeon_number == 1:  # 15*15 사이즈 맵에 들어갔을 때
                # 던전 벽을 벗어나지 못하게 함
                if not ((self.map_size[1][0] <= new_position.x() <= self.map_size[1][1]) and (
                        self.map_size[1][2] < new_position.y() < self.map_size[1][3])):  # 미궁 x값, 미궁 y값 설정
                    self.Character_QLabel_2.setGeometry(previous_position)
                # 던전 내에 위치한 벽을 벗어나지 못하게 함
                if self.block_dungeon_wall(new_position, previous_position, wall_list, 1):
                    self.Character_QLabel_2.setGeometry(previous_position)
            elif self.dungeon_number == 2:  # 16 * 16 사이즈 맵에 들어갔을 때
                if not ((self.map_size[2][0] <= new_position.x() <= self.map_size[2][1]) and (
                        self.map_size[2][2] < new_position.y() < self.map_size[2][3])):  # 미궁 x값, 미궁 y값 설정
                    self.Character_QLabel_2.setGeometry(previous_position)
                if self.block_dungeon_wall(new_position, previous_position, wall_list, 2):
                    self.Character_QLabel_2.setGeometry(previous_position)
            elif self.dungeon_number == 3:  # 17 * 17 사이즈 맵에 들어갔을 때
                if not ((self.map_size[3][0] <= new_position.x() <= self.map_size[3][1]) and (
                        self.map_size[3][2] < new_position.y() < self.map_size[3][3])):  # 미궁 x값, 미궁 y값 설정
                    self.Character_QLabel_2.setGeometry(previous_position)
                if self.block_dungeon_wall(new_position, previous_position, wall_list, 3):
                    self.Character_QLabel_2.setGeometry(previous_position)
            elif self.dungeon_number == 4:  # 18 * 18 사이즈 맵에 들어갔을 때
                if not ((self.map_size[4][0] <= new_position.x() <= self.map_size[4][1]) and (
                        self.map_size[4][2] < new_position.y() < self.map_size[4][3])):  # 미궁 x값, 미궁 y값 설정
                    self.Character_QLabel_2.setGeometry(previous_position)
                if self.block_dungeon_wall(new_position, previous_position, wall_list, 4):
                    self.Character_QLabel_2.setGeometry(previous_position)




        # 이외 필드일때(전투일때) pass
        else:
            pass

            # 현재위치 왼쪽 상단에 출력


        # # 던전필드 2일때
        # elif current_index == 2:
        #     previous_position_2 = self.label_63.geometry()  # 움직이는 {라벨} 현재 위치 정보 가져옴 <= 이전위치
        #     if event.key() == Qt.Key_A:  # A 눌렀을 때
        #         self.label_63.setPixmap(self.character_left_img)
        #         new_position = self.label_63.geometry().translated(-20, 0)  # 새 포지션 값 저장
        #         self.label_63.move(self.label_63.x() - 20, self.label_63.y())  # 왼쪽으로 20  이동
        #     elif event.key() == Qt.Key_D:  # D 눌렀을 때
        #         self.label_63.setPixmap(self.character_right_img)
        #         new_position = self.label_63.geometry().translated(20, 0)  # 이하동일
        #         self.label_63.move(self.label_63.x() + 20, self.label_63.y())  # 오른쪽으로 20 이동
        #     elif event.key() == Qt.Key_W:  # W눌렀을 때
        #         new_position = self.label_63.geometry().translated(0, -20)
        #         self.label_63.move(self.label_63.x(), self.label_63.y() - 20)  # 위로 20 이동
        #     elif event.key() == Qt.Key_S:  # S눌렀을 때
        #         new_position = self.label_63.geometry().translated(0, 20)
        #         self.label_63.move(self.label_63.x(), self.label_63.y() + 20)  # 아래로 20 이동
        #     else:
        #         return
        #
        #     # 현재위치 왼쪽 상단에 출력
        #     self.TopUI_Coordinate_Label.setText(f"x좌표: {self.label_63.pos().x()}, y좌표:{self.label_63.pos().y()}")
        #
        #     # 라벨(벽과)겹치면 이전 위치로 이동하도록 함
        #     for label in self.label_list_battlefield_2:  # 라벨 정보 리스트 가져옴
        #         if label != self.label_63 and label != self.label_26 and new_position.intersects(label.geometry()):  # 캐릭터 라벨, 배경 라벨은 제외.
        #             print(f'{label.objectName()}와 겹침')  # 확인용
        #             self.label_63.setGeometry(previous_position_2)  # 겹치면 이전 위치로 이동
        #             break  # for문 break
        #     # if not ((558 <= new_position.x() <= 1054) and (168 < new_position.y() < 662)):
        #     #     self.label_5.setGeometry(previous_position)

    def block_dungeon_wall(self, new_position, previous_position, wall_list, num):
        """유저가 던전벽에서 나아가지 못하게 하기"""
        for key, value in wall_list.items():
            if key == num:
                for i in value:
                    if i[0] < new_position.x() < i[1] and i[2] < new_position.y() < i[3]:
                        self.Character_QLabel_2.setGeometry(previous_position)
                        return True
        return False

    def show_messagebox(self, text):
        """특정 문구 메세지박스 띄워주기"""
        reply = QMessageBox()
        reply.setText(text)
        reply.exec_()

    def move_to_dungeon(self):
        """던전으로 랜덤 이동하는 부분"""

        # 던전 이미지 불러오기
        dungeon_img_1 = QPixmap('./배경/던전_1.png')
        dungeon_img_2 = QPixmap('./배경/던전_2.png')
        dungeon_img_3 = QPixmap('./배경/던전_3.png')
        dungeon_img_4 = QPixmap('./배경/던전_4.png')

        self.StackWidget_Field.setCurrentIndex(1)  # 던전필드로 이동
        self.portal_sample.hide()  # 던전 필드로 이동할 때 포탈 숨겨주기

        # 던전에서 움직일 캐릭터 라벨 만들어주기
        self.Character_QLabel_2 = QLabel(self)
        self.Character_QLabel_2.setFixedSize(30, 50)  # 임시 라벨크기 지정
        self.Character_QLabel_2.setPixmap(
            self.character_right_img.scaled(QSize(30, 50), aspectRatioMode=Qt.IgnoreAspectRatio))
        self.Character_QLabel_2.show()

        # 던전 랜덤 가는 부분
        random_dungeon_num = random.randint(1, 4)

        if random_dungeon_num == 1:
            self.dungeon_number = 1  # 키프레스가 인식해야할 값에 1로 넣어줌
            self.dungeon_img_label.setPixmap(dungeon_img_1)
            # self.StackWidget_Field.setCurrentIndex(1)  # 1번 던전 필드로 이동
            self.Character_QLabel_2.move(601, 673)  # 캐릭터 던전 입구로 보내기
        elif random_dungeon_num == 2:
            self.dungeon_number = 2
            self.dungeon_img_label.setPixmap(dungeon_img_2)
            self.Character_QLabel_2.move(572, 693)  # 캐릭터 던전 입구로 보내기
            # self.Show_Dungeon_Entrance(2)  # 던전 입구 만들기
        elif random_dungeon_num == 3:
            self.dungeon_number = 3
            self.dungeon_img_label.setPixmap(dungeon_img_3)
            self.Character_QLabel_2.move(560, 702)  # 캐릭터 던전 입구로 보내기
            # self.Show_Dungeon_Entrance(3)  # 던전 입구 만들기
        elif random_dungeon_num == 4:
            self.dungeon_number = 4
            self.dungeon_img_label.setPixmap(dungeon_img_4)
            self.Character_QLabel_2.move(503, 723)  # 캐릭터 던전 입구로 보내기
            # self.Show_Dungeon_Entrance(4)  # 던전 입구 만들기
        self.Show_Dungeon_Entrance(random_dungeon_num)  # 던전 입구 만들기

    def Show_Dungeon_Entrance(self, map_num):
        """던전 입구 랜덤으로 만들어주는 함수"""

        # 미궁 버튼 임시로 만들어주기
        self.entrance = QLabel(self)
        self.entrance.setText("미궁")
        self.entrance.setFixedSize(30, 30)  # 임시 라벨지정
        self.entrance.setStyleSheet('background-color: blue')
        self.entrance.move(random.randint(self.map_size[map_num][0], self.map_size[map_num][1]),
                           random.randint(self.map_size[map_num][2], self.map_size[map_num][3]))  # 던전 15*15 사이즈
        self.entrance.show()

        # 보스 몬스터 위치 임시로 만들어주기
        self.boss_monster = QLabel(self)  # 보스 몬스터 나타날 포탈 임시
        self.boss_monster.setText("몬스터")
        self.boss_monster.setFixedSize(30, 30)  # 임시 라벨크기지정
        self.boss_monster.setStyleSheet('background-color: red')  # 임시로 빨간색으로
        self.boss_monster.move(random.randint(self.map_size[map_num][0], self.map_size[map_num][1]),
                               random.randint(self.map_size[map_num][2], self.map_size[map_num][3]))  # 보스 몬스터 랜덤으로 등장
        self.boss_monster.show()

        # self.check_collision(self.entrance)  # 미궁 만들어지는 곳 중복체크 하는 함수로 이동하기
        # self.check_collision(self.boss_monster)  # 보스몬스터 만들어지는 곳 중복체크 하는 함수로 이동하기

        #검은 라벨 만들어서 위에 덮기(유저가 플레이할 때 던전이 안보이게)
        black_label = QLabel(self)
        black_label.move(0, 30)
        black_label.setStyleSheet('background-color: rgba(0, 0, 0, 200)')
        black_label.setFixedSize(1615, 834)
        black_label.show()

    def check_collision(self, label):
        """새로 미궁 만들어지는 곳 중복체크 하는 함수"""
        if self.label_2 in self.label_list:
            self.label_list.remove(self.label_2)  # 캐릭터 지우기
        if self.label_5 in self.label_list:
            self.label_list.remove(self.label_5)  # 배경 지우기
        # if self.black_label in self.label_list:
        #     self.label_list.remove(self.black_label) # 배경 지우기

        for other_label in self.label_list:  # 라벨이 겹치면 값 재설정
            if label.geometry().intersects(other_label.geometry()):
                label.move(random.randint(self.map_size[1][0], self.map_size[1][1]),
                           random.randint(self.map_size[1][2], map_size[1][3]))
                self.check_collision(label)  # 재귀함수로 이 함수 다시 사용
                break

    # def let_user_know_portal_loacation(self)  #유저가 포탈 위치 알게 되는 함수
    # self.{던전포탈위치상태} = True
    # def lab_hide(self):
    #  """던전에서 포탈 위치 보여주는 함수"""
    #     if self.{던전포탈위치상태} ==  True:
    #         self.{던전포탈위치상태} = False
    #         self.{배경위검은라벨}.hide()
    #     else:
    #         self.{던전포탈위치상태} = True
    #         self.{배경위검은라벨}.show()

    # def 승리함수(self, 이긴위치):
    # 승리했을 때 어떤 상황에 따라 어떤 보상을 줄 지 선택하기
    #

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
