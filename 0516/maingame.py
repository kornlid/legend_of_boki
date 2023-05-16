import os
import random
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic, Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
sys.setrecursionlimit(10 ** 7)  # 재귀함수 제한


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path('maingame.ui')
form_class = uic.loadUiType(form)[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)  # 프레임 지우기
        self.showFullScreen()  # 풀스크린 화면 만들기
        # self.exitAction.triggered.connect(qApp.closeAllWindows) # 게임 종료 이벤트

        # TODO 처음 게임 시작했을 때 시작 화면 보여주기
        self.StackWidget_Field.setCurrentIndex(0)  # 일반필드용

        # TODO 랜덤확률로 수호대 위치 4군데 중 1군데로 설정시키기 (왼, 오, 위, 아래)
        # 포탈 생성하기
        self.portal_sample = QLabel(self)
        self.portal_sample.setFixedSize(40, 40)
        self.portal_sample.setText("포탈")
        self.portal_sample.setStyleSheet('background-color: blue')
        self.portal_sample.show()

        # 캐릭터의 위치에 따라 포탈 위치 변경
        random_spot = random.randrange(1, 4)
        if random_spot == 1:
            self.label.move(790, 0)  # 캐릭터가 상단에 위치할 때
            self.portal_sample.move(random.randint(0, 1580), random.randint(390, 780))
        elif random_spot == 2:
            self.label.move(0, 390)  # 캐릭터가 왼쪽 중앙에 위치할 때
            self.portal_sample.move(random.randint(790, 1580), random.randint(0, 780))
        elif random_spot == 3:
            self.label.move(790, 780)  # 캐릭터가 하단에 위치할 때
            self.portal_sample.move(random.randint(0, 1580), random.randint(0, 390))
        elif random_spot == 4:
            self.label.move(1580, 390)  # 캐릭터가 오른쪽 중앙에 위치할 때ㅑ
            self.portal_sample.move(random.randint(0, 790), random.randint(0, 780))

        # 캐릭터 이미지 가져오기
        self.character_right_img = QPixmap('character_right.png')
        self.character_left_img = QPixmap('character_left.png')

        # 이 부분에서 랜덤값으로 던전 맵 임시생성하는 부분 추가하기
        # 1, 2, 3 중 하나의 값이 나오면 스택드 위젯 값 가져오기

        self.label_list = self.Page_Dungeon_Field.findChildren(QLabel)  # {던전 필드1}에 있는 라벨 정보 가져와서 리스트에 저장
        self.label_list_battlefield_2 = self.Page_Dungeon_Field_1.findChildren(QLabel)  # {던전 필드2}에 있는 라벨 정보 가져와서 리스트에 저장

        for i in self.label_list:
            print(i.objectName())

    def keyPressEvent(self, event):
        """키값 입력받아 라벨 움직이는 함수"""

        current_index = self.StackWidget_Field.currentIndex()  # 현재 스택위젯 값 가져오기

        # 노말필드일 때
        if current_index == 0:
            # 랜덤 값에 따라 이동 / 적 만남 / 수호대 만남 / 아이템 획득 (추가해야 함)
            previous_position = self.label_5.geometry()  # 움직이는 {라벨} 현재 위치 정보 가져옴 <= 이전위치
            if event.key() == Qt.Key_A:  # A 눌렀을 때
                self.label.setPixmap(self.character_left_img)
                self.label.move(self.label.x() - 20, self.label.y())  # 왼쪽으로 20  이동
            elif event.key() == Qt.Key_D:  # D 눌렀을 때
                self.label.setPixmap(self.character_right_img)
                self.label.move(self.label.x() + 20, self.label.y())  # 오른쪽으로 20  이동
            elif event.key() == Qt.Key_W:  # W눌렀을 때
                self.label.move(self.label.x(), self.label.y() - 20)  # 위로 20 이동
            elif event.key() == Qt.Key_S:  # S눌렀을 때
                self.label.move(self.label.x(), self.label.y() + 20)  # 위로 20 이동
            else:
                return

            # 현재위치 왼쪽 상단에 출력
            self.TopUI_Coordinate_Label.setText(
                f"x좌표: {self.label.pos().x()}, y좌표:{self.label.pos().y()}")  # 함수에서 구현되는지 확인하기

            # 일반필드에서 포탈 만났을 때
            if self.label.geometry().intersects(self.portal_sample.geometry()):  # 포탈 만나면
                self.move_to_deongun()  # 랜덤으로 던전으로 이동

        # 던전입구1일 때
        elif current_index == 1:
            previous_position = self.label_5.geometry()  # 움직이는 {라벨} 현재 위치 정보 가져옴 <= 이전위치
            if event.key() == Qt.Key_A:  # A 눌렀을 때
                self.label_5.setPixmap(self.character_left_img)
                new_position = self.label_5.geometry().translated(-20, 0)  # 새 포지션 값 저장
                self.label_5.move(self.label_5.x() - 20, self.label_5.y())  # 왼쪽으로 20  이동
            elif event.key() == Qt.Key_D:  # D 눌렀을 때
                self.label_5.setPixmap(self.character_right_img)
                new_position = self.label_5.geometry().translated(20, 0)  # 이하동일
                self.label_5.move(self.label_5.x() + 20, self.label_5.y())  # 오른쪽으로 20 이동
            elif event.key() == Qt.Key_W:  # W눌렀을 때
                new_position = self.label_5.geometry().translated(0, -20)
                self.label_5.move(self.label_5.x(), self.label_5.y() - 20)  # 위로 20 이동
            elif event.key() == Qt.Key_S:  # S눌렀을 때
                new_position = self.label_5.geometry().translated(0, 20)
                self.label_5.move(self.label_5.x(), self.label_5.y() + 20)  # 아래로 20 이동
            else:
                return

            # 현재위치 왼쪽 상단에 출력
            self.TopUI_Coordinate_Label.setText(f"x좌표: {self.label_5.pos().x()}, y좌표:{self.label_5.pos().y()}")

            # 던전에서 미궁 만났을 때 메세지 출력(임시) -> 코드 합치면 메세지 뜬 후 전투상황으로 이동하도록 하기
            if self.label_5.geometry().intersects(self.entrance.geometry()):
                reply = QMessageBox()
                reply.setText("미궁을 만났습니다!")
                reply.exec_()

            # 라벨(벽과)겹치면 이전 위치로 이동하도록 함
            for label in self.label_list:  # 라벨 정보 리d스트 가져옴
                if label != self.label_5 and label != self.label_2 and new_position.intersects(label.geometry()):  # 만약 겹치면 break
                    print(f'{label.objectName()}와 겹침')  # 확인용
                    self.label_5.setGeometry(previous_position)
                    break

            # 던전 벽 캐릭터가 벗어나지 못하게
            if not ((558 <= new_position.x() <= 1054) and (168 < new_position.y() < 662)):  # 미궁 x값, 미궁 y값 설정
                self.label_5.setGeometry(previous_position)


        # 던전필드 2일때
        elif current_index == 2:
            previous_position_2 = self.label_63.geometry()  # 움직이는 {라벨} 현재 위치 정보 가져옴 <= 이전위치
            if event.key() == Qt.Key_A:  # A 눌렀을 때
                self.label_63.setPixmap(self.character_left_img)
                new_position = self.label_63.geometry().translated(-20, 0)  # 새 포지션 값 저장
                self.label_63.move(self.label_63.x() - 20, self.label_63.y())  # 왼쪽으로 20  이동
            elif event.key() == Qt.Key_D:  # D 눌렀을 때
                self.label_63.setPixmap(self.character_right_img)
                new_position = self.label_63.geometry().translated(20, 0)  # 이하동일
                self.label_63.move(self.label_63.x() + 20, self.label_63.y())  # 오른쪽으로 20 이동
            elif event.key() == Qt.Key_W:  # W눌렀을 때
                new_position = self.label_63.geometry().translated(0, -20)
                self.label_63.move(self.label_63.x(), self.label_63.y() - 20)  # 위로 20 이동
            elif event.key() == Qt.Key_S:  # S눌렀을 때
                new_position = self.label_63.geometry().translated(0, 20)
                self.label_63.move(self.label_63.x(), self.label_63.y() + 20)  # 아래로 20 이동
            else:
                return

            # 현재위치 왼쪽 상단에 출력
            self.TopUI_Coordinate_Label.setText(f"x좌표: {self.label_63.pos().x()}, y좌표:{self.label_63.pos().y()}")

            # 라벨(벽과)겹치면 이전 위치로 이동하도록 함
            for label in self.label_list_battlefield_2:  # 라벨 정보 리스트 가져옴
                if label != self.label_63 and label != self.label_26 and new_position.intersects(label.geometry()):  # 캐릭터 라벨, 배경 라벨은 제외.
                    print(f'{label.objectName()}와 겹침')  # 확인용
                    self.label_63.setGeometry(previous_position_2)  # 겹치면 이전 위치로 이동
                    break  # for문 break
            # if not ((558 <= new_position.x() <= 1054) and (168 < new_position.y() < 662)):
            #     self.label_5.setGeometry(previous_position)

    # 함수로 키 입력 단순화 해보려고 했으나 실패. 시도했지만 코드를 줄이는데 큰 영향을 안 줌
    # def move_label(self, label, direction, distance):
    #     """라벨 움직이는 부분 함수로 연결"""
    #     if direction == 'left':
    #         label.setPixmap(self.character_left_img)
    #         label.move(label.x() - distance, label.y())
    #     elif direction == 'right':
    #         label.setPixmap(self.character_right_img)
    #         label.move(label.x() + distance, label.y())
    #     elif direction == 'up':
    #         label.setPixmap(self.character_left_img)
    #         label.move(label.x(), label.y() - distance)
    #     elif direction == 'down':
    #         label.setPixmap(self.character_left_img)
    #         label.move(label.x(), label.y() + distance)
    # 
    #     self.TopUI_Coordinate_Label.setText(f"x좌표: {label.pos().x()}, y좌표:{label.pos().y()}") #왼쪽상단에 현재위치 표시

    def move_to_deongun(self):
        """던전으로 이동하는 부분"""
        # last_position = self.label.geometry()  # 마지막 좌표 기억
        # self.label_5.setGeometry(last_position) # 마지막 좌표로 이동한 후 다음 필드에서 동일한 곳에 떨어지게 함 -> 던전 크기 수정으로 취소
        self.portal_sample.hide()  # 던전 필드로 이동할 때 포탈 숨겨주기
        random_dungeon_num = 1  # random.randint(1, 2)  # 던전 랜덤으로 가는 값 추가(4까지 추가 예정)
        if random_dungeon_num == 1:
            self.StackWidget_Field.setCurrentIndex(1)  # 1번 던전 필드로 이동
            self.Show_Dungeon_Entrance()  # 던전 입구 만들기
        elif random_dungeon_num == 2:
            self.StackWidget_Field.setCurrentIndex(2)  # 2번 던전 필드로 이동

    def Show_Dungeon_Entrance(self):
        """던전 입구 랜덤으로 만들어주는 함수"""

        # 미궁 버튼 임시로 만들어주기
        self.entrance = QLabel(self)
        self.entrance.setText("미궁")
        self.entrance.setFixedSize(30, 30)  # 임시 라벨지정
        self.entrance.setStyleSheet('background-color: blue')
        self.entrance.move(random.randint(558, 1054), random.randint(168, 662)) #던전 15*15 사이즈

        #몬스터 위치 임시로 만들어주기
        self.monster = QLabel(self)
        self.monster.setText("몬스터")
        self.monster.setFixedSize(30, 30)  # 임시 라벨지정
        self.monster.setStyleSheet('background-color: red')
        self.monster.move(random.randint(558, 1054), random.randint(168, 662))



        self.check_collision(self.entrance)  # 미궁 만들어지는 곳 중복체크 하는 함수로 이동하기
        self.check_collision(self.monster)  # 미궁 만들어지는 곳 중복체크 하는 함수로 이동하기

        self.entrance.show()
        self.monster.show()

        # 검은 라벨 만들어서 위에 덮기(유저가 플레이할 때 던전이 안보이게)
        # black_label = QLabel(self)
        # black_label.move(0, 30)
        # black_label.setStyleSheet('background-color: rgba(0, 0, 0, 200)')
        # black_label.setFixedSize(1615, 834)
        # black_label.show()

    def check_collision(self, label):
        """새로 미궁 만들어지는 곳 중복체크 하는 함수"""
        if self.label_2 in self.label_list:
            self.label_list.remove(self.label_2) # 캐릭터 지우기
        if self.label_5 in self.label_list:
            self.label_list.remove(self.label_5) # 배경 지우기


        for other_label in self.label_list:  # 라벨이 겹치면 값 재설정
            if label.geometry().intersects(other_label.geometry()):
                label.move(random.randint(558, 1054), random.randint(168, 662))
                self.check_collision(label)  # 재귀함수로 이 함수 다시 사용
                break

    # def 아이템 얻는 함수(self):
    # 3. 아이템 얻기
    ## 10%의 확률로 텐트 겟
    ## 레벨에 따른 포션 겟
    ## 포션 얻으면 lcd 창에 표시해주기
    #### 직업 변경권은 어떻게 얻더라?

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

    # def 전투함수(self):
    # 전투로 창이동시키기
    # self.StackWidget_Field.setCurrentIndex(2) #배틀필드 페이지 2

    ## 일반몬스터 만났을 때
    ### 몬스터, 캐릭터 정보 들어가게 하기 (+ hp, mp 정보도) <- 혜빈이 오늘 한거 붙여넣기하기
    ### 전투 시작하면 캐릭터 장비를 각각의 스택위젯 창에 업데이트 시키기 -> 이건 해야함

    #### 일반공격 선택시 -> hp 가 0초과인 몬스터 버튼 활성화 -> 공격력 25%로 먹이기 -> 상태창에 얼마나 데미지 입혔는지 띄우기 ->  몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> 아군 중 전투가능이 없으면(hp 가 모두 없다면 전투 실패)
    #### 스킬 선택시 -> 위젯 띄우기 -> 캐릭터의 정보가 불러와져서 캐릭터의 스킬만 활성화 -> 클릭하면 몬스터에 공격 데미지 상태창에 표시 -> 몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> hp가 모두 없다면 전투 실패
    #### 아이템 선택시 -> 장비 및 소비 창 활성화
    ##### 소비창 버튼 클릭하면 선택한 캐릭터 mp hp 영향 -> 상태창에 띄우기 -> hpmp 라벨 변경 -> 몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> 다음 캐릭터가 없으면 상대턴으로 넘어감
    ##### 장비창 버튼 클릭하면 각 캐릭터 콤보박스 이동 -> 강화석 있다면 +버튼 활성화 -> (+)버튼 누르면 장비 업그레이드, 상태창에 정보 띄우기
    #### 회피 선택시 - 30%의 확률로 회피 성공. -> 몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴이동. 마지막 캐릭터일시 1번 캐릭터로 -> hpmp가 모두 없다면 전투 실패

    ##수호대 만났을 때
    ## 수호대 정보 들어가게 하기
    ## 수호대, 캐릭터 정보 들어가게 하기
    #### 공격 선택시 -> hp 가 0초과인 수호대 버튼 활성화 -> 공격력 랜덤으로 먹이기 -> 상태창에 얼마나 데미지 입혔는지 띄우기 ->  수호대가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> hp 가 모두 없다면 전투 실패
    #### 스킬 선택시 -> 스택 위젯 띄우기 -> 캐릭터의 정보가 불러와져서 캐릭터의 스킬만 활성화 -> 클릭하면 수호대 공격 데미지 상태창에 표시 -> 수호대가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> hpmp가 모두 없다면 전투 실패
    #### 아이템 선택시 -> 장비 및 소비 창 활성화
    ##### 소비창 버튼 클릭하면 캐릭터 mp hp 영향 -> 수호대가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> hpmp가 모두 없다면 전투 실패
    ##### 장비창 버튼 클릭하면 각 캐릭터 콤보박스 이동 -> 강화석 있다면 +버튼 활성화 ->[ 장비가 노발 장비라면 하급 강화석 필요, 레어 장비라면 상급 강화석 필요. ]->(+)버튼 누르면 장비 업그레이드, 상태창에 정보 띄우기
    #### 회피 선택시 - 몇 프로의 확률로 회피 성공. -> 몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴이동. 마지막 캐릭터일시 1번 캐릭터로 -> hpmp가 모두 없다면 전투 실패

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
