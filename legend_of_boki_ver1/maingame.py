import os
import random
import sys
import time

from PyQt5.QtWidgets import *
from PyQt5 import uic, Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

sys.setrecursionlimit(10 ** 7)  # 재귀함수 제한


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('maingame_final.ui')
main_game = uic.loadUiType(form)[0]


class Status:
    """각 캐릭터 정보 만들어주는 클래스"""

    def __init__(self, class_name, character_name, hp, mp, level):
        self.class_name = class_name
        self.character_name = character_name
        self.hp = hp
        self.mp = mp
        self.level = level

    def get_classname(self):  # 클래스이름
        return self.class_name

    def get_charactername(self):  # 캐릭터이름
        return self.character_name

    def get_hp(self):  # hp 반환
        return self.hp * self.level

    def get_level(self):  # 레벨 반환
        return self.level

    def get_mp(self):  # mp 반환
        return self.mp


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
        ## 배틀필드에서 들어갈 유저 캐릭터
        self.archer = QPixmap('./캐릭터/궁수.png')
        self.white_wizard = QPixmap('./캐릭터/백법사.png')
        self.black_wizard = QPixmap('./캐릭터/흑법사.png')
        self.red_wizard = QPixmap('./캐릭터/적법사.png')
        self.sword_man = QPixmap('./캐릭터/검사.png')
        self.warrior= QPixmap('./캐릭터/전사.png')
        # 캐릭터 별 프레임
        self.frame_class_list = [self.Frame_Class1_Status, self.Frame_Class2_Status,
                                 self.Frame_Class3_Status, self.Frame_Class4_Status, self.Frame_Class5_Status]

        # 스킬 버튼 가져오기
        self.skill_btn_set = self.Widget_Skill.findChildren(QPushButton)
        # 스킬 레이아웃 가져오기
        self.Widget_Skill_set = self.Widget_Skill.findChildren(QGraphicsWidget)

        # 유저턴 / 몬스터턴 턴 지정
        self.user_turn = 0  # 유저
        self.mon_turn = 0  # 몬스터

        # 캐릭터 이름 리스트
        self.character_name = ['미하일', '루미너스', '알렉스', '샐러맨더', '메르데스', '랜슬롯']
        class_1 = Status('전사', '미하일', 300, 0, 1)
        class_2 = Status('백법사', '루미너스', 200, 150, 1)
        class_3 = Status('흑법사', '알렉스', 200, 150, 1)
        class_4 = Status('적법사', '샐러맨더', 150, 150, 1)
        class_5 = Status('궁수', '메르데스', 150, 150, 1)
        class_6 = Status('검사', '랜슬롯', 150, 150, 1)
        self.list_class = [class_1, class_2, class_3, class_4, class_5, class_6]  # 클래스들 리스트에 담기


        # 유저는 보스를 이길 때까지 던전에 입장하지 못함
        self.user_can_enter_dungeon = False

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

        random_spot = random.randint(1, 4) #시작 캐릭터 위치 랜덤으로 위치시키기
        self.Character_QLabel.move(positions[random_spot][0], positions[random_spot][1]) #캐릭터를 상하좌우로 위치시키기
        self.portal_sample.move(random.randint(1, 1580), random.randint(1, 780)) #포탈 위치 랜덤으로 배정





        # 던전필드에 있는 라벨 정보 가져오기

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
                self.battle_ground() #전투 함수로 이동

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

            # 던전에서 몬스터 만났을 때 전투 이동
            if self.label_5.geometry().intersects(self.boss_monster.geometry()):
                self.show_messagebox("보스몬스터를 만났습니다!\n전투에 진입합니다.")
                # 전투로 스택위젯 이동
                # 전투함수로 이동
                self.user_can_enter_dungeon = True  # 전투에서 이기면 상태 True로 만들어주기

            # 던전에서 미궁 만났을 때 메세지 출력(임시) -> 코드 합치면 메세지 뜬 후 전투상황으로 이동하도록 하기
            if self.label_5.geometry().intersects(self.entrance.geometry()) and self.user_can_enter_dungeon == True:
                self.show_messagebox("미궁을 만났습니다!")
                # 이후 던전으로



            # 라벨(벽과)겹치면 이전 위치로 이동하도록 함
            for label in self.label_list:  # 라벨 정보 리스트 가져옴
                if label != self.label_5 and label != self.label_2 and new_position.intersects(
                        label.geometry()):  # 만약 겹치면 break
                    print(f'{label.objectName()}와 겹침')  # 확인용
                    self.label_5.setGeometry(previous_position)
                    break

            # 던전 벽 캐릭터가 벗어나지 못하게
            if not ((558 <= new_position.x() <= 1054) and (168 < new_position.y() < 662)):  # 미궁 x값, 미궁 y값 설정
                self.label_5.setGeometry(previous_position)

        # 이외 필드일때(전투일때) pass
        else:
            pass

        # 현재위치 왼쪽 상단에 출력
        self.TopUI_Coordinate_Label.setText(
            f"x좌표: {self.Character_QLabel.pos().x()}, y좌표:{self.Character_QLabel.pos().y()}")

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



    def battle_ground(self):
        """일반 공격필드 메인함수"""

        self.portal_sample.hide()  # 포탈 숨겨주고
        self.StackWidget_Field.setCurrentIndex(2)  # 전투필드로 이동

        # 캐릭터 별 프레임
        frame_class_list = []
        for frame in range(1, 5+1):
            frame_class_list.append(f'self.Frame_Class{frame}_Status')

        #첫번째 프레임 제외하고 False
        for FCS in self.frame_class_list[1:]:
            FCS.setEnabled(False)

        what_enemy_will_user_encounter = 1#random.randint(1, 100) #어떤 적을 만날지 랜덤 설정
        if what_enemy_will_user_encounter <= 75: #75%의 확률로 일반 적을 만난다
            self.Log_textEdit.append("일반몬스터를 만났습니다.") #상태창에 표시해주기
            ## 일반몬스터 만났을 때

            random.shuffle(self.list_class)  # 클래스 리스트 랜덤으로 섞기

            # 랜덤으로 섞은 캐릭터 클래스 창에 지정해 주기
            for i in range(5):
                getattr(self, f'Status{i + 1}_1_Class').setText(self.list_class[i].class_name)  # 클래스명 지정
                getattr(self, f'Status{i + 1}_1_Name').setText(self.list_class[i].character_name)  # 캐릭터명 지정
                getattr(self, f'Status{i + 1}_2_HpValue').setText(str(self.list_class[i].hp) + "/" + str(self.list_class[i].get_hp()))  # hp(기본 값/변하는 값)
                getattr(self, f'Status{i + 1}_2_HpValue').setAlignment(Qt.AlignCenter)
                getattr(self, f'Status{i + 1}_3_MpValue').setText(str(self.list_class[i].mp) + "/" + str(self.list_class[i].get_mp()))  # mp(기본 값/변하는 값)

            # Class_1_QLabel 라벨에 유저 사진 넣어주기
            classes = ['전사', '백법사', '흑법사', '적법사', '궁수', '검사']  # 캐릭터 이름 담기
            class_images = [self.warrior, self.white_wizard, self.black_wizard, self.red_wizard, self.archer, self.sword_man]  # 이미지 리스트와 맞추기

            # 클래스 직업군 텍스트 가져오기
            class_index1 = classes.index(self.Status1_1_Class.text())
            class_index2 = classes.index(self.Status2_1_Class.text())
            class_index3 = classes.index(self.Status3_1_Class.text())
            class_index4 = classes.index(self.Status4_1_Class.text())
            class_index5 = classes.index(self.Status5_1_Class.text())

            # 직업군에 따라 이미지 넣어주기
            self.Class_1_QLabel.setPixmap(class_images[class_index1])
            self.Class_2_QLabel.setPixmap(class_images[class_index2])
            self.Class_3_QLabel.setPixmap(class_images[class_index3])
            self.Class_4_QLabel.setPixmap(class_images[class_index4])
            self.Class_5_QLabel.setPixmap(class_images[class_index5])

            ### 몬스터, 캐릭터 정보 들어가게 하기 (+ hp, mp 정보도)
            monster_num = random.randint(1, 10) #몬스터 등장 개체수 랜덤 지정
            monster_hp_dit = {} #몬스터 hp 들어갈 딕셔너리
            for i in range(1, monster_num + 1):
                monster_hp = random.randint(200, 1000)
                getattr(self, f"Monster_{i}_QLabel").setText(f"몬스터 등장\n체력은{monster_hp}")  # 라벨에는 사진 넣기(이후에), 체력은 프로그래스 바로 연결
                monster_hp_dit[i] = monster_hp
                getattr(self, f"Monster_{i}_QProgressBar").setRange(0, 1000)  # 프로그래스바 최솟값 / 최댓값 설정
                getattr(self, f"Monster_{i}_QProgressBar").setValue(monster_hp)  # 몬스터 체력 프로그래스바에 설정
                getattr(self, f"Monster_{i}_QButton").setEnabled(False) # 몬스터 공격버튼 선택 안되게 하기

            for j in range(monster_num + 1, 10 + 1): #나온 몬스터 이외의 창은 숨기기
                getattr(self, f"Monster_{j}_QProgressBar").hide()
                getattr(self, f"Monster_{j}_QButton").hide()
                getattr(self, f"Monster_{j}_Name").hide()

            ### 전투 시작하면 캐릭터 장비를 각각의 스택위젯 창에 업데이트 시키기 -> 이건 해야함

            #### 일반공격 선택시 -> 다른 버튼들 비활성화 -> hp 가 0초과인 몬스터 버튼 활성화 -> 공격력 25%로 먹이기 -> 상태창에 얼마나 데미지 입혔는지 띄우기 ->  몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> 아군 중 전투가능이 없으면(hp 가 모두 없다면 전투 실패)
            self.Status1_Action1_Attack.clicked(self, btn_false(1)) #선택한 버튼 객체 보내주기

            #### 스킬 선택시 -> 위젯 띄우기 -> 캐릭터의 정보가 불러와져서 캐릭터의 스킬만 활성화 -> 클릭하면 몬스터에 공격 데미지 상태창에 표시 -> 몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> hp가 모두 없다면 전투 실패
            #### 아이템 선택시 -> 장비 및 소비 창 활성화
            ##### 소비창 버튼 클릭하면 선택한 캐릭터 mp hp 영향 -> 상태창에 띄우기 -> hpmp 라벨 변경 -> 몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> 다음 캐릭터가 없으면 상대턴으로 넘어감
            ##### 장비창 버튼 클릭하면 각 캐릭터 콤보박스 이동 -> 강화석 있다면 +버튼 활성화 -> (+)버튼 누르면 장비 업그레이드, 상태창에 정보 띄우기
            #### 회피 선택시 - 30%의 확률로 회피 성공. -> 몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴이동. 마지막 캐릭터일시 1번 캐릭터로 -> hpmp가 모두 없다면 전투 실패




        else:# 25%의 확률로 수호대를 만난다.
            self.Log_textEdit.append("수호대를 만났습니다.")
            ##수호대 만났을 때
            ## 수호대 정보 들어가게 하기
            ## 수호대, 캐릭터 정보 들어가게 하기
            #### 공격 선택시 -> hp 가 0초과인 수호대 버튼 활성화 -> 공격력 랜덤으로 먹이기 -> 상태창에 얼마나 데미지 입혔는지 띄우기 ->  수호대가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> hp 가 모두 없다면 전투 실패
            #### 스킬 선택시 -> 스택 위젯 띄우기 -> 캐릭터의 정보가 불러와져서 캐릭터의 스킬만 활성화 -> 클릭하면 수호대 공격 데미지 상태창에 표시 -> 수호대가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> hpmp가 모두 없다면 전투 실패
            #### 아이템 선택시 -> 장비 및 소비 창 활성화
            ##### 소비창 버튼 클릭하면 캐릭터 mp hp 영향 -> 수호대가 다 죽지 않았다면 -> 다음 캐릭터로 턴 이동 -> hpmp가 모두 없다면 전투 실패
            ##### 장비창 버튼 클릭하면 각 캐릭터 콤보박스 이동 -> 강화석 있다면 +버튼 활성화 ->[ 장비가 노발 장비라면 하급 강화석 필요, 레어 장비라면 상급 강화석 필요. ]->(+)버튼 누르면 장비 업그레이드, 상태창에 정보 띄우기
            #### 회피 선택시 - 몇 프로의 확률로 회피 성공. -> 몬스터가 다 죽지 않았다면 -> 다음 캐릭터로 턴이동. 마지막 캐릭터일시 1번 캐릭터로 -> hpmp가 모두 없다면 전투 실패

        self.Widget_Skill.hide()  # 위젯 스킬 창 투명화

    def btn_false(self, idx):
        btn_info = self.sender()
        if btn_info == '1. 공격'
        if Status1_Action1_Attack
            Status1_Action2_Skill
            Status1_Action3_Item
            Status1_Action4_Run

    def show_messagebox(self, text):
        """특정 문구 메세지박스 띄워주기"""
        reply = QMessageBox()
        reply.setText(text)
        reply.exec_()

    def move_to_dungeon(self):
        """던전으로 랜덤 이동하는 부분"""
        # last_position = self.label.geometry()  # 마지막 좌표 기억
        # self.label_5.setGeometry(last_position) # 마지막 좌표로 이동한 후 다음 필드에서 동일한 곳에 떨어지게 함 -> 던전 크기 수정으로 취소 / 삭제예정
        self.portal_sample.hide()  # 던전 필드로 이동할 때 포탈 숨겨주기
        # 여기서 self.user_can_enter_dungeon = True로 바꿔주기

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
        self.entrance.move(random.randint(558, 1054), random.randint(168, 662))  # 던전 15*15 사이즈


        # 몬스터 위치 임시로 만들어주기
        self.boss_monster = QLabel(self)  # 보스 몬스터 나타날 포탈 임시
        self.boss_monster.setText("몬스터")
        self.boss_monster.setFixedSize(30, 30)  # 임시 라벨지정
        self.boss_monster.setStyleSheet('background-color: red')  # 임시로 빨간색으로
        self.boss_monster.move(random.randint(558, 1054), random.randint(168, 662))  # 보스 몬스터 랜덤으로 등장

        #몬스터 위치 임시로 만들어주기
        self.boss_monster = QLabel(self) # 보스 몬스터 나타날 포탈 임시
        self.boss_monster.setText("몬스터")
        self.boss_monster.setFixedSize(30, 30)  # 임시 라벨지정
        self.boss_monster.setStyleSheet('background-color: red') #임시로 빨간색으로
        self.boss_monster.move(random.randint(558, 1054), random.randint(168, 662)) # 보스 몬스터 랜덤으로 등장


        self.check_collision(self.entrance)  # 미궁 만들어지는 곳 중복체크 하는 함수로 이동하기
        self.check_collision(self.boss_monster)  # 미궁 만들어지는 곳 중복체크 하는 함수로 이동하기

        self.entrance.show()
        self.boss_monster.show()

        # 검은 라벨 만들어서 위에 덮기(유저가 플레이할 때 던전이 안보이게)
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
                label.move(random.randint(558, 1054), random.randint(168, 662))
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
