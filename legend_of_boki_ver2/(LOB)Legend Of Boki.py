import os
import random
import sys

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import uic, Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt, QByteArray, QSize

from maingame import Ui_Maingame as game


class Status:
    def __init__(self, class_name, character_name, hp, mp, level):
        self.class_name = class_name
        self.character_name = character_name
        self.hp = hp
        self.mp = mp
        self.level = level

    def get_classname(self):
        return self.class_name

    def get_charactername(self):
        return self.character_name

    def get_hp(self):
        return self.hp * self.level

    def get_level(self):
        return self.level

    def get_mp(self):
        return self.mp


class MonsterOption:
    def __init__(self, field, name, img, level, hp, atk):
        self.field = field
        self.name = name
        self.image = img
        self.level = level
        self.hp = hp
        self.atk = atk

    def get_field(self):
        return self.field

    def get_name(self):
        return self.name

    def get_image(self):
        return self.image

    def get_level(self):
        return self.level

    def get_hp(self):
        return self.hp

    def get_atk(self):
        return self.atk


class SkillOption:
    def __init__(self, name, img, value, mp, target, turn):
        self.name = name
        self.img = img
        self.value = value
        self.mp = mp
        self.target = target
        self.turn = turn

    def get_name(self):
        return self.name

    def get_img(self):
        return self.img

    def get_value(self):
        return self.value

    def get_target(self):
        return self.target

    def get_mp(self):
        return self.mp

    def get_turn(self):
        return self.turn


# 더 추가할 필요가 있다면 추가하시면 됩니다. 예: (from PyQt5.QtGui import QIcon)
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path('maingame.ui')
form_class = uic.loadUiType(form)[0]


