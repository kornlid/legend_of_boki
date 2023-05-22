import os
import random
import sys
import time

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
        """클래스 이름"""
        return self.class_name

    def get_charactername(self):
        """캐릭터 이름"""
        return self.character_name

    def get_maxhp(self):
        """max_hp 반환"""
        return self.hp * self.level  # 반환 hp = 기존 hp * level

    def get_nowhp(self):
        """현재 hp"""
        return self.get_maxhp()  # max_hp값 리턴

    def get_level(self):
        """클래스 레벨"""
        return self.level

    def get_maxmp(self):
        """최대 mp"""
        return self.mp * self.level  # mp* 레벨 리턴


class MonsterOption:
    """
    몬스터 상속 클래스: 몬스터 필드/ 이름/ 이미지/ 레벨/ hp/ 공격력
    """

    def __init__(self, field, name, img, level, hp, atk):
        """몬스터 필드/ 이름/ 이미지/ 레벨/ hp/ 공격력"""
        self.field = field
        self.name = name
        self.image = img
        self.level = level
        self.hp = hp
        self.atk = atk

    def get_field(self):
        """소속 필드"""
        return self.field

    def get_name(self):
        """몬스터 이름"""
        return self.name

    def get_image(self):
        """몬스터 이미지"""
        return self.image

    def get_level(self):
        """몬스터 레벨"""
        return self.level

    def get_hp(self):
        """몬스터 체력"""
        return self.hp

    def get_atk(self):
        """몬스터 공격력"""
        return self.atk


