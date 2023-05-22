import os
import random
import sys

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import uic, Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt, QByteArray, QSize, QTimer

from maingame import Ui_Maingame as game


class Status:
    """
    직업 상속 클래스
    """

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
    """
    몬스터 상속 클래스
    """

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
    """
    스킬 상속 클래스
    """

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


class WindowClass(QMainWindow, game):
    """
    메인 게임 진행
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 공격 타입 구분 초기 설정값
        self.attackType = 0

        # 유저 턴 구분 초기 설정값
        self.user_turn = 0

        # ui 하단 버튼 비활성화
        for i in range(1, 6):
            getattr(self, f'Status{i}_Action1_Attack').setEnabled(False)
            getattr(self, f'Status{i}_Action2_Skill').setEnabled(False)
            getattr(self, f'Status{i}_Action3_Item').setEnabled(False)
            getattr(self, f'Status{i}_Action4_Run').setEnabled(False)

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
            getattr(self, f'Status{i + 1}_1_Class').setText(list_class[i].class_name)  # 클래스명 지정
            getattr(self, f'Status{i + 1}_1_Class').setAlignment(Qt.AlignCenter)  # 텍스트 가운데 정렬
            getattr(self, f'Status{i + 1}_1_Class').setStyleSheet('QLabel{background-color:#55aaff;}')  # 클래스 배경 색상 지정
            getattr(self, f'Status{i + 1}_1_Name').setText(list_class[i].character_name)  # 캐릭터명 지정
            getattr(self, f'Status{i + 1}_1_Name').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i + 1}_2_HpValue').setText(
                str(list_class[i].hp) + "/" + str(list_class[i].get_hp()))  # hp(기본 값/변하는 값)
            getattr(self, f'Status{i + 1}_2_HpValue').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i + 1}_3_MpValue').setText(
                str(list_class[i].mp) + "/" + str(list_class[i].get_mp()))  # mp(기본 값/변하는 값)
            getattr(self, f'Status{i + 1}_3_MpValue').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i + 1}_2_Hp').setStyleSheet('QLabel{background-color:#55aaff;}')  # hp, mp 배경 색상 지정
            getattr(self, f'Status{i + 1}_3_Mp').setStyleSheet('QLabel{background-color:#55aaff;}')

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

        # 임시로 포탈 하나 만들기
        self.portal_sample = QLabel(self)
        self.portal_sample.setFixedSize(40, 40)
        self.portal_sample.setText("포탈")
        self.portal_sample.setStyleSheet('background-color: blue')
        self.portal_sample.show()
        self.portal_sample.move(random.randint(0, 1580), random.randint(0, 760))  # 포탈 위치 랜덤으로 배정

        # 던전필드에 던전 이미지 들어갈 라벨 만들기
        self.dungeon_img_label = QLabel(self.Page_Dungeon_Field)  # 던전필드에 던전이미지 들어갈 라벨 추가, 던전필드를 부모로 설정
        self.dungeon_img_label.setGeometry(0, 0, 1580, 780)
        self.dungeon_img_label.show()

        # 유령 이미지 불러오기
        self.ghost_img_top = QPixmap('./ghost_img/ghost_top.png')  # 귀신 이미지 상
        self.ghost_img_right = QPixmap('./ghost_img/ghost_right.png')  # 우
        self.ghost_img_left = QPixmap('./ghost_img/ghost_left.png')  # 좌
        self.ghost_img_bottom = QPixmap('./ghost_img/ghost_bottom.png')  # 하
        self.ghost_img_right_top = QPixmap('./ghost_img/ghost_right_top.png')  # 우상
        self.ghost_img_left_top = QPixmap('./ghost_img/ghost_left_top.png')  # 좌상
        self.ghost_img_left_bottom = QPixmap('./ghost_img/ghost_left_bottom.png')  # 좌하
        self.ghost_img_right_bottom = QPixmap('./ghost_img/ghost_right_bottom.png')  # 좌하
        self.random_num = 1  # 유령 움직임 초기설정

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

        # 던전 맵 사이즈(크기별)
        self.map_size = {
            1: [529, 1049, 129, 649],  # 맵 1번 x시작, x끝, y시작, y끝
            2: [505, 1063, 115, 664],  # 맵 2번 x시작, x끝, y시작, y끝
            3: [491, 1088, 91, 688],  # 맵 3번 x시작, x끝, y시작, y끝
            4: [475, 1104, 73, 703],  # 맵 4번 x시작, x끝, y시작, y끝
        }

        # 던전맵 벽 값 지정
        self.wall_list = {
            1: [(530, 631, 383, 397),  # 던전 맵 1
                (650, 670, 455, 657),
                (871, 885, 127, 320),
                (800, 1051, 449, 470), ],
            2: [(781, 798, 108, 322),  # 던전 맵 2
                (502, 935, 451, 470)],
            3: [(490, 708, 395, 417),  # 던전 맵 3
                (694, 708, 401, 518),
                (871, 887, 440, 696),
                (870, 885, 89, 306),
                (872, 953, 295, 307)],
            4: [(475, 545, 311, 430),  # 던전 맵 4
                (675, 720, 526, 535),
                (650, 691, 207, 537),
                (675, 939, 206, 219),
                (904, 940, 204, 536),
                (894, 940, 526, 538),
                (928, 1109, 384, 397), ]
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
        self.skillbox()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        # self.exitAction.triggered.connect(qApp.closeAllWindows) # 게임 종    료 이벤트
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
        self.Btn_Equip.clicked.connect(lambda y: self.use_uiABC(4))
        self.Btn_Portion.clicked.connect(lambda y: self.use_uiABC(0))
        self.Btn_Status.clicked.connect(lambda y: self.use_uiABC(2))

        for num in range(1, 6):  # 액션버튼 1~4 시그널 슬롯 연결
            getattr(self, f'Status{num}_Action1_Attack').clicked.connect(lambda x, y=num: self.nomalact(y))
            getattr(self, f'Status{num}_Action2_Skill').clicked.connect(self.skillopen)
            getattr(self, f'Status{num}_Action3_Item').clicked.connect(lambda y: self.use_uiABC(1))

        self.pushbox = [self.Class2_Skill1_Btn, self.Class2_Skill2_Btn, self.Class2_Skill3_Btn, self.Class2_Skill4_Btn,
                        self.Class2_Skill5_Btn, self.Class2_Skill6_Btn, self.Class3_Skill1_Btn, self.Class3_Skill2_Btn,
                        self.Class3_Skill3_Btn, self.Class3_Skill4_Btn, self.Class4_Skill1_Btn, self.Class4_Skill2_Btn,
                        self.Class4_Skill3_Btn, self.Class4_Skill4_Btn, self.Class4_Skill5_Btn, self.Class4_Skill6_Btn,
                        self.Class4_Skill7_Btn, self.Class5_Skill1_Btn, self.Class5_Skill2_Btn, self.Class5_Skill3_Btn,
                        self.Class6_Skill1_Btn]

        # 몬스터 공격 버튼 연결 과정 -=================================================-
        self.actbtnbox = []
        for i in range(1, 11):
            self.actbtnbox.append(getattr(self, f'Monster_{i}_QButton'))

        for idx, actbtn in enumerate(self.actbtnbox):
            actbtn.clicked.connect(lambda x, y=idx + 1: self.atktype(y))

        # 몬스터 공격 버튼 연결 과정 -=================================================-끝
        self.Skill_exit_Btn.clicked.connect(self.Widget_Skill.close)
        for btn in self.actbtnbox:
            btn.hide()

        self.progressBarbox = self.frame_2.findChildren(QProgressBar)
        for pro in self.progressBarbox:
            pro.hide()

        self.choice_btn = 1
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
    # def skillwidgetreset(self):

    # self.Monster_1_QButton.setUpdatesEnabled(True)
    # 공격 타입에 따른 데미지 방식
    def atktype(self, typenum):
        # 스킬 공격시 적 데미지 입는 로직
        if self.attackType == 1:
            self.skillact(typenum)
            self.user_Turn()

        #일반 공격시 적 데미지 입는 로직
        elif self.attackType == 0:
            if getattr(self, f'Monster_{typenum}_QProgressBar').value() > self.choice_btn:
                getattr(self, f'Monster_{typenum}_QProgressBar').setValue(
                    getattr(self, f'Monster_{typenum}_QProgressBar').value() - self.choice_btn)
                self.Log_textEdit.append(
                    getattr(self, f'Monster_{typenum}_Name').text() + "에게 %d만큼 피해를 입혔습니다." % self.choice_btn)
            elif getattr(self, f'Monster_{typenum}_QProgressBar').value() < self.choice_btn:
                if getattr(self, f'Monster_{typenum}_QProgressBar').value() < self.choice_btn:
                    getattr(self, f'Monster_{typenum}_QLabel').hide()
                    getattr(self, f'Monster_{typenum}_QButton').hide()
                    getattr(self, f'Monster_{typenum}_Name').hide()
                    getattr(self, f'Monster_{typenum}_QProgressBar').hide()
                    self.Log_textEdit.append("%s을 처치하였습니다." % getattr(self, f'Monster_{typenum}_Name').text())
                    getattr(self, f'Monster_{typenum}_Name').setText("")
            self.cnt = 0
            for i in range(1, 11):
                if getattr(self, f'Monster_{i}_Name').text() == "":
                    self.cnt += 1
                if self.cnt == 10:
                    self.Log_textEdit.setText("몬스터를 전부 처치하여 필드로 돌아왔습니다.")
                    self.Log_textEdit.append("보상 : 경험치 50exp")
                    self.StackWidget_Field.setCurrentIndex(0)
                    self.HoldSwitch = 0
                    self.cnt = 0
            for object in self.pushbox:
                object.setChecked(False)
            for actbtn in self.actbtnbox:
                actbtn.setEnabled(False)
            self.user_Turn()


    # 해당 직업의 스킬만 열리게하는 함수
    def skill_btn(self, index_):
        # self.Widget_Skill.show()
        frames = [
            self.Frame_Class1,
            self.Frame_Class2,
            self.Frame_Class3,
            self.Frame_Class4,
            self.Frame_Class5,
            self.Frame_Class6
        ]
        for idx, frame in enumerate(frames):
            if idx == index_ - 1:
                frame.setEnabled(True)  # 해당 스킬 프레임만 활성화
            else:
                frame.setEnabled(False)  # 그 이외는 비활성화

    # 유저 턴 넘기는 함수
    def user_Turn(self):  # 몬스터 공격 버튼 눌렀을 때 함수

        self.user_turn += 1

        if self.user_turn >= len(self.frame_class_list):  # 6번 돌리면 초기화 해줌 if self.user_turn >= 6:
            self.user_turn = 0

        for idx, FCS in enumerate(self.frame_class_list):  # 턴에 따른 버튼 활성화
            if self.user_turn == idx:
                FCS.setEnabled(True)
                # print('유저 활성화')
                for btn in range(1, 6):  # 턴 변경에 따른 하단 ui 버튼 모두 활성화
                    getattr(self, f'Status{btn}_Action1_Attack').setEnabled(True)
                    getattr(self, f'Status{btn}_Action1_Attack').setStyleSheet('')  # 버튼 스타일 디폴트로 다시 변경
                    getattr(self, f'Status{btn}_Action2_Skill').setEnabled(True)
                    getattr(self, f'Status{btn}_Action2_Skill').setStyleSheet('')
                    getattr(self, f'Status{btn}_Action3_Item').setEnabled(True)
                    getattr(self, f'Status{btn}_Action3_Item').setStyleSheet('')
                    getattr(self, f'Status{btn}_Action4_Run').setEnabled(True)
                    getattr(self, f'Status{btn}_Action4_Run').setStyleSheet('')
                    self.btn_clicked = -1
            else:
                FCS.setEnabled(False)
                # print('유저 비활성화')

            # self.mon_Turn()
            # self.portion_reset()

    # 혜빈 파일 함수===================================================================================================끝끝
    # 혜빈 파일 함수===================================================================================================끝끝
    # 혜빈 파일 함수===================================================================================================끝끝

    # 소연 파일 함수 시작===============================================================================================시작시작
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

        # 유령 크기 고정해주기
        self.ghost_fixed_size = 100

        # 던전에서 돌아다닐 유령 담길 라벨 만들어주기
        self.ghost_label = QLabel(self.Page_Dungeon_Field)
        self.ghost_label.setPixmap(self.ghost_img_right.scaled(QSize(self.ghost_fixed_size, self.ghost_fixed_size),
                                                               aspectRatioMode=Qt.IgnoreAspectRatio)) #이미지 고정

        # 유령 방향 타이머
        self.position = QTimer()
        self.position.setInterval(3000)
        self.position.timeout.connect(self.direction)
        self.position.start()

        # 유령 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_label)
        self.timer.start(40)

        # 던전 랜덤으로 가는 부분
        random_dungeon_num = random.randint(1, 4)

        # 유령 위치 던전 내로 고정하기
        self.ghost_label.move(
            random.randint(self.map_size[random_dungeon_num][0], self.map_size[random_dungeon_num][1]),
            random.randint(self.map_size[random_dungeon_num][2], self.map_size[random_dungeon_num][3]))

        # 유령 라벨 show()시키기
        self.ghost_label.show()

        print('던전번호는', random_dungeon_num) # 확인용

        # 던전 사이즈에 따라 다르게 이동
        if random_dungeon_num == 1: #15*15 던전일 때
            self.dungeon_number = 1  # 키프레스가 인식해야할 값에 1로 넣어줌
            self.dungeon_img_label.setPixmap(dungeon_img_1)
            self.Character_QLabel_2.move(592, 631)  # 캐릭터 던전 입구로 보내기
        elif random_dungeon_num == 2: #16*16 던전일 때
            self.dungeon_number = 2
            self.dungeon_img_label.setPixmap(dungeon_img_2)
            self.Character_QLabel_2.move(567, 644)  # 캐릭터 던전 입구로 보내기
        elif random_dungeon_num == 3: #17*17 던전일 때
            self.dungeon_number = 3
            self.dungeon_img_label.setPixmap(dungeon_img_3)
            self.Character_QLabel_2.move(558, 657)  # 캐릭터 던전 입구로 보내기
        elif random_dungeon_num == 4: #18*18 던전일 때
            self.dungeon_number = 4
            self.dungeon_img_label.setPixmap(dungeon_img_4)
            self.Character_QLabel_2.move(504, 674)  # 캐릭터 던전 입구로 보내기

        # 던전 입구 만들기
        self.Show_Dungeon_Entrance(random_dungeon_num)

    def Show_Dungeon_Entrance(self, map_num):
        """던전 입구 랜덤으로 만들어주는 함수"""

        # 미궁 버튼 임시로 만들어주기
        self.entrance = QLabel(self)
        self.entrance.setText("미궁") #임시지정(이미지 씌우기는 나중에)
        self.entrance.setFixedSize(30, 30)  # 임시 라벨 크기 지정
        self.entrance.setStyleSheet('background-color: blue') #임시 라벨 색 지정
        self.entrance.move(random.randint(self.map_size[map_num][0], self.map_size[map_num][1]),
                           random.randint(self.map_size[map_num][2], self.map_size[map_num][3]))  # 던전 15*15 사이즈
        self.entrance.show() #미궁 띄우기

        # 보스 몬스터 위치 임시로 만들어주기
        self.boss_monster = QLabel(self)  # 보스 몬스터 나타날 포탈 임시
        self.boss_monster.setText("몬스터")
        self.boss_monster.setFixedSize(30, 30)  # 임시 라벨크기지정
        self.boss_monster.setStyleSheet('background-color: red')  # 임시로 빨간색으로
        self.boss_monster.move(random.randint(self.map_size[map_num][0], self.map_size[map_num][1]),
                               random.randint(self.map_size[map_num][2], self.map_size[map_num][3]))  # 보스 몬스터 랜덤으로 등장
        self.boss_monster.show() #보스몬스터 띄우기

        # 검은 라벨 만들어서 위에 덮기(유저가 플레이할 때 던전이 안보이게)
        # black_label = QLabel(self)
        # black_label.move(0, 30)
        # black_label.setStyleSheet('background-color: rgba(0, 0, 0, 100)')  # 100으로 설정되어 있는 투명도 높이면 어두워짐
        # black_label.setFixedSize(1580, 720) #사이즈고정
        # black_label.show()

    def block_dungeon_wall(self, new_position, previous_position, wall_list, num):
        """유저가 던전벽에서 나아가지 못하게 하기"""
        for key, value in wall_list.items():
            if key == num: #특정 던전 사이즈일때
                for i in value: #딕셔너리 내 리스트 x, y값 가져와서 비교(self.wall_list 검색해보면 됨)
                    if i[0] < new_position.x() < i[1] and i[2] < new_position.y() < i[3]: #벽 x, y값 사이에 들어가면
                        self.Character_QLabel_2.setGeometry(previous_position) #이전 위치로 이동
                        return True #True 반환
        return False

    def show_messagebox(self, text):
        """특정 문구 메세지박스 띄워주기"""
        reply = QMessageBox()
        reply.setText(text)
        reply.exec_()

    def direction(self):
        """유령 방향 랜덤으로 지정 및 변환"""

        # 랜덤값 따라 방향지정
        self.random_num = random.randint(1, 6)

        # 랜덤값 따라 이미지 변환
        if self.random_num == 1:  # 우하
            self.ghost_label.setPixmap(
                self.ghost_img_right_bottom.scaled(QSize(self.ghost_fixed_size, self.ghost_fixed_size),
                                                   aspectRatioMode=Qt.IgnoreAspectRatio))
        elif self.random_num == 2:  # 우상
            self.ghost_label.setPixmap(
                self.ghost_img_right_top.scaled(QSize(self.ghost_fixed_size, self.ghost_fixed_size),
                                                aspectRatioMode=Qt.IgnoreAspectRatio))
        elif self.random_num == 3:  # 좌상
            self.ghost_label.setPixmap(
                self.ghost_img_left_top.scaled(QSize(self.ghost_fixed_size, self.ghost_fixed_size),
                                               aspectRatioMode=Qt.IgnoreAspectRatio))
        elif self.random_num == 4:  # 좌하
            self.ghost_label.setPixmap(
                self.ghost_img_left_bottom.scaled(QSize(self.ghost_fixed_size, self.ghost_fixed_size),
                                                  aspectRatioMode=Qt.IgnoreAspectRatio))
        elif self.random_num == 5:  # 왼쪽
            self.ghost_label.setPixmap(self.ghost_img_left.scaled(QSize(self.ghost_fixed_size, self.ghost_fixed_size),
                                                                  aspectRatioMode=Qt.IgnoreAspectRatio))
        elif self.random_num == 6:  # 오른쪽
            self.ghost_label.setPixmap(self.ghost_img_right.scaled(QSize(self.ghost_fixed_size, self.ghost_fixed_size),
                                                                   aspectRatioMode=Qt.IgnoreAspectRatio))

    def move_label(self):
        """유령 움직임 조정 함수"""

        # 현재 라벨 포지션 받기
        current_pos = self.ghost_label.pos()

        # x, y값 조정
        x_start = self.map_size[self.dungeon_number][0]
        x_end = self.map_size[self.dungeon_number][1]
        y_start = self.map_size[self.dungeon_number][2]
        y_end = self.map_size[self.dungeon_number][3]

        # 새 위치 변수 초기화
        new_x = current_pos.x()
        new_y = current_pos.y()

        # 새 위치 계산
        if self.random_num == 1:  # 우하
            new_x = min(current_pos.x() + 1, x_end)
            new_y = min(current_pos.y() + 1, y_end)
        elif self.random_num == 2:  # 우상
            new_x = min(current_pos.x() + 1, x_end)
            new_y = max(current_pos.y() - 1, y_start)
        elif self.random_num == 3:  # 좌상
            new_x = max(current_pos.x() - 1, x_start)
            new_y = max(current_pos.y() - 1, y_start)
        elif self.random_num == 4:  # 좌하
            new_x = max(current_pos.x() - 1, x_start)
            new_y = min(current_pos.y() + 1, y_end)
        elif self.random_num == 5:  # 왼쪽
            new_x = max(current_pos.x() - 1, x_start)
            new_y = current_pos.y()
        elif self.random_num == 6:  # 오른쪽
            new_x = min(current_pos.x() + 1, x_end)
            new_y = current_pos.y()

        #이 부분은 굳이인것 같아서 일단 주석처리함

        # elif self.random_num == 7:  # 상
        #     self.ghost_label.setPixmap(self.ghost_img_top.scaled(QSize(self.ghost_fixed_size, self.ghost_fixed_size), aspectRatioMode=Qt.IgnoreAspectRatio))
        #     new_x = current_pos.x()
        #     new_y = max(current_pos.y() - 1, y_start)
        # else:  # 하
        #     self.ghost_label.setPixmap(
        #         self.ghost_img_bottom.scaled(QSize(self.ghost_fixed_size, self.ghost_fixed_size), aspectRatioMode=Qt.IgnoreAspectRatio))
        #     new_x = current_pos.x()
        #     new_y = min(current_pos.y() + 1, y_end)

        # 유령라벨 새 포지션으로 옮기기
        self.ghost_label.move(new_x, new_y)

    # 소연 함수 끝 ==========================================================================================================

    def skillbox(self):
        """
        스킬 상속 이후 리턴 값으로 리스트 줌
        :return:
        """
        self.skill_1 = SkillOption("힐", None, random.randrange(30, 70), 10, 0, 1)
        self.skill_2 = SkillOption("그레이트 힐", None, random.randrange(60, 100), 20, 0, 1)
        self.skill_3 = SkillOption("힐 올", None, random.randrange(40, 80), 10, 0, 1)
        self.skill_4 = SkillOption("공격력 Up", None, random.randrange(30, 70), 10, 0, 1)
        self.skill_5 = SkillOption("방어력 Up", None, random.randrange(30, 70), 10, 0, 1)
        self.skill_6 = SkillOption("맵 핵", None, 0, 0, 1, 1)

        self.skill_7 = SkillOption("파이어 볼", "검사버프스킬 모션-1.gif", 30, 10, 1, 1)
        self.skill_8 = SkillOption("파이어 월", None, random.randrange(40, 60), 10, 2, 1)
        self.skill_9 = SkillOption("썬더브레이커", None, random.randrange(400, 500), 10, 2, 1)
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
        return self.skillall

    def nomalact(self, num):
        self.attackType = 0
        self.choice_btn = num*100
        for actbtn in self.actbtnbox:
            actbtn.setEnabled(True)

    def skillopen(self):
        self.attackType = 1
        self.Widget_Skill.show()
        for idx, skillbtn in enumerate(self.pushbox):
            skillbtn.clicked.connect(lambda x, y=idx + 1: self.btnname(y))

    def skillact(self, btn):
        self.skillbox()
        if len(self.choice_btn) != 0:
            for skill in self.skillall:
                if ((skill.name == self.choice_btn)
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
                        self.Log_textEdit.dappend("%s을 처치하였습니다." % getattr(self, f'Monster_{btn}_Name').text())
                        getattr(self, f'Monster_{btn}_Name').setText("")
                elif ((skill.name == self.choice_btn)
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
                for object in self.pushbox:
                    object.setChecked(False)
                self.Widget_Skill.close()
                for actbtn in self.actbtnbox:
                    actbtn.setEnabled(False)

    # self.choice_btn에 해당하는 버튼의 스킬 이름을 담는 함수
    def btnname(self, obnum):
        for skillbtn in self.pushbox:
            skillbtn.disconnect()
        self.dict_skillname = {1: "힐", 2: "그레이트 힐", 3: "힐 올", 4: "공격력 업", 5: "방어력 업", 6: "맵핵", 7: "파이어 볼", 8: "파이어 월",
                               9: "블리자드", 10: "썬더브레이커", 11: "힐", 12: "그레이트 힐", 13: "힐 올", 14: "파이어 볼", 15: "파이어 월",
                               16: "블리자드", 17: "썬더브레이커", 18: "집중타", 19: "듀얼 샷", 20: "마스터 샷", 21: "강타"}
        self.choice_btn = self.dict_skillname[obnum]
        for skill in self.skillall:
            if skill.target == 0:
                for actbtn in self.actbtnbox:
                    actbtn.setEnabled(False)
            elif skill.target >= 1:
                for actbtn in self.actbtnbox:
                    actbtn.setEnabled(True)

        # skillname_dict

        # if btn.clicked:
        #     self.choice_btn.append(self.pushbox.pop(self.pushbox.index(btn)))
        #     for hold in self.pushbox:
        #         hold.setEnabled(False)
        #             self.Log_textEdit.append(str(self.choice_btn[0]))
        #             for skill in self.skillall:
        #                 if self.choice_btn[0].text() == skill.name and skill.target == 0:
        #                     for act in self.actbtnbox:
        #                         act.setEnabled(False)
        #                 elif self.choice_btn[0].text() == skill.name and skill.target <= 2:
        #                     for act in self.actbtnbox:
        #                         act.setEnabled(True)
        # else:
        #     self.pushbox.append(self.choice_btn.pop(0))
        #     for hold in self.pushbox:
        #         hold.setEnabled(True)
        #     for act in self.actbtnbox:
        #         act.setEnabled(False)

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

    # 하단 ui 버튼 클릭 시 다른 버튼 비활성화 함수 =========================================================================================
    def change(self, get):
        if get == '1':
            for i in range(5):
                getattr(self, f'Status{i + 1}_Action1_Attack').setEnabled(True)
                getattr(self, f'Status{i + 1}_Action2_Skill').setEnabled(False)
                getattr(self, f'Status{i + 1}_Action3_Item').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action4_Run').setDisabled(True)
        elif get == '2':
            for i in range(5):
                getattr(self, f'Status{i + 1}_Action1_Attack').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action2_Skill').setEnabled(True)
                getattr(self, f'Status{i + 1}_Action3_Item').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action4_Run').setDisabled(True)
        elif get == '3':
            for i in range(5):
                getattr(self, f'Status{i + 1}_Action1_Attack').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action2_Skill').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action3_Item').setEnabled(True)
                getattr(self, f'Status{i + 1}_Action4_Run').setDisabled(True)
        elif get == '4':
            for i in range(5):
                getattr(self, f'Status{i + 1}_Action1_Attack').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action2_Skill').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action3_Item').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action4_Run').setEnabled(True)

    # 캐릭터 방향키로 움직이기===============================================================================================
    # 캐릭터 방향키로 움직이기===============================================================================================
    # 캐릭터 방향키로 움직이기===============================================================================================
    def keyPressEvent(self, event):

        #소연 keypressevent 함수 내 수정(current_index값 받아오기)===========================================================

        # 현재 스택위젯 값 가져오기
        current_index = self.StackWidget_Field.currentIndex()

        ## 일반필드일 때
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


                elif rand_event <= 7:
                    self.HoldSwitch = 1  # 스택 위젯 페이지 이동후에도 캐릭터 이동하는 현상 예외처리
                    enemy_rand = random.randrange(4)
                    if enemy_rand < 3:
                        self.Log_textEdit.setText("적을 만났습니다.")
                        pass # 테스트 위한 pass

                        # """
                        # 적을 만났을때 설정값
                        # """
                        # # 인벤토리 ui를 소비창으로 변경
                        # self.StackWidget_Item.setCurrentWidget(self.Page_Use)
                        #
                        # # 인벤토리 선택 버튼 및 소비 아이템 버튼 비활성화
                        # self.Btn_Equip.setEnabled(False)
                        # self.Btn_Portion.setEnabled(False)
                        # self.Btn_Status.setEnabled(False)
                        #
                        # # 소비 아이템 클릭 비활성화
                        # for btn in range(1, 15):
                        #     getattr(self, f'Portion_{btn}_Btn').setEnabled(False)
                        #
                        # # 1번 턴만 활성화 나머지 비활성화
                        # getattr(self, f'Status{1}_Action1_Attack').setEnabled(True)
                        # getattr(self, f'Status{1}_Action2_Skill').setEnabled(True)
                        # getattr(self, f'Status{1}_Action3_Item').setEnabled(True)
                        # getattr(self, f'Status{1}_Action4_Run').setEnabled(True)
                        #
                        # skills = {'미하일': 1, '루미너스': 2, '알렉스': 3, '샐러맨더': 4, '메르데스': 5,
                        #           '랜슬롯': 6}  # 각 이름에 대한 인덱스를 찾아서 람다 함수 내에서 스킬 버튼을 연결
                        # name_text = self.Status1_1_Name.text()
                        # name_text2 = self.Status2_1_Name.text()
                        # name_text3 = self.Status3_1_Name.text()
                        # name_text4 = self.Status4_1_Name.text()
                        # name_text5 = self.Status5_1_Name.text()
                        # self.Status1_Action2_Skill.clicked.connect(
                        #     lambda x, index=skills.get(name_text): self.skill_btn(index))
                        # self.Status2_Action2_Skill.clicked.connect(
                        #     lambda x, index=skills.get(name_text2): self.skill_btn(index))
                        # self.Status3_Action2_Skill.clicked.connect(
                        #     lambda x, index=skills.get(name_text3): self.skill_btn(index))
                        # self.Status4_Action2_Skill.clicked.connect(
                        #     lambda x, index=skills.get(name_text4): self.skill_btn(index))
                        # self.Status5_Action2_Skill.clicked.connect(
                        #     lambda x, index=skills.get(name_text5): self.skill_btn(index))
                        #
                        # # 하단 ui 버튼 클릭 시 다른 버튼 비활성화 시키기
                        # for btn in range(1, 6):
                        #     getattr(self, f'Status{btn}_Action1_Attack').clicked.connect(lambda: self.change('1'))
                        #     getattr(self, f'Status{btn}_Action2_Skill').clicked.connect(lambda: self.change('2'))
                        #     getattr(self, f'Status{btn}_Action3_Item').clicked.connect(lambda: self.change('3'))
                        #     getattr(self, f'Status{btn}_Action4_Run').clicked.connect(lambda: self.change('4'))
                        #
                        # # 몬스터 랜덤 등장 구현
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
                        #
                        # self.StackWidget_Field.setCurrentIndex(2)
                        # self.Page_Use.setEnabled(False)

                    else:
                        self.Log_textEdit.append("타 수호대를 만났습니다.")
                        self.HoldSwitch = 0  # 추후 수정 : 수호대는 아직 설정안해놔서 걸리면 다시 움직일수있게 홀드스위치 0으로 돌림
                        # self.StackWidget_Field.setCurrentIndex(2)
                        # self.HoldSwitch = 1  # 스택 위젯 페이지 이동후에도 캐릭터 이동하는 현상 예외처리


                elif rand_event > 7:
                    self.Log_textEdit.append("아이템을 획득하였습니다.")
                    """
                    길준 : 여기를 채워주세요
                    """
            # 왼쪽 상단에 변경된 죄표 값 출력
            self.TopUI_Coordinate_Label.setText(f"x좌표: {lab_x_} y좌표: {lab_y_}")

            # (미궁 포탈 위치 - 캐릭터 위치)를 절대값으로 만듬 <= 왜 절대값으로 만들죠?!?!
            ## 임시 주석처리
            # if ((abs(self.Potal_QLabel.pos().x() - self.Character_QLabel.pos().x()) < 20)
            #         and (abs(self.Potal_QLabel.pos().y() - self.Character_QLabel.pos().y()) < 20)):
            #     # 미궁 이동
            #     self.StackWidget_Field.setCurrentIndex(1)
            #     self.Log_textEdit.append("포탈을 탔습니다.")  # 미궁 이동시 출력문
            #     self.HoldSwitch = 1  # 스택 위젯 페이지 이동후에도 캐릭터 이동하는 현상 예외처리

            # 일반필드에서 포탈 만났을 때
            if self.Character_QLabel.geometry().intersects(self.portal_sample.geometry()):  # 포탈 만나면
                self.move_to_dungeon()  # 랜덤으로 던전으로 이동

        ## 던전필드일때
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

            if self.Character_QLabel_2.geometry().intersects(self.boss_monster.geometry()):
                # 던전에서 몬스터 만났을 때 전투 이동
                self.show_messagebox("보스몬스터를 만났습니다!\n전투에 진입합니다.")
                # 전투로 스택위젯 이동
                # 전투함수로 이동
                self.user_can_enter_dungeon = True  # 전투에서 이기면 상태 True로 만들어주기

            # 던전에서 미궁 만났을 때 메세지 출력(임시) -> 코드 합치면 메세지 뜬 후 전투상황으로 이동하도록 하기
            if self.Character_QLabel_2.geometry().intersects(
                    self.entrance.geometry()) and self.user_can_enter_dungeon == True:
                self.show_messagebox("미궁을 만났습니다!")

            # 던전 벽 캐릭터가 벗어나지 못하게

            # 15*15 사이즈 맵에 들어갔을 때
            if self.dungeon_number == 1:
                # 던전 벽을 벗어나지 못하게 함
                if not ((self.map_size[1][0] <= new_position.x() <= self.map_size[1][1]) and (
                        self.map_size[1][2] < new_position.y() < self.map_size[1][3])):  # 미궁 x값, 미궁 y값 설정
                    self.Character_QLabel_2.setGeometry(previous_position)
                # 던전 내에 위치한 벽을 벗어나지 못하게 함
                if self.block_dungeon_wall(new_position, previous_position, self.wall_list, 1):
                    self.Character_QLabel_2.setGeometry(previous_position)

            # 16 * 16 사이즈 맵에 들어갔을 때
            elif self.dungeon_number == 2:
                if not ((self.map_size[2][0] <= new_position.x() <= self.map_size[2][1]) and (
                        self.map_size[2][2] < new_position.y() < self.map_size[2][3])):  # 미궁 x값, 미궁 y값 설정
                    self.Character_QLabel_2.setGeometry(previous_position)
                if self.block_dungeon_wall(new_position, previous_position, self.wall_list, 2):
                    self.Character_QLabel_2.setGeometry(previous_position)

            # 17 * 17 사이즈 맵에 들어갔을 때
            elif self.dungeon_number == 3:
                if not ((self.map_size[3][0] <= new_position.x() <= self.map_size[3][1]) and (
                        self.map_size[3][2] < new_position.y() < self.map_size[3][3])):  # 미궁 x값, 미궁 y값 설정
                    self.Character_QLabel_2.setGeometry(previous_position)
                if self.block_dungeon_wall(new_position, previous_position, self.wall_list, 3):
                    self.Character_QLabel_2.setGeometry(previous_position)

            # 18 * 18 사이즈 맵에 들어갔을 때
            elif self.dungeon_number == 4:
                if not ((self.map_size[4][0] <= new_position.x() <= self.map_size[4][1]) and (
                        self.map_size[4][2] < new_position.y() < self.map_size[4][3])):  # 미궁 x값, 미궁 y값 설정
                    self.Character_QLabel_2.setGeometry(previous_position)
                if self.block_dungeon_wall(new_position, previous_position, self.wall_list, 4):
                    self.Character_QLabel_2.setGeometry(previous_position)

        # # 이외 필드일때(전투일때) pass
        # else:
        #     pass
        else:
            return


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