class WindowClass(QMainWindow, game):
    """
    메인 게임 진행
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.MainFrame_Bottom.setEnabled(False)

        # 혜빈 코드 취합 본 시작===========================================================================================
        # 해당 인스턴스에 캐릭터 정보 저장
        self.class_1 = Status('전사', '미하일', 300, 0, 1)
        self.class_2 = Status('백법사', '루미너스', 200, 150, 1)
        self.class_3 = Status('흑법사', '알렉스', 200, 150, 1)
        self.class_4 = Status('적법사', '샐러맨더', 150, 150, 1)
        self.class_5 = Status('궁수', '메르데스', 150, 150, 1)
        self.class_6 = Status('검사', '랜슬롯', 150, 150, 1)

        # 인스턴스 리스트화
        list_class = [self.class_1, self.class_2, self.class_3, self.class_4, self.class_5, self.class_6]

        # 리스트를 셔플로 돌려줌
        random.shuffle(list_class)

        for i in range(5):
            getattr(self, f'Status{i+1}_1_Class').setText(list_class[i].class_name)     # 클래스명 지정
            getattr(self, f'Status{i+1}_1_Class').setAlignment(Qt.AlignCenter)          # 텍스트 가운데 정렬
            getattr(self, f'Status{i+1}_1_Class').setStyleSheet('QLabel{background-color:#55aaff;}')     # 클래스 배경 색상 지정
            getattr(self, f'Status{i+1}_1_Name').setText(list_class[i].character_name)      # 캐릭터명 지정
            getattr(self, f'Status{i+1}_1_Name').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i+1}_2_HpValue').setText(str(list_class[i].hp)+"/"+str(list_class[i].get_hp()))  # hp(기본 값/변하는 값)
            getattr(self, f'Status{i+1}_2_HpValue').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i+1}_3_MpValue').setText(str(list_class[i].mp)+"/"+str(list_class[i].get_mp()))  # mp(기본 값/변하는 값)
            getattr(self, f'Status{i+1}_3_MpValue').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i+1}_2_Hp').setStyleSheet('QLabel{background-color:#55aaff;}')       # hp, mp 배경 색상 지정
            getattr(self, f'Status{i+1}_3_Mp').setStyleSheet('QLabel{background-color:#55aaff;}')
        # 여기까지 잘먹음

        # 캐릭터 별 프레임
        self.frame_class_list = [self.Frame_Class1_Status, self.Frame_Class2_Status,
                                 self.Frame_Class3_Status, self.Frame_Class4_Status, self.Frame_Class5_Status]

        # 혜빈 코드 취합 본 끝 ============================================================================================

        # 소연 취합 시작 ==================================================================================================


        # 유저는 보스를 이길 때까지 던전에 입장하지 못함
        self.user_can_enter_dungeon = False
        # 랜덤 던전 스팟 번호
        self.dungeon_number = 0

        # 처음 게임 시작했을 때 시작 화면 보여주기
        self.StackWidget_Field.setCurrentIndex(0)  # 일반필드로 이동

        #임시로 포탈 하나 만들기
        self.portal_sample = QLabel(self)
        self.portal_sample.setFixedSize(40, 40)
        self.portal_sample.setText("포탈")
        self.portal_sample.setStyleSheet('background-color: blue')
        self.portal_sample.show()

        #던전필드에 던전 이미지 들어갈 라벨 만들기
        self.dungeon_img_label = QLabel(self.Page_Dungeon_Field) #던전필드에 던전이미지 들어갈 라벨 추가, 던전필드를 부모로 설정
        self.dungeon_img_label.setGeometry(0, 0, 1615, 834)
        self.dungeon_img_label.show()

        #  이 부분은 아래와 중복
        # # 캐릭터의 위치에 따라 포탈 위치 변경 / 유저의 x, y값 지정하기
        # positions = {
        #     1: (790, 0),  # 상단
        #     2: (0, 390),  # 왼쪽 중앙
        #     3: (790, 780),  # 하단
        #     4: (1580, 390)  # 오른쪽 중앙
        # }
        #
        # random_spot = random.randint(1, 4)  # 시작 캐릭터 위치 랜덤으로 위치시키기
        # self.Character_QLabel.move(positions[random_spot][0], positions[random_spot][1])  # 캐릭터를 상하좌우로 위치시키기
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

        # ++ keypressevent 함수에 추가로 추합
        # ==================================================================================================================



        # 몬스터 상속
        self.nomalfield_fire_monster1 = MonsterOption("불의 지역", "불타는 나무정령", "character_1.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.nomalfield_fire_monster2 = MonsterOption("불의 지역", "불의 정령", "character_2.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.nomalfield_fire_monster3 = MonsterOption("불의 지역", "불타는 골렘", "character_3.png", 1,
                                                      random.randrange(200, 1000), 50)
        # 각 클래스 스킬 상속
        self.skill_1 = SkillOption("힐", None, random.randrange(30, 70), 10, 0, 1)
        self.skill_2 = SkillOption("그레이트 힐", None, random.randrange(60, 100), 20, 0, 1)
        self.skill_3 = SkillOption("힐 올", None, random.randrange(40, 80), 10, 0, 1)
        self.skill_4 = SkillOption("공격력 Up", None, random.randrange(30, 70), 10, 0, 1)
        self.skill_5 = SkillOption("방어력 Up", None, random.randrange(30, 70), 10, 0, 1)
        self.skill_6 = SkillOption("맵 핵", None, 0, 0, 1, 1)

        self.skill_7 = SkillOption("파이어 볼", "검사버프스킬 모션-1.gif", 30, 10, 1, 1)
        self.skill_8 = SkillOption("파이어 월", None, random.randrange(40, 60), 10, 2, 1)
        self.skill_9 = SkillOption("썬더브레이커", None, random.randrange(70, 90), 10, 2, 1)
        self.skill_10 = SkillOption("블리자드", None, random.randrange(90, 120), 10, 2, 1)

        self.skill_11 = SkillOption("집중타", None, random.randrange(20, 50), 10, 1, 1)
        self.skill_12 = SkillOption("듀얼 샷", None, random.randrange(40, 60), 10, 1, 1)
        self.skill_13 = SkillOption("마스터 샷", None, random.randrange(50, 70), 10, 1, 1)

        self.skill_14 = SkillOption("강타", None, random.randrange(2, 50), 10, 1, 1)
        self.skillall = [self.skill_1, self.skill_3, self.skill_4, self.skill_5, self.skill_6, self.skill_7,
                         self.skill_8, self.skill_9, self.skill_10, self.skill_11, self.skill_12, self.skill_13,
                         self.skill_14]

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        # self.exitAction.triggered.connect(qApp.closeAllWindows) # 게임 종료 이벤트
        # TODO 캐릭터 움직일 때 마다 x, y 좌표 반영하기
        ## [임시 캐릭터 설정]
        self.character_left_img = QPixmap('character_left.png')  # 캐릭터 왼쪽 이미지
        self.character_right_img = QPixmap('character_right.png')  # 캐릭터 오른쪽 이미지
        self.potal_img = QPixmap('potal.png')  # 임시 미궁 이미지
        self.back_ground_label.setPixmap(QtGui.QPixmap("용암.png"))  # 임시 일반 필드 배경 이미지
        self.back_ground_label.move(0, -1)  # 배경 위치 조정
        self.Widget_Skill.move(826, -1)  # 전투중 스킬 선택시 생성되는 스킬 위젯 위치
        self.HoldSwitch = 0
        self.Widget_Skill.hide()
        self.Page_Use_ing.setEnabled(False)
        # self.Page_Equip.setEnabled(False)
        self.Btn_Equip.clicked.connect(lambda y : self.use_uiABC(4))
        self.Btn_Portion.clicked.connect(lambda y : self.use_uiABC(0))
        self.Btn_Status.clicked.connect(lambda y : self.use_uiABC(2))
        for num in range(1, 6): # 액션버튼 1~4 시그널 슬롯 연결
            getattr(self, f'Status{num}_Action2_Skill').clicked.connect(self.skillopen)
            getattr(self, f'Status{num}_Action3_Item').clicked.connect(lambda y : self.use_uiABC(1))
        self.pushbox = self.Widget_Skill.findChildren(QPushButton)
        self.actbtnbox = []
        for i in range(1, 11):
            self.actbtnbox.append(getattr(self, f'Monster_{i}_QButton'))
        for idx, actbtn in enumerate(self.actbtnbox):
            actbtn.clicked.connect(lambda x, y=idx + 1: self.skillact(y))
        self.Skill_exit_Btn.clicked.connect(self.Widget_Skill.close)
        for btn in self.actbtnbox:
            btn.hide()

        self.progressBarbox = self.frame_2.findChildren(QProgressBar)
        for pro in self.progressBarbox:
            pro.hide()

        for skillbtn in self.pushbox:
            skillbtn.clicked.connect(self.skillchoice)

        self.choice_btn = []
        self.choicecnt = 0

        self.cnt = 0
        # 수호대 스폰 지역 랜덤 설정 및 미궁 랜덤 생성 (조건 = 무조건 수호대 스폰 지역 반대 편에 포탈 나오게함)========================
        random_spot = random.randrange(1, 5)
        if random_spot == 1:  # 숲의 지역 스폰 장소
            self.Character_QLabel.setPixmap(self.character_left_img)
            self.Character_QLabel.move(100, 520)
            self.Potal_QLabel.move(random.randint(860, 1580), random.randint(0, 780))
            self.TopUI_Map_Label.setText("숲의 지역")

        elif random_spot == 2:  # 불의 지역 스폰 장소
            self.Character_QLabel.setPixmap(self.character_left_img)
            self.Character_QLabel.move(360, 40)
            self.Potal_QLabel.move(random.randint(0, 1580), random.randint(420, 780))
            self.TopUI_Map_Label.setText("불의 지역")

        elif random_spot == 3:  # 눈의 지역 스폰 장소
            self.Character_QLabel.setPixmap(self.character_left_img)
            self.Character_QLabel.move(1280, 20)
            self.Potal_QLabel.move(random.randint(0, 820), random.randint(0, 780))
            self.TopUI_Map_Label.setText("눈의 지역")
        elif random_spot == 4:  # 물의 지역 스폰 장소
            self.Character_QLabel.setPixmap(self.character_left_img)
            self.Character_QLabel.move(1320, 540)
            self.Potal_QLabel.move(random.randint(0, 1580), random.randint(0, 380))
            self.TopUI_Map_Label.setText("물의 지역")

        # 왼쪽 상단에 초기 죄표 값 출력
        self.TopUI_Coordinate_Label.setText(
            f"x좌표: {self.Character_QLabel.pos().x()} y좌표: {self.Character_QLabel.pos().y()}")
    # 혜빈 파일 함수===================================================================================================시작




    # 혜빈 파일 함수===================================================================================================끝끝
    def skillopen(self):
        self.Widget_Skill.show()

    def skillact(self, btn):
        # 각 클래스 스킬 상속
        self.skill_1 = SkillOption("힐", None, random.randrange(30, 70), 10, 0, 1)
        self.skill_2 = SkillOption("그레이트 힐", None, random.randrange(60, 100), 20, 0, 1)
        self.skill_3 = SkillOption("힐 올", None, random.randrange(40, 80), 10, 0, 1)
        self.skill_4 = SkillOption("공격력 Up", None, random.randrange(30, 70), 10, 0, 1)
        self.skill_5 = SkillOption("방어력 Up", None, random.randrange(30, 70), 10, 0, 1)
        self.skill_6 = SkillOption("맵 핵", None, 0, 0, 1, 1)

        self.skill_7 = SkillOption("파이어 볼", "검사버프스킬 모션-1.gif", 30, 10, 1, 1)
        self.skill_8 = SkillOption("파이어 월", None, random.randrange(40, 60), 10, 2, 1)
        self.skill_9 = SkillOption("썬더브레이커", None, random.randrange(70, 90), 10, 2, 1)
        self.skill_10 = SkillOption("블리자드", None, random.randrange(90, 120), 10, 2, 1)

        self.skill_11 = SkillOption("집중타", None, random.randrange(20, 50), 10, 1, 1)
        self.skill_12 = SkillOption("듀얼 샷", None, random.randrange(40, 60), 10, 1, 1)
        self.skill_13 = SkillOption("마스터 샷", None, random.randrange(50, 70), 10, 1, 1)

        self.skill_14 = SkillOption("강타", None, random.randrange(2, 50), 10, 1, 1)
        self.skillall = [self.skill_1, self.skill_3, self.skill_4, self.skill_5, self.skill_6,
                         self.skill_7,
                         self.skill_8, self.skill_9, self.skill_10, self.skill_11, self.skill_12,
                         self.skill_13,
                         self.skill_14]
        if len(self.choice_btn) > 0:
            for skill in self.skillall:
                if ((skill.name == self.choice_btn[0].text())
                        and (skill.target == 1)):
                    getattr(self, f'Monster_{btn}_QProgressBar').setValue(
                        getattr(self, f'Monster_{btn}_QProgressBar').value() - skill.value)
                    self.Log_textEdit.append("해당 %s에게 %s을(를) %d만큼 입혔습니다." % (
                    getattr(self, f'Monster_{btn}_Name').text(), skill.name, skill.value))
                    if getattr(self, f'Monster_{btn}_QProgressBar').value() < skill.value:
                        getattr(self, f'Monster_{btn}_QLabel').hide()
                        getattr(self, f'Monster_{btn}_QButton').hide()
                        getattr(self, f'Monster_{btn}_Name').hide()
                        getattr(self, f'Monster_{btn}_QProgressBar').hide()
                        self.Log_textEdit.append("%s을 처치하였습니다." % getattr(self, f'Monster_{btn}_Name').text())
                        getattr(self, f'Monster_{btn}_Name').setText("")
                elif ((skill.name == self.choice_btn[0].text())
                      and (skill.target == 2)):
                    for i in range(1, 11):
                        getattr(self, f'Monster_{i}_QProgressBar').setValue(
                            getattr(self, f'Monster_{i}_QProgressBar').value() - skill.value)
                        if getattr(self, f'Monster_{i}_QProgressBar').value() < skill.value:
                            getattr(self, f'Monster_{i}_QLabel').hide()
                            getattr(self, f'Monster_{i}_QButton').hide()
                            getattr(self, f'Monster_{i}_Name').hide()
                            getattr(self, f'Monster_{i}_QProgressBar').hide()
                            if getattr(self, f'Monster_{i}_Name').text() != "":
                                self.Log_textEdit.append("%s을 처치하였습니다." % getattr(self, f'Monster_{i}_Name').text())
                                getattr(self, f'Monster_{i}_Name').setText("")
                    self.Log_textEdit.append("전체 적에게 %s을(를) %d만큼 입혔습니다." % (skill.name, skill.value))
                self.cnt = 0
                for i in range(1, 11):
                    if getattr(self, f'Monster_{i}_Name').text() == "":
                        self.cnt += 1
                    if self.cnt == 10:
                        # for hold in self.pushbox:
                        #     hold.setEnabled(True)
                        self.Log_textEdit.setText("몬스터를 전부 처치하여 필드로 돌아왔습니다.")
                        self.Log_textEdit.append("보상 : 경험치 50exp")
                        self.StackWidget_Field.setCurrentIndex(0)
                        self.HoldSwitch = 0
                        self.cnt = 0

    def skillchoice(self):
        if len(self.choice_btn) < 1:
            for btn in self.pushbox:
                if btn.isChecked():
                    self.choice_btn.append(self.pushbox.pop(self.pushbox.index(btn)))
                    for hold in self.pushbox:
                        hold.setEnabled(False)
                    for skill in self.skillall:
                        if self.choice_btn[0].text() == skill.name and skill.target == 0:
                            for act in self.actbtnbox:
                                act.setEnabled(False)
                        elif self.choice_btn[0].text() == skill.name and skill.target <= 2:
                            for act in self.actbtnbox:
                                act.setEnabled(True)
        else:
            self.pushbox.append(self.choice_btn.pop(0))
            for hold in self.pushbox:
                hold.setEnabled(True)
            for act in self.actbtnbox:
                act.setEnabled(False)

    def use_uiABC(self, num):
        if num == 0:
            self.StackWidget_Item.setCurrentIndex(0)
        elif num == 1:
            self.Page_Use.setEnabled(True)
            self.StackWidget_Item.setCurrentIndex(0)
        elif num == 2:
            self.Page_Use_ing.setEnabled(False)
            self.StackWidget_Item.setCurrentIndex(1)
        elif num == 3:
            self.Page_Use_ing.setEnabled(True)
            self.StackWidget_Item.setCurrentIndex(1)
        elif num == 4:
            self.StackWidget_Item.setCurrentIndex(2)
    # 소연 함수 시작 ========================================================================================================

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
        random_dungeon_num = 4 #random.randint(1, 4)
        print('던전번호는', random_dungeon_num)
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

        # 검은 라벨 만들어서 위에 덮기(유저가 플레이할 때 던전이 안보이게) <= 일단 ㄱ
        black_label = QLabel(self)
        black_label.move(0, 30)
        black_label.setStyleSheet('background-color: rgba(0, 0, 0, 200)') #200으로 설정되어 있는 투명도 높이면 어두워짐
        black_label.setFixedSize(1580, 780)
        black_label.show()

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

    # 소연 함수 끝 ==========================================================================================================
    # 캐릭터 방향키로 움직이기===============================================================================================
    def keyPressEvent(self, event):

        # 소연 추합 부분 시작==============================================================
        # 현재 스택위젯 값 가져오기
        current_index = self.StackWidget_Field.currentIndex()


        # ==(소연)================<아래 코드와 중복된 내용인듯> =======================
        # # 랜덤값에 따라 얻는 부분
        # user_item_get = ''  # 어떤 아이템을 얻을지 표시
        # user_random_get = {1: "아이템을 획득했습니다.", 2: '전투로 이동합니다.', 3: '한칸 이동합니다.', }  # 랜덤분기에 따른 결과값
        # # user_item_get = ['포션', '텐트'] / 포션에 대해 정확히 정하기(회의시간에)
        #
        # # 노말필드일 때
        # if current_index == 0:
        #     # 노말필드일때 랜덤값에 따라 이동하기
        #     # 랜덤 값에 따라 이동 / 적 만남 / 수호대 만남 / 아이템 획득 (추가해야 함)
        #     user_motion_random_val = random.randint(1, 3)  # 사용자가 정해질 랜덤값
        #     if user_motion_random_val == 1:  # 아이템을 획득할 경우
        #         user_motion_random_potion_get = random.randint(1, 100)  # 아이템을 얻게 되었을 때 다시 랜덤값 추출하기
        #         print(user_motion_random_potion_get)
        #         if user_motion_random_val == 1 and 0 < user_motion_random_potion_get <= 10:  # 아이템 얻을 확률33% * 텐트얻을확률 10%
        #             user_item_get = '텐트'
        #         if user_motion_random_val == 1 and 10 < user_motion_random_potion_get <= 100:  # 아이템 얻을 확률33% * 포션얻을확률 90%
        #             user_item_get = '포션'
        #
        #     if user_motion_random_val == 2:  # 전투할 경우
        #         """
        #         전투 매커니즘으로 연결 필요
        #         """
        #
        #     self.Log_textEdit.append(f"{user_item_get}{user_random_get[user_motion_random_val]} ")  # 상태창에 추가하기





        #일반필드일 때
        if current_index == 0:

            # 움직이는 {라벨} 현재 위치 정보 가져옴 <= 이전위치
            previous_position = self.Character_QLabel.geometry()

            rand_event = random.randrange(1, 11)
            if ((event.key() == Qt.Key_A)  # "a"키를 누를경우 캐릭터 현재 x값을 -20
                    and (self.Character_QLabel.x() > 0)):
                self.Character_QLabel.setPixmap(self.character_left_img)
                self.Character_QLabel.move(self.Character_QLabel.x() - 20, self.Character_QLabel.y())

            elif ((event.key() == Qt.Key_D)  # "d"키를 누를경우 캐릭터 현재 x값을 +20
                  and (self.Character_QLabel.x() < 1560)):
                self.Character_QLabel.setPixmap(self.character_right_img)
                self.Character_QLabel.move(self.Character_QLabel.x() + 20, self.Character_QLabel.y())

            elif ((event.key() == Qt.Key_W)  # "w"키를 누를경우 캐릭터 현재 y값을 -20
                  and (self.Character_QLabel.y() > -20)):
                self.Character_QLabel.move(self.Character_QLabel.x(), self.Character_QLabel.y() - 20)

            elif ((event.key() == Qt.Key_S)  # "s"키를 누를경우 캐릭터 현재 y값을 +20
                  and (self.Character_QLabel.y() < 740)):
                self.Character_QLabel.move(self.Character_QLabel.x(), self.Character_QLabel.y() + 20)

            else:  # 방향키 이외의 키를 눌렀을때를 위한 예외처리
                rand_event = 999
                return
            lab_x_ = self.Character_QLabel.pos().x()  # 캐릭터의 현재 x값을 구한 후 lab_x_변수에 담음
            lab_y_ = self.Character_QLabel.pos().y()  # 캐릭터의 현재 y값을 구한 후 lab_y_변수에 담음

            if ((self.Character_QLabel.x() >= 0)  # 캐릭터가 다음칸으로 이동했을때 나오는 분기점 및 예외처리
                    and (self.Character_QLabel.x() <= 1580)
                    and (self.Character_QLabel.y() >= 0)
                    and (self.Character_QLabel.y() <= 780)):
                # 확률 33.33%
                if rand_event <= 5:
                    self.Log_textEdit.append("1칸 이동하였습니다.")
                elif rand_event == 6 or rand_event == 7:
                    pass
                    enemy_rand = random.randrange(4)
                    if enemy_rand < 3:

                        self.Log_textEdit.setText("적을 만났습니다.")
                        pass
                        # self.StackWidget_Field.setCurrentIndex(2)
                        # self.MainFrame_Bottom.setEnabled(True)
                        # self.Page_Use.setEnabled(False)
                        # self.StackWidget_Item.setCurrentWidget(self.Page_Use)
                        # self.j = 1
                        # for num in range(1, random.randrange(2, 11)):
                        #     getattr(self, f'Monster_{num}_Name').setText(
                        #         getattr(self, f'nomalfield_fire_monster{self.j}').name)  # 몬스터 이름
                        #     getattr(self, f'Monster_{num}_Name').setStyleSheet("Color : white")
                        #     getattr(self, f'Monster_{num}_QLabel').setPixmap(
                        #         QPixmap(getattr(self, f'nomalfield_fire_monster{self.j}').image))  # 몬스터 이미지
                        #     getattr(self, f'Monster_{num}_QProgressBar').setMaximum(
                        #         getattr(self, f'nomalfield_fire_monster{self.j}').hp)  # 몬스터 체력
                        #     getattr(self, f'Monster_{num}_QProgressBar').setValue(
                        #         getattr(self, f'nomalfield_fire_monster{self.j}').hp)  # 몬스터 체력
                        #     getattr(self, f'Monster_{num}_QButton').setEnabled(False)
                        #     getattr(self, f'Monster_{num}_Name').show()
                        #     getattr(self, f'Monster_{num}_QLabel').show()
                        #     getattr(self, f'Monster_{num}_QButton').show()
                        #     getattr(self, f'Monster_{num}_QProgressBar').show()
                        #     if self.j < 3:
                        #         self.j += 1
                        #     else:
                        #         self.j = 1
                        # self.HoldSwitch = 1  # 스택 위젯 페이지 이동후에도 캐릭터 이동하는 현상 예외처리
                    else:
                        self.Log_textEdit.append("타 수호대를 만났습니다.")
                        # self.StackWidget_Field.setCurrentIndex(2)
                        # self.HoldSwitch = 1  # 스택 위젯 페이지 이동후에도 캐릭터 이동하는 현상 예외처리
                elif rand_event > 7:
                    self.Log_textEdit.append("아이템을 획득하였습니다.")
                    """
                    길준 : 여기를 채워주세요
                    """
            # 왼쪽 상단에 변경된 죄표 값 출력
            self.TopUI_Coordinate_Label.setText(f"x좌표: {lab_x_} y좌표: {lab_y_}")

            # # (미궁 포탈 위치 - 캐릭터 위치)를 절대값으로 만듬 < == 왜 절대값으로 만들죠?
            # if ((abs(self.Potal_QLabel.pos().x() - self.Character_QLabel.pos().x()) < 20)
            #         and (abs(self.Potal_QLabel.pos().y() - self.Character_QLabel.pos().y()) < 20)):
            #     # 미궁 이동
            #     self.StackWidget_Field.setCurrentIndex(1)
            #     self.Log_textEdit.append("포탈을 탔습니다.")  # 미궁 이동시 출력문
            #     self.HoldSwitch = 1  # 스택 위젯 페이지 이동후에도 캐릭터 이동하는 현상 예외처리

            # 일반필드에서 포탈 만났을 때
            if self.Character_QLabel.geometry().intersects(self.portal_sample.geometry()):  # 포탈 만나면
                self.move_to_dungeon()  # 랜덤으로 던전으로 이동

            # 던전입구1일 때

        #던전필드일때
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
                self.Character_QLabel_2.move(self.Character_QLabel_2.x(),
                                             self.Character_QLabel_2.y() - 20)  # 위로 20 이동
            elif event.key() == Qt.Key_S:  # S눌렀을 때
                new_position = self.Character_QLabel_2.geometry().translated(0, 20)
                self.Character_QLabel_2.move(self.Character_QLabel_2.x(),
                                             self.Character_QLabel_2.y() + 20)  # 아래로 20 이동
            else:
                return

            # 좌표 위에 찍어주기
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

            # 15*15 사이즈 맵에 들어갔을 때
            if self.dungeon_number == 1:
                # 던전 벽을 벗어나지 못하게 함
                if not ((self.map_size[1][0] <= new_position.x() <= self.map_size[1][1]) and (
                        self.map_size[1][2] < new_position.y() < self.map_size[1][3])):  # 미궁 x값, 미궁 y값 설정
                    self.Character_QLabel_2.setGeometry(previous_position)
                # 던전 내에 위치한 벽을 벗어나지 못하게 함
                if self.block_dungeon_wall(new_position, previous_position, wall_list, 1):
                    self.Character_QLabel_2.setGeometry(previous_position)

            # 16 * 16 사이즈 맵에 들어갔을 때
            elif self.dungeon_number == 2:
                if not ((self.map_size[2][0] <= new_position.x() <= self.map_size[2][1]) and (
                        self.map_size[2][2] < new_position.y() < self.map_size[2][3])):  # 미궁 x값, 미궁 y값 설정
                    self.Character_QLabel_2.setGeometry(previous_position)
                if self.block_dungeon_wall(new_position, previous_position, wall_list, 2):
                    self.Character_QLabel_2.setGeometry(previous_position)

            # 17 * 17 사이즈 맵에 들어갔을 때
            elif self.dungeon_number == 3:
                if not ((self.map_size[3][0] <= new_position.x() <= self.map_size[3][1]) and (
                        self.map_size[3][2] < new_position.y() < self.map_size[3][3])):  # 미궁 x값, 미궁 y값 설정
                    self.Character_QLabel_2.setGeometry(previous_position)
                if self.block_dungeon_wall(new_position, previous_position, wall_list, 3):
                    self.Character_QLabel_2.setGeometry(previous_position)

            # 18 * 18 사이즈 맵에 들어갔을 때
            elif self.dungeon_number == 4:
                if not ((self.map_size[4][0] <= new_position.x() <= self.map_size[4][1]) and (
                        self.map_size[4][2] < new_position.y() < self.map_size[4][3])):  # 미궁 x값, 미궁 y값 설정
                    self.Character_QLabel_2.setGeometry(previous_position)
                if self.block_dungeon_wall(new_position, previous_position, wall_list, 4):
                    self.Character_QLabel_2.setGeometry(previous_position)

    # # 이외 필드일때(전투일때) pass
    # else:
    #     pass


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
# 여기에 시그널, 설정
# 여기에 함수 설정


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()