class SkillOption:
    """
    스킬 상속 클래스: 이름, 이미지, 데미지 값, 소비mp(스킬마나), 스킬 종류, ??
    """

    def __init__(self, name, img, value, mp, target, turn):
        self.name = name
        self.img = img
        self.value = value
        self.mp = mp
        self.target = target
        self.turn = turn

    def get_name(self):
        """스킬 이름"""
        return self.name

    def get_img(self):
        """스킬 이미지"""
        return self.img

    def get_value(self):
        """스킬 데미지 값"""
        return self.value

    def get_target(self):
        """스킬 종류 구별(버프, 단일, 전체)"""
        return self.target

    def get_mp(self):
        """스킬 마나"""
        return self.mp

    def get_turn(self):
        """몰루<--??오잉"""
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
        self.class_turn = [1, 2, 3, 4, 5]

        # ui 하단 버튼 비활성화
        for i in range(1, 6):
            getattr(self, f'Status{i}_Action1_Attack').setEnabled(False)
            getattr(self, f'Status{i}_Action2_Skill').setEnabled(False)
            getattr(self, f'Status{i}_Action3_Item').setEnabled(False)
            getattr(self, f'Status{i}_Action4_Run').setEnabled(False)

        # 혜빈 코드 취합 본 시작===========================================================================================
        # 해당 인스턴스에 캐릭터 정보 저장
        self.guardLevel = 1

        self.guardoption()  # 캐릭터 생성해줌
        self.StautsHpall = []
        self.StautsMpall = []
        self.Statusclass = []

        # 리스트를 셔플로 돌려줌
        # 위 self.guardoption()에서 생성한 클래스 캐릭터들의 값총 6개-(전체정보/최대hp/최대mp)저장
        random.shuffle(self.list_class)

        # 위에서 섞은 list_class에서 1부터 5까지 가져와 담아줌
        for i in range(1, 6):
            # 빈 리스트에 추가
            self.Statusclass.append(self.list_class[i - 1][0])  # 빈 리스트 Statusclass에 하나씩 전체정보를 append해줌
            self.StautsHpall.append(self.list_class[i - 1][1])  # 빈 리스트 StautsHpall에 하나씩 최대hp를 append해줌
            self.StautsMpall.append(self.list_class[i - 1][1])  # 빈 리스트 StautsMpall에 하나씩 최대mp를 append해줌

            # 하단 ui에 캐릭터 추가
            getattr(self, f'Status{i}_1_Class').setText(self.list_class[i - 1][0].class_name)  # 클래스명 지정
            getattr(self, f'Status{i}_1_Name').setText(self.list_class[i - 1][0].character_name)  # 캐릭터명 지정
            getattr(self, f'Status{i}_2_HpValue').setText(
                str(self.list_class[i - 1][1]) + "/" + str(self.list_class[i - 1][0].get_maxhp()))  # hp(기본 값/변하는 값)
            getattr(self, f'Status{i}_3_MpValue').setText(
                str(self.list_class[i - 1][2]) + "/" + str(self.list_class[i - 1][0].get_maxmp()))  # mp(기본 값/변하는 값)

            # 정렬 및 스타일시트 배경 디자인
            getattr(self, f'Status{i}_2_HpValue').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i}_1_Name').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i}_3_MpValue').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i}_1_Class').setAlignment(Qt.AlignCenter)  # 텍스트 가운데 정렬
            getattr(self, f'Status{i}_1_Class').setStyleSheet('QLabel{background-color:#55aaff;}')  # 클래스 배경 색상 지정
            getattr(self, f'Status{i}_2_Hp').setStyleSheet('QLabel{background-color:#55aaff;}')  # hp, mp 배경 색상 지정
            getattr(self, f'Status{i}_3_Mp').setStyleSheet('QLabel{background-color:#55aaff;}')

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

        # 몬스터 상속 - 몬스터 필드/ 이름/ 이미지/ 레벨/ hp/ 공격력(임시로100)
        self.nomalfield_fire_monster1 = MonsterOption("불의 지역", "불타는 나무정령", "character_1.png", 1,
                                                      random.randrange(200, 1000), 100)
        self.nomalfield_fire_monster2 = MonsterOption("불의 지역", "불의 정령", "character_2.png", 1,
                                                      random.randrange(200, 1000), 100)
        self.nomalfield_fire_monster3 = MonsterOption("불의 지역", "불타는 골렘", "character_3.png", 1,
                                                      random.randrange(200, 1000), 100)
        # 몬스터 담아주기
        self.monsterbox = [self.nomalfield_fire_monster1, self.nomalfield_fire_monster2, self.nomalfield_fire_monster3]

        # 스킬 상속 이후 리턴 값으로 리스트 줌
        self.skillbox()

        ## 임시 캐릭터 설정

        self.character_left_img = QPixmap('character_left.png')  # 캐릭터 왼쪽 이미지
        self.character_right_img = QPixmap('character_right.png')  # 캐릭터 오른쪽 이미지

        ## 배경 및 위젯 설정
        self.back_ground_label.setPixmap(QtGui.QPixmap("용암.png"))  # 임시 일반 필드 배경 이미지
        self.back_ground_label.move(0, -1)  # 배경 위치 조정
        self.Widget_Skill.move(826, -1)  # 전투중 스킬 선택시 생성되는 스킬 위젯 위치
        self.Widget_Skill.hide()  # 위젯창은 숨겨 둠

        # 헤더 프레임 없애고 전체화면으로 띄우기
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        # self.exitAction.triggered.connect(qApp.closeAllWindows) # 게임 종료 이벤트

        self.HoldSwitch = 0
        self.Page_Use_ing.setEnabled(False)  # 캐릭터 세부정보창 비활성화(우측 상단 index-1)
        # self.Page_Equip.setEnabled(False)
        self.Btn_Equip.clicked.connect(lambda y: self.use_uiABC(4))  # 우측 상단 장비 버튼 클릭하면 장비창 이동
        self.Btn_Portion.clicked.connect(lambda y: self.use_uiABC(0))  # 포션버튼 클릭하면 포션 이동
        self.Btn_Status.clicked.connect(lambda y: self.use_uiABC(2))  # 캐릭터 세부 장비 활성화

        # 여기서부터 봐야 함
        for num in range(1, 6):  # 액션버튼 1~4 시그널 슬롯 연결
            getattr(self, f'Status{num}_Action1_Attack').clicked.connect(
                lambda x, y=num: self.nomalact(y))  # 일반공격함수로 연결
            getattr(self, f'Status{num}_Action2_Skill').clicked.connect(self.skillopen)  # 스킬옵션 함수로 연결
            getattr(self, f'Status{num}_Action3_Item').clicked.connect(lambda y: self.use_uiABC(1))

        # 클래스 스킬 버튼들 리스트화 /
        # #미하일 도발스킬 / #루미너스 스킬: 힐, 그레이트힐, 힐올, 공격력업, 방어력업, 맵핵 / #알렉스 스킬: 파이어볼, 파이어월, 블리자드, 썬더브레이커 / # 메르데스 집중타, 듀얼샷, 마스터샷 / #샐리멘더 힐, 그레이트힐, 힐올, 파이어볼 파이어월, 블리자드 썬더브레이커
        self.pushbox = [self.Class1_Skill1_Btn, self.Class2_Skill1_Btn, self.Class2_Skill2_Btn, self.Class2_Skill3_Btn,
                        self.Class2_Skill4_Btn, self.Class2_Skill5_Btn, self.Class2_Skill6_Btn,
                        self.Class3_Skill1_Btn, self.Class3_Skill2_Btn, self.Class3_Skill3_Btn, self.Class3_Skill4_Btn,
                        self.Class4_Skill1_Btn, self.Class4_Skill2_Btn, self.Class4_Skill3_Btn,
                        self.Class4_Skill4_Btn, self.Class4_Skill5_Btn, self.Class4_Skill6_Btn, self.Class4_Skill7_Btn,
                        self.Class5_Skill1_Btn, self.Class5_Skill2_Btn, self.Class5_Skill3_Btn,
                        self.Class6_Skill1_Btn]  # 강타

        # 아이템 사용 버튼 리스트화 및 연결
        self.itemusebox = []  # 아이템을 사용할 부분 담아줌 빈 리스트에
        for btn in range(1, 15):  # 1번부터 14까지 포션 버튼을 리스트에 담아준다.
            self.itemusebox.append(getattr(self, f'Portion_{btn}_Btn'))

        for idx, usebtn in enumerate(self.itemusebox): # 포션버튼 객체가 리스트에 담아진 걸 인덱스, 버튼으로 for문 돌려줌
            usebtn.clicked.connect(lambda x, y=idx + 1: self.itemuse(y)) #만약 버튼이 클릭되면 인덱스 값 가지고 itemuse버튼으로 연결

        # 몬스터 공격 버튼 연결 과정 -=================================================-
        self.actbtnbox = [] # 빈 리스트에 몬스터 공격버튼 담아줌
        for i in range(1, 11): # 1부터 10번까지 리스트에 공격버튼 객체 담아준다
            self.actbtnbox.append(getattr(self, f'Monster_{i}_QButton'))

        for idx, actbtn in enumerate(self.actbtnbox): # 몬스터 공격버튼 누르면
            actbtn.clicked.connect(lambda x, y=idx + 1: self.atktype(y))

        # 몬스터 공격 버튼 연결 과정 -=================================================-끝
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
            self.TopUI_Map_Label.setText("숲의 지역")

        elif random_spot == 2:  # 불의 지역 스폰 장소
            self.Character_QLabel.setPixmap(self.character_left_img)
            self.Character_QLabel.move(360, 40)
            self.TopUI_Map_Label.setText("불의 지역")

        elif random_spot == 3:  # 눈의 지역 스폰 장소
            self.Character_QLabel.setPixmap(self.character_left_img)
            self.Character_QLabel.move(1280, 20)
            self.TopUI_Map_Label.setText("눈의 지역")
        elif random_spot == 4:  # 물의 지역 스폰 장소
            self.Character_QLabel.setPixmap(self.character_left_img)
            self.Character_QLabel.move(1320, 540)
            self.TopUI_Map_Label.setText("물의 지역")

        # 왼쪽 상단에 초기 죄표 값 출력
        self.TopUI_Coordinate_Label.setText(
            f"x좌표: {self.Character_QLabel.pos().x()} y좌표: {self.Character_QLabel.pos().y()}")

    # 혜빈 파일 함수===================================================================================================시작
    def guardoption(self):
        """캐릭터 생성 및 hp/mp 저장"""
        self.class_1 = Status('전사', '미하일', 300, 0, self.guardLevel)
        self.class_2 = Status('백법사', '루미너스', 200, 150, self.guardLevel)
        self.class_3 = Status('흑법사', '알렉스', 200, 150, self.guardLevel)
        self.class_4 = Status('적법사', '샐러맨더', 150, 150, self.guardLevel)
        self.class_5 = Status('궁수', '메르데스', 150, 150, self.guardLevel)
        self.class_6 = Status('검사', '랜슬롯', 150, 150, self.guardLevel)

        self.class1_nowhp = self.class_1.get_maxhp()
        self.class2_nowhp = self.class_2.get_maxhp()
        self.class3_nowhp = self.class_3.get_maxhp()
        self.class4_nowhp = self.class_4.get_maxhp()
        self.class5_nowhp = self.class_5.get_maxhp()
        self.class6_nowhp = self.class_6.get_maxhp()

        self.class1_nowmp = self.class_1.get_maxmp()
        self.class2_nowmp = self.class_2.get_maxmp()
        self.class3_nowmp = self.class_3.get_maxmp()
        self.class4_nowmp = self.class_4.get_maxmp()
        self.class5_nowmp = self.class_5.get_maxmp()
        self.class6_nowmp = self.class_6.get_maxmp()
        self.list_class = [[self.class_1, self.class1_nowhp, self.class1_nowmp],
                           [self.class_2, self.class2_nowhp, self.class2_nowmp],
                           [self.class_3, self.class3_nowhp, self.class3_nowmp],
                           [self.class_4, self.class4_nowhp, self.class4_nowmp],
                           [self.class_5, self.class5_nowhp, self.class5_nowmp],
                           [self.class_6, self.class6_nowhp, self.class6_nowmp]]
        return self.list_class

    # def skillwidgetreset(self):
    def battleclear(self):
        """몬스터 전부 처치 이후 버튼 클리어 함수"""
        for object in self.pushbox:
            object.setChecked(False)
        for actbtn in self.actbtnbox:
            actbtn.setEnabled(False)
        for i in range(1, 6):
            getattr(self, f'Status{i}_Action1_Attack').setEnabled(False)
            getattr(self, f'Status{i}_Action2_Skill').setEnabled(False)
            getattr(self, f'Status{i}_Action3_Item').setEnabled(False)
            getattr(self, f'Status{i}_Action4_Run').setEnabled(False)
        for i in self.frame_class_list:
            i.setEnabled(True)

    # self.Monster_1_QButton.setUpdatesEnabled(True)
    # 공격 타입에 따른 데미지 방식

    def atktype(self, typenum):
        # 스킬 공격시 적 데미지 입는 로직
        if self.attackType == 1: # 공격 타입이 1이라면
            self.skillact(typenum) # 몬스터에게 공격
        # 일반 공격시 적 데미지 입는 로직
        elif self.attackType == 0: # 공격 타입이 0이라면
            #몬스터의 체력이 1보다 클 경우 프로그레스 바에 표시
            if getattr(self, f'Monster_{typenum}_QProgressBar').value() > self.choice_btn: #여기서부터 이해가 안되기 시작한다.
                getattr(self, f'Monster_{typenum}_QProgressBar').setValue(
                    getattr(self, f'Monster_{typenum}_QProgressBar').value() - self.choice_btn)
                self.Log_textEdit.append(
                    getattr(self, f'Monster_{typenum}_Name').text() + "에게 %d만큼 피해를 입혔습니다." % self.choice_btn)
            #몬스터의 체력이
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
                return self.battleclear()
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
        for rockbtn in self.actbtnbox:
            rockbtn.setEnabled(False)
        self.user_turn += 1

        if self.user_turn >= len(self.frame_class_list):  # 6번 돌리면 초기화 해줌 if self.user_turn >= 6:
            self.Monster_Turn()
            self.user_turn = 0

        for idx, FCS in enumerate(self.frame_class_list):  # 턴에 따른 버튼 활성화
            if self.user_turn == idx:
                FCS.setEnabled(True)
                # elif self.class_turn[idx-1] == 1:
                #     FCS.setEnabled(False)
                # print('유저 활성화')
                for btn in range(1, len(self.frame_class_list) + 1):  # 턴 변경에 따른 하단 ui 버튼 모두 활성화
                    getattr(self, f'Status{btn}_Action1_Attack').setEnabled(True)
                    getattr(self, f'Status{btn}_Action1_Attack').setStyleSheet('')  # 버튼 스타일 디폴트로 다시 변경
                    getattr(self, f'Status{btn}_Action2_Skill').setEnabled(True)
                    getattr(self, f'Status{btn}_Action2_Skill').setStyleSheet('')
                    getattr(self, f'Status{btn}_Action3_Item').setEnabled(True)
                    getattr(self, f'Status{btn}_Action3_Item').setStyleSheet('')
                    getattr(self, f'Status{btn}_Action4_Run').setEnabled(True)
                    getattr(self, f'Status{btn}_Action4_Run').setStyleSheet('')
                    # self.user_turn += 1
                    # self.btn_clicked = -1 #멀까요
            else:
                # self.user_turn += 1
                FCS.setEnabled(False)

                # print('유저 비활성화')

            # self.mon_Turn() #몬스터 버튼 비활성화
            # self.portion_reset()

    def Monster_Turn(self):
        self.num = 0
        self.guardoption()
        self.monlifecnt = 0  # 존재하는 몬스터 마리수
        for num in range(1, 11):
            if getattr(self, f'Monster_{num}_Name').text() != "":
                for monster in self.monsterbox:  # 몬스터들의 이름 리스트 [self.nomalfield_fire_monster1, self.nomalfield_fire_monster2, self.nomalfield_fire_monster3]
                    if monster.name == getattr(self, f'Monster_{num}_Name').text():
                        self.classnum = random.randrange(1, 6)
                        if self.StautsHpall[self.classnum - 1] > monster.atk:
                            self.StautsHpall[self.classnum - 1] = self.StautsHpall[self.classnum - 1] - monster.atk
                            getattr(self, f'Status{self.classnum}_2_HpValue').setText(
                                str(self.StautsHpall[self.classnum - 1]) + "/" + str(
                                    self.Statusclass[self.classnum - 1].get_maxhp()))
                            self.Log_textEdit.append("%s이 %s에게 데미지를 %d만큼 입혔습니다." % (
                            monster.name, getattr(self, f'Status{self.classnum}_1_Name').text(), monster.atk))
                        else:
                            self.Log_textEdit.append(
                                "%s가 사망하였습니다." % getattr(self, f'Status{self.classnum}_1_Name').text())
                            getattr(self, f'Status{self.classnum}_2_HpValue').setText(
                                "0" + "/" + str(self.Statusclass[self.classnum - 1].get_maxhp()))
                            if self.classnum - 1 < len(self.frame_class_list):
                                self.class_list = self.frame_class_list.pop(self.classnum - 1)
                                print(self.class_list)
                            else:
                                print("벗어난 인덱스:", self.classnum - 1)
                            # self.class_list = self.frame_class_list.pop(self.classnum-1)
                            # print(self.class_list)
                            # continue

    # 혜빈 파일 함수===================================================================================================끝끝
    # 혜빈 파일 함수===================================================================================================끝끝
    # 혜빈 파일 함수===================================================================================================끝끝

    # 소연 임시 함수 =================

    def set_actions_enabled(self, status_count, enabled):
        """클래스 프레임 활성화/비활성화 시키기"""
        for i in range(1, status_count + 1):
            getattr(self, f'Status{i}_Action1_Attack').setEnabled(enabled)
            getattr(self, f'Status{i}_Action2_Skill').setEnabled(enabled)
            getattr(self, f'Status{i}_Action3_Item').setEnabled(enabled)
            getattr(self, f'Status{i}_Action4_Run').setEnabled(enabled)

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
                                                               aspectRatioMode=Qt.IgnoreAspectRatio))  # 이미지 고정

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

        print('던전번호는', random_dungeon_num)  # 확인용

        # 던전 사이즈에 따라 다르게 이동
        if random_dungeon_num == 1:  # 15*15 던전일 때
            self.dungeon_number = 1  # 키프레스가 인식해야할 값에 1로 넣어줌
            self.dungeon_img_label.setPixmap(dungeon_img_1)
            self.Character_QLabel_2.move(592, 631)  # 캐릭터 던전 입구로 보내기
        elif random_dungeon_num == 2:  # 16*16 던전일 때
            self.dungeon_number = 2
            self.dungeon_img_label.setPixmap(dungeon_img_2)
            self.Character_QLabel_2.move(567, 644)  # 캐릭터 던전 입구로 보내기
        elif random_dungeon_num == 3:  # 17*17 던전일 때
            self.dungeon_number = 3
            self.dungeon_img_label.setPixmap(dungeon_img_3)
            self.Character_QLabel_2.move(558, 657)  # 캐릭터 던전 입구로 보내기
        elif random_dungeon_num == 4:  # 18*18 던전일 때
            self.dungeon_number = 4
            self.dungeon_img_label.setPixmap(dungeon_img_4)
            self.Character_QLabel_2.move(504, 674)  # 캐릭터 던전 입구로 보내기

        # 던전 입구 만들기
        self.Show_Dungeon_Entrance(random_dungeon_num)

    def Show_Dungeon_Entrance(self, map_num):
        """던전 입구 랜덤으로 만들어주는 함수"""

        # 미궁 버튼 임시로 만들어주기
        self.entrance = QLabel(self)
        self.entrance.setText("미궁")  # 임시지정(이미지 씌우기는 나중에)
        self.entrance.setFixedSize(30, 30)  # 임시 라벨 크기 지정
        self.entrance.setStyleSheet('background-color: blue')  # 임시 라벨 색 지정
        self.entrance.move(random.randint(self.map_size[map_num][0], self.map_size[map_num][1]),
                           random.randint(self.map_size[map_num][2], self.map_size[map_num][3]))  # 던전 15*15 사이즈
        self.entrance.show()  # 미궁 띄우기

        # 보스 몬스터 위치 임시로 만들어주기
        self.boss_monster = QLabel(self)  # 보스 몬스터 나타날 포탈 임시
        self.boss_monster.setText("몬스터")
        self.boss_monster.setFixedSize(30, 30)  # 임시 라벨크기지정
        self.boss_monster.setStyleSheet('background-color: red')  # 임시로 빨간색으로
        self.boss_monster.move(random.randint(self.map_size[map_num][0], self.map_size[map_num][1]),
                               random.randint(self.map_size[map_num][2], self.map_size[map_num][3]))  # 보스 몬스터 랜덤으로 등장
        self.boss_monster.show()  # 보스몬스터 띄우기

        # 검은 라벨 만들어서 위에 덮기(유저가 플레이할 때 던전이 안보이게)
        black_label = QLabel(self)
        black_label.move(0, 30)
        black_label.setStyleSheet('background-color: rgba(0, 0, 0, 100)')  # 100으로 설정되어 있는 투명도 높이면 어두워짐
        black_label.setFixedSize(1580, 780)  # 사이즈고정
        black_label.show()

    def block_dungeon_wall(self, new_position, previous_position, wall_list, num):
        """유저가 던전벽에서 나아가지 못하게 하기"""
        for key, value in wall_list.items():
            if key == num:  # 특정 던전 사이즈일때
                for i in value:  # 딕셔너리 내 리스트 x, y값 가져와서 비교(self.wall_list 검색해보면 됨)
                    if i[0] < new_position.x() < i[1] and i[2] < new_position.y() < i[3]:  # 벽 x, y값 사이에 들어가면
                        self.Character_QLabel_2.setGeometry(previous_position)  # 이전 위치로 이동
                        return True  # True 반환
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

        # 유령라벨 새 포지션으로 옮기기
        self.ghost_label.move(new_x, new_y)

    # 소연 함수 끝 ==========================================================================================================

    def skillbox(self):
        """
        스킬 상속 이후 리턴 값으로 리스트 줌
        :return:
        """

        # SkillOption 클래스: 이름, 이미지, 데미지 값, 소비mp(스킬마나), 스킬 종류(0-버프, 1-단일, 2-전체), ??
        self.skill_1 = SkillOption("힐", None, random.randrange(30, 70), 10, 0, 1)
        self.skill_2 = SkillOption("그레이트 힐", None, random.randrange(60, 100), 20, 0, 1)
        self.skill_3 = SkillOption("힐 올", None, random.randrange(40, 80), 10, 0, 1)
        self.skill_4 = SkillOption("공격력 Up", None, random.randrange(30, 70), 10, 0, 1)
        self.skill_5 = SkillOption("방어력 Up", None, random.randrange(30, 70), 10, 0, 1)
        self.skill_6 = SkillOption("맵 핵", None, 0, 0, 1, 1)

        self.skill_7 = SkillOption("파이어 볼", "검사버프스킬 모션-1.gif", 300, 10, 1, 1)
        self.skill_8 = SkillOption("파이어 월", None, random.randrange(400, 600), 10, 2, 1)
        self.skill_9 = SkillOption("썬더브레이커", None, random.randrange(400, 500), 10, 2, 1)
        self.skill_10 = SkillOption("블리자드", None, random.randrange(900, 1200), 10, 2, 1)

        self.skill_11 = SkillOption("집중타", None, random.randrange(200, 500), 10, 1, 1)
        self.skill_12 = SkillOption("듀얼 샷", None, random.randrange(400, 600), 10, 1, 1)
        self.skill_13 = SkillOption("마스터 샷", None, random.randrange(500, 700), 10, 1, 1)

        self.skill_14 = SkillOption("강타", None, random.randrange(20, 500), 10, 1, 1)
        self.skill_15 = SkillOption("도발", None, 0, 10, 3, 1)
        self.skillall = [self.skill_1, self.skill_3, self.skill_4, self.skill_5, self.skill_6,
                         self.skill_7, self.skill_8, self.skill_9, self.skill_10, self.skill_11,
                         self.skill_12, self.skill_13, self.skill_14, self.skill_15]

        # 스킬들을 담아서 return 해줌
        return self.skillall

    def nomalact(self, num):
        """일반공격 함수"""
        self.attackType = 0  # 공격타입 0
        self.choice_btn = num * 10  # 이건뭐니
        for actbtn in self.actbtnbox:  # 공격할 몬스터 pushButton담긴 리스트
            actbtn.setEnabled(True)

    def skillopen(self):
        """클래스가 스킬함수버튼 클릭했을 때"""
        self.attackType = 1  # 공격타입 1
        self.Widget_Skill.show()  # 스킬위젯 창 띄워주기
        for rockbtn in self.pushbox:
            rockbtn.setEnabled(True)
        for idx, skillbtn in enumerate(self.pushbox):
            skillbtn.clicked.connect(lambda x, y=idx + 1: self.btnname(y))

    def skillact(self, btn):
        """몬스터에게 공격하는 함수"""
        # self.skillbox()
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
                        self.Log_textEdit.append("%s을 처치하였습니다." % getattr(self, f'Monster_{btn}_Name').text())
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
                # 전사 스킬 이벤트
                elif ((skill.name == self.choice_btn)
                      and (skill.target == 3)):
                    self.Log_textEdit.append("아무일도 없었다..")
                    time.sleep(.5)

                self.Widget_Skill.close()
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
                    return self.battleclear()
            self.user_Turn()

    # self.choice_btn에 해당하는 버튼의 스킬 이름을 담는 함수
    def btnname(self, obnum):
        for skillbtn in self.pushbox:
            skillbtn.disconnect()

        self.dict_skillname = {1: "힐", 2: "그레이트 힐", 3: "힐 올", 4: "공격력 업", 5: "방어력 업", 6: "맵핵", 7: "파이어 볼", 8: "파이어 월",
                               9: "블리자드", 10: "썬더브레이커", 11: "힐", 12: "그레이트 힐", 13: "힐 올", 14: "파이어 볼", 15: "파이어 월",
                               16: "블리자드", 17: "썬더브레이커", 18: "집중타", 19: "듀얼 샷", 20: "마스터 샷", 21: "강타", 22: "도발"}
        self.choice_btn = self.dict_skillname[obnum]

        for skill in self.skillall:
            if skill.name == self.choice_btn and skill.target == 0:
                for actbtn in self.actbtnbox:
                    actbtn.setEnabled(False)
            if skill.name == self.choice_btn and skill.target >= 1:
                for actbtn in self.actbtnbox:
                    actbtn.setEnabled(True)
        self.Log_textEdit.append(self.pushbox[obnum - 1].text() + "을(를) 선택하셨습니다.")
        for rockbtn in self.pushbox:
            rockbtn.setEnabled(False)

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

    # 상황에 따른 ui 선택 활성화 여부
    def use_uiABC(self, num):
        """0:소비아이템창/ 1:소비아이템활성화/ 2:캐릭터세부창비활성화/ 3:캐릭터세부창활성화/ 4:장비창이동"""
        if num == 0:  # 소비아이템 창
            self.StackWidget_Item.setCurrentIndex(0)
        elif num == 1:  # 소비아이템 활성화
            """전투시 아이템 버튼을 클릭하면 사용할수있는 소비아이템들이 활성화됨"""
            self.Page_Use.setEnabled(True)
            for btn in range(1, 11):
                getattr(self, f'Portion_{btn}_Btn').setEnabled(True)
            self.StackWidget_Item.setCurrentIndex(0)
        elif num == 2:  # 캐릭터 세부창 비활성화

            self.Page_Use_ing.setEnabled(False)
            self.StackWidget_Item.setCurrentIndex(1)
        elif num == 3:  # 캐릭터 세부창 활성화
            self.Page_Use_ing.setEnabled(True)
            self.StackWidget_Item.setCurrentIndex(1)
        elif num == 4:  # 장비창 이동
            self.StackWidget_Item.setCurrentIndex(2)

    def itemuse(self, num):
        """아이템 선택시 발동되는 함수"""

        self.Log_textEdit.append(getattr(self, f'Portion_{num}_Btn').text()) # 상태창에 어떤 버튼 클릭했는지 보여줌
        # 아이템 취합시 추가 로직 해야됨
        # 아이템 취합시 추가 로직 해야됨
        # 아이템 취합시 추가 로직 해야됨
        # 아이템 취합시 추가 로직 해야됨
        # 아이템 취합시 추가 로직 해야됨

    # 하단 ui 버튼 클릭 시 다른 버튼 비활성화 함수 =========================================================================================
    def change(self, get):
        if get == '1':
            self.Log_textEdit.append("일반 공격을 선택하였습니다.")
            for i in range(5):
                getattr(self, f'Status{i + 1}_Action1_Attack').setEnabled(True)
                getattr(self, f'Status{i + 1}_Action2_Skill').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action3_Item').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action4_Run').setDisabled(True)
        elif get == '2':
            self.Log_textEdit.append("스킬 공격을 선택하였습니다.")
            for i in range(5):
                getattr(self, f'Status{i + 1}_Action1_Attack').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action2_Skill').setEnabled(True)
                getattr(self, f'Status{i + 1}_Action3_Item').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action4_Run').setDisabled(True)
        elif get == '3':
            self.Log_textEdit.append("아이템 사용을 선택하셨습니다.")
            for i in range(5):
                getattr(self, f'Status{i + 1}_Action1_Attack').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action2_Skill').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action3_Item').setEnabled(True)
                getattr(self, f'Status{i + 1}_Action4_Run').setDisabled(True)
        elif get == '4':
            self.Log_textEdit.append("도망을 선택하였습니다.")
            self.Class1_DetailsStatus_ConditionValue.setText("방어중")
            for i in range(5):
                getattr(self, f'Status{i + 1}_Action1_Attack').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action2_Skill').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action3_Item').setDisabled(True)
                getattr(self, f'Status{i + 1}_Action4_Run').setEnabled(True)

    # def defensemode(self):
    # 123123123123123123
    # 캐릭터 방향키로 움직이기===============================================================================================
    # 캐릭터 방향키로 움직이기===============================================================================================
    # 캐릭터 방향키로 움직이기===============================================================================================
    def keyPressEvent(self, event):

        # 소연 keypressevent 함수 내 수정(current_index값 받아오기)===========================================================

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

                        """
                        적을 만났을때 설정값
                        """
                        # # 아이템 사용시 전체 트루로 만들어줘야해요 그래야 꺼졌을때 다시 켜지니까
                        # for usebtn in self.itemusebox:
                        #     usebtn.setEnabled(True)

                        self.user_turn = 0  # 유저 턴 중간에 끝나면 초기화 안된상태로 넘어감 그래서 예외처리함
                        self.user_turn = 0  # 유저 턴 중간에 끝나면 초기화 안된상태로 넘어감 그래서 예외처리함

                        for rockbtn in self.frame_class_list:
                            rockbtn.setEnabled(True)
                        self.portal_sample.hide()
                        # 인벤토리 ui를 소비창으로 변경
                        self.StackWidget_Item.setCurrentWidget(self.Page_Use)

                        # 인벤토리 선택 버튼 및 소비 아이템 버튼 비활성화
                        self.Btn_Equip.setEnabled(False)
                        self.Btn_Portion.setEnabled(False)
                        self.Btn_Status.setEnabled(False)

                        # 소비 아이템 클릭 비활성화
                        for btn in range(1, 15):
                            getattr(self, f'Portion_{btn}_Btn').setEnabled(False)
                        # 하단 ui 버튼 클릭 시 다른 버튼 비활성화 시키기
                        # 1번 턴만 활성화 나머지 비활성화
                        getattr(self, f'Status{1}_Action1_Attack').setEnabled(True)
                        getattr(self, f'Status{1}_Action2_Skill').setEnabled(True)
                        getattr(self, f'Status{1}_Action3_Item').setEnabled(True)
                        getattr(self, f'Status{1}_Action4_Run').setEnabled(True)

                        for btn in range(1, 6):  # 추후 삭제 대상
                            getattr(self, f'Status{btn}_Action1_Attack').clicked.connect(lambda: self.change('1'))
                            getattr(self, f'Status{btn}_Action2_Skill').clicked.connect(lambda: self.change('2'))
                            getattr(self, f'Status{btn}_Action3_Item').clicked.connect(lambda: self.change('3'))
                            getattr(self, f'Status{btn}_Action4_Run').clicked.connect(lambda: self.change('4'))

                        # 캐릭터 창 초기 [0] 빼고 비활성화 상태
                        for FCS in self.frame_class_list[1:]:
                            FCS.setEnabled(False)

                        skills = {'미하일': 1, '루미너스': 2, '알렉스': 3, '샐러맨더': 4, '메르데스': 5,
                                  '랜슬롯': 6}  # 각 이름에 대한 인덱스를 찾아서 람다 함수 내에서 스킬 버튼을 연결
                        name_text = self.Status1_1_Name.text()
                        name_text2 = self.Status2_1_Name.text()
                        name_text3 = self.Status3_1_Name.text()
                        name_text4 = self.Status4_1_Name.text()
                        name_text5 = self.Status5_1_Name.text()
                        self.Status1_Action2_Skill.clicked.connect(
                            lambda x, index=skills.get(name_text): self.skill_btn(index))
                        self.Status2_Action2_Skill.clicked.connect(
                            lambda x, index=skills.get(name_text2): self.skill_btn(index))
                        self.Status3_Action2_Skill.clicked.connect(
                            lambda x, index=skills.get(name_text3): self.skill_btn(index))
                        self.Status4_Action2_Skill.clicked.connect(
                            lambda x, index=skills.get(name_text4): self.skill_btn(index))
                        self.Status5_Action2_Skill.clicked.connect(
                            lambda x, index=skills.get(name_text5): self.skill_btn(index))

                        # 몬스터 랜덤 등장 구현
                        self.j = 1
                        for num in range(1, random.randrange(2, 11)):
                            getattr(self, f'Monster_{num}_Name').setText(
                                getattr(self, f'nomalfield_fire_monster{self.j}').name)  # 몬스터 이름
                            getattr(self, f'Monster_{num}_Name').setStyleSheet("Color : white")
                            getattr(self, f'Monster_{num}_QLabel').setPixmap(
                                QPixmap(getattr(self, f'nomalfield_fire_monster{self.j}').image))  # 몬스터 이미지
                            getattr(self, f'Monster_{num}_QProgressBar').setMaximum(
                                getattr(self, f'nomalfield_fire_monster{self.j}').hp)  # 몬스터 체력
                            getattr(self, f'Monster_{num}_QProgressBar').setValue(
                                getattr(self, f'nomalfield_fire_monster{self.j}').hp)  # 몬스터 체력
                            getattr(self, f'Monster_{num}_QButton').setEnabled(False)
                            getattr(self, f'Monster_{num}_Name').show()
                            getattr(self, f'Monster_{num}_QLabel').show()
                            getattr(self, f'Monster_{num}_QButton').show()
                            getattr(self, f'Monster_{num}_QProgressBar').show()
                            if self.j < 3:
                                self.j += 1
                            else:
                                self.j = 1

                        self.StackWidget_Field.setCurrentIndex(2)
                        self.Page_Use.setEnabled(False)

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
