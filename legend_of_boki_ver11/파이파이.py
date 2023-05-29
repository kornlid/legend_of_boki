import os
import random
import sys
import time

# from PyQt5.QtWidgets import *
# from PyQt5 import QtWidgets
# from PyQt5 import uic, Qt
# from PyQt5 import QtGui
# from PyQt5.QtGui import QPixmap, QMovie, QFontDatabase, QFont, QColor
# from PyQt5.QtCore import Qt, QByteArray, QSize, QTimer, QPropertyAnimation, QPoint
# from PyQt5 import QtCore
# from PyQt5.QtWidgets import *
from PyQt5 import uic, Qt, QtGui, QtWidgets
# from PyQt5.QtGui import QPixmap, QMovie, QFontDatabase, QFont
# from PyQt5.QtCore import * #Qt, QByteArray, QSize, QTimer
from PyQt5.Qt import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


from maingame import Ui_Maingame as game
from opening import Ui_MainWindow

class Boki_Opening(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # # 전체화면으로 재생
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(1920, 1080)
        # self.showFullScreen()
        self.setCentralWidget(QWidget())
        self.setupUi(self)
        self.opening()

        self.start_btn.clicked.connect(self.btn_start)
        self.end_btn.clicked.connect(lambda :self.close())

    def opening(self):
        self.label = self.logo
        # 불투명도 이펙트 객체 생성
        self.opacityeffect = QGraphicsOpacityEffect()
        self.opacityeffect.setOpacity(1)
        self.label.setGraphicsEffect(self.opacityeffect)

        self.animation = QPropertyAnimation(self.opacityeffect, b'opacity')
        self.animation.setDuration(3500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def btn_start(self):
        self.close()    # 메인 윈도우 닫기

        self.videoplayer = VideoPlayer()
        self.videoplayer.show()

class VideoPlayer_Closing(QWidget):
    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        videoItem = QGraphicsVideoItem()
        # videoItem.setWindowFlag(Qt.FramelessWindowHint)
        videoItem.setSize(QSizeF(self.width(), self.height()))
        scene = QGraphicsScene(self)
        scene.addItem(videoItem)
        graphicsView = QGraphicsView(scene)
        layout = QVBoxLayout()
        layout.addWidget(graphicsView)
        self.setLayout(layout)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(videoItem)

        # stateChanged 시그널 연결
        self.mediaPlayer.stateChanged.connect(self.handleStateChanged)

        self.load()
        self.mediaPlayer.play()

    def keyPressEvent(self, e):
        # """단축키"""
        # print('state: ' + str(self.mediaPlayer.state()))
        # print('mediaStatus: ' + str(self.mediaPlayer.mediaStatus()))
        # print('error: ' + str(self.mediaPlayer.error()))
        # if e.key() == Qt.Key_L: # L키는 로드
        #     print('loading')
        #     self.load()
        # if e.key() == Qt.Key_P: # P키는 플레잉
        #     print('playing')
        #     self.mediaPlayer.play()
        if e.key() == Qt.Key_Q: # Q키 누르면 종료
            self.close()

        else:
            return

    def load(self):
        """wmv 파일 로드하기"""
        local = QUrl.fromLocalFile('./video/boki_endingcredits.wmv')
        media = QMediaContent(local)
        self.mediaPlayer.setMedia(media)

    def handleStateChanged(self, state):
        """비디오가 종료되면 화면도 꺼지게 하는 함수"""
        if state == QMediaPlayer.StoppedState:
            self.close()


class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        videoItem = QGraphicsVideoItem()
        # videoItem.setWindowFlag(Qt.FramelessWindowHint)
        videoItem.setSize(QSizeF(self.width(), self.height()))
        scene = QGraphicsScene(self)
        scene.addItem(videoItem)
        graphicsView = QGraphicsView(scene)
        layout = QVBoxLayout()
        layout.addWidget(graphicsView)
        self.setLayout(layout)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(videoItem)

        # stateChanged 시그널 연결
        self.mediaPlayer.stateChanged.connect(self.handleStateChanged)

        self.load()
        self.mediaPlayer.play()

    def keyPressEvent(self, e):
        # """단축키"""
        # print('state: ' + str(self.mediaPlayer.state()))
        # print('mediaStatus: ' + str(self.mediaPlayer.mediaStatus()))
        # print('error: ' + str(self.mediaPlayer.error()))
        # if e.key() == Qt.Key_L: # L키는 로드
        #     print('loading')
        #     self.load()
        # if e.key() == Qt.Key_P: # P키는 플레잉
        #     print('playing')
        #     self.mediaPlayer.play()
        if e.key() == Qt.Key_Q: # Q키 누르면 종료
            self.close()

        else:
            return

    def load(self):
        """wmv 파일 로드하기"""
        local = QUrl.fromLocalFile('./video/boki_prologue.wmv')
        media = QMediaContent(local)
        self.mediaPlayer.setMedia(media)

    def handleStateChanged(self, state):
        """비디오가 종료되면 화면도 꺼지게 하는 함수"""
        if state == QMediaPlayer.StoppedState:
            self.close()

    # def main_start(self):
    #     self.windowclass = self.WindowClass()
    #     self.windowclass.show()

    def closeEvent(self, event):
        QTimer.singleShot(1000, lambda: myWindow_2.show())  # 2초뒤에 창 열기
        # myWindow_2.show()
        event.accept()


class Status:
    """
    직업 상속 클래스
    """

    def __init__(self, class_name, character_name, hp, mp, level, class_img):
        self.class_name = class_name
        self.character_name = character_name
        self.hp = hp
        self.mp = mp
        self.level = level
        self.class_img = class_img

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

    def get_image(self):
        """캐릭터 이미지"""
        return self.class_img


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
    스킬 상속 클래스: 이름, 이미지, 데미지 값, 소비mp(스킬마나), 스킬 종류, 사용 턴, 제한 레벨
    """

    def __init__(self, name, img, value, mp, target, turn, rockonlevel):
        self.name = name
        self.img = img
        self.value = value
        self.mp = mp
        self.target = target
        self.turn = turn
        self.rockonlevel = rockonlevel

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
        """스킬 사용 턴"""
        return self.turn

    def get_rockonlevel(self):
        return self.rockonlevel

class ItemMain:
    """ 아이템 상속 클래스(부모)"""
    def __init__(self, item_name):
        super().__init__()

        self.name = item_name

    def get_name(self):
        return self.name


class Equipment(ItemMain):
    """ 장비 아이템 상속 클래스"""
    def __init__(self, name, img,item_location):
        super().__init__(name)

        self.location = item_location
        self.img = img

    def get_item_location(self):
        return self.location

class Weapon(Equipment):
    """ 무기 아이템 상속 클래스"""
    def __init__(self, name, img, location, weapon_damage):
        super().__init__(name, img, location)

        self.damage = weapon_damage

    def get_weapon_damage(self):
        return self.damage

class Armor(Equipment):
    """ 장비 아이템 상속 클래스"""
    def __init__(self, name, img, location, armor_defence):
        super().__init__(name, img, location)

        self.armor = armor_defence

    def get_armor_defence(self):
        return self.armor


class Consumable(ItemMain):
    """ 소비 아이템 상속 클래스"""
    def __init__(self, name, recovery, stack):
        super().__init__(name)
        self.recovery = recovery
        self.stack = stack

    def get_recovery_value(self):
        return self.recovery

    def get_stack(self):
        return self.stack




class WindowClass(QMainWindow, game):
    """
    메인 게임 진행
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 소연 파일 취합 2차 =========================================================================================================

        self.dungeon_floor = 1 #던전 층수 세는 변수
        self.battle_cnt = 0 # 총 경기횟수 세는 변수(일반필드)
        self.battle_cnt_for_dungeon = 0 # 총 경기횟수 세는 변수(던전필드)
        self.StackWidget_Item.setCurrentWidget(self.Page_Equip)
        # 클래스 값 넣어줄 리스트 mp / hp
        self.class_hp_mp_present_value_list = [
            [self.Status1_2_HpValue, self.Status1_3_MpValue],
            [self.Status2_2_HpValue, self.Status2_3_MpValue],
            [self.Status3_2_HpValue, self.Status3_3_MpValue],
            [self.Status4_2_HpValue, self.Status4_3_MpValue],
            [self.Status5_2_HpValue, self.Status5_3_MpValue],
        ]
        self.make_effect_list()

        self.class_label_list = [self.Class_1_QLabel, self.Class_2_QLabel, self.Class_3_QLabel, self.Class_4_QLabel,
                                 self.Class_5_QLabel]
        # QFont 객체를 만든다.
        # font = QFont('Neo둥근모', 12)
        font_style = 'font-family: Neo둥근모;'
        self.setStyleSheet(font_style)

        # 유저가 보스 만났을 때 보스 캐릭터 열림
        self.user_meet_boss = False

        # 유저는 보스를 이길 때까지 던전에 입장하지 못함
        self.user_can_enter_dungeon = False

        # 랜덤 던전 스팟 번호
        self.dungeon_number = 0

        # 처음 게임 시작했을 때 시작 화면 보여주기
        # self.StackWidget_Field.setCurrentIndex(0)  # 일반필드로 이동

        # 임시로 포탈 하나 만들기
        self.portal_sample = QLabel(self)
        # self.Qmovi = QMovie("./image/mingungpotal.gif")
        #2023.05.25 07.54
        self.movie = QMovie("./image/mingungpotal.gif", QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)

        self.portal_sample.setMovie(self.movie)
        self.portal_sample.setFixedSize(100, 100)
        self.movie.start()

        # QLabel에 동적 이미지 삽입

        # self.portal_sample.setStyleSheet('background-color: blue')
        self.portal_sample.move(random.randint(0, 1580), random.randint(0, 760))  # 포탈 위치 랜덤으로 배정

        # 던전필드에 던전 이미지 들어갈 라벨 만들기
        self.dungeon_img_label = QLabel(self.Page_Dungeon_Field)  # 던전필드에 던전이미지 들어갈 라벨 추가, 던전필드를 부모로 설정
        self.dungeon_img_label.setGeometry(0, 0, 1580, 780)
        self.dungeon_img_label.show()

        # 유령 이미지 불러오기
        self.ghost_img_top = QPixmap('./image/ghost_img/ghost_top.png')  # 귀신 이미지 상
        self.ghost_img_right = QPixmap('./image/ghost_img/ghost_right.png')  # 우
        self.ghost_img_left = QPixmap('./image/ghost_img/ghost_left.png')  # 좌
        self.ghost_img_bottom = QPixmap('./image/ghost_img/ghost_bottom.png')  # 하
        self.ghost_img_right_top = QPixmap('./image/ghost_img/ghost_right_top.png')  # 우상
        self.ghost_img_left_top = QPixmap('./image/ghost_img/ghost_left_top.png')  # 좌상
        self.ghost_img_left_bottom = QPixmap('./image/ghost_img/ghost_left_bottom.png')  # 좌하
        self.ghost_img_right_bottom = QPixmap('./image/ghost_img/ghost_right_bottom.png')  # 좌하
        self.random_num = 1  # 유령 움직임 초기설정

        #라벨 이미지 가져오기
        self.mark_img = QPixmap('./image/mark.png')

        # 느낌표 담을 라벨 만들어주기
        self.mark_label = QLabel(self)
        self.mark_label.setPixmap(self.mark_img.scaled(QSize(50, 50), aspectRatioMode=Qt.IgnoreAspectRatio))
        self.mark_label.setStyleSheet('background-color: transparent')
        self.mark_label.hide()

        # 응답 상태(동시다발적으로 유령만날 때마다 메세지 뜨지 않게)
        self.reply_state = False

        # 이스터에그 리스트
        self.msg_sample_list = {
            1: "그거 아시나요? 우리반에는 점심시간만 되면 배드민턴을 하는 사람들이 있다고 합니다.",
            2: "그거아시나요? 개발원 식당에서 나오는 라면은 물 70퍼 스프 30퍼로 구성되어있습니다.",
            3: "그거 아시나요? 옆팀 팀장님 >시연< 은 가위손 스킬을 지녔습니다.",
            4: "아이템 Hp(소)는 Hp(소) 만큼의 회복량을 가지고있습니다",
            5: "Tip. 그거 아시나요? 스킬 버튼을 누르면 스킬창이 뜹니다",
            6: "사실 미하일은 이혼 전적이 있습니다...",
            7: " 그거 아시나요? 게임 제작자도 엔딩을 못 봤습니다",
            8: "그거 아시나요?? 랜슬롯은 남자를..",
            9: "우리 낭만코더 리보키의 팀장은 커피를 한번에 세잔을 마실 수 있습니다.",
            10: "Tip. 깡깡.... 깡 (파스락)",
            11: "그거 아시나요? 우리반에는 매일 달리는 경주마가 있습니다.",
            12: "그거 아시나요? 이동녀크는 1층의 보스입니다."
        }

        # 일반필드 맵 사이즈
        self.normal_field_size = [-20, 1580, -20, 780]


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



        # 일단 임시로 옮겨놓음
        # 코드 간소화 (소연수정)

        # attack_buttons = [
        #     self.Status1_Action1_Attack,
        #     self.Status2_Action1_Attack,
        #     self.Status3_Action1_Attack,
        #     self.Status4_Action1_Attack,
        #     self.Status5_Action1_Attack
        # ]
        # item_buttons = [
        #     self.Status1_Action3_Item,
        #     self.Status2_Action3_Item,
        #     self.Status3_Action3_Item,
        #     self.Status4_Action3_Item,
        #     self.Status5_Action3_Item
        # ]
        # run_buttons = [
        #     self.Status1_Action4_Run,
        #     self.Status2_Action4_Run,
        #     self.Status3_Action4_Run,
        #     self.Status4_Action4_Run,
        #     self.Status5_Action4_Run
        # ]
        # monster_buttons = [
        #     self.Monster_1_QButton,
        #     self.Monster_2_QButton,
        #     self.Monster_3_QButton,
        #     self.Monster_4_QButton,
        #     self.Monster_5_QButton,
        #     self.Monster_6_QButton,
        #     self.Monster_7_QButton,
        #     self.Monster_8_QButton,
        #     self.Monster_9_QButton,
        #     self.Monster_10_QButton
        # ]
        #
        # for index, button in enumerate(monster_buttons, start=1):
        #     button.clicked.connect(lambda index=index: self.monster_got_damage(index))
        #
        # for index, button in enumerate(run_buttons, start=1):
        #     button.clicked.connect(lambda index=index: self.Run_function(index))
        #
        # for index, button in enumerate(item_buttons, start=1):
        #     button.clicked.connect(lambda index=index: self.item_function(index))
        #
        # for index, button in enumerate(attack_buttons, start=1):
        #     button.clicked.connect(lambda x, index=index: self.attack_function(index))

        self.Status1_Action1_Attack.clicked.connect(lambda: self.attack_function(1))
        self.Status2_Action1_Attack.clicked.connect(lambda: self.attack_function(2))
        self.Status3_Action1_Attack.clicked.connect(lambda: self.attack_function(3))
        self.Status4_Action1_Attack.clicked.connect(lambda: self.attack_function(4))
        self.Status5_Action1_Attack.clicked.connect(lambda: self.attack_function(5))

        # for i in range(1,6):
        #     getattr(self, f"Status{i}_Action1_Attack").clicked.connect(lambda x, y=i: self.attack_function(y))

        self.Status1_Action3_Item.clicked.connect(lambda: self.Iteam_function(1))
        self.Status2_Action3_Item.clicked.connect(lambda: self.Iteam_function(2))
        self.Status3_Action3_Item.clicked.connect(lambda: self.Iteam_function(3))
        self.Status4_Action3_Item.clicked.connect(lambda: self.Iteam_function(4))
        self.Status5_Action3_Item.clicked.connect(lambda: self.Iteam_function(5))

        self.Status1_Action4_Run.clicked.connect(lambda: self.Run_function(1))
        self.Status2_Action4_Run.clicked.connect(lambda: self.Run_function(2))
        self.Status3_Action4_Run.clicked.connect(lambda: self.Run_function(3))
        self.Status4_Action4_Run.clicked.connect(lambda: self.Run_function(4))
        self.Status5_Action4_Run.clicked.connect(lambda: self.Run_function(5))


        # 몬스터 버튼 클릭하면 몬스터 공격 함수로 넘어감
        for j in range(1, 11):
            getattr(self, f"Monster_{j}_QButton").clicked.connect(lambda x, y = j: self.monster_got_damage(y))

        # self.Monster_1_QButton.clicked.connect(lambda x: self.monster_got_damage(1))
        # self.Monster_2_QButton.clicked.connect(lambda x: self.monster_got_damage(2))
        # self.Monster_3_QButton.clicked.connect(lambda x: self.monster_got_damage(3))
        # self.Monster_4_QButton.clicked.connect(lambda x: self.monster_got_damage(4))
        # self.Monster_5_QButton.clicked.connect(lambda x: self.monster_got_damage(5))
        # self.Monster_6_QButton.clicked.connect(lambda x: self.monster_got_damage(6))
        # self.Monster_7_QButton.clicked.connect(lambda x: self.monster_got_damage(7))
        # self.Monster_8_QButton.clicked.connect(lambda x: self.monster_got_damage(8))
        # self.Monster_9_QButton.clicked.connect(lambda x: self.monster_got_damage(9))
        # self.Monster_10_QButton.clicked.connect(lambda x: self.monster_got_damage(10))

        # 공격 타입 구분 초기 설정값
        self.attackType = 0

        # 유저 턴 구분 초기 설정값
        self.user_turn = 0
        self.class_alive = []
        self.class_turn = [1, 2, 3, 4, 5]

        # ui 하단 버튼 비활성화
        for i in range(1, 6):
            getattr(self, f'Status{i}_Action1_Attack').setEnabled(False)
            getattr(self, f'Status{i}_Action2_Skill').setEnabled(False)
            getattr(self, f'Status{i}_Action3_Item').setEnabled(False)
            getattr(self, f'Status{i}_Action4_Run').setEnabled(False)

        # 혜빈 코드 취합 본 시작===========================================================================================

        # 해당 인스턴스에 캐릭터 정보 저장
        self.guardLevel = 1 #치트키 팔쉽레벨
        self.guardlist = ["대지", "별", "달", "빛"]
        self.guardname = random.choice(self.guardlist)
        self.TopUI_Level_Label.setText("%s의 수호대 Level : %d" % (self.guardname, self.guardLevel))
        self.label_74.setText("%s의 수호대 스테이터스 창"%self.guardname)
        self.label_74.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.guardoption()  # 캐릭터 생성해줌
        self.StautsHpall = []
        self.StautsMpall = []
        self.Statusclass = []

        # 리스트를 셔플로 돌려줌
        # 위 self.guardoption()에서 생성한 클래스 캐릭터들의 값총 6개-(전체정보/최대hp/최대mp)저장
        random.shuffle(self.list_class)



        # 유저 체력을 리스트에 담아준다.
        self.class_hp_dict = {}
        self.class_hp_dict_last = {}
        self.class_mp_dict = {}
        self.class_mp_dict_last = {}
        for i in range(1, 6):  # 서플로 돌려준 클래스유저들의 체력을 빈 딕셔너리에 1부터 5까지 담아줌 <- 수정함
            self.class_hp_dict[i] = self.list_class[i - 1][1]
        self.class_hp_dict_last[0] = self.list_class[-1][1]
        for i in range(1, 6):  # 서플로 돌려준 클래스유저들의 마나를 빈 딕셔너리에 1부터 5까지 담아줌 <- 수정함
            self.class_mp_dict[i] = self.list_class[i - 1][2]
        self.class_mp_dict_last[0] = self.list_class[-1][2]
        print('유저 HP체력 확인용', self.class_hp_dict)
        print('유저 MP마나 확인용', self.class_mp_dict)

        # 위에서 섞은 list_class을 프레임에 1부터 5까지 가져와 담아줌
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
            getattr(self, f'Class_{i}_QLabel').setPixmap(QtGui.QPixmap(self.list_class[i - 1][3]))

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
        self.itemusebox = [] # 아이템 버튼 담기는 박스
        for btn in range(1, 15):
            self.itemusebox.append(getattr(self, f'Portion_{btn}_Btn'))
        for idx, cont in enumerate(self.itemusebox): #아이템 버튼 연결
            cont.clicked.connect(lambda x, y=idx + 1: self.Iteam_name(y))
        # 혜빈 코드 취합 본 끝 ============================================================================================
        """길준이 형님 취합 - 코드 시작 findnum:0921"""
        # 아이템 코드 취합 시작 ===========================================================================================

        self.item_img()
        self.item_set()
        # 아이템 프리셋 호출
        self.item_class_1 = self.class_warrior
        self.item_class_2 = self.class_whitewizard
        self.item_class_3 = self.class_blackwizard
        self.item_class_4 = self.class_redwizard
        self.item_class_5 = self.class_archer
        self.item_class_6 = self.class_swordman
        # 아이템 프리셋 호출 후 리스트 작성
        self.hp_s = self.item_consumable_hp_S
        self.hp_m = self.item_consumable_hp_M
        self.hp_l = self.item_consumable_hp_L
        self.mp_s = self.item_consumable_mp_S
        self.mp_m = self.item_consumable_mp_M
        self.mp_l = self.item_consumable_mp_L
        self.all_s = self.item_consumable_all_S
        self.all_m = self.item_consumable_all_M
        self.all_l = self.item_consumable_all_L
        self.resurrection = self.item_consumable_resurrection
        self.tent = self.item_consumable_tent
        self.change = self.item_consumable_change
        self.enhancement_low = self.item_consumable_enhancement_low
        self.enhancement_high = self.item_consumable_enhancement_high

        self.item_list = [self.hp_s, self.hp_m, self.hp_l, self.mp_s, self.mp_m, self.mp_l,
                          self.all_s, self.all_m, self.all_l, self.resurrection, self.tent, self.change,
                          self.enhancement_low, self.enhancement_high]

        self.class_item_list()
        self.class_name_reset()

        for i in range(len(self.list_class)):
            if self.list_class[0][0] == getattr(self, f'class_{i + 1}'):
                first_page = i + 1
        self.first_page = first_page
        self.combobox_add()
        self.status_page_reset()

        # 장비 업그레이드용 카운터
        self.item_class_upgrade_counter_1 = [0, 0, 0, 0, 0, 0, 0]
        self.item_class_upgrade_counter_2 = [0, 0, 0, 0, 0, 0, 0]
        self.item_class_upgrade_counter_3 = [0, 0, 0, 0, 0, 0, 0]
        self.item_class_upgrade_counter_4 = [0, 0, 0, 0, 0, 0, 0]
        self.item_class_upgrade_counter_5 = [0, 0, 0, 0, 0, 0, 0]
        self.item_class_upgrade_counter_6 = [0, 0, 0, 0, 0, 0, 0]
        self.upgrade_index = 0  # 장비 강화 캐릭터 선택을 위한 페이지 인덱스 값

        self.StackWidget_Equip.setCurrentWidget(getattr(self, f'Class_{first_page}_Equip_Page'))
        self.get_index()
        self.item_upgrade_button_reset()
        self.Btn_Equip.setEnabled(False)
        self.Btn_Portion.setEnabled(True)
        self.Btn_Status.setEnabled(True)

        self.Btn_Portion.clicked.connect(lambda: self.StackWidget_Item.setCurrentWidget(self.Page_Use))
        self.Btn_Portion.clicked.connect(self.use_page)
        self.Btn_Equip.clicked.connect(lambda: self.StackWidget_Item.setCurrentWidget(self.Page_Equip))
        self.Btn_Equip.clicked.connect(self.equip_page)
        self.Btn_Equip.clicked.connect(self.get_index)
        self.Btn_Equip.clicked.connect(self.item_upgrade_button_reset)
        self.Btn_Status.clicked.connect(lambda: self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing))
        self.Btn_Status.clicked.connect(self.status_page)
        self.consumable_reset()

        # 콤보박스 선택에 따라 장비창 변환
        self.ComboBox_Class.activated[str].connect(self.class_equip_page)
        self.ComboBox_Class.activated[str].connect(self.get_index)  # 장비강화 캐릭터 선택을 위한 페이지 인덱스 값 추출

        # 장비강화
        self.item_upgrade_button_reset()
        for i in range(6):
            getattr(self, f'Equip{i + 1}_1Helmet_Btn').clicked.connect(self.helmet_upgrade)
        for i in range(6):
            getattr(self, f'Equip{i + 1}_2_Armor_Btn').clicked.connect(self.armor_upgrade)
        for i in range(6):
            getattr(self, f'Equip{i + 1}_3_Pants_Btn').clicked.connect(self.pants_upgrade)
        for i in range(6):
            getattr(self, f'Equip{i + 1}_5_Hand_Btn').clicked.connect(self.glove_upgrade)
        for i in range(6):
            getattr(self, f'Equip{i + 1}_6_Weapon_Btn').clicked.connect(self.weapon_upgrade)
        for i in range(6):
            getattr(self, f'Equip{i + 1}_7_Shield_Btn').clicked.connect(self.shield_upgrade)
        for i in range(6):
            getattr(self, f'Equip{i + 1}_8_Cloak_Btn').clicked.connect(self.cloak_upgrade)

        # 포션 사용
        self.Portion_1_Btn.clicked.connect(self.hp_using_1)
        self.Portion_2_Btn.clicked.connect(self.hp_using_2)
        self.Portion_3_Btn.clicked.connect(self.hp_using_3)
        self.Portion_4_Btn.clicked.connect(self.mp_using_1)
        self.Portion_5_Btn.clicked.connect(self.mp_using_2)
        self.Portion_6_Btn.clicked.connect(self.mp_using_3)
        self.Portion_7_Btn.clicked.connect(self.all_using_1)
        self.Portion_8_Btn.clicked.connect(self.all_using_2)
        self.Portion_9_Btn.clicked.connect(self.all_using_3)
        self.Portion_10_Btn.clicked.connect(self.revive_using)
        self.Portion_11_Btn.clicked.connect(self.tent_use)
        self.Portion_12_Btn.clicked.connect(self.class_change_using)

        """길준이 형님 취합 - 코드 종료"""
        # ++ keypressevent 함수에 추가로 추합
        # ==================================================================================================================

        # 몬스터 상속 - 몬스터 필드/ 이름/ 이미지/ 레벨/ hp/ 공격력(임시로100)
        # 변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""
        """배경 모음"""
        self.nomalfield_fire_background = ["./image/배경/fire_1.png", "./image/배경/fire_2.png", "./image/배경/fire_3.png"]
        self.nomalfield_ice_background = ["./image/배경/ice_1.png", "./image/배경/ice_2.png", "./image/배경/ice_3.png"]
        self.nomalfield_forest_background = ["./image/배경/forest_1.png", "./image/배경/forest_2.png", "./image/배경/forest_3.png"]
        self.nomalfield_water_background = ["./image/배경/water_1.png", "./image/배경/water_2.png", "./image/배경/water_3.png"]
        self.nomalfield_backgroundBox = [self.nomalfield_fire_background, self.nomalfield_ice_background,
                                         self.nomalfield_forest_background, self.nomalfield_water_background]
        self.battlefield_background = ["./image/배경/dungeon_1.png", "./image/배경/dungeon_2.png", "./image/배경/dungeon_3.png", "./image/배경/dungeon_4.png", "./image/배경/dungeon_5.png"]

        """불의 지역 몬스터들"""
        self.nomalfield_fire_monster1 = MonsterOption("불의 지역", "흔하게 생긴 불돼지", "./image/MonsterImage/fire_1.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.nomalfield_fire_monster2 = MonsterOption("불의 지역", "불의 골렘", "./image/MonsterImage/fire_2.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.nomalfield_fire_monster3 = MonsterOption("불의 지역", "불의 정령", "./image/MonsterImage/fire_3.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.nomalfield_fire_monster4 = MonsterOption("불의 지역", "불에 익지않는 크랩", "./image/MonsterImage/fire_4.png", 1,
                                                      random.randrange(200, 1000), 50)

        """눈의 지역 몬스터들"""
        self.nomalfield_ice_monster1 = MonsterOption("눈의 지역", "눈의 정령", "./image/MonsterImage/ice_1.png", 1,
                                                     random.randrange(200, 1000), 50)
        self.nomalfield_ice_monster2 = MonsterOption("눈의 지역", "눈속에서 타오르는 불", "./image/MonsterImage/ice_2.png", 1,
                                                     random.randrange(200, 1000), 50)
        self.nomalfield_ice_monster3 = MonsterOption("눈의 지역", "몰루판다", "./image/MonsterImage/ice_3.png", 1,
                                                     random.randrange(200, 1000), 50)
        self.nomalfield_ice_monster4 = MonsterOption("눈의 지역", "눈보라를 날리는 양", "./image/MonsterImage/ice_4.png", 1,
                                                     random.randrange(200, 1000), 50)

        """대지의 지역 몬스터들"""
        self.nomalfield_forest_monster1 = MonsterOption("대지의 지역", "흔한 번데기", "./image/MonsterImage/forest_1.png", 1,
                                                        random.randrange(200, 1000), 50)
        self.nomalfield_forest_monster2 = MonsterOption("대지의 지역", "늙은 장수풍뎅이", "./image/MonsterImage/forest_2.png", 1,
                                                        random.randrange(200, 1000), 50)
        self.nomalfield_forest_monster3 = MonsterOption("대지의 지역", "억울한 슬라임", "./image/MonsterImage/forest_3.png", 1,
                                                        random.randrange(200, 1000), 50)
        self.nomalfield_forest_monster4 = MonsterOption("대지의 지역", "어딘가 위험한 식물", "./image/MonsterImage/forest_4.png", 1,
                                                        random.randrange(200, 1000), 50)

        """물의 지역 몬스터들"""
        self.nomalfield_water_monster1 = MonsterOption("물의 지역", "탁한 기운의 도룡뇽", "./image/MonsterImage/water_1.png", 1,
                                                       random.randrange(200, 1000), 50)
        self.nomalfield_water_monster2 = MonsterOption("물의 지역", "단단한 붕어", "./image/MonsterImage/water_2.png", 1,
                                                       random.randrange(200, 1000), 50)
        self.nomalfield_water_monster3 = MonsterOption("물의 지역", "위험해보이는 붕어", "./image/MonsterImage/water_3.png", 1,
                                                       random.randrange(200, 1000), 50)
        self.nomalfield_water_monster4 = MonsterOption("물의 지역", "그냥 상어", "./image/MonsterImage/water_4.png", 1,
                                                       random.randrange(200, 1000), 50)

        """던전 필드 몬스터들"""
        self.dugeonfield_1st_monster1 = MonsterOption("던전 1층", "킬러비", "./image/MonsterImage/dugeonmonster_1.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster2 = MonsterOption("던전 1층", "던전 박쥐", "./image/MonsterImage/dugeonmonster_2.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster3 = MonsterOption("던전 2층", "평범한 슬라임", "./image/MonsterImage/dugeonmonster_3.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster4 = MonsterOption("던전 2층", "차가운 슬라임", "./image/MonsterImage/dugeonmonster_4.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster5 = MonsterOption("던전 3층", "외눈박이 촉수 문어", "./image/MonsterImage/dugeonmonster_5.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster6 = MonsterOption("던전 3층", "푸른 킬러 플라워", "./image/MonsterImage/dugeonmonster_6.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster7 = MonsterOption("던전 4층", "그린 드래곤", "./image/MonsterImage/dugeonmonster_7.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster8 = MonsterOption("던전 4층", "히드라", "./image/MonsterImage/dugeonmonster_8.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster9 = MonsterOption("던전 5층", "레드 드래곤", "./image/MonsterImage/dugeonmonster_9.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster10 = MonsterOption("던전 5층", "붉은 킬러 플라워", "./image/MonsterImage/dugeonmonster_10.png", 1,
                                                       random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster11 = MonsterOption("던전 6층", "독침 전갈", "./image/MonsterImage/dugeonmonster_11.png", 1,
                                                       random.randrange(200, 1000), 50)
        self.dugeonfield_1st_monster12 = MonsterOption("던전 6층", "베젤부부의 하수인", "./image/MonsterImage/dugeonmonster_12.png", 1,
                                                       random.randrange(200, 1000), 50)
        """던전 보스 몬스터"""
        self.dugeonfield_Boss1 = MonsterOption("던전 1층", "이동려크", "./image/MonsterImage/dugeonfield_Boss1.png", 1,
                                               random.randrange(25000, 35000), 50)
        self.dugeonfield_Boss2 = MonsterOption("던전 2층", "조동혀니", "./image/MonsterImage/dugeonfield_Boss2.png", 1,
                                               random.randrange(45000, 55000), 50)
        self.dugeonfield_Boss3 = MonsterOption("던전 3층", "류홍보기", "./image/MonsterImage/dugeonfield_Boss3.png", 1,
                                               random.randrange(65000, 75000), 50)
        self.dugeonfield_Boss4 = MonsterOption("던전 4층", "코로나 공주", "./image/MonsterImage/dugeonfield_Boss4.png", 1,
                                               random.randrange(75000, 85000), 50)
        self.dugeonfield_Boss5 = MonsterOption("던전 5층", "이땅보키", "./image/MonsterImage/dugeonfield_Boss5.png", 1,
                                               random.randrange(85000, 599999), 50)
        self.dugeonfield_Boss6 = MonsterOption("던전 6층", "환생한 보키", "./image/MonsterImage/dugeonfield_Boss6.png", 1,
                                               random.randrange(999999, 9999999), 50)
        self.dugeonfield_Boss7 = MonsterOption("던전 7층", "로드 오브 보키", "./image/MonsterImage/dugeonfield_Boss7.png", 1,
                                               random.randrange(9999999, 99999990), 50)

        """상속받은 이미지와 이미지값을 담은 리스트들을 한곳에 담아주기"""
        self.firemonsterbox = [self.nomalfield_fire_monster1, self.nomalfield_fire_monster2,
                               self.nomalfield_fire_monster3,
                               self.nomalfield_fire_monster4]

        self.icemonsterbox = [self.nomalfield_ice_monster1, self.nomalfield_ice_monster2, self.nomalfield_ice_monster3,
                              self.nomalfield_ice_monster4]

        self.forestmonsterbox = [self.nomalfield_forest_monster1, self.nomalfield_forest_monster2,
                                 self.nomalfield_forest_monster3,
                                 self.nomalfield_forest_monster4]

        self.watermonsterbox = [self.nomalfield_water_monster1, self.nomalfield_water_monster2,
                                self.nomalfield_water_monster3,
                                self.nomalfield_water_monster4]
        self.nomalfieldallBox = [self.firemonsterbox, self.icemonsterbox, self.forestmonsterbox, self.watermonsterbox]

        self.dugeonfieldbox = [self.dugeonfield_1st_monster1, self.dugeonfield_1st_monster2,
                               self.dugeonfield_1st_monster3, self.dugeonfield_1st_monster4,
                               self.dugeonfield_1st_monster5, self.dugeonfield_1st_monster6,
                               self.dugeonfield_1st_monster7, self.dugeonfield_1st_monster8,
                               self.dugeonfield_1st_monster9, self.dugeonfield_1st_monster10,
                               self.dugeonfield_1st_monster11, self.dugeonfield_1st_monster12]
        self.dugeonBossbox = [self.dugeonfield_Boss1, self.dugeonfield_Boss2, self.dugeonfield_Boss3,
                             self.dugeonfield_Boss4, self.dugeonfield_Boss5, self.dugeonfield_Boss6,
                             self.dugeonfield_Boss7]
        # 변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""변경사항""""""""

        # 스킬 상속 이후 리턴 값으로 리스트 줌
        self.skillbox()

        ## 임시 캐릭터 설정

        self.character_left_img = QPixmap('./image/character_left.png')  # 캐릭터 왼쪽 이미지
        self.character_right_img = QPixmap('./image/character_right.png')  # 캐릭터 오른쪽 이미지

        ## 배경 및 위젯 설정
        self.back_ground_label.setPixmap(QtGui.QPixmap("./image/용암.png"))  # 임시 일반 필드 배경 이미지
        self.back_ground_label.move(0, -1)  # 배경 위치 조정
        self.Widget_Skill.move(826, -1)  # 전투중 스킬 선택시 생성되는 스킬 위젯 위치
        self.Widget_Skill.hide()  # 위젯창은 숨겨 둠

        # 헤더 프레임 없애고 전체화면으로 띄우기
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        # self.exitAction.triggered.connect(qApp.closeAllWindows) # 게임 종료 이벤트

        # self.HoldSwitch = 0
        # self.Page_Use_ing.setEnabled(False)  # 캐릭터 세부정보창 비활성화(우측 상단 index-1)
        # # self.Page_Equip.setEnabled(False)
        # self.Btn_Equip.clicked.connect(lambda y: self.use_uiABC(4))  # 우측 상단 장비 버튼 클릭하면 장비창 이동
        # self.Btn_Portion.clicked.connect(lambda y: self.use_uiABC(0))  # 포션버튼 클릭하면 포션 이동
        # self.Btn_Status.clicked.connect(lambda y: self.use_uiABC(2))  # 캐릭터 세부 장비 활성화

        # # 여기서부터 봐야 함
        for num in range(1, 6):  # 액션버튼 1~4 시그널 슬롯 연결
            #     getattr(self, f'Status{num}_Action1_Attack').clicked.connect(
            #         lambda x, y=num: self.nomalact(y))  # 일반공격함수로 연결
            getattr(self, f'Status{num}_Action2_Skill').clicked.connect(
                lambda x, y=num: self.skillopen(y))  # 스킬옵션 함수로 연결
        #     getattr(self, f'Status{num}_Action3_Item').clicked.connect(lambda y: self.use_uiABC(1))

        # 클래스 스킬 버튼들 리스트화 /
        # #미하일 도발스킬 / #루미너스 스킬: 힐, 그레이트힐, 힐올, 공격력업, 방어력업, 맵핵 / #알렉스 스킬: 파이어볼, 파이어월, 블리자드, 썬더브레이커 / # 메르데스 집중타, 듀얼샷, 마스터샷 / #샐리멘더 힐, 그레이트힐, 힐올, 파이어볼 파이어월, 블리자드 썬더브레이커
        self.pushbox = [self.Class2_Skill1_Btn, self.Class2_Skill2_Btn, self.Class2_Skill3_Btn,
                        self.Class2_Skill4_Btn, self.Class2_Skill5_Btn, self.Class2_Skill6_Btn,
                        self.Class3_Skill1_Btn, self.Class3_Skill2_Btn, self.Class3_Skill3_Btn, self.Class3_Skill4_Btn,
                        self.Class4_Skill1_Btn, self.Class4_Skill2_Btn, self.Class4_Skill3_Btn,
                        self.Class4_Skill4_Btn, self.Class4_Skill5_Btn, self.Class4_Skill6_Btn, self.Class4_Skill7_Btn,
                        self.Class5_Skill1_Btn, self.Class5_Skill2_Btn, self.Class5_Skill3_Btn,
                        self.Class6_Skill1_Btn, self.Class1_Skill1_Btn]  # 강타

        # 수호대 스폰 지역 랜덤 설정 및 미궁 랜덤 생성 (조건 = 무조건 수호대 스폰 지역 반대 편에 포탈 나오게함)========================
        # 소연수정 딕셔너리 이용
        locations = {1: ("숲의 지역", 100, 520),
                     2: ("불의 지역", 360, 40),
                     3: ("눈의 지역", 1280, 20),
                     4: ("물의 지역", 1320, 540)}
        random_spot = random.randrange(1, 5) # 이거 깔끔하니 좋네요
        location = locations[random_spot]
        self.Character_QLabel.setPixmap(self.character_left_img)
        self.Character_QLabel.move(location[1], location[2])
        self.TopUI_Map_Label.setText(location[0])

        # if random_spot == 1:  # 숲의 지역 스폰 장소
        #     self.Character_QLabel.setPixmap(self.character_left_img)
        #     self.Character_QLabel.move(100, 520)
        #     self.TopUI_Map_Label.setText("숲의 지역")
        # elif random_spot == 2:  # 불의 지역 스폰 장소
        #     self.Character_QLabel.setPixmap(self.character_left_img)
        #     self.Character_QLabel.move(360, 40)
        #     self.TopUI_Map_Label.setText("불의 지역")
        # elif random_spot == 3:  # 눈의 지역 스폰 장소
        #     self.Character_QLabel.setPixmap(self.character_left_img)
        #     self.Character_QLabel.move(1280, 20)
        #     self.TopUI_Map_Label.setText("눈의 지역")
        # elif random_spot == 4:  # 물의 지역 스폰 장소
        #     self.Character_QLabel.setPixmap(self.character_left_img)
        #     self.Character_QLabel.move(1320, 540)
        #     self.TopUI_Map_Label.setText("물의 지역")

        # 왼쪽 상단에 초기 죄표 값 출력
        self.TopUI_Coordinate_Label.setText(
            f"x좌표: {self.Character_QLabel.pos().x()} y좌표: {self.Character_QLabel.pos().y()}")


        ## 7층가기버튼
        self.win_btn_2.clicked.connect(self.force_win_2)
        # # 강제승리버튼
        self.win_btn.clicked.connect(self.force_win)

    def force_win_2(self):
        self.dungeon_floor = 7
        self.StackWidget_Field.setCurrentIndex(1)
        self.move_to_dungeon()
        self.user_win_the_boss_stage(True)
        print("지나감")

    def force_win(self):
        """강제승리버튼"""
        if self.battle_type == '일반전투':
            for i in range(1, len(self.monster_hp_dict.keys())+1):
               self.monster_hp_dict[i] = 0
            print(self.monster_hp_dict)
            self.go_to_normalfield()
        elif self.battle_type == '던전전투':
            for i in range(1, len(self.dungeon_random_monster_hp.keys())+1):
               self.dungeon_random_monster_hp[i] = 0
            print(self.dungeon_random_monster_hp)
            self.go_to_dungeonfield()
            #여기에 던전으로 다시 돌아가는 함수로 이동하기


    def guardoption(self):
        """캐릭터 생성 및 hp/mp 저장"""
        self.class_1 = Status('전사', '미하일', 300, 0, self.guardLevel, "./image/캐릭터 및 수호대/class_1.png")
        self.class_2 = Status('백법사', '루미너스', 200, 150, self.guardLevel, "./image/캐릭터 및 수호대/class_2.png")
        self.class_3 = Status('흑법사', '알렉스', 200, 150, self.guardLevel, "./image/캐릭터 및 수호대/class_3.png")
        self.class_4 = Status('적법사', '샐러맨더', 150, 150, self.guardLevel, "./image/캐릭터 및 수호대/class_4.png")
        self.class_5 = Status('궁수', '메르데스', 150, 150, self.guardLevel, "./image/캐릭터 및 수호대/class_5.png")
        self.class_6 = Status('검사', '랜슬롯', 150, 150, self.guardLevel, "./image/캐릭터 및 수호대/class_6.png")

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
        self.list_class = [[self.class_1, self.class1_nowhp, self.class1_nowmp, self.class_1.class_img],
                           [self.class_2, self.class2_nowhp, self.class2_nowmp, self.class_2.class_img],
                           [self.class_3, self.class3_nowhp, self.class3_nowmp, self.class_3.class_img],
                           [self.class_4, self.class4_nowhp, self.class4_nowmp, self.class_4.class_img],
                           [self.class_5, self.class5_nowhp, self.class5_nowmp, self.class_5.class_img],
                           [self.class_6, self.class6_nowhp, self.class6_nowmp, self.class_6.class_img]]
        return self.list_class

    def skillbox(self):
        """
        스킬 상속 이후 리턴 값으로 리스트 줌
        :return:
        """

        # SkillOption 클래스: 이름, 이미지, 데미지 값, 소비mp(스킬마나), 스킬 종류(0-버프, 1-단일, 2-전체), 사용횟수 턴, 제한 레벨
        # find : 2023.05.25 AM 10:03 (스킬에 해금 레벨 추가 수정)
        self.skill_1 = SkillOption("힐", None, random.randrange(30, 71), 0.1, 0, 1, 1)
        self.skill_2 = SkillOption("그레이트 힐", None, random.randrange(60, 101), 0.2, 0, 1, 15)
        self.skill_3 = SkillOption("힐 올", None, random.randrange(40, 81), 10, 0.5, 1, 30)
        self.skill_4 = SkillOption("공격력 업", None, random.randrange(30, 71), 0.1, 0, 1, 10)
        self.skill_5 = SkillOption("방어력 업", None, random.randrange(30, 71), 0.1, 0, 1, 15)
        self.skill_6 = SkillOption("맵 핵", None, 0, 0, 1, 1, 30)

        self.skill_7 = SkillOption("파이어 볼", None, 1.3, 0.1, 1, 1, 1)
        self.skill_8 = SkillOption("파이어 월", None, random.uniform(1.4, 1.6), 0.2, 2, 1, 15)
        self.skill_9 = SkillOption("썬더브레이커", None, random.uniform(1.6, 1.8), 0.3, 2, 1, 20)
        self.skill_10 = SkillOption("블리자드", None, random.uniform(1.8, 2.0), 0.4, 2, 1, 25)

        self.skill_11 = SkillOption("집중타", None, random.uniform(1.2, 1.5), 0.1, 1, 1, 10)
        self.skill_12 = SkillOption("듀얼 샷", None, random.uniform(1.4, 1.6), 0.2, 1, 1, 15)
        self.skill_13 = SkillOption("마스터 샷", None, random.uniform(1.5, 1.7), 0.3, 1, 1, 20)

        self.skill_14 = SkillOption("강타", None, random.uniform(2.0, 50.0), 0.1, 1, 1, 10)
        self.skill_15 = SkillOption("도발", None, 0, 0, 3, 1, 1)
        self.skillall = [self.skill_1, self.skill_2, self.skill_3, self.skill_4, self.skill_5, self.skill_6,
                         self.skill_7, self.skill_8, self.skill_9, self.skill_10, self.skill_11,
                         self.skill_12, self.skill_13, self.skill_14, self.skill_15]

        # 스킬들을 담아서 return 해줌
        return self.skillall


    # 소연 함수 추가 ==================================================================================================================


    def move_to_dungeon(self):
        """던전으로 랜덤 이동하는 부분"""
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
        self.position.timeout.connect(self.ghost_direction)
        self.position.start()

        # 유령 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_label)
        self.timer.start(40)

        # 던전 랜덤으로 가는 부분
        random_dungeon_num = random.randint(1, 4)
        self.random_num_for_teleport = random_dungeon_num
        # 유령 위치 던전 내로 고정하기
        self.ghost_label.move(
            random.randint(self.map_size[random_dungeon_num][0], self.map_size[random_dungeon_num][1]),
            random.randint(self.map_size[random_dungeon_num][2], self.map_size[random_dungeon_num][3]))
        # 유령 라벨 show()시키기
        self.ghost_label.show()
        print('던전번호는', random_dungeon_num)  # 확인용

        self.dungeon_number = random_dungeon_num # 던전 사이즈마다 다르게 이동
        self.dungen_map_dict = {
            1: ['./image/배경/던전_1.png', 592, 631],
            2: ['./image/배경/던전_2.png', 567, 644],
            3: ['./image/배경/던전_3.png', 558, 657],
            4: ['./image/배경/던전_4.png', 504, 674],
        }
        self.dungeon_img_label.setPixmap(QPixmap(self.dungen_map_dict[random_dungeon_num][0]))
        self.Character_QLabel_2.move(self.dungen_map_dict[random_dungeon_num][1], self.dungen_map_dict[random_dungeon_num][2])

        # 던전 입구 만들기
        self.Show_Dungeon_Entrance(random_dungeon_num)

    def Show_Dungeon_Entrance(self, map_num):
        """던전 입구 랜덤으로 만들어주는 함수"""
        # 미궁 버튼 임시로 만들어주기
        self.entrance = QLabel(self)
        self.entrance.setText("미궁")  # 임시지정(이미지 씌우기는 나중에)
        self.entrance.setFixedSize(50, 50)  # 임시 라벨 크기 지정
        self.entrance.setStyleSheet('background-color: transparent')  # 임시 라벨 색 지정
        self.entrance.setPixmap(QtGui.QPixmap('./image/door_closed.png').scaled(QSize(30, 30), aspectRatioMode=Qt.IgnoreAspectRatio))

        self.entrance.move(random.randint(self.map_size[map_num][0], self.map_size[map_num][1]),
                           random.randint(self.map_size[map_num][2], self.map_size[map_num][3]))  # 던전 15*15 사이즈
        self.entrance.show()  # 미궁 띄우기

        # 보스 MonsterImage 위치 임시로 만들어주기
        self.boss_monster = QLabel(self)  # 보스 MonsterImage 나타날 포탈 임시
        self.boss_monster.setText("MonsterImage")
        self.boss_monster.setFixedSize(30, 30)  # 임시 라벨크기지정
        self.boss_monster.setStyleSheet('background-color: red')  # 임시로 빨간색으로
        self.boss_monster.move(random.randint(self.map_size[map_num][0], self.map_size[map_num][1]),
                               random.randint(self.map_size[map_num][2],
                                              self.map_size[map_num][3]))  # 보스 MonsterImage 랜덤으로 등장
        self.boss_monster.show()  # 보스몬스터 띄우기

        # 검은 라벨 만들어서 위에 덮기(유저가 플레이할 때 던전이 안보이게)
        # black_label = QLabel(self)
        # black_label.move(0, 30)
        # black_label.setStyleSheet('background-color: rgba(0, 0, 0, 100)')  # 100으로 설정되어 있는 투명도 높이면 어두워짐
        # black_label.setFixedSize(1580, 780)  # 사이즈고정
        # black_label.show()

    def block_dungeon_for_type(self, character, dungeon_num, new_x, new_y, new_p, before_p):
        """던전 크기별로 맵에서 나가지 못하게 하기"""
        if not ((self.map_size[dungeon_num][0] <= new_x <= self.map_size[dungeon_num][1]) and (
                self.map_size[dungeon_num][2] <= new_y <= self.map_size[dungeon_num][3])):
            character.setGeometry(before_p)
        if self.block_dungeon_wall(new_p, before_p, self.wall_list, dungeon_num):
            character.setGeometry(before_p)

    def block_dungeon_wall(self, new_position, previous_position, wall_list, num):
        """유저가 던전벽에서 나아가지 못하게 하기"""
        for key, value in wall_list.items():
            if key == num:  # 특정 던전 사이즈일때
                for i in value:  # 딕셔너리 내 리스트 x, y값 가져와서 비교(self.wall_list 검색해보면 됨)
                    if i[0] < new_position.x() < i[1] and i[2] < new_position.y() < i[3]:  # 벽 x, y값 사이에 들어가면
                        self.Character_QLabel_2.setGeometry(previous_position)  # 이전 위치로 이동
                        return True  # True 반환
        return False

    def block_normal_field(self, now_x, now_y):
        """일반필드 맵에서 벗어나지 못하게 하기"""


        if not ((self.normal_field_size[0] < now_x < self.normal_field_size[1]) and
                (self.normal_field_size[2] < now_y < self.normal_field_size[3])):
            return True
        return False

    def show_messagebox(self, text):
        """특정 문구 메세지박스 띄워주기"""
        reply = QMessageBox()
        reply.setText(text)
        reply.exec_()

    def ghost_direction(self):
        """유령 방향 랜덤으로 지정 및 변환"""
        # 랜덤값 따라 방향지정
        self.random_num = random.randint(1, 6)
        # print('유령랜덤값: ',self.random_num)
        ghost_direction = {
            1: self.ghost_img_right_bottom,  # 우하
            2: self.ghost_img_right_top,  # 우상
            3: self.ghost_img_left_top,  # 좌상
            4: self.ghost_img_left_bottom,  # 좌하
            5: self.ghost_img_left,  # 왼쪽
            6: self.ghost_img_right,  # 오른쪽
        }
        self.ghost_label.setPixmap(
            ghost_direction[self.random_num].scaled(QSize(self.ghost_fixed_size, self.ghost_fixed_size),
                                                    aspectRatioMode=Qt.IgnoreAspectRatio))

    def move_label(self):
        """유령 움직임 조정 함수"""
        # 현재 라벨 포지션 받기
        current_pos = self.ghost_label.pos()
        # x, y값 조정
        x_start, x_end = self.map_size[self.dungeon_number][0], self.map_size[self.dungeon_number][1]
        y_start, y_end = self.map_size[self.dungeon_number][2], self.map_size[self.dungeon_number][3]

        # 새 위치 계산
        new_positions = {
            1: (min(current_pos.x() + 1, x_end), min(current_pos.y() + 1, y_end)),  # 우하
            2: (min(current_pos.x() + 1, x_end), max(current_pos.y() - 1, y_start)),  # 우상
            3: (max(current_pos.x() - 1, x_start), max(current_pos.y() - 1, y_start)),  # 좌상
            4: (max(current_pos.x() - 1, x_start), min(current_pos.y() + 1, y_end)),  # 좌하
            5: (max(current_pos.x() - 1, x_start), current_pos.y()),  # 왼쪽
            6: (min(current_pos.x() + 1, x_end), current_pos.y())  # 오른쪽
        }
        new_x, new_y = new_positions[self.random_num]

        # 유령라벨 새 포지션으로 옮기기
        self.ghost_label.move(new_x, new_y)

    def return_user_state(self):
        """유저턴 초기화 시켜주기"""
        self.user_turn = 0
        for i in range(1, 6):  # 서플로 돌려준 클래스유저들의 체력을 빈 딕셔너리에 1부터 5까지 다시 담아주고
            self.class_hp_dict[i] = self.list_class[i - 1][1]
            self.class_mp_dict[i] = self.list_class[i - 1][2]
        for i in range(1, 6):  #유저가 죽으면 체력회복
            self.class_hp_mp_present_value_list[i - 1][0].setText(
                f'{self.class_hp_dict[i]}/{self.Statusclass[i - 1].get_maxhp()}')  # hp판에 변경된 값 넣어주기
            self.class_hp_mp_present_value_list[i - 1][1].setText(
                f'{self.class_mp_dict[i]}/{self.Statusclass[i - 1].get_maxmp()}')  # mp판에 변경된 값 넣어주기

    def checkCollision(self, obj1, obj2):
        """겹치면 true반환"""
        x1, y1, w1, h1 = abs(obj1.x()), abs(obj1.y()), abs(obj1.width()), abs(obj1.height())
        x2, y2, w2, h2 = abs(obj2.x()), abs(obj2.y()), abs(obj2.width()), abs(obj2.height())
        if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
            return True
        return False

    def show_messagebox_easter_egg(self):
        """이스터에그 메세지 박스 보여주기 (질문하는 메세지박스 띄우기)"""
        self.reply_state = True
        # paper_img = QPixmap('구겨진_종이조각-removebg-preview.png')

        msg_box = QMessageBox()
        msg_box.setIconPixmap(QPixmap("./image/paper.png"))
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
            pass # 일단 패스 msg_box.setIconPixmap(QPixmap('./image/모야.jpg')) #호현 머리자르는 사진
        msg_box.setText(f"쪽지에 작성된 내용은...\n{self.msg_sample_list[ranodm_num]}")
        msg_box.exec_()
        self.mark_label.hide()

    def item_get_and_exclamentation_mark(self):
        """아이템 주움과 동시에 !마크 뜨는 함수"""
        # mark_label =

    def Add_Dungeon_monster_info(self):
        """던전 몬스터들을 나오게 함(일반몬스터와 로직 같음)"""

        self.dungeon_random_monster_hp = {}  # 던전 몬스터 체력 담기
        dungeon_monster_style = []  # 던전 몬스터 스타일 담기

        # 던전 전투 배경 담아주기
        dungeon_background_random = random.randint(1, 5)
        self.back_ground_label.setPixmap(
            QtGui.QPixmap(self.battlefield_background[dungeon_background_random - 1]).scaled(QSize(1580, 830),
                                                                                             aspectRatioMode=Qt.IgnoreAspectRatio))

        if self.user_meet_boss == True: #보스몬스터 나오게 하기

            # 보스몬스터는 무조건 1번에 들어가게 하기
            self.Monster_1_Name.setText(self.dugeonBossbox[self.dungeon_floor - 1].name)  # 보스 이름
            self.Monster_1_QLabel.setPixmap(QPixmap(self.dugeonBossbox[self.dungeon_floor - 1].image))  # 보스몬스터 이미지
            self.Monster_1_QProgressBar.setMaximum(self.dugeonBossbox[self.dungeon_floor - 1].hp)  # 보스몬스터 최대 hp 프로그래스바 1번에 담아주기
            self.Monster_1_QProgressBar.setValue(self.dugeonBossbox[self.dungeon_floor - 1].hp)  # 보스몬스터 현재 hp 프로그래스바 1번에 담아주기
            self.dungeon_random_monster_hp[1] = self.dugeonBossbox[
                self.dungeon_floor - 1].hp  # 보스몬스터와 몬스터들 hp딕셔너리 1번에 보스몬스터 hp 담아주기
            self.Monster_1_Name.show()  # 몬스터들 속성 보여주기 아래는 동일함
            self.Monster_1_QLabel.show()
            self.Monster_1_QButton.show()
            self.Monster_1_QProgressBar.show()

            #보스몬스터와 나오는 랜덤 몬스터 숫자
            dungeon_monster_num = random.randint(0, 6)
            print('보스몬스터와 함게 나오는 던전몬스터 등장 숫자',dungeon_monster_num)
            for i in range(1, dungeon_monster_num+1):
                dungeon_monster_style.append(random.randint(1, 12))

            for num in range(2, dungeon_monster_num + 2):
                monster = self.dugeonfieldbox[dungeon_monster_style[num-2]-1]
                getattr(self, f'Monster_{num}_Name').setText(monster.name)  # MonsterImage 이름
                getattr(self, f'Monster_{num}_QLabel').setPixmap(QPixmap(monster.image))  # MonsterImage 이미지
                getattr(self, f'Monster_{num}_QProgressBar').setMaximum(monster.hp)  # MonsterImage 체력
                self.dungeon_random_monster_hp[num] = monster.hp  # MonsterImage 체력 더하기
                getattr(self, f'Monster_{num}_QProgressBar').setValue(monster.hp)  # MonsterImage 체력
                getattr(self, f'Monster_{num}_QButton').setEnabled(False)
                getattr(self, f'Monster_{num}_Name').show()
                getattr(self, f'Monster_{num}_QLabel').show()
                getattr(self, f'Monster_{num}_QButton').show()
                getattr(self, f'Monster_{num}_QProgressBar').show()

            for num in range(dungeon_monster_num+2, 10 + 1):
                getattr(self, f'Monster_{num}_Name').hide()
                getattr(self, f'Monster_{num}_QLabel').hide()
                getattr(self, f'Monster_{num}_QButton').hide()
                getattr(self, f'Monster_{num}_QProgressBar').hide()

        else:
            dungeon_monster_random_num = random.randint(1, 10) #던전몬스터 숫자
            print('던전몬스터 등장 숫자: ',dungeon_monster_random_num)
            for i in range(1, dungeon_monster_random_num+1): #던전 몬스터 스타일 담기
                dungeon_monster_style.append(random.randint(1, 12))

            for num in range(1, dungeon_monster_random_num + 1):
                monster = self.dugeonfieldbox[dungeon_monster_style[num-1]-1]
                getattr(self, f'Monster_{num}_Name').setText(monster.name)  # MonsterImage 이름
                getattr(self, f'Monster_{num}_QLabel').setPixmap(QPixmap(monster.image))  # MonsterImage 이미지
                getattr(self, f'Monster_{num}_QProgressBar').setMaximum(monster.hp)  # MonsterImage 체력
                self.dungeon_random_monster_hp[num] = monster.hp  # MonsterImage 체력 더하기
                getattr(self, f'Monster_{num}_QProgressBar').setValue(monster.hp)  # MonsterImage 체력
                getattr(self, f'Monster_{num}_QButton').setEnabled(False)
                getattr(self, f'Monster_{num}_Name').show()
                getattr(self, f'Monster_{num}_QLabel').show()
                getattr(self, f'Monster_{num}_QButton').show()
                getattr(self, f'Monster_{num}_QProgressBar').show()

            for num in range(dungeon_monster_random_num+1, 10 + 1):
                getattr(self, f'Monster_{num}_Name').hide()
                getattr(self, f'Monster_{num}_QLabel').hide()
                getattr(self, f'Monster_{num}_QButton').hide()
                getattr(self, f'Monster_{num}_QProgressBar').hide()

        print('던전몬스터스타일', dungeon_monster_style)  # 확인용
        self.portal_hide(True)

    def portal_hide(self, state):
        """던전 입장할 때 없애줄 라벨들(보스몬스터, 포탈, 캐릭터 라벨)"""
        if state == True:
            self.boss_monster.hide()
            self.entrance.hide()
            self.Character_QLabel_2.hide()
        else:
            self.boss_monster.show()
            self.entrance.show()
            self.Character_QLabel_2.show()

    def map_hack(self):
        """맵핵 구현 함수"""
        self.StackWidget_Field.setCurrentIndex(1) # 던전으로 갔다가
        self.portal_hide(False)

        QTimer.singleShot(3000, lambda: self.StackWidget_Field.setCurrentIndex(2))
        QTimer.singleShot(3000, lambda: self.portal_hide(True))
        QTimer.singleShot(3000, lambda: self.portal_timer.stop())

        #0.5초동안 깜빡거리게
        self.portal_timer = QTimer()
        self.portal_timer.start(100)
        self.portal_timer.timeout.connect(self.blink_portal)

    def blink_portal(self):
        if self.entrance.palette().color(QtGui.QPalette.Background) == QtGui.QColor('transparent'):
            self.entrance.setStyleSheet('background-color: red')
        else:
            self.entrance.setStyleSheet('background-color: transparent')
        # 소연 함수 끝 ===================================================================================================================


    # 신규함수 ========================================================================================================================

    # 몬스터가 랜덤 등장하는 부분
    def Add_Monster_info(self):
        # MonsterRand
        """MonsterImage 랜덤 등장 구현"""
        monster_random_num = random.randrange(2, 11)  # MonsterImage 랜덤 등장 숫자
        self.monster_hp_dict = {}  # 빈 딕셔너리에 MonsterImage 체력 담기
        list_fieldname = ["불", "눈", "숲", "물"]
        list_namecolor = ["Color : white", "Color : red", "Color : white", "Color : white"]
        for idx, fieldname in enumerate(list_fieldname):
            if fieldname == self.user_location(self.Character_QLabel.x(), self.Character_QLabel.y()): #소연수정
                self.monrand = random.randrange(0, 3)
                self.back_ground_label.setPixmap(QtGui.QPixmap(self.nomalfield_backgroundBox[idx][self.monrand]).scaled(QSize(1580, 830),aspectRatioMode=Qt.IgnoreAspectRatio))
                self.namecolor = list_namecolor[idx]

        for num in range(1, monster_random_num):
            for idx, field in enumerate(list_fieldname):
                if field == self.user_location(self.Character_QLabel.x(), self.Character_QLabel.y()):
                    self.monrand = random.randrange(0, 4)
                    self.monster = self.nomalfieldallBox[idx][self.monrand]
            getattr(self, f'Monster_{num}_Name').setText(self.monster.name)  # MonsterImage 이름
            getattr(self, f'Monster_{num}_Name').setStyleSheet(self.namecolor)
            getattr(self, f'Monster_{num}_QLabel').setPixmap(QPixmap(self.monster.image))  # MonsterImage 이미지
            getattr(self, f'Monster_{num}_QProgressBar').setMaximum(self.monster.hp)  # MonsterImage 체력
            self.monster_hp_dict[num] = self.monster.hp  # MonsterImage 체력 더하기
            getattr(self, f'Monster_{num}_QProgressBar').setValue(self.monster.hp)  # MonsterImage 체력
            getattr(self, f'Monster_{num}_QButton').setEnabled(False)
            getattr(self, f'Monster_{num}_Name').show()
            getattr(self, f'Monster_{num}_QLabel').show()
            getattr(self, f'Monster_{num}_QButton').show()
            getattr(self, f'Monster_{num}_QProgressBar').show()

        print("몬스터체력", self.monster_hp_dict)

        for num in range(monster_random_num, 10 + 1):
            getattr(self, f'Monster_{num}_Name').hide()
            getattr(self, f'Monster_{num}_QLabel').hide()
            getattr(self, f'Monster_{num}_QButton').hide()
            getattr(self, f'Monster_{num}_QProgressBar').hide()


    # 전투 시작
    # 유저 턴 시작
    def User_Turn(self):
        """유저 턴이었을 때"""
        if self.battle_type == '일반전투':
            if self.go_to_normalfield(): #일반필드나가기
                return
            if self.user_turn >= 5:  # 만약 유저 턴이 5보다 크다면
                self.user_turn = 1  # 1로 만들어준다.
                print("여기서 오류가 나나요 여기는 유저턴임 몬스터가 유저 때리기 전임")
                self.monster_attack_users()  # 이거 여기다 넣으니까 (동시 다발적으로 캐릭터가 죽으면 턴이 넘어가도 몬스터가 공격을안함) 이 현상이 해결됨..

            else:
                self.user_turn += 1  # 그렇지 않다면 턴 더해주기
            print('현재 턴은', self.user_turn)  # 확인용


        ###################################################################
        if self.battle_type == '던전전투':
            if self.go_to_dungeonfield(): #던전필드로 나가기
                return

            if self.user_turn >= 5:  # 만약 유저 턴이 5보다 크다면
                self.user_turn = 1  # 1로 만들어준다.
                print("여기서 오류가 나나요 여기는 유저턴임 몬스터가 유저 때리기 전임")
                self.monster_attack_users()  # 이거 여기다 넣으니까 (동시 다발적으로 캐릭터가 죽으면 턴이 넘어가도 몬스터가 공격을안함) 이 현상이 해결됨..
            else:
                self.user_turn += 1  # 그렇지 않다면 턴 더해주기
            print('현재 턴은', self.user_turn)  # 확인용


        # 유저턴 hp 0 이상이면 활성화 / 아니면 다음 턴으로 넘어감
        selected_character_hp = self.class_hp_dict[self.user_turn]  # 선택된 캐릭터의 hp
        if selected_character_hp > 0:
            self.active_class_frame(self.user_turn)  # 해당 클래스 버튼들 활성화 및 다른 프레임 버튼들 비활성화

        else:
            self.User_Turn()  # 0보다 작으면 다시 User_Turn 돌아감 (재귀함수)






    def change_the_portal_location(self, index, num):
        """포탈 위치 랜덤 배정"""
        if index == 1:
            self.battle_cnt += 1
        if index == 2:
            self.battle_cnt_for_dungeon += 1

        if self.battle_cnt % num == 0 and index == 1: #노말필드일 경우
            self.Log_textEdit.append(f'전투가 {num}번 되었습니다. 포탈 위치를 변경합니다.')
            print(f"############################일반필드전투가 {num}번 되었습니다. 포탈 위치를 변경합니다.")
            self.portal_sample.move(random.randint(0, 1580), random.randint(0, 760))  # 포탈 위치 랜덤으로 배정

        if self.battle_cnt_for_dungeon % num == 0 and index == 2:# 던전필드인 경우
            self.Log_textEdit.append(f'전투가 {num}번 되었습니다. 포탈 위치를 변경합니다.')
            print(f"############################던전필드전투가 {num}번 되었습니다. 포탈 위치를 변경합니다.")
            random_x = random.randint(self.map_size[self.random_num_for_teleport][0],self.map_size[self.random_num_for_teleport][1])
            random_y = random.randint(self.map_size[self.random_num_for_teleport][2],self.map_size[self.random_num_for_teleport][3])
            self.entrance.move(random_x, random_y)

    def go_to_normalfield(self):
        # 만약 모든 유저 hp가 0이면 일반필드로 나가게 함
        if all(h == 0 for h in self.class_hp_dict.values()):

            print("유저체력 부족해서 죽은 경우")
            self.Log_textEdit.append('유저 체력이 부족하여 후퇴합니다...한 발자국만 움직여 보자...')
            self.set_actions_enabled(5, False)  # 클래스들의 모든 버튼 비활성화 시켜줌 <= 지금 작동 안함 살려조ㅁ
            self.current_index = 0
            self.return_user_state() #유저들의 체력 초기화
            self.change_the_portal_location(1, 10) # 미궁 랜덤 스팟
            self.StackWidget_Field.setCurrentIndex(0)  # 일반필드로 이동
            self.portal_sample.show()
            if self.guardLevel < 50:
                self.item_list[-2].stack = self.item_list[-2].stack + 5
            else:
                self.item_list[-2].stack = self.item_list[-2].stack + 5
                self.item_list[-1].stack = self.item_list[-1].stack + 5
            self.consumable_reset()
            return True


        if all(v == 0 for v in self.monster_hp_dict.values()):
            self.guardLevel += 1

            print("현재 레벨 %d(몬스터 처치한 경우)" % self.guardLevel)
            self.TopUI_Level_Label.setText("%s의 수호대 Level : %d" % (self.guardname, self.guardLevel))
            print("몬스터 체력이 0입니다.")
            self.Log_textEdit.append('몬스터를 모두 처치했습니다....')
            # noraml_previous_position
            self.user_turn = 0
            self.set_actions_enabled(5, False) #클래스들의 모든 버튼 비활성화 시키기
            self.Character_QLabel.move(self.normal_previous_position.x(), self.normal_previous_position.y())
            self.change_the_portal_location(1, 10)  # 미궁 랜덤 스팟
            self.StackWidget_Field.setCurrentIndex(0)  # 일반필드로 이동
            print('몬스터 다 죽이고 나왔을 때 유저턴', self.user_turn)
            self.portal_sample.show()
            return True
        return False

    def go_to_dungeonfield(self):
        """던전에서 싸우고 다시 던전으로 돌아가는 함수"""

        if all(h == 0 for h in self.class_hp_dict.values()):

            print("유저체력 부족해서 죽은 경우")
            self.Log_textEdit.append('유저 체력이 부족하여 후퇴합니다...한 발자국만 움직여 보자...')
            self.set_actions_enabled(5, False)  # 클래스들의 모든 버튼 비활성화 시켜줌 <= 지금 작동 안함 살려조ㅁ
            self.change_the_portal_location(2, 7) # 전투 7번만다 미궁 랜덤 스팟
            self.return_user_state()  # 유저들의 체력 초기화
            self.StackWidget_Field.setCurrentIndex(1)  # 던전필드로 이동
            self.portal_hide(False) # 포탈, 캐릭터, 보스포탈 나오게 하기
            self.user_win_the_boss_stage(self.user_meet_boss)
            return True

        if all(v == 0 for v in self.dungeon_random_monster_hp.values()):
            self.guardLevel += 1
            print("현재 레벨 %d(몬스터 처치한 경우)" % self.guardLevel)
            self.TopUI_Level_Label.setText("%s의 수호대 Level : %d" % ("땅", self.guardLevel))
            print("몬스터 체력이 0입니다.")
            if self.guardLevel < 50:
                self.item_list[-2].stack = self.item_list[-2].stack + 5
            else:
                self.item_list[-2].stack = self.item_list[-2].stack + 5
                self.item_list[-1].stack = self.item_list[-1].stack + 5
            self.consumable_reset()
            self.Log_textEdit.append('몬스터를 모두 처치했습니다....')
            self.user_turn = 0
            self.set_actions_enabled(5, False)  # 클래스들의 모든 버튼 비활성화 시키기
            self.StackWidget_Field.setCurrentIndex(1)  # 던전필드로 이동
            print('몬스터 다 죽이고 나왔을 때 유저턴', self.user_turn)
            self.portal_hide(False)  # 포탈, 캐릭터, 보스포탈 나오게 하기
            self.change_the_portal_location(2, 7) # 전투 7번마다 랜덤 스팟되게 하기
            self.user_win_the_boss_stage(self.user_meet_boss)
            return True
        return False

    def user_win_the_boss_stage(self, state):
        """보스와의 전투에서 이겼을 때 변하는 부분"""
        #TODO 여기에 에필로그 이동으로 이동하기 중요 중요 중요
        if state == True:
            self.dungeon_floor += 1
            print('던전층: ', self.dungeon_floor)
            self.show_messagebox("어디선가 문이 열리는 소리가 들립니다...")
            self.user_meet_boss = False
            self.entrance.setPixmap(QtGui.QPixmap('./image/downstair.png'))
            map_num = self.random_num_for_teleport
            self.boss_monster.move(random.randint(self.map_size[map_num][0], self.map_size[map_num][1]),
                                   random.randint(self.map_size[map_num][2], self.map_size[map_num][3]))
            # self.boss_monster.close()
            if self.dungeon_floor == 8:
                self.show_messagebox("당신은 게임을 클리어했습니다!")
                self.show_ending() #엔딩 크레딧 넣기

                # 여기에 엔딩 크레딧 넣기 중요 중요 중요

    def skillopen(self, num):
        """스킬 함수(스킬 버튼 외 다른 버튼 비활성화, 몬스터 공격 버튼 활성화) # 일단 기존 함수 제외하고 쓰는중"""
        # 스킬 버튼 외에 다른 버튼 비활성화
        self.carit = num
        self.attackType = 1
        self.Log_textEdit.append(getattr(self, f"Status{num}_1_Name").text() + "이(가)스킬버튼을 선택했습니다.")
        # 추가 항목 frames는 스킬 위젯에 각각의 클래스별 프레임들을 담아둔 리스트
        frames = [
            self.Frame_Class1,
            self.Frame_Class2,
            self.Frame_Class3,
            self.Frame_Class4,
            self.Frame_Class5,
            self.Frame_Class6
        ]
        # getattr를 써서 스킬위젯의 클래스 네임을 가져오려했는데 예) <b>미<b/><b>하<b/><b>일<b/> 이렇게 가져와짐
        # 고로 그냥 리스트 만들어서 썼심
        self.class_name_list = ["미하일", "루미너스", "알렉스", "샐러맨더", "메르데스", "랜슬롯"]
        self.class_atk = 1
        # 시작하기전에 프레임 전부 잠굼
        for rock in frames:
            rock.setEnabled(False) # 모든 클래스 버튼 잠구기
        # find : 2023.05.25 AM 09:55
        for rock in self.pushbox:
            rock.setEnabled(False) # 클래스별 버튼 잠구기 ( 레벨에 따라 열리게 하기위한 조건)

        # 해당하는 프레임만 열었음 내가 선택한 클래스 네임과 스킬 위젯 클래스 네임 비교해서 맞으면 켜라라고 했음
        for classnum in range(0, 6):
            if getattr(self, f"Status{num}_1_Name").text() == self.class_name_list[classnum]:
                frames[classnum].setEnabled(True) # 선택한 클래스와 스킬위젯의 클래스이름 비교 맞으면 setEnabled를 True로
                for skill in self.skillall: # 스킬들을 전부 체크
                    if skill.rockonlevel <= self.guardLevel: # 그 스킬들중 해금 레벨에 해당하는것들만 찾기
                        for rockon in self.pushbox: # 스킬 버튼 전부 체크
                            if rockon.text() == skill.name: # 스킬들중 해금레벨에 해당하는 스킬버튼 활성화
                                rockon.setEnabled(True)
                self.class_atk = int(getattr(self, f'Class{num}_DetailsStatus_AtkValue').text()) #해당하는 클래스의 공격력을 가져옴
                self.class_mp = int(self.class_mp_dict.get(num))

        getattr(self, f'Status{num}_Action1_Attack').setEnabled(False)
        getattr(self, f'Status{num}_Action3_Item').setEnabled(False)
        getattr(self, f'Status{num}_Action4_Run').setEnabled(False)
        self.Widget_Skill.show()
        for idx, skillbtn in enumerate(self.pushbox):
            skillbtn.clicked.connect(lambda x, y=idx + 1, z = self.class_atk, u = self.class_mp, n = num: self.btnname(y, z, u, n))

    def btnname(self, obnum, classatk, classmp, classnum):
        """스킬 선택 관련 버튼 타겟 0이면 아군 적용 타겟 1이면 적군 단일 적용 타겟 2면 적군 전체 적용"""
        print("넘어온 클래스의 공격력 값 : %d"%classatk)
        print("넘어온 클래스의 마나 값 : %d"%classmp)
        print("넘어온 클래스 번호 값 : %d"%classnum)
        for skillbtn in self.pushbox:
            skillbtn.disconnect()

        self.dict_skillname = {1: "힐", 2: "그레이트 힐", 3: "힐 올", 4: "공격력 업", 5: "방어력 업", 6: "맵핵", 7: "파이어 볼",
                               8: "파이어 월",
                               9: "블리자드", 10: "썬더브레이커", 11: "힐", 12: "그레이트 힐", 13: "힐 올", 14: "파이어 볼", 15: "파이어 월",
                               16: "블리자드", 17: "썬더브레이커", 18: "집중타", 19: "듀얼 샷", 20: "마스터 샷", 21: "강타", 22: "도발"}
        self.dict_skill_damage = {"힐": 0, "그레이트 힐": 0, "힐 올": 0, "공격력 업": 0, "방어력 업": 0, "맵핵": 0, "파이어 볼": 100,
                                  "파이어 월": 200, "블리자드": 300, "썬더브레이커": 400, "집중타": 100, "듀얼 샷": 200, "마스터 샷": 300,
                                  " 강타": 500, "도발": 0}
        self.heal_list = ["힐", "그레이트 힐", "힐 올"]
        self.buff_list = ["공격력 업", "방어력 업"]
        self.choice_btn = self.dict_skillname[obnum]
        self.target = self.skillact()
        for skill in self.skillall:
            if self.choice_btn == skill.name and skill.target == 0:
                self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
                self.Page_Use_ing.setEnabled(True)
                self.monster_btn_active(False)
                if self.choice_btn in self.heal_list:
                    for i in range(1, 7):
                        getattr(self, f'Class_{i}_Btn').clicked.connect(lambda x, y = i: self.skill_heal(y))
                        self.Log_textEdit.append(self.pushbox[obnum - 1].text() + "을(를) 선택하셨습니다.\n↓")
                        return
                elif self.choice_btn in self.buff_list:
                    if self.choice_btn == "방어력 업":
                        for i in range(1, 6):
                            getattr(self, f"Class{i}_DetailsStatus_ShieldValue").setText(
                                str(int(int(getattr(self, f'Class{i}_DetailsStatus_ShieldValue').text()) * 1.5)))
                        self.Log_textEdit.append("아군 전원이 1턴간 방어력 50퍼가 증가하였습니다")
                    else:
                        for i in range(1, 6):
                            self.damage_status = str(int((self.class_item[i - 1][4].damage * self.guardLevel) * 10 * 1.5))
                            getattr(self, f'Class{i}_DetailsStatus_AtkValue').setText(self.damage_status)
                        for i in range(1, 6):
                            getattr(self, f"Class{i}_DetailsStatus_ShieldValue").setText(
                                str(int(int(getattr(self, f'Class{i}_DetailsStatus_ShieldValue').text()) * 1.5)))
                        self.Log_textEdit.append("아군 전원이 1턴간 방어력 50퍼가 증가하였습니다")
                    for skill in self.skillall:
                        if self.dict_skillname[obnum] == skill.name:
                            print("내가 선택한 스킬 이름", skill.name)
                            print("내가 클릭한 버튼 값 :%d" % skill.value)
                            print("내가 선택한 스킬의 마나 값 %d" % skill.mp)
                            # find : 2023.05.25 AM 10:37
                            self.skill_mpvlaue = int(classmp * skill.mp)
                            self.choice_btn = int(classatk * skill.value)
                    if self.class_mp_dict[classnum] >= self.skill_mpvlaue:
                        self.class_mp_dict[classnum] -= self.skill_mpvlaue
                    else:
                        self.class_mp_dict[classnum] = 0
                    self.status_page_reset()
                    self.low_ui_reset()
                    self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
                    if self.user_turn >= 5:
                        self.user_turn = 0
                        self.monster_attack_users()
                        return
                    print("힐썼을때 유저턴 ", self.user_turn)
                    self.User_Turn()
                    return
            elif skill.name == self.choice_btn and skill.target >= 1:
                self.monster_btn_active(True)
        self.Log_textEdit.append(self.pushbox[obnum - 1].text() + "을(를) 선택하셨습니다.\n↓")
        for rockbtn in self.pushbox:
            rockbtn.setEnabled(False)
        self.skill_mpvlaue = 0
        for skill in self.skillall:
            if self.dict_skillname[obnum] == skill.name:
                print("내가 선택한 스킬 이름", skill.name)
                print("내가 클릭한 버튼 값 :%d" % skill.value)
                print("내가 선택한 스킬의 마나 값 %d"% skill.mp)
                # find : 2023.05.25 AM 10:37
                self.skill_mpvlaue = int(classmp * skill.mp)
                self.choice_btn = int(classatk*skill.value)
        if self.class_mp_dict[classnum] >= self.skill_mpvlaue:
            self.class_mp_dict[classnum] -= self.skill_mpvlaue
        else:
            self.class_mp_dict[classnum] = 0
        self.status_page_reset()
        self.low_ui_reset()
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        print("내가 클릭한 버튼 값 :%d" % obnum)
        print("내가 선택한 스킬의 공격력:%d"%self.choice_btn)

    def skillact(self):
        """스킬 선택했을때 그 스킬이름과 같은 데미지가 적용하게 하는 함수
        순서 : 스킬 버튼을 클릭한다 -> self.choice_btn에 스킬이름이 담긴다 -> 이 함수에서 스킬 데미지로 치환한다."""
        self.skillbox()
        for skill in self.skillall:
            if ((skill.name == self.choice_btn)
                    and (skill.target == 1)):
                return 1
            elif ((skill.name == self.choice_btn)
                  and (skill.target == 2)):
                return 2
            elif ((skill.name == self.choice_btn)
                  and (skill.target == 3)):
                return 3
            elif ((skill.name == self.choice_btn)
                  and (skill.target == 0)): # 스킬 타겟이 0번일때 페이지 이동하면서 그 페이지 활성화
                return 0
    def skill_buff(self, num):
        pass
    def skill_heal(self, num):
        """힐을 썼을때 여기 함수 타서 힐적용됨"""
        for i in range(6):
            if self.list_class[i][0].character_name == '루미너스' or self.list_class[i][0].character_name == "샐러맨더":
                healer = i+1
        if self.choice_btn == '힐':
            heal_rate = self.skill_1.value/100

            if self.class_mp_dict[healer] < 10:
                self.Log_textEdit.append('마나가 부족합니다')

            else:
                self.class_mp_dict[healer] = int(self.class_mp_dict[healer] - self.skill_1.mp)
                self.class_hp_dict[num] = self.class_hp_dict[num] + (self.list_class[num-1][0].get_maxhp() * heal_rate)
                if self.class_hp_dict[num] > self.list_class[num-1][0].get_maxhp():
                    self.class_hp_dict[num] = self.list_class[num-1][0].get_maxhp()
                self.Log_textEdit.append('%s의 체력을 %d%% 회복하였습니다' %
                                         (self.list_class[num-1][0].character_name, int(heal_rate*100)))

        elif self.choice_btn == '그레이트 힐':
            great_heal_rate = self.skill_2.value/100
            if self.class_mp_dict[2] < 20:
                self.Log_textEdit.append('마나가 부족합니다')

            else:
                self.class_mp_dict[healer] = self.class_mp_dict[healer] - self.skill_2.mp
                self.class_hp_dict[num] = self.class_hp_dict[num] + (self.list_class[num-1][0].get_maxhp() * great_heal_rate)
                if self.class_hp_dict[num] > self.list_class[num-1][0].get_maxhp():
                    self.class_hp_dict[num] = self.list_class[num-1][0].get_maxhp()
                self.Log_textEdit.append('%s의 체력을 %d%% 회복하였습니다' %
                                         (self.list_class[num - 1][0].character_name, int(great_heal_rate * 100)))

        elif self.choice_btn == '힐 올':
            all_heal_rate = self.skill_3.value/100
            if self.class_mp_dict[healer] < 10:
                self.Log_textEdit.append('마나가 부족합니다')

            else:
                self.class_mp_dict[healer] = self.class_mp_dict[healer] - self.skill_3.mp
                alive_class = [key for key, value in self.class_hp_dict.items() if value > 0]
                for i in range(len(alive_class)):
                    if self.class_hp_dict[i+1] == 0:
                        pass
                    else:
                        self.class_hp_dict[i+1] = \
                            self.class_hp_dict[i+1] + (self.list_class[i][0].get_maxhp() * all_heal_rate)
                        if self.class_hp_dict[i+1] > self.list_class[i][0].get_maxhp():
                            self.class_hp_dict[i+1] = self.list_class[i][0].get_maxhp()
                self.Log_textEdit.append('아군 전체의 체력을 %d%% 회복하였습니다' % int(all_heal_rate * 100))
        self.status_page_reset()
        self.low_ui_reset()
        self.Widget_Skill.close()
        if self.user_turn >= 5:
            self.user_turn = 0
            self.monster_attack_users()
            return
        print("힐썼을때 유저턴 ", self.user_turn)
        self.User_Turn()
        for i in range(6):
            getattr(self, f'Class_{i + 1}_Btn').disconnect()





    def attack_function(self, num):
        """공격 함수(공격버튼 외 다른 버튼 비활성화, 몬스터 공격버튼 활성화)"""
        self.attackType = 0
        self.carit = num
        self.Log_textEdit.append(getattr(self, f"Status{num}_1_Name").text()+"이(가) 공격버튼을 선택했습니다.")
        self.name = [self.list_class[0][0].character_name, self.list_class[1][0].character_name,
                     self.list_class[2][0].character_name, self.list_class[3][0].character_name,
                     self.list_class[4][0].character_name, self.list_class[5][0].character_name]
        selection_class = self.name.index(getattr(self, f'Status{num}_1_Name').text())+1
        self.choice_btn = int(getattr(self, f'Class{selection_class}_DetailsStatus_AtkValue').text())
        print(self.name)
        print(selection_class)
        print(getattr(self, f'Status{num}_1_Name').text())
        print("클래스의 이름은?? : "+getattr(self, f'Class{selection_class}_DetailsStatus_Name').text())
        print("클래스의 공격력 : %d"%int(getattr(self, f'Class{selection_class}_DetailsStatus_AtkValue').text()))

        # fixfind
        # 공격 버튼 외에 다른 버튼 비활성화
        getattr(self, f'Status{num}_Action2_Skill').setEnabled(False)
        getattr(self, f'Status{num}_Action3_Item').setEnabled(False)
        getattr(self, f'Status{num}_Action4_Run').setEnabled(False)

        # 몬스터 공격 버튼 활성화
        self.monster_btn_active(True)

    def Iteam_function(self, num):
        """아이템 선택시 나머지 버튼 잠김"""
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        self.Page_Use.setEnabled(True)
        self.Log_textEdit.append(getattr(self, f"Status{num}_1_Name").text()+"이(가) 아이템버튼을 선택했습니다.\n↓")
        getattr(self, f'Status{num}_Action1_Attack').setEnabled(False)
        getattr(self, f'Status{num}_Action2_Skill').setEnabled(False)
        getattr(self, f'Status{num}_Action4_Run').setEnabled(False)

    def Iteam_name(self, num):
        """아이템 선택시 발동되는 함수"""
        self.Log_textEdit.append(getattr(self, f'Portion_{num}_Btn').text()) # 해당 아이템 클릭시 상호작용 확인용


    def Run_function(self, num):
        self.Log_textEdit.append(getattr(self, f"Class{num}_DetailsStatus_Name").text()+"이(가) 도망버튼을 클릭하였습니다.\n↓")
        if self.user_turn >= 5:
            self.user_turn = 0
            self.monster_attack_users()
            return
        # 도망 성공시 방어력 * 100시켜줌
        # 도망확률 30퍼
        self.run_rand = random.randrange(0,10)
        if self.run_rand <= 3:
            self.Log_textEdit.append(getattr(self, f"Class{num}_DetailsStatus_Name").text()+"이(가) 방어에 성공하였습니다.\n↓")
            getattr(self, f"Class{num}_DetailsStatus_ShieldValue").setText(str(int(getattr(self, f'Class{num}_DetailsStatus_ShieldValue').text())*100))
            self.Log_textEdit.append("1턴동안 방어력이 %s로 상승하였습니다.\n어떠한 공격이든 막을수 있을것입니다..\n"%getattr(self, f"Class{num}_DetailsStatus_ShieldValue").text())
            self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        else:
            self.Log_textEdit.append(getattr(self, f"Class{num}_DetailsStatus_Name").text() + "이(가) 방어에 실패하였습니다.\n")

        self.User_Turn()

        getattr(self, f'Status{num}_Action1_Attack').setEnabled(False)
        getattr(self, f'Status{num}_Action2_Skill').setEnabled(False)
        getattr(self, f'Status{num}_Action3_Item').setEnabled(False)

    def monster_got_damage(self, num):

        """몬스터 데미지 입는 함수"""
        self.atkup_reset(self.carit)
        if self.battle_type == '일반전투':
            monster_hp = self.monster_hp_dict
        elif self.battle_type == '던전전투':
            monster_hp = self.dungeon_random_monster_hp


        if self.attackType == 1:
            if self.target == 2:
                for i in range(1, len(self.monster_hp_dict.keys()) + 1):
                    monster_hp[i] -= self.choice_btn
                    self.Log_textEdit.append(
                        "%s에게 %d만큼의 데미지를 입혔습니다." % (getattr(self, f'Monster_{i}_Name').text(), self.choice_btn))
            elif self.target == 1:
                print("내가 선택한 스킬의 데미지%d"%self.choice_btn)
                self.Log_textEdit.append("%s에게 %d만큼의 데미지를 입혔습니다."%(getattr(self, f'Monster_{num}_Name').text(), self.choice_btn))
                monster_hp[num] -= self.choice_btn
            elif self.target == 3:
                self.provocation_skill_motion()

            self.Widget_Skill.close()
        elif self.attackType == 0:
            self.attack_effect(num-1)
            monster_hp[num] -= self.choice_btn  # 임시로 몬스터 체력에는 100씩 데미지 입힘


        print(f'{num}번 몬스터의 맞은 후 체력: {monster_hp[num]}')  # 확인용

        if self.battle_type == '일반전투':
            if self.go_to_normalfield():
                return
        if self.battle_type == '던전전투':
            if self.go_to_dungeonfield():
                return

        # 체력 0인 얘들은 안보여주기
        for m, n in monster_hp.items():
            if n < 0:
                print(f'{m}번 몬스터를 처치했습니다.')  # 콘솔 확인용

                self.Log_textEdit.append(f'{m}번 몬스터를 처치했습니다.')
                #132123132132132
                monster_hp[m] = 0

                # 죽은 몬스터 구성들은 숨겨주기
                getattr(self, f'Monster_{m}_Name').hide()
                getattr(self, f'Monster_{m}_QLabel').hide()
                getattr(self, f'Monster_{m}_QButton').hide()
                getattr(self, f'Monster_{m}_QProgressBar').hide()

        if self.battle_type == '일반전투':
            if self.go_to_normalfield():
                return
        if self.battle_type == '던전전투':
            if self.go_to_dungeonfield():
                return
        # if all(v == 0 for v in self.monster_hp_dict.values()):
        #     self.guardLevel += 1  # 적을 모두처치하면 레벨업 +1
        #     print("현재 레벨 %d" % self.guardLevel)
        #     self.TopUI_Level_Label.setText("%s의 수호대 Level : %d" % ("땅", self.guardLevel))
        #     print("몬스터 체력이 0입니다.")
        #     self.Log_textEdit.append('몬스터를 모두 처치했습니다....')
        #     self.StackWidget_Field.setCurrentIndex(0)  # 일반필드로 이동

        # 프로그래스바에 유저가 때린 몬스터 체력 넣어주기
        getattr(self, f'Monster_{num}_QProgressBar').setValue(monster_hp[num])  # 몬스터 체력

        # 몬스터 버튼 비활성화
        self.monster_btn_active(False)

        # 공격 버튼 비활성화
        getattr(self, f'Status{self.user_turn}_Action1_Attack').setEnabled(False)

        print(f'다음 턴으로 넘어가야됨=========================(지금 유저턴{self.user_turn})')
        # self.go_to_normalfield()

        if self.user_turn == 5:
            self.user_turn = 0  # 유저 턴 0으로 만들어주고 다른 버튼들 비활성화 시켜줌(나중에 단축시킬 것)
            self.set_actions_enabled(5, False)  # 비활성화 시켜주고 소연수정
            ### 몬스터 공격 함수로 넘어가야됨
            print("몬스터 데미지 입는 곳 가기 전임")
            self.monster_attack_users()

        else:  # 유저턴이 5 미만이면 다시 유저턴으로 돌아감
            ################################### 다음 턴으로 넘어가기 몬스터 턴에서 더해주기!!!!!!!!!!!! ########################################
            self.User_Turn()




    def monster_attack_users(self):
        """몬스터가 유저 랜덤으로 때리는 함수"""
        # 살아있는 몬스터가 돌아가면서 랜덤으로 유저 때림
        # 유저hp가 0이 되면 패스
        # 살아있는 몬스터 수 세기(죽으면 hide() 시켜줌)


        if self.battle_type == '일반전투':
            monster_hp = self.monster_hp_dict
        elif self.battle_type == '던전전투':
            monster_hp = self.dungeon_random_monster_hp

        self.alive_monster = []  # 살아있는 몬스터 리스트에 담아주기
        for i, j in monster_hp.items():  # 몬스터 체력 딕셔너리는 몬스터 호출 함수 Add_Monster_info 에 있음. 여기서 체력을 가져와줌
            print(i, j)  # 확인용
            if j > 0:  # 만약 몬스터 체력이 0 이상이면
                self.alive_monster.append(i)  # 빈 리스트에 더해준다.
                pass
            elif j <= 0:  # 만약 몬스터 체력이 0 이면
                pass

        print('살아있는 몬스터 리스트는', self.alive_monster)

        # 살아있는 클래스 수 세기
        self.alive_class = [key for key, value in self.class_hp_dict.items() if value > 0]


        # 어떤 클래스 때릴지 랜덤으로 리스트에 추가 - 몬스터 갯수만큼 세주기
        # 수정해서 미안하지만 리스트 6번을 공격 대상에서 빼야 했어서 어쩔 수 없었음
        attacked_class_list = []
        for i in range(1, len(self.alive_monster) + 1):
            attacked_class_list.append(random.choice(self.alive_class))

        print("attacked_class_list", attacked_class_list)

        # 클래스의 hp 깎아준다
        # 클래스 라벨들


        # 클래스 값 넣어줄 리스트
        class_hp_present_value_list = [
            self.Status1_2_HpValue,
            self.Status2_2_HpValue,
            self.Status3_2_HpValue,
            self.Status4_2_HpValue,
            self.Status5_2_HpValue,
        ]
        death_class = []

        if not self.user_meet_boss: #보스를 만나지 않은 경우(일반몬스터)

            for m in range(1, len(self.alive_monster) + 1):
                # self.Log_textEdit.append(f"{m}번째 몬스터가 {attacked_class_list[m - 1]}번 클래스를 100만큼 때립니다...")
                self.nomalfield_monster_skill = random.randrange(0,10)
                if self.nomalfield_monster_skill > 3:
                    self.Log_textEdit.append(f"{m}번째 몬스터가 스킬을 사용하여 %s에게 %d의 데미지를 입혔습니다"%(getattr(self, f"Status{attacked_class_list[m - 1]}_1_Name").text(),int(self.class_hp_dict[attacked_class_list[m - 1]]/10)))
                    self.nomalfield_atk = 0.3
                else:
                    self.Log_textEdit.append(f"{m}번째 몬스터가 일반 공격을 사용하여 %s에게 %d의 데미지를 입혔습니다"%(getattr(self, f"Status{attacked_class_list[m - 1]}_1_Name").text(),int(self.class_hp_dict[attacked_class_list[m - 1]]/10)))
                    self.nomalfield_atk = 0.1
                if (int(self.class_hp_dict[attacked_class_list[m - 1]] * self.nomalfield_atk) < int(getattr(self, f'Class{attacked_class_list[m - 1]}_DetailsStatus_ShieldValue').text())):
                    self.Log_textEdit.append("%s이(가) 방어력이 높아 적의 공격을 막았습니다"%(getattr(self, f"Status{attacked_class_list[m - 1]}_1_Name").text()))
                else:
                    self.class_hp_dict[attacked_class_list[m - 1]] = self.class_hp_dict[attacked_class_list[m - 1]] - (int(self.class_hp_dict[attacked_class_list[m - 1]]/10) - int(getattr(self, f'Class{attacked_class_list[m - 1]}_DetailsStatus_ShieldValue').text()))    # 임시로 100씩 때린다 <- 방어력을 넣어 공격력 감쇄 추가해봄
                print(self.class_hp_dict)  # 확인용

                for i in range(1, 6):
                    if self.class_hp_dict[i] <= 0:
                        if attacked_class_list[m - 1] not in death_class:
                            death_class.append(attacked_class_list[m - 1])
                            self.class_hp_dict[attacked_class_list[m - 1]] = 0
                            print('죽은 클래스는', death_class)
                            self.Log_textEdit.append(f"{attacked_class_list[m - 1]}번 클래스가 사망했습니다.")
                            print(f"{attacked_class_list[m - 1]}번 클래스가 사망했습니다.")
                        else:
                            self.class_hp_dict[attacked_class_list[m - 1]] = 0
        else:
            user_atk = random.randrange(5)
            self.boss_monster_skill = random.randrange(0, 10)
            if self.boss_monster_skill > 7:
                self.Log_textEdit.append("보스몬스터가 스킬을 사용하여 %s에게 %d의 데미지를 입혔습니다" % (
                getattr(self, f"Status{attacked_class_list[user_atk - 1]}_1_Name").text(),
                int(self.class_hp_dict[attacked_class_list[user_atk - 1]] / 50)))
                self.nomalfield_atk = 0.3
            else:
                self.Log_textEdit.append("보스몬스터가 스킬을 사용하여 %s에게 %d의 데미지를 입혔습니다" % (
                getattr(self, f"Status{attacked_class_list[user_atk - 1]}_1_Name").text(),
                int(self.class_hp_dict[attacked_class_list[user_atk - 1]] / 10)))
                self.nomalfield_atk = 0.1
            if (int(self.class_hp_dict[attacked_class_list[user_atk - 1]] * self.nomalfield_atk) < int(
                    getattr(self, f'Class{attacked_class_list[user_atk - 1]}_DetailsStatus_ShieldValue').text())):
                self.Log_textEdit.append("%s이(가) 방어력이 높아 적의 공격을 막았습니다" % (
                    getattr(self, f"Status{attacked_class_list[user_atk - 1]}_1_Name").text()))
            else:
                self.class_hp_dict[attacked_class_list[user_atk - 1]] = self.class_hp_dict[attacked_class_list[user_atk - 1]] - (
                            int(self.class_hp_dict[attacked_class_list[user_atk - 1]] / 10) - int(getattr(self,
                                                                                                   f'Class{attacked_class_list[user_atk - 1]}_DetailsStatus_ShieldValue').text()))  # 임시로 100씩 때린다 <- 방어력을 넣어 공격력 감쇄 추가해봄
            print(self.class_hp_dict)  # 확인용
            for m in range(2, len(self.alive_monster) + 1):
                # self.Log_textEdit.append(f"{m}번째 몬스터가 {attacked_class_list[m - 1]}번 클래스를 100만큼 때립니다...")
                self.nomalfield_monster_skill = random.randrange(0,10)
                if self.nomalfield_monster_skill > 3:
                    self.Log_textEdit.append(f"{m}번째 몬스터가 스킬을 사용하여 %s에게 %d의 데미지를 입혔습니다"%(getattr(self, f"Status{attacked_class_list[m - 1]}_1_Name").text(),int(self.class_hp_dict[attacked_class_list[m - 1]]/10)))
                    self.nomalfield_atk = 0.3
                else:
                    self.Log_textEdit.append(f"{m}번째 몬스터가 일반 공격을 사용하여 %s에게 %d의 데미지를 입혔습니다"%(getattr(self, f"Status{attacked_class_list[m - 1]}_1_Name").text(),int(self.class_hp_dict[attacked_class_list[m - 1]]/10)))
                    self.nomalfield_atk = 0.1
                if (int(self.class_hp_dict[attacked_class_list[m - 1]] * self.nomalfield_atk) < int(getattr(self, f'Class{attacked_class_list[m - 1]}_DetailsStatus_ShieldValue').text())):
                    self.Log_textEdit.append("%s이(가) 방어력이 높아 적의 공격을 막았습니다"%(getattr(self, f"Status{attacked_class_list[m - 1]}_1_Name").text()))
                else:
                    self.class_hp_dict[attacked_class_list[m - 1]] = self.class_hp_dict[attacked_class_list[m - 1]] - (int(self.class_hp_dict[attacked_class_list[m - 1]]/10) - int(getattr(self, f'Class{attacked_class_list[m - 1]}_DetailsStatus_ShieldValue').text()))    # 임시로 100씩 때린다 <- 방어력을 넣어 공격력 감쇄 추가해봄
                print(self.class_hp_dict)  # 확인용

                for i in range(1, 6):
                    if self.class_hp_dict[i] <= 0:
                        if attacked_class_list[m - 1] not in death_class:
                            death_class.append(attacked_class_list[m - 1])
                            self.class_hp_dict[attacked_class_list[m - 1]] = 0
                            print('죽은 클래스는', death_class)
                            self.Log_textEdit.append(f"{attacked_class_list[m - 1]}번 클래스가 사망했습니다.")
                            print(f"{attacked_class_list[m - 1]}번 클래스가 사망했습니다.")
                        else:
                            self.class_hp_dict[attacked_class_list[m - 1]] = 0

        #비석
        for j in death_class:
            self.class_label_list[j - 1].setPixmap(QtGui.QPixmap('./image/비석.png'))

        for i in range(1, 6):
            class_hp_present_value_list[i - 1].setText(
                f'{self.class_hp_dict[i]}/{self.Statusclass[i - 1].get_maxhp()}')  # hp판에 변경된 값 넣어주기

        print("몬스터 공격이 종료되었습니다.")
        self.status_page_reset()    #페이지 리셋 추가
        #여기에서 일반필드로 가는 부분 추가 980625

        self.User_Turn()

    def monster_btn_active(self, state):
        """몬스터 버튼 활성화 함수"""
        for i in range(1, 11):
            getattr(self, f'Monster_{i}_QButton').setEnabled(state)
        # Monster_1_QButton

    def active_class_frame(self, index):
        """특정 클래스 프레임 활성화 """
        print('가져온 인덱스는', index)
        for num in range(1, 6):
            if num == index:
                getattr(self, f'Status{num}_Action1_Attack').setEnabled(True)
                getattr(self, f'Status{num}_Action2_Skill').setEnabled(True)
                getattr(self, f'Status{num}_Action3_Item').setEnabled(True)
                getattr(self, f'Status{num}_Action4_Run').setEnabled(True)
            else:
                getattr(self, f'Status{num}_Action1_Attack').setEnabled(False)
                getattr(self, f'Status{num}_Action2_Skill').setEnabled(False)
                getattr(self, f'Status{num}_Action3_Item').setEnabled(False)
                getattr(self, f'Status{num}_Action4_Run').setEnabled(False)

    def set_actions_enabled(self, status_count, enabled):
        """클래스 프레임 활성화/비활성화 시키기"""
        for i in range(1, status_count + 1):
            getattr(self, f'Status{i}_Action1_Attack').setEnabled(enabled)
            getattr(self, f'Status{i}_Action2_Skill').setEnabled(enabled)
            getattr(self, f'Status{i}_Action3_Item').setEnabled(enabled)
            getattr(self, f'Status{i}_Action4_Run').setEnabled(enabled)

    def teleport_in_dungeon(self):
        """던전 내 캐릭터가 텔레포트 하는 함수"""
        # TODO 기능 구현 후 적용하기(구현 완. m키로 단축기 설정)
        random_x = random.randint(self.map_size[self.random_num_for_teleport][0], self.map_size[self.random_num_for_teleport][1])
        random_y = random.randint(self.map_size[self.random_num_for_teleport][2], self.map_size[self.random_num_for_teleport][3])
        self.Character_QLabel_2.move(random_x, random_y)

    def move_mihail(self):
        """미하일 움직임 좌표 찍기"""
        random_x = random.randint(self.normal_field_size[0], self.normal_field_size[1])
        random_y = random.randint(self.normal_field_size[2], self.normal_field_size[3])
        self.mihail_label.move(random_x, random_y)

    def provocation_skill_motion(self):
        """미하일의 도발 스킬"""
        # 미하일 번호를 가져와서
        # 테스트 미하일 번호
        for i, j in enumerate(self.list_class):
            if j[0].character_name == '미하일':
                mihail_num = i+1
        if mihail_num == '':
            mihail_num = None

        print('미하일 번호는', mihail_num)

        # 그 라벨의 기본 움직임 x, y를 가져온다.
        lab_basic_position = {
            1: [1300, 25],
            2: [1300, 175],
            3: [1300, 325],
            4: [1300, 500],
            5: [1300, 650],
        }
        # 그 라벨을 가져온다.
        self.mihail_label = self.class_label_list[mihail_num-1]

        # 그 라벨의 이미지를 랜덤으로 배치하게 한다.
        moving_timer = QTimer() #미하일이 움직이는 라벨
        moving_timer.start(100) #100밀리세컨 마다 움직임
        moving_timer.timeout.connect(self.move_mihail) #100세컨마다 미하일 움직임 함수로 이동
        QTimer.singleShot(3000, lambda: moving_timer.stop()) #3초 지나면 움직임 멈춤
        QTimer.singleShot(3000, lambda: self.Log_textEdit.append("미하일의 춤은 현란했다")) #3초 지나면 움직임 멈춤

        QTimer.singleShot(3000, lambda: self.mihail_label.move(lab_basic_position[mihail_num][0], lab_basic_position[mihail_num][1])) #랜덤 숫자만큼 움직임


        # # 그리고 타이머가 끝난 후 그 라벨을 기존 위치로 위치시킨다.


    def keyPressEvent(self, event):

        # 소연 keypressevent 함수 내 수정(current_index값 받아오기)===========================================================
        # 소연수정추가 - 딕셔너리로 수정
        # 방향키와 좌표 변화값을 저장하는 딕셔너리
        directions = {
            Qt.Key_A: (-20, 0),  # 왼쪽
            Qt.Key_D: (20, 0),  # 오른쪽
            Qt.Key_W: (0, -20),  # 위로
            Qt.Key_S: (0, 20)  # 아래로
        }

        # 현재 스택위젯 값 가져오기
        self.current_index = self.StackWidget_Field.currentIndex()

        ## 일반필드일 때
        if self.current_index == 0:
            if event.key() == Qt.Key_P:
                self.show_ending() #확인용
            self.battle_type = '일반전투'
            # self.portal_sample.show()
            # 움직이는 {라벨} 현재 위치 정보 가져옴 <= 이전위치
            self.normal_previous_position = self.Character_QLabel.geometry()

            if event.key() in directions:  # 방향키 눌렀을 때
                if event.key() == list(directions.keys())[0]:
                    self.Character_QLabel.setPixmap(self.character_left_img)
                if event.key() == list(directions.keys())[1]:
                    self.Character_QLabel.setPixmap(self.character_right_img)
                dx, dy = directions[event.key()]  # 방향키에 해당하는 좌표 변화값을 가져옴
                new_position = self.Character_QLabel.geometry().translated(dx, dy)  # 새 위치 계산
                self.Character_QLabel.move(new_position.x(), new_position.y())  # 새 위치로 이동

                #벽 안나가게 하기
                if self.block_normal_field(new_position.x(), new_position.y()):
                    self.Character_QLabel.setGeometry(self.normal_previous_position)
                    return

                # 왼쪽 상단에 변경된 죄표 값 출력
                self.TopUI_Coordinate_Label.setText(
                    f"x좌표: {self.Character_QLabel.pos().x()} y좌표: {self.Character_QLabel.pos().y()}")

            else:  # 방향키 이외의 키를 눌렀을때를 위한 예외처리
                return

            # 랜덤값 추출 (이동, 전투, 수호대, 포션겟)
            rand_event = random.randrange(1, 11)

            # 50% 확률로 절반 이동
            if rand_event <= 5:
                self.Log_textEdit.append("1칸 이동하였습니다.")

            elif rand_event <= 6:
                self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
                self.status_page_reset()
                self.low_ui_reset()
                self.HoldSwitch = 1  # 스택 위젯 페이지 이동후에도 캐릭터 이동하는 현상 예외처리
                enemy_rand = random.randrange(4)

                if enemy_rand < 3:
                    self.Log_textEdit.setText("적을 만났습니다.")
                    self.portal_sample.hide()
                    self.StackWidget_Field.setCurrentIndex(2)  # 전투필드로 이동
                    self.Add_Monster_info()
                    self.User_Turn()
                    """
                    적을 만났을때 설정값
                    """
                    self.Widget_Skill.close()
                    #나중에 삭제
                    # self.win_btn.show()

                    # 인벤토리 ui를 소비창으로 변경
                    self.StackWidget_Item.setCurrentWidget(self.Page_Use)
                    self.Page_Use.setEnabled(False)
                    self.Btn_Equip.setEnabled(False)
                    self.Btn_Portion.setEnabled(False)
                    self.Btn_Status.setEnabled(False)


                else:
                    self.Log_textEdit.append("타 수호대를 만났습니다.")
                    self.Log_textEdit.setText("적을 만났습니다.")
                    self.portal_sample.hide()
                    self.StackWidget_Field.setCurrentIndex(2)  # 전투필드로 이동
                    self.Add_Monster_info()
                    self.User_Turn()
                    """
                    적을 만났을때 설정값
                    """

                    # 나중에 삭제
                    # self.win_btn.show()

                    # 인벤토리 ui를 소비창으로 변경
                    self.StackWidget_Item.setCurrentWidget(self.Page_Use)
                    self.Page_Use.setEnabled(False)
                    self.Btn_Equip.setEnabled(False)
                    self.Btn_Portion.setEnabled(False)
                    self.Btn_Status.setEnabled(False)

            elif rand_event > 6:
                    tent_rate = random.randint(1, 100)
                    if tent_rate < 10:
                        self.item_list[10].stack += 1
                        self.Log_textEdit.append("%s 를 획득하였습니다."
                                                 % self.item_list[10].name)
                        self.consumable_reset()
                    elif self.guardLevel <= 20:
                        self.item_list[0].stack += 1
                        self.item_list[3].stack += 1
                        self.Log_textEdit.append("%s ,%s 를 획득하였습니다."
                                                 % (self.item_list[0].name, self.item_list[3].name))
                        self.consumable_reset()
                    elif 20 < self.guardLevel <= 40:
                        self.item_list[1].stack += 1
                        self.item_list[4].stack += 1
                        self.Log_textEdit.append("%s ,%s 를 획득하였습니다."
                                                 % (self.item_list[1].name, self.item_list[4].name))
                        self.consumable_reset()
                    elif 40 < self.guardLevel <= 60:
                        self.item_list[2].stack += 1
                        self.item_list[5].stack += 1
                        self.Log_textEdit.append("%s ,%s 를 획득하였습니다."
                                                 % (self.item_list[2].name, self.item_list[5].name))
                        self.consumable_reset()
                    elif 60 < self.guardLevel <= 70:
                        self.item_list[6].stack += 1
                        self.Log_textEdit.append("%s 를 획득하였습니다."
                                                 % self.item_list[6].name)
                        self.consumable_reset()
                    elif 70 < self.guardLevel <= 80:
                        self.item_list[7].stack += 1
                        self.Log_textEdit.append("%s 를 획득하였습니다."
                                                 % self.item_list[7].name)
                        self.consumable_reset()
                    else:
                        self.item_list[8].stack += 1
                        self.Log_textEdit.append("%s 를 획득하였습니다."
                                                 % self.item_list[8].name)
                        self.consumable_reset()


            # 일반필드에서 포탈 만났을 때
            if self.Character_QLabel.geometry().intersects(self.portal_sample.geometry()):  # 포탈 만나면
                self.move_to_dungeon()  # 랜덤으로 던전으로 이동


        ## 던전필드일때
        elif self.current_index == 1:
            if event.key() == Qt.Key_M:
                self.teleport_in_dungeon()
            self.battle_type = '던전전투'
            previous_position = self.Character_QLabel_2.geometry()  # 이전 위치

            if event.key() in directions:  # 방향키가 눌렸을 때
                if event.key() == list(directions.keys())[0]:
                    self.Character_QLabel_2.setPixmap(self.character_left_img.scaled(QSize(30, 50), aspectRatioMode=Qt.IgnoreAspectRatio))
                if event.key() == list(directions.keys())[1]:
                    self.Character_QLabel_2.setPixmap(self.character_right_img.scaled(QSize(30, 50), aspectRatioMode=Qt.IgnoreAspectRatio))
                dx, dy = directions[event.key()]  # 방향키에 해당하는 좌표 변화값을 가져옴
                new_position = self.Character_QLabel_2.geometry().translated(dx, dy)  # 새 위치 계산
                self.Character_QLabel_2.move(new_position.x(), new_position.y())  # 새 위치로 이동
            else:
                return

            # 좌표 위에 찍어주기
            self.TopUI_Coordinate_Label.setText(
                f"x좌표: {self.Character_QLabel_2.pos().x()}, y좌표:{self.Character_QLabel_2.pos().y()}")

            # 980625소연수정필요
            ### TODO 랜덤값에 따라 아이템 획득(미완), 던전몬스터들 나오게 하기(완), 1칸 이동
            random_num_for_user_next_action = random.randint(1, 8)
            if random_num_for_user_next_action == 1:
                self.Add_Dungeon_monster_info()
                self.StackWidget_Field.setCurrentIndex(2)  # 전투필드로 이동
                # self.win_btn.show()
                self.User_Turn()

            # 던전에서 MonsterImage 만났을 때 전투 이동
            if self.Character_QLabel_2.geometry().intersects(self.boss_monster.geometry()):
                self.show_messagebox("보스몬스터를 만났습니다!\n전투에 진입합니다.")
                # 전투로 스택위젯 이동 / 전투함수로 이동
                self.user_can_enter_dungeon = True  # 전투에서 이기면 상태 True로 만들어주기
                self.user_meet_boss = True
                self.Add_Dungeon_monster_info() # 보스몬스터 등장
                self.StackWidget_Field.setCurrentIndex(2)  # 전투필드로 이동
                self.User_Turn()

            if self.reply_state == False and self.checkCollision(self.Character_QLabel_2, self.ghost_label): #던전 내 포탈 탔을 때
                # self.dungeon_floor += 1
                self.mark_label.move(self.Character_QLabel_2.x() + 10, self.Character_QLabel_2.y())
                self.mark_label.show()
                self.show_messagebox_easter_egg()

            # 보스 몬스터 이기면 던전으로 다시 이동
            #  던전에서 미궁 만났을 때 메세지 출력(임시) -> 코드 합치면 메세지 뜬 후 전투상황으로 이동하도록 하기
            if self.Character_QLabel_2.geometry().intersects(
                    self.entrance.geometry()) and self.user_can_enter_dungeon == True:
                self.show_messagebox("미궁을 만났습니다!")

                #수정필요 수정필요 980625
                self.user_can_enter_dungeon = False
                self.boss_monster.close()
                self.entrance.hide()
                self.ghost_label.hide()
                self.Character_QLabel_2.hide()
                self.move_to_dungeon()

            # 던전 벽 캐릭터가 벗어나지 못하게
            self.block_dungeon_for_type(self.Character_QLabel_2, self.dungeon_number, new_position.x(),
                                        new_position.y(), new_position, previous_position)

            pass
        else: #배틀필드인경우
            if event.key() == Qt.Key_H: # 맵핵 위한 치트키
                self.map_hack()
            if event.key() == Qt.Key_O:
                self.provocation_skill_motion()
            else:
                return




    def user_location(self, x, y):
        """유저의 위치값 반환함"""
        user_present_location = {
            '불': [0, 760, -20, 360],  # 불의지역 x1, x2, y3, y4  값
            '눈': [780, 1560, -20, 360],  # 눈의지역
            '숲': [0, 760, 380, 740],  # 숲의지역
            '물': [780, 1560, 380, 740]  # 물의지역
        }
        for key, value in user_present_location.items():
            if value[0] <= x <= value[1] and value[2] <= y <= value[3]:
                return key


    """길준이 형님 코드 취합 - 함수"""
    def hp_using_1(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.hp_recovery_1(y))

        # self.Class_1_Btn.clicked.connect(lambda: self.hp_recovery_1(1))
        # self.Class_2_Btn.clicked.connect(lambda: self.hp_recovery_1(2))
        # self.Class_3_Btn.clicked.connect(lambda: self.hp_recovery_1(3))
        # self.Class_4_Btn.clicked.connect(lambda: self.hp_recovery_1(4))
        # self.Class_5_Btn.clicked.connect(lambda: self.hp_recovery_1(5))
        # self.Class_6_Btn.clicked.connect(lambda: self.hp_recovery_1(6))

    def hp_using_2(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.hp_recovery_2(y))

    def hp_using_3(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.hp_recovery_3(y))

    def mp_using_1(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.mp_recovery_1(y))

    def mp_using_2(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.mp_recovery_2(y))

    def mp_using_3(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.mp_recovery_3(y))

    def all_using_1(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.all_recovery_1(y))

    def all_using_2(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.all_recovery_2(y))

    def all_using_3(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.all_recovery_3(y))

    def revive_using(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(True)
        for j in range(1, 7):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.revive(y))

    # def tent_use_using(self):
    #     self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
    #     for i in range(1, 7):
    #         getattr(self, f'Class_{i}_Btn').setEnabled(True)
    #     for j in range(1, 7):
    #         getattr(self, f'Class_{j}_Btn').clicked.connect(lambda: self.tent_use(j))

    def class_change_using(self):
        self.StackWidget_Item.setCurrentWidget(self.Page_Use_ing)
        self.Page_Use_ing.setEnabled(True)
        for i in range(0, 5):
            getattr(self, f'Class_{i+1}_Btn').setEnabled(True)
        self.Class_6_Btn.setEnabled(False)
        for j in range(1, 6):
            getattr(self, f'Class_{j}_Btn').clicked.connect(lambda x, y=j: self.class_change(y))

    def hp_recovery_1(self, num):
        if num == 6:
            self.item_list[0].stack -= 1
            self.StackWidget_Item.setCurrentWidget(self.Page_Use)
            return self.Log_textEdit.append("그는 출전하지않아서 먹지 못해요 애꿏은 포션만 땅에 버렸네요..")
        before = self.class_hp_dict[num]
        if before == 0:
            self.Log_textEdit.append('죽은자는 먹을수가 없어요. 포션님이 가출하였습니다')
            self.item_list[0].stack -= 1
        else:
            self.class_hp_dict[num] = self.class_hp_dict[num] + self.hp_s.recovery
            after = self.class_hp_dict[num]
            # str(self.list_class[i - 1][0].get_maxhp())
            # self.list_class[i - 1][1]
            if before < self.list_class[num - 1][0].get_maxhp() <= after:
                self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
                self.Log_textEdit.append("%s 의 체력을 최대치까지 회복했습니다"
                                         % getattr(self, f'class_{num}').character_name)
                self.item_list[0].stack -= 1

            elif self.class_hp_dict[num] >= self.list_class[num - 1][0].get_maxhp():
                self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
                self.Log_textEdit.append('이미 체력이 최대치입니다. 포션님이 가출하였습니다')
                self.item_list[0].stack -= 1
            else:
                self.Log_textEdit.append("%s 의 체력을 %s 만큼 회복했습니다" %
                                         (self.list_class[num - 1][0].character_name, self.hp_s.recovery))
                self.item_list[0].stack -= 1


        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()
        if self.user_turn >= 5:
            self.user_turn = 0
            self.monster_attack_users()
            return
        self.User_Turn()
        self.consumable_reset()
        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        # for i in range(1, 7):
        #     getattr(self, f'Class_{i}_Btn').disconnect()

    def hp_recovery_2(self, num):
        if num == 6:
            self.item_list[0].stack -= 1
            self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        before = self.class_hp_dict[num]
        if before == 0:
            self.Log_textEdit.append('죽은자는 먹을수가 없어요. 포션님이 가출하였습니다')
            self.item_list[1].stack -= 1
        else:
            self.class_hp_dict[num] = self.class_hp_dict[num] + self.hp_m.recovery
            after = self.class_hp_dict[num]

            if before < self.list_class[num - 1][0].get_maxhp() <= after:
                self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
                self.Log_textEdit.append("%s 의 체력을 최대치까지 회복했습니다"
                                         % getattr(self, f'class_{num}').character_name)
                self.item_list[1].stack -= 1

            elif self.class_hp_dict[num] >= self.list_class[num - 1][0].get_maxhp():
                self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
                self.Log_textEdit.append('이미 체력이 최대치입니다. 포션님이 가출하였습니다')
                self.item_list[1].stack -= 1

            else:
                self.Log_textEdit.append("%s 의 체력을 %s 만큼 회복했습니다" %
                                         (self.list_class[num - 1][0].character_name, self.hp_m.recovery))
                self.item_list[1].stack -= 1

        self.consumable_reset()
        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def hp_recovery_3(self, num):
        if num == 6:
            self.item_list[0].stack -= 1
            self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        before = self.class_hp_dict[num]
        if before == 0:
            self.Log_textEdit.append('죽은자는 먹을수가 없어요. 포션님이 가출하였습니다')
            self.item_list[2].stack -= 1
        else:
            self.class_hp_dict[num] = self.class_hp_dict[num] + self.hp_l.recovery
            after = self.class_hp_dict[num]

            if before < self.list_class[num - 1][0].get_maxhp() <= after:
                self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
                self.Log_textEdit.append("%s 의 체력을 최대치까지 회복했습니다"
                                         % getattr(self, f'class_{num}').character_name)
                self.item_list[2].stack -= 1

            elif self.class_hp_dict[num] >= self.list_class[num - 1][0].get_maxhp():
                self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
                self.Log_textEdit.append('이미 체력이 최대치입니다. 포션님이 가출하였습니다')
                self.item_list[2].stack -= 1

            else:
                self.Log_textEdit.append("%s 의 체력을 %s 만큼 회복했습니다" %
                                         (self.list_class[num - 1][0].character_name, self.hp_l.recovery))
                self.item_list[2].stack -= 1

        self.consumable_reset()
        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)

        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def mp_recovery_1(self, num):
        if num == 6:
            self.item_list[0].stack -= 1
            self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        if getattr(self, f'class_{num}').class_name == '전사':
            self.Log_textEdit.append("전사는 회복시킬 마나가 없습니다")
            self.item_list[3].stack -= 1
        else:
            before = self.class_mp_dict[num]
            if before == 0:
                self.Log_textEdit.append('죽은자는 먹을수가 없어요. 포션님이 가출하였습니다')
                self.item_list[3].stack -= 1
            else:
                self.class_mp_dict[num] = self.class_mp_dict[num] + self.mp_s.recovery
                after = self.class_mp_dict[num]

                if before < self.list_class[num - 1][0].get_maxmp() <= after:
                    self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                    self.Log_textEdit.append("%s 의 마나를 최대치까지 회복했습니다"
                                             % getattr(self, f'class_{num}').character_name)
                    self.item_list[3].stack -= 1

                elif self.class_mp_dict[num] >= self.list_class[num - 1][0].get_maxmp():
                    self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                    self.Log_textEdit.append('이미 마나가 최대치입니다. 포션님이 가출하였습니다')
                    self.item_list[3].stack -= 1

                else:
                    self.Log_textEdit.append("%s 의 마나를 %s 만큼 회복했습니다" % (
                        getattr(self, f'class_{num}').character_name, self.mp_s.recovery))
                    self.item_list[3].stack -= 1

        self.consumable_reset()
        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def mp_recovery_2(self, num):
        if num == 6:
            self.item_list[0].stack -= 1
            self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        if getattr(self, f'class_{num}').class_name == '전사':
            self.Log_textEdit.append("전사는 회복시킬 마나가 없습니다")
            self.item_list[4].stack -= 1
        else:
            before = self.class_mp_dict[num]
            if before == 0:
                self.Log_textEdit.append('죽은자는 먹을수가 없어요. 포션님이 가출하였습니다')
                self.item_list[4].stack -= 1
            else:
                self.class_mp_dict[num] = self.class_mp_dict[num] + self.mp_m.recovery
                after = self.class_mp_dict[num]

                if before < self.list_class[num - 1][0].get_maxmp() <= after:
                    self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                    self.Log_textEdit.append("%s 의 마나를 최대치까지 회복했습니다"
                                             % getattr(self, f'class_{num}').character_name)
                    self.item_list[4].stack -= 1

                elif self.class_mp_dict[num] >= self.list_class[num - 1][0].get_maxmp():
                    self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                    self.Log_textEdit.append('이미 마나가 최대치입니다. 포션님이 가출하였습니다')
                    self.item_list[4].stack -= 1

                else:
                    self.Log_textEdit.append("%s 의 마나를 %s 만큼 회복했습니다" % (
                        getattr(self, f'class_{num}').character_name, self.mp_m.recovery))
                    self.item_list[4].stack -= 1

        self.consumable_reset()
        self.low_ui_reset()
        self.status_page_reset()

        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def mp_recovery_3(self, num):
        if num == 6:
            self.item_list[0].stack -= 1
            self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        if getattr(self, f'class_{num}').class_name == '전사':
            self.Log_textEdit.append("전사는 회복시킬 마나가 없습니다")
            self.item_list[5].stack -= 1
        else:
            before = self.class_mp_dict[num]
            if before == 0:
                self.Log_textEdit.append('죽은자는 먹을수가 없어요. 포션님이 가출하였습니다')
                self.item_list[5].stack -= 1
            else:
                self.class_mp_dict[num] = self.class_mp_dict[num] + self.mp_l.recovery
                after = self.class_mp_dict[num]

                if before < self.list_class[num - 1][0].get_maxmp() <= after:
                    self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                    self.Log_textEdit.append("%s 의 마나를 최대치까지 회복했습니다"
                                             % getattr(self, f'class_{num}').character_name)
                    self.item_list[5].stack -= 1

                elif self.class_mp_dict[num] >= self.list_class[num - 1][0].get_maxmp():
                    self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                    self.Log_textEdit.append('이미 마나가 최대치입니다. 포션님이 가출하였습니다')
                    self.item_list[5].stack -= 1

                else:
                    self.Log_textEdit.append("%s 의 마나를 %s 만큼 회복했습니다" % (
                        getattr(self, f'class_{num}').character_name, self.mp_l.recovery))
                    self.item_list[5].stack -= 1

        self.consumable_reset()

        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def all_recovery_1(self, num):
        if num == 6:
            self.item_list[0].stack -= 1
            self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        # getattr(self, f'class_{num}').hp = getattr(self, f'class_{num}').hp + ((체력 최대치) * self.all_s.recovery)
        # if getattr(self, f'class_{num}').hp > (체력 최대치)
        #     getattr(self, f'class_{num}').hp = (체력 최대치)
        # getattr(self, f'class_{num}').mp = getattr(self, f'class_{num}').mp + ((마나 최대치) * self.all_s.recovery)
        # if getattr(self, f'class_{num}').mp > (마나 최대치)
        #     getattr(self, f'class_{num}').mp = (마나 최대치)

        before_hp = self.class_hp_dict[num]
        if before_hp == 0:
            self.Log_textEdit.append('죽은자는 먹을수가 없어요. 포션님이 가출하였습니다')
            self.item_list[6].stack -= 1
        else:
            self.class_hp_dict[num] = self.class_hp_dict[num] + int(
                    self.list_class[num - 1][0].get_maxhp() * self.all_s.recovery)
            after_hp = self.class_hp_dict[num]
            before_mp = self.class_mp_dict[num]
            self.class_mp_dict[num] = self.list_class[num - 1][2] + int(
                    self.list_class[num - 1][0].get_maxmp() * self.all_s.recovery)
            after_mp = self.class_mp_dict[num]

            if self.class_hp_dict[num] >= self.list_class[num - 1][0].get_maxhp() \
                    and self.class_mp_dict[num] >= self.list_class[num - 1][0].get_maxmp():
                self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
                self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                self.Log_textEdit.append('이미 체력과 마나가 최대치입니다. 포션은 하늘위로')
                self.item_list[6].stack -= 1

            else:
                if before_hp < self.list_class[num - 1][0].get_maxhp() <= after_hp:
                    self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
                    self.Log_textEdit.append("%s 의 체력을 최대치까지 회복했습니다"
                                             % getattr(self, f'class_{num}').character_name)

                else:
                    self.Log_textEdit.append("%s 의 체력를 %s %% 만큼 회복했습니다" % (
                        getattr(self, f'class_{num}').character_name, self.all_s.recovery*100))

                if before_mp < self.list_class[num - 1][0].get_maxmp() <= after_mp:
                    self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                    self.Log_textEdit.append("%s 의 마나를 최대치까지 회복했습니다"
                                             % getattr(self, f'class_{num}').character_name)

                else:
                    self.Log_textEdit.append("%s 의 마나를 %s %% 만큼 회복했습니다" % (
                        getattr(self, f'class_{num}').character_name, self.all_s.recovery * 100))

                self.item_list[6].stack -= 1

        self.consumable_reset()
        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def all_recovery_2(self, num):
        if num == 6:
            self.item_list[0].stack -= 1
            self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        # getattr(self, f'class_{num}').hp = getattr(self, f'class_{num}').hp + ((체력 최대치) * self.all_m.recovery)
        # if getattr(self, f'class_{num}').hp > (체력 최대치)
        #     getattr(self, f'class_{num}').hp = (체력 최대치)
        # getattr(self, f'class_{num}').mp = getattr(self, f'class_{num}').mp + ((마나 최대치) * self.all_m.recovery)
        # if getattr(self, f'class_{num}').mp > (마나 최대치)
        #     getattr(self, f'class_{num}').mp = (마나 최대치)
        before_hp = self.list_class[num - 1][1]
        if before_hp == 0:
            self.Log_textEdit.append('죽은자는 먹을수가 없어요. 포션님이 가출하였습니다')
            self.item_list[7].stack -= 1
        else:
            self.list_class[num - 1][1] = self.list_class[num - 1][1] + (
                    self.list_class[num - 1][0].get_maxhp() * self.all_m.recovery)
            after_hp = self.list_class[num - 1][1]
            before_mp = self.list_class[num - 1][2]
            self.list_class[num - 1][2] = self.list_class[num - 1][2] + (
                    self.list_class[num - 1][0].get_maxmp() * self.all_m.recovery)
            after_mp = self.list_class[num - 1][2]

            if self.list_class[num - 1][1] >= self.list_class[num - 1][0].get_maxhp() \
                    and self.list_class[num - 1][2] >= self.list_class[num - 1][0].get_maxmp():
                self.list_class[num - 1][1] = self.list_class[num - 1][0].get_maxhp()
                self.list_class[num - 1][2] = self.list_class[num - 1][0].get_maxmp()
                self.Log_textEdit.append('이미 체력과 마나가 최대치입니다. 포션은 하늘위로')
                self.item_list[7].stack -= 1
            else:
                if before_hp < self.list_class[num - 1][0].get_maxhp() <= after_hp:
                    self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
                    self.Log_textEdit.append("%s 의 체력을 최대치까지 회복했습니다"
                                              % getattr(self, f'class_{num}').character_name)

                else:
                    self.Log_textEdit.append("%s 의 체력를 %s %% 만큼 회복했습니다" % (
                        getattr(self, f'class_{num}').character_name, self.all_s.recovery * 100))

                if before_mp < self.list_class[num - 1][0].get_maxmp() <= after_mp:
                    self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                    self.Log_textEdit.append("%s 의 마나를 최대치까지 회복했습니다"
                                             % getattr(self, f'class_{num}').character_name)
                else:
                    self.Log_textEdit.append("%s 의 마나를 %s %% 만큼 회복했습니다" % (
                    getattr(self, f'class_{num}').character_name, self.all_s.recovery * 100))

            self.item_list[7].stack -= 1

        self.consumable_reset()
        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def all_recovery_3(self, num):
        if num == 6:
            self.item_list[0].stack -= 1
            self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        before_hp = self.list_class[num - 1][1]
        if before_hp == 0:
            self.Log_textEdit.append('죽은자는 먹을수가 없어요. 포션님이 가출하였습니다')
            self.item_list[8].stack -= 1
        else:
            if self.class_hp_dict[num] >= self.list_class[num - 1][0].get_maxhp() \
                    and self.class_mp_dict[num] >= self.list_class[num - 1][0].get_maxmp():
                self.Log_textEdit.append('이미 체력과 마나가 최대치입니다')
                pass
            else:
                self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
                self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
                self.Log_textEdit.append("체력과 마나를 전부 회복했습니다")

        self.item_list[8].stack -= 1
        self.consumable_reset()

        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def revive(self, num):
        # getattr(self, f'class_{num}').hp = (체력 최대치)
        # getattr(self, f'class_{num}').mp = (마나 최대치)
        self.class_hp_dict[num] = self.list_class[num - 1][0].get_maxhp()
        self.class_mp_dict[num] = self.list_class[num - 1][0].get_maxmp()
        self.Log_textEdit.append("체력과 마나를 전부 회복했습니다")

        self.item_list[9].stack -= 1
        self.consumable_reset()

        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').disconnect()
        # '선택된' 캐릭터 전투불능 해제

    def tent_use(self):
        self.item_list[10].stack -= 1
        # for i in range(1, 7):
        # getattr(self, f'class_{i}').hp = getattr(self, f'class_{i}').hp (최대치)
        # for j in range(1, 7):
        # getattr(self, f'class_{j}').mp = getattr(self, f'class_{j}').mp (최대치)
        # '모든' 캐릭터 전투불능 해제
        for i in range(len(self.class_hp_dict)):
            self.class_hp_dict[i] = self.list_class[i - 1][0].get_maxhp()
            self.class_mp_dict[i] = self.list_class[i - 1][0].get_maxmp()
        self.Log_textEdit.append("체력과 마나를 전부 회복했습니다")
        self.consumable_reset()
        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        for k in range(1, 7):
            getattr(self, f'Class_{k}_Btn').disconnect()

    def class_change(self, num):
        # 1-6

        self.Log_textEdit.append('%s이/가 후퇴하고 %s이/가 출전하였습니다.'
                                 % (self.list_class[num-1][0].character_name, self.list_class[-1][0].character_name))
        self.ComboBox_Class.clear()  # 콤보박스 리스트 전부 제거
        go_battle = self.list_class.pop(-1)  # 대기중인 캐릭터를 이름 리스트에서 추출
        out_battle = self.list_class.pop(num-1)  # 빠질 캐릭터를 이름 리스트에서 추출
        self.list_class.insert(num-1, go_battle)  # 들어갈 캐릭터를 빠진 캐릭터 위치로 이동
        self.list_class.append(out_battle)  # 빠질 캐릭터를 대기 위치로 이동
        temp_stat_in_hp = self.class_hp_dict_last.pop(0)
        temp_stat_out_hp = self.class_hp_dict.pop(num)
        self.class_hp_dict[num] = temp_stat_in_hp
        self.class_hp_dict_last[0] = temp_stat_out_hp

        temp_stat_in_mp = self.class_mp_dict_last.pop(0)
        temp_stat_out_mp = self.class_mp_dict.pop(num)
        self.class_mp_dict[num] = temp_stat_in_mp
        self.class_mp_dict_last[0] = temp_stat_out_mp

        self.Statusclass.clear()
        self.StautsHpall.clear()
        self.StautsMpall.clear()
        print('유저 체력 확인용', self.class_hp_dict)

        # 위에서 섞은 list_class을 프레임에 1부터 5까지 가져와 담아줌
        for i in range(1, 6):
            # 빈 리스트에 추가
            self.Statusclass.append(self.list_class[i - 1][0])  # 빈 리스트 Statusclass에 하나씩 전체정보를 append해줌
            self.StautsHpall.append(self.list_class[i - 1][1])  # 빈 리스트 StautsHpall에 하나씩 최대hp를 append해줌
            self.StautsMpall.append(self.list_class[i - 1][1])  # 빈 리스트 StautsMpall에 하나씩 최대mp를 append해줌

        self.class_equip_page()
        self.class_name_reset()
        self.low_ui_reset()
        self.item_list[11].stack -= 1
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
        self.consumable_reset()
        self.combobox_add()  # 콤보박스를 리스트 대로 재작성
        self.low_ui_reset()
        self.status_page_reset()
        self.Page_Use_ing.setEnabled(False)
        for i in range(1, 6):
            getattr(self, f'Class_{i}_Btn').disconnect()

    def item_set(self):
        self.item_consumable_hp_S = Consumable("HP포션 (소)", 50, 10)
        self.item_consumable_hp_M = Consumable("HP포션 (중)", 100, 0)
        self.item_consumable_hp_L = Consumable("HP포션 (대)", 150, 0)
        self.item_consumable_mp_S = Consumable("MP포션 (소)", 50, 10)
        self.item_consumable_mp_M = Consumable("MP포션 (중)", 100, 0)
        self.item_consumable_mp_L = Consumable("MP포션 (대)", 150, 0)
        self.item_consumable_all_S = Consumable("All포션 (소)", 0.25, 0)
        self.item_consumable_all_M = Consumable("All포션 (중)", 0.5, 0)
        self.item_consumable_all_L = Consumable("All포션 (대)", 1, 0)
        self.item_consumable_resurrection = Consumable('부활포션', 1, 0)
        self.item_consumable_tent = Consumable('텐트', 1, 0)
        self.item_consumable_change = Consumable('직업변경권', 0, 0)
        self.item_consumable_enhancement_low = Consumable('강화석 하급', 0, 0)
        self.item_consumable_enhancement_high = Consumable('강화석 상급', 0, 0)

        # 무기 순서 : 검(0) 방패(3) 숏스태프(6) 롱스태프(9) 룬스태프(12) 보우(15)
        self.weapon_list = [Weapon('조잡한 검', '무기', self.sword_img_1, 10),
                            Weapon('튼튼한 검', '무기',  self.sword_img_2, 20),
                            Weapon('보키 검', '무기', self.sword_img_3, 40),
                            Weapon('가죽 방패', '방패', self.shield_img_1, 10),
                            Weapon('사슬 방패', '방패',self.shield_img_2, 20),
                            Weapon('철 방패', '방패', self.shield_img_3, 40),
                            Weapon('조잡한 숏스태프', self.shortstaff_img_1, '무기', 10),
                            Weapon('튼튼한 숏스태프', self.shortstaff_img_2, '무기', 20),
                            Weapon('보키 숏스태프', self.shortstaff_img_3, '무기', 40),
                            Weapon('조잡한 롱스태프', self.longstaff_img_1, '무기', 10),
                            Weapon('튼튼한 롱스태프', self.longstaff_img_2, '무기', 20),
                            Weapon('보키 롱스태프',self.longstaff_img_3, '무기', 40),
                            Weapon('조잡한 룬스태프', self.runestaff_img_1, '무기', 10),
                            Weapon('튼튼한 룬스태프', self.runestaff_img_2, '무기', 20),
                            Weapon('보키 룬스태프', self.runestaff_img_3, '무기', 40),
                            Weapon('조잡한 보우',self.bot_img_1, '무기', 10),
                            Weapon('튼튼한 보우', self.bot_img_2, '무기', 20),
                            Weapon('보키 보우', self.bot_img_3, '무기', 40)]

        self.head_list = [Armor('허름한 천두건', self.lobehead_img_1, '머리', 5),
                          Armor('튼튼한 천두건', self.lobehead_img_2, '머리', 10),
                          Armor('보키 천두건', self.lobehead_img_3, '머리', 20),
                          Armor('조잡한 가죽투구', self.leatherhead_img_1, '머리', 10),
                          Armor('튼튼한 가죽투구',self.leatherhead_img_2, '머리', 15),
                          Armor('보키 가죽투구', self.leatherhead_img_3, '머리', 30),
                     Armor('조잡한 철투구', self.heavyhead_img_1, '머리', 15),
                          Armor('튼튼한 철투구', self.heavyhead_img_2, '머리', 20),
                          Armor('보키 철투구', self.heavyhead_img_3, '머리', 40)]

        self.armor_list = [Armor('허름한 천갑옷', self.lobe_img_1, '상의', 10),
                           Armor('튼튼한 천갑옷', self.lobe_img_2, '상의', 20),
                           Armor('보키 천갑옷', self.lobe_img_3, '상의', 40),
                      Armor('허름한 가죽갑옷', self.leather_img_1, '상의', 15),
                           Armor('튼튼한 가죽갑옷', self.leather_img_2, '상의', 30),
                           Armor('보키 가죽갑옷', self.leather_img_3, '상의', 60),
                      Armor('조잡한 중갑옷', self.heavy_img_1, '상의', 25),
                           Armor('튼튼한 중갑옷', self.heavy_img_2, '상의', 50),
                           Armor('보키 중갑옷', self.heavy_img_3, '상의', 100),
                      Armor('조잡한 경갑옷', self.light_img_1, '상의', 20),
                           Armor('튼튼한 경갑옷', self.light_img_2, '상의', 40),
                           Armor('보키 경갑옷', self.light_img_3, '상의', 80)]

        self.pants_list = [Armor('허름한 천바지', self.lobepants_img_1, '하의', 10),
                           Armor('튼튼한 천바지', self.lobepants_img_2, '하의', 12),
                           Armor('보키 천바지', self.lobepants_img_3, '하의', 14),
                      Armor('허름한 가죽바지', self.leatherpants_img_1, '하의', 12),
                           Armor('튼튼한 가죽바지', self.leatherpants_img_2, '하의', 14),
                           Armor('보키 가죽바지', self.leatherpants_img_3, '하의', 16),
                      Armor('허름한 중갑바지', self.heavypants_img_1, '하의', 16),
                           Armor('튼튼한 중갑바지', self.heavypants_img_2, '하의', 18),
                           Armor('보키 중갑바지', self.heavypants_img_3, '하의', 20),
                      Armor('허름한 경갑바지', self.lightpants_img_1, '하의', 14),
                           Armor('튼튼한 경갑바지', self.lightpants_img_2, '하의', 16),
                           Armor('보키 경갑바지', self.lightpants_img_3, '하의', 18)]

        self.glove_list = [Armor('허름한 천장갑', self.lobeglove_img_1, '장갑', 5),
                           Armor('튼튼한 천장갑', self.lobeglove_img_2, '장갑', 7),
                           Armor('보키 천장갑', self.lobeglove_img_3, '장갑', 9),
                      Armor('허름한 가죽장갑', self.lethergolve_img_1, '장갑', 7),
                           Armor('튼튼한 가죽장갑', self.lethergolve_img_2, '장갑', 9),
                           Armor('보키 가죽장갑', self.lethergolve_img_3, '장갑', 11),
                      Armor('허름한 사슬장갑', self.chainglove_img_1, '장갑', 9),
                           Armor('견고한 사슬장갑', self.chainglove_img_2, '장갑', 11),
                           Armor('보키 사슬장갑', self.chainglove_img_3, '장갑', 13)]

        self.cloak_list = [Armor('허름한 천망토', self.cloak_img_1, '망토', 5),
                           Armor('튼튼한 천망토', self.cloak_img_2, '망토', 10),
                           Armor('보키 천망토', self.cloak_img_3, '망토', 15),
                      Armor('허름한 가죽망토', self.leathercloak_img_1, '망토', 10),
                           Armor('튼튼한 가죽망토', self.leathercloak_img_2, '망토', 15),
                           Armor('보키 가죽망토', self.leathercloak_img_3, '망토', 20)]

        self.class_warrior = [self.head_list[6], self.armor_list[6], self.pants_list[6], self.glove_list[6],
                         self.weapon_list[0], self.weapon_list[3], self.cloak_list[3]]

        self.class_whitewizard = [self.head_list[0], self.armor_list[0], self.pants_list[0], self.glove_list[0],
                             self.weapon_list[6], self.weapon_list[3], self.cloak_list[0]]

        self.class_blackwizard = [self.head_list[0], self.armor_list[0], self.pants_list[0], self.glove_list[0],
                                  self.weapon_list[9], self.weapon_list[3], self.cloak_list[0]]

        self.class_redwizard = [self.head_list[3], self.armor_list[3], self.pants_list[3], self.glove_list[3],
                           self.weapon_list[12], self.weapon_list[3], self.cloak_list[3]]

        self.class_archer = [self.head_list[3], self.armor_list[3], self.pants_list[3], self.glove_list[3],
                        self.weapon_list[15], None, self.cloak_list[3]]

        self.class_swordman = [self.head_list[3], self.armor_list[9], self.pants_list[9], self.glove_list[3],
                          self.weapon_list[0], None, self.cloak_list[3]]

        self.list_consumable = [self.item_consumable_hp_S, self.item_consumable_hp_M, self.item_consumable_hp_L,
                           self.item_consumable_mp_S, self.item_consumable_mp_M, self.item_consumable_mp_L,
                           self.item_consumable_all_S, self.item_consumable_all_M, self.item_consumable_all_L,
                           self.item_consumable_resurrection, self.item_consumable_tent, self.item_consumable_change,
                           self.item_consumable_enhancement_low, self.item_consumable_enhancement_high]

    def combobox_add(self):
        self.ComboBox_Class.addItem(self.list_class[0][0].character_name)
        self.ComboBox_Class.addItem(self.list_class[1][0].character_name)
        self.ComboBox_Class.addItem(self.list_class[2][0].character_name)
        self.ComboBox_Class.addItem(self.list_class[3][0].character_name)
        self.ComboBox_Class.addItem(self.list_class[4][0].character_name)
        self.ComboBox_Class.setCurrentIndex(0)

    def item_img(self):
        self.lobehead_img_1 = QPixmap('./image/item/lobehead_1.png')
        self.lobehead_img_2 = QPixmap('./image/item/lobehead_2.png')
        self.lobehead_img_3 = QPixmap('./image/item/lobehead_3.png')
        self.leatherhead_img_1 = QPixmap('./image/item/leatherhelm_1.png')
        self.leatherhead_img_2 = QPixmap('./image/item/leatherhelm_2.png')
        self.leatherhead_img_3 = QPixmap('./image/item/leatherhelm_3.png')
        self.heavyhead_img_1 = QPixmap('./image/item/heavyhelm_1.png')
        self.heavyhead_img_2 = QPixmap('./image/item/heavyhelm_2.png')
        self.heavyhead_img_3 = QPixmap('./image/item/heavyhelm_3.png')
        self.lobe_img_1 = QPixmap('./image/item/lobe_1.png')
        self.lobe_img_2 = QPixmap('./image/item/lobe_2.png.png')
        self.lobe_img_3 = QPixmap('./image/item/lobe_3.png.png')
        self.leather_img_1 = QPixmap('./image/item/leather_1.png.png')
        self.leather_img_2 = QPixmap('./image/item/leather_2.png.png')
        self.leather_img_3 = QPixmap('./image/item/leather_3.png.png')
        self.heavy_img_1 = QPixmap('./image/item/heavy_1.png')
        self.heavy_img_2 = QPixmap('./image/item/heavy_2.png')
        self.heavy_img_3 = QPixmap('./image/item/heavy_3.png')
        self.light_img_1 = QPixmap('./image/item/light_1.png')
        self.light_img_2 = QPixmap('./image/item/light_2.png')
        self.light_img_3 = QPixmap('./image/item/light_3.png')
        self.lobepants_img_1 = QPixmap('./image/item/lobepants_1.png')
        self.lobepants_img_2 = QPixmap('./image/item/lobepants_2.png')
        self.lobepants_img_3 = QPixmap('./image/item/lobepants_3.png')
        self.leatherpants_img_1 = QPixmap('./image/item/leatherpants_1.png')
        self.leatherpants_img_2 = QPixmap('./image/item/leatherpants_2.png')
        self.leatherpants_img_3 = QPixmap('./image/item/leatherpants_3.png')
        self.heavypants_img_1 = QPixmap('./image/item/heavypants_1.png')
        self.heavypants_img_2 = QPixmap('./image/item/heavypants_2.png')
        self.heavypants_img_3 = QPixmap('./image/item/heavypants_3.png')
        self.lightpants_img_1 = QPixmap('./image/item/lightpants_1.png')
        self.lightpants_img_2 = QPixmap('./image/item/lightpants_2.png')
        self.lightpants_img_3 = QPixmap('./image/item/lightpants_3.png')
        self.lobeglove_img_1 =QPixmap('./image/item/lobegolve_1.png')
        self.lobeglove_img_2 =QPixmap('./image/item/lobegolve_2.png')
        self.lobeglove_img_3 =QPixmap('./image/item/lobegolve_3.png')
        self.lethergolve_img_1 = QPixmap('./image/item/leatherglove_1.png')
        self.lethergolve_img_2 =  QPixmap('./image/item/leatherglove_2.png')
        self.lethergolve_img_3 =QPixmap('./image/item/leatherglove_3.png')
        self.chainglove_img_1 = QPixmap('./image/item/chainglove_1.png')
        self.chainglove_img_2 = QPixmap('./image/item/chainglove_2.png')
        self.chainglove_img_3 =QPixmap('./image/item/chainglove_3.png')
        self.cloak_img_1 =  QPixmap('./image/item/cloak_1.png')
        self.cloak_img_2 = QPixmap('./image/item/cloak_2.png')
        self.cloak_img_3 = QPixmap('./image/item/cloak_3.png')
        self.leathercloak_img_1 = QPixmap('./image/item/leathercloak_1.png')
        self.leathercloak_img_2 = QPixmap('./image/item/leathercloak_2.png')
        self.leathercloak_img_3 = QPixmap('./image/item/leathercloak_3.png')

        self.sword_img_1 = QPixmap('./image/item/sword_1.png')
        self.sword_img_2 = QPixmap('./image/item/sword_2.png')
        self.sword_img_3 = QPixmap('./image/item/sword_3.png')
        self.shield_img_1 = QPixmap('./image/item/shield_1.png')
        self.shield_img_2 = QPixmap('./image/item/shield_2.png')
        self.shield_img_3 = QPixmap('./image/item/shield_3.png')
        self.shortstaff_img_1 = QPixmap('./image/item/shortstaff_1.png')
        self.shortstaff_img_2 = QPixmap('./image/item/shortstaff_2.png')
        self.shortstaff_img_3 = QPixmap('./image/item/shortstaff_3.png')
        self.longstaff_img_1 = QPixmap('./image/item/longstaff_1.png')
        self.longstaff_img_2 = QPixmap('./image/item/longstaff_2.png')
        self.longstaff_img_3 = QPixmap('./image/item/longstaff_3.png')
        self.runestaff_img_1 =  QPixmap('./image/item/runestaff_1.png')
        self.runestaff_img_2 =  QPixmap('./image/item/runestaff_2.png')
        self.runestaff_img_3 = QPixmap('./image/item/runestaff_3.png')
        self.bot_img_1 = QPixmap('./image/item/bow_1.png')
        self.bot_img_2 = QPixmap('./image/item/bow_2.png')
        self.bot_img_3 = QPixmap('./image/item/bow_3.png')


    def helmet_upgrade(self):

        item_name_before = getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name
        upgrade_rate = random.randint(1, 100)

        if getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[0] == 0 and upgrade_rate < 4:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[0] = self.head_list[1]
                getattr(self, f'Equip{self.upgrade_index+1}_1Helmet_Label').setPixmap(self.head_list[1].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[0] = self.head_list[4]
                getattr(self, f'Equip{self.upgrade_index + 1}_1Helmet_Label').setPixmap(self.head_list[4].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name.find('철') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[0] = self.head_list[7]
                getattr(self, f'Equip{self.upgrade_index + 1}_1Helmet_Label').setPixmap(self.head_list[7].img)
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[0] = 1
            self.item_list[-2].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[0] == 1 and upgrade_rate < 2:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[0] = self.head_list[2]
                getattr(self, f'Equip{self.upgrade_index + 1}_1Helmet_Label').setPixmap(self.head_list[2].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[0] = self.head_list[5]
                getattr(self, f'Equip{self.upgrade_index + 1}_1Helmet_Label').setPixmap(self.head_list[5].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name.find('철') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[0] = self.head_list[8]
                getattr(self, f'Equip{self.upgrade_index + 1}_1Helmet_Label').setPixmap(self.head_list[8].img)
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[0] = 2
            self.item_list[-1].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[0].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[0] == 0:
            self.item_list[-2].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[0] == 1:
            self.item_list[-1].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        self.consumable_reset()
        self.item_upgrade_button_reset()

    def armor_upgrade(self):

        item_name_before = getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name
        upgrade_rate = random.randint(1, 100)

        if getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[1] == 0 and upgrade_rate < 4:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = self.armor_list[1]
                getattr(self, f'Equip{self.upgrade_index + 1}_2_Armor_Label').setPixmap(self.armor_list[1].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = self.armor_list[4]
                getattr(self, f'Equip{self.upgrade_index + 1}_2_Armor_Label').setPixmap(self.armor_list[4].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('중') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = self.armor_list[7]
                getattr(self, f'Equip{self.upgrade_index + 1}_2_Armor_Label').setPixmap(self.armor_list[7].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('경') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = self.armor_list[10]
                getattr(self, f'Equip{self.upgrade_index + 1}_2_Armor_Label').setPixmap(self.armor_list[10].img)
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[1] = 1
            self.item_list[-2].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[1] == 1 and upgrade_rate < 2:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = self.armor_list[2]
                getattr(self, f'Equip{self.upgrade_index + 1}_2_Armor_Label').setPixmap(self.armor_list[2].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = self.armor_list[5]
                getattr(self, f'Equip{self.upgrade_index + 1}_2_Armor_Label').setPixmap(self.armor_list[5].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('철') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = self.armor_list[8]
                getattr(self, f'Equip{self.upgrade_index + 1}_2_Armor_Label').setPixmap(self.armor_list[8].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('경') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1] = self.armor_list[11]
                getattr(self, f'Equip{self.upgrade_index + 1}_2_Armor_Label').setPixmap(self.armor_list[11].img)
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[1] = 2
            self.item_list[-1].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[1] == 0:
            self.item_list[-2].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[1] == 1:
            self.item_list[-1].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        self.consumable_reset()
        self.item_upgrade_button_reset()

    def pants_upgrade(self):
        item_name_before = getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name
        upgrade_rate = random.randint(1, 100)
        if getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[2] == 0 and upgrade_rate < 4:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = self.pants_list[1]
                getattr(self, f'Equip{self.upgrade_index + 1}_3_Pants_Label').setPixmap(self.pants_list[1].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = self.pants_list[4]
                getattr(self, f'Equip{self.upgrade_index + 1}_3_Pants_Label').setPixmap(self.pants_list[4].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('중') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = self.pants_list[7]
                getattr(self, f'Equip{self.upgrade_index + 1}_3_Pants_Label').setPixmap(self.pants_list[7].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('경') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = self.pants_list[10]
                getattr(self, f'Equip{self.upgrade_index + 1}_3_Pants_Label').setPixmap(self.pants_list[10].img)
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[2] = 1
            self.item_list[-2].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[2] == 1 and upgrade_rate < 2:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = self.pants_list[2]
                getattr(self, f'Equip{self.upgrade_index + 1}_3_Pants_Label').setPixmap(self.pants_list[2].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = self.pants_list[5]
                getattr(self, f'Equip{self.upgrade_index + 1}_3_Pants_Label').setPixmap(self.pants_list[5].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('철') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = self.pants_list[8]
                getattr(self, f'Equip{self.upgrade_index + 1}_3_Pants_Label').setPixmap(self.pants_list[8].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name.find('경') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[2] = self.pants_list[11]
                getattr(self, f'Equip{self.upgrade_index + 1}_3_Pants_Label').setPixmap(self.pants_list[11].img)
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[2] = 2
            self.item_list[-1].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[2].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[2] == 0:
            self.item_list[-2].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[2] == 1:
            self.item_list[-1].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        self.consumable_reset()
        self.item_upgrade_button_reset()

    def glove_upgrade(self):
        item_name_before = getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name
        upgrade_rate = random.randint(1, 100)

        if getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[3] == 0 and upgrade_rate < 4:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[3] = self.glove_list[1]
                getattr(self, f'Equip{self.upgrade_index + 1}_5_Hand_Label').setPixmap(self.glove_list[1].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[3] = self.glove_list[4]
                getattr(self, f'Equip{self.upgrade_index + 1}_5_Hand_Label').setPixmap(self.glove_list[4].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name.find('사슬') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[3] = self.glove_list[7]
                getattr(self, f'Equip{self.upgrade_index + 1}_5_Hand_Label').setPixmap(self.glove_list[7].img)
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[3] = 1
            self.item_list[-2].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))
        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[3] == 1 and upgrade_rate < 2:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[3] = self.glove_list[2]
                getattr(self, f'Equip{self.upgrade_index + 1}_5_Hand_Label').setPixmap(self.glove_list[2].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[3] = self.glove_list[5]
                getattr(self, f'Equip{self.upgrade_index + 1}_5_Hand_Label').setPixmap(self.glove_list[5].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name.find('사슬') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[3] = self.glove_list[8]
                getattr(self, f'Equip{self.upgrade_index + 1}_5_Hand_Label').setPixmap(self.glove_list[8].img)
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[3] = 2
            self.item_list[-1].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[3].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[3] == 0:
            self.item_list[-2].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[3] == 1:
            self.item_list[-1].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        self.consumable_reset()
        self.item_upgrade_button_reset()

    def weapon_upgrade(self):
        item_name_before = getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name
        upgrade_rate = random.randint(1, 100)
        if getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[4] == 0 and upgrade_rate < 4:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('검') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = self.weapon_list[1]
                getattr(self, f'Equip{self.upgrade_index + 1}_6_Weapon_Label').setPixmap(self.weapon_list[1].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('숏') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = self.weapon_list[7]
                getattr(self, f'Equip{self.upgrade_index + 1}_6_Weapon_Label').setPixmap(self.weapon_list[7].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('롱') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = self.weapon_list[10]
                getattr(self, f'Equip{self.upgrade_index + 1}_6_Weapon_Label').setPixmap(self.weapon_list[10].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('룬') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = self.weapon_list[13]
                getattr(self, f'Equip{self.upgrade_index + 1}_6_Weapon_Label').setPixmap(self.weapon_list[13].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('보우') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = self.weapon_list[16]
                getattr(self, f'Equip{self.upgrade_index + 1}_6_Weapon_Label').setPixmap(self.weapon_list[16].img)
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[4] = 1
            self.item_list[-2].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))
        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[4] == 1 and upgrade_rate < 2:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('검') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = self.weapon_list[2]
                getattr(self, f'Equip{self.upgrade_index + 1}_6_Weapon_Label').setPixmap(self.weapon_list[2].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('숏') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = self.weapon_list[8]
                getattr(self, f'Equip{self.upgrade_index + 1}_6_Weapon_Label').setPixmap(self.weapon_list[8].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('롱') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = self.weapon_list[11]
                getattr(self, f'Equip{self.upgrade_index + 1}_6_Weapon_Label').setPixmap(self.weapon_list[11].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('룬') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = self.weapon_list[14]
                getattr(self, f'Equip{self.upgrade_index + 1}_6_Weapon_Label').setPixmap(self.weapon_list[14].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name.find('보우') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[4] = self.weapon_list[17]
                getattr(self, f'Equip{self.upgrade_index + 1}_6_Weapon_Label').setPixmap(self.weapon_list[17].img)
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[4] = 2
            self.item_list[-1].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[4].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))
        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[4] == 0:
            self.item_list[-2].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[4] == 1:
            self.item_list[-1].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)
        self.consumable_reset()
        self.item_upgrade_button_reset()

    def shield_upgrade(self):
        item_name_before = getattr(self, f'item_class_{self.upgrade_index + 1}')[5].name
        upgrade_rate = random.randint(1, 100)

        if getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[5] == 0 and upgrade_rate < 4:
            getattr(self, f'item_class_{self.upgrade_index + 1}')[5] = self.weapon_list[4]
            getattr(self, f'Equip{self.upgrade_index + 1}_7_Shield_Label').setPixmap(self.weapon_list[4].img)
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[5] = 1
            self.item_list[-2].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[5].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[5] == 1 and \
                getattr(self, f'item_class_{self.upgrade_index + 1}')[1].name.find('중') != -1 and upgrade_rate < 2:
            getattr(self, f'item_class_{self.upgrade_index + 1}')[5] = self.weapon_list[5]
            getattr(self, f'Equip{self.upgrade_index + 1}_7_Shield_Label').setPixmap(self.weapon_list[5].img)
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[5] = 2
            self.item_list[-1].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[5].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[5] == 0:
            self.item_list[-2].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[5] == 1:
            self.item_list[-1].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        self.consumable_reset()
        self.item_upgrade_button_reset()

    def cloak_upgrade(self):
        item_name_before = getattr(self, f'item_class_{self.upgrade_index + 1}')[6].name
        upgrade_rate = random.randint(1, 100)
        if getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[6] == 0 and upgrade_rate < 4:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[6].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[6] = self.cloak_list[1]
                getattr(self, f'Equip{self.upgrade_index + 1}_8_Cloak_Label').setPixmap(self.cloak_list[1].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[6].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[6] = self.cloak_list[4]
                getattr(self, f'Equip{self.upgrade_index + 1}_8_Cloak_Label').setPixmap(self.cloak_list[4].img)
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[6] = 1
            self.item_list[-2].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[6].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))
        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[6] == 1 and upgrade_rate < 2:
            if getattr(self, f'item_class_{self.upgrade_index + 1}')[6].name.find('천') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[6] = self.cloak_list[2]
                getattr(self, f'Equip{self.upgrade_index + 1}_8_Cloak_Label').setPixmap(self.cloak_list[2].img)
            elif getattr(self, f'item_class_{self.upgrade_index + 1}')[6].name.find('가죽') != -1:
                getattr(self, f'item_class_{self.upgrade_index + 1}')[6] = self.cloak_list[5]
                getattr(self, f'Equip{self.upgrade_index + 1}_8_Cloak_Label').setPixmap(self.cloak_list[5].img)
            getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[6] = 2
            self.item_list[-1].stack -= 1
            class_name = self.ComboBox_Class.currentText()
            item_name_after = getattr(self, f'item_class_{self.upgrade_index + 1}')[6].name
            self.Log_textEdit.append(f'[%s]의 [%s]을/를 [%s](으)로 업그레이드 하였습니다'
                                     % (class_name, item_name_before, item_name_after))
        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[6] == 0:
            self.item_list[-2].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)

        elif getattr(self, f'item_class_upgrade_counter_{self.upgrade_index + 1}')[6] == 1:
            self.item_list[-1].stack -= 1
            self.Log_textEdit.append("%s 강화에 실패하였습니다" % item_name_before)
        self.consumable_reset()
        self.item_upgrade_button_reset()

    def class_name_reset(self):
        self.list_class_name = [self.list_class[0][0].character_name, self.list_class[1][0].character_name,
                                self.list_class[2][0].character_name, self.list_class[3][0].character_name,
                                self.list_class[4][0].character_name, self.list_class[5][0].character_name]

    def item_upgrade_button_reset(self):
        for i in range(0, 6):
            if self.item_list[-2].stack > 0 or self.item_list[-1].stack > 0:
                getattr(self, f'Equip{i + 1}_1Helmet_Btn').setEnabled(True)
            if self.item_list[-2].stack > 0 or self.item_list[-1].stack > 0:
                getattr(self, f'Equip{i + 1}_2_Armor_Btn').setEnabled(True)
            if self.item_list[-2].stack > 0 or self.item_list[-1].stack > 0:
                getattr(self, f'Equip{i + 1}_3_Pants_Btn').setEnabled(True)
            if self.item_list[-2].stack > 0 or self.item_list[-1].stack > 0:
                getattr(self, f'Equip{i + 1}_5_Hand_Btn').setEnabled(True)
            if self.item_list[-2].stack > 0 or self.item_list[-1].stack > 0:
                getattr(self, f'Equip{i + 1}_6_Weapon_Btn').setEnabled(True)
            if self.item_list[-2].stack > 0 or self.item_list[-1].stack > 0:
                getattr(self, f'Equip{i + 1}_7_Shield_Btn').setEnabled(True)
            if self.item_list[-2].stack > 0 or self.item_list[-1].stack > 0:
                getattr(self, f'Equip{i + 1}_8_Cloak_Btn').setEnabled(True)

            if self.item_list[-2].stack == 0 or \
                    (self.item_list[-1].stack == 0 and getattr(self, f'item_class_upgrade_counter_{i + 1}')[
                        0] == 1):
                getattr(self, f'Equip{i + 1}_1Helmet_Btn').setEnabled(False)
            if self.item_list[-2].stack == 0 or \
                    (self.item_list[-1].stack == 0 and getattr(self, f'item_class_upgrade_counter_{i + 1}')[
                        1] == 1):
                getattr(self, f'Equip{i + 1}_2_Armor_Btn').setEnabled(False)
            if self.item_list[-2].stack == 0 or \
                    self.item_list[-1].stack == 0 and getattr(self, f'item_class_upgrade_counter_{i + 1}')[2] == 1:
                getattr(self, f'Equip{i + 1}_3_Pants_Btn').setEnabled(False)
            if self.item_list[-2].stack == 0 or \
                    self.item_list[-1].stack == 0 and getattr(self, f'item_class_upgrade_counter_{i + 1}')[3] == 1:
                getattr(self, f'Equip{i + 1}_5_Hand_Btn').setEnabled(False)
            if self.item_list[-2].stack == 0 or \
                    self.item_list[-1].stack == 0 and getattr(self, f'item_class_upgrade_counter_{i + 1}')[4] == 1:
                getattr(self, f'Equip{i + 1}_6_Weapon_Btn').setEnabled(False)
            if self.item_list[-2].stack == 0 or \
                    self.item_list[-1].stack == 0 and getattr(self, f'item_class_upgrade_counter_{i + 1}')[5] == 1:
                getattr(self, f'Equip{i + 1}_7_Shield_Btn').setEnabled(False)
            if self.item_list[-2].stack == 0 or \
                    self.item_list[-1].stack == 0 and getattr(self, f'item_class_upgrade_counter_{i + 1}')[6] == 1:
                getattr(self, f'Equip{i + 1}_8_Cloak_Btn').setEnabled(False)

            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[0] == 2:
                getattr(self, f'Equip{i + 1}_1Helmet_Btn').setEnabled(False)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[1] == 2:
                getattr(self, f'Equip{i + 1}_2_Armor_Btn').setEnabled(False)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[2] == 2:
                getattr(self, f'Equip{i + 1}_3_Pants_Btn').setEnabled(False)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[3] == 2:
                getattr(self, f'Equip{i + 1}_5_Hand_Btn').setEnabled(False)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[4] == 2:
                getattr(self, f'Equip{i + 1}_6_Weapon_Btn').setEnabled(False)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[5] == 1:
                getattr(self, f'Equip{i + 1}_7_Shield_Btn').setEnabled(False)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[5] == 1 and \
                    getattr(self, f'item_class_{i + 1}')[1].name.find('중') != -1:
                getattr(self, f'Equip{i + 1}_7_Shield_Btn').setEnabled(True)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[5] == 2:
                getattr(self, f'Equip{i + 1}_7_Shield_Btn').setEnabled(False)
            if getattr(self, f'item_class_upgrade_counter_{i + 1}')[6] == 2:
                getattr(self, f'Equip{i + 1}_8_Cloak_Btn').setEnabled(False)

            if getattr(self, f'item_class_{i + 1}')[5] is None:
                getattr(self, f'Equip{i + 1}_7_Shield_Btn').setEnabled(False)
            if getattr(self, f'item_class_{i + 1}')[1].name.find('천') != -1:
                getattr(self, f'Equip{i + 1}_7_Shield_Btn').setEnabled(False)

    def class_equip_page(self):
        self.character_selection = self.ComboBox_Class.currentText()
        if self.character_selection == '미하일':
            self.StackWidget_Equip.setCurrentWidget(self.Class_1_Equip_Page)
        elif self.character_selection == '루미너스':
            self.StackWidget_Equip.setCurrentWidget(self.Class_2_Equip_Page)
        elif self.character_selection == '알렉스':
            self.StackWidget_Equip.setCurrentWidget(self.Class_3_Equip_Page)
        elif self.character_selection == '샐러맨더':
            self.StackWidget_Equip.setCurrentWidget(self.Class_4_Equip_Page)
        elif self.character_selection == '메르데스':
            self.StackWidget_Equip.setCurrentWidget(self.Class_5_Equip_Page)
        elif self.character_selection == '랜슬롯':
            self.StackWidget_Equip.setCurrentWidget(self.Class_6_Equip_Page)


    def atkup_reset(self, num):
        self.damage_status = str((self.class_item[num-1][4].damage * self.guardLevel) * 10)
        getattr(self, f'Class{num}_DetailsStatus_AtkValue').setText(self.damage_status)
    def status_page_reset(self):
        for i in range(len(self.list_class)):
            # 0-6
            getattr(self, f'Class{i + 1}_DetailsStatus_Name').setText(self.list_class[i][0].character_name)
            getattr(self, f'Class{i + 1}_DetailsStatus_Class').setText(self.list_class[i][0].class_name)

            if self.class_item[i][5] is None:
                self.defence_status = str(int(((self.class_item[i][0].armor + self.class_item[i][1].armor +
                                      self.class_item[i][2].armor + self.class_item[i][3].armor +
                                      self.class_item[i][6].armor) * self.guardLevel)*0.1))
            else:
                self.defence_status = str(int(((self.class_item[i][0].armor + self.class_item[i][1].armor +
                                      self.class_item[i][2].armor + self.class_item[i][3].armor +
                                      self.class_item[i][5].damage + self.class_item[i][6].armor) * self.guardLevel)*0.1))
            getattr(self, f'Class{i+1}_DetailsStatus_ShieldValue').setText(self.defence_status)
        for j in range(len(self.list_class) - 1):
            getattr(self, f'Class{j + 1}_DetailsStatus_ConditionValue').setText('출전중')
        self.Class6_DetailsStatus_ConditionValue.setText('휴식중')
        for k in range(len(self.list_class) - 1):
            getattr(self, f'Class{k + 1}_DetailsStatus_HpValue').setText(str(self.class_hp_dict.get(k+1)) +
                                                                         "/" + str(self.list_class[k][0].get_maxhp()))
            getattr(self, f'Class{k + 1}_DetailsStatus_MpValue').setText(str(self.class_mp_dict.get(k+1)) +
                                                                         "/" + str(self.list_class[k][0].get_maxmp()))
        self.Class6_DetailsStatus_HpValue.setText((str(self.class_hp_dict_last.get(0)) +
                                                                         "/" + str(self.list_class[5][0].get_maxhp())))
        self.Class6_DetailsStatus_MpValue.setText((str(self.class_mp_dict_last.get(0)) +
                                                   "/" + str(self.list_class[5][0].get_maxmp())))

    def low_ui_reset(self):
        for i in range(1, 6):
            # 하단 ui에 캐릭터 추가
            getattr(self, f'Status{i}_1_Class').setText(self.list_class[i - 1][0].class_name)  # 클래스명 지정
            getattr(self, f'Status{i}_1_Name').setText(self.list_class[i - 1][0].character_name)  # 캐릭터명 지정
            getattr(self, f'Status{i}_2_HpValue').setText(
                str(self.class_hp_dict.get(i)) + "/" + str(self.list_class[i - 1][0].get_maxhp()))  # hp(기본 값/변하는 값)
            getattr(self, f'Status{i}_3_MpValue').setText(
                str(self.class_mp_dict.get(i)) + "/" + str(self.list_class[i - 1][0].get_maxmp()))  # mp(기본 값/변하는 값)

            # 정렬 및 스타일시트 배경 디자인
            getattr(self, f'Status{i}_2_HpValue').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i}_1_Name').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i}_3_MpValue').setAlignment(Qt.AlignCenter)
            getattr(self, f'Status{i}_1_Class').setAlignment(Qt.AlignCenter)  # 텍스트 가운데 정렬
            getattr(self, f'Status{i}_1_Class').setStyleSheet('QLabel{background-color:#55aaff;}')  # 클래스 배경 색상 지정
            getattr(self, f'Status{i}_2_Hp').setStyleSheet('QLabel{background-color:#55aaff;}')  # hp, mp 배경 색상 지정
            getattr(self, f'Status{i}_3_Mp').setStyleSheet('QLabel{background-color:#55aaff;}')

    def class_item_list(self):
        self.class_item = []
        for i in range(6):
            if self.list_class[i][0].class_name == '전사':
                self.class_item.append(self.class_warrior)
            elif self.list_class[i][0].class_name == '백법사':
                self.class_item.append(self.class_whitewizard)
            elif self.list_class[i][0].class_name == '흑법사':
                self.class_item.append(self.class_blackwizard)
            elif self.list_class[i][0].class_name == '적법사':
                self.class_item.append(self.class_redwizard)
            elif self.list_class[i][0].class_name == '궁수':
                self.class_item.append(self.class_archer)
            elif self.list_class[i][0].class_name == '검사':
                self.class_item.append(self.class_swordman)




    def get_index(self):
        self.upgrade_index = self.StackWidget_Equip.currentIndex()

    def consumable_reset(self):
        """소모품 갯수 갱신 함수"""
        for i in range(len(self.item_list) - 2):
            if self.item_list[i].stack > 0:
                getattr(self, f'Portion_{i + 1}_Btn').setEnabled(True)

        for i in range(len(self.item_list) - 2):
            if self.item_list[i].stack == 0:
                getattr(self, f'Portion_{i + 1}_Btn').setEnabled(False)

        for i in range(len(self.item_list)):
            getattr(self, f'Portion_{i + 1}_Value').display(self.item_list[i].stack)

    def use_page(self):
        self.Btn_Portion.setEnabled(False)
        self.Btn_Status.setEnabled(True)
        self.Btn_Equip.setEnabled(True)
        self.consumable_reset()

    def equip_page(self):
        self.Btn_Portion.setEnabled(True)
        self.Btn_Status.setEnabled(True)
        self.Btn_Equip.setEnabled(False)
        self.item_upgrade_button_reset()

    def status_page(self):
        self.Btn_Portion.setEnabled(True)
        self.Btn_Status.setEnabled(False)
        for i in range(1, 7):
            getattr(self, f'Class_{i}_Btn').setEnabled(False)
        self.Btn_Equip.setEnabled(True)
        self.status_page_reset()

    def make_effect_list(self):
        self.attack_effect_timer = QTimer(self)
        self.attack_effect_normal = QMovie('./image/Effect/attack_effect_2.gif')
        self.attack_effect_fire = QMovie('./image/Effect/fire_effect_2.gif')
        self.attack_effect_ice = QMovie('./image/Effect/ice_effect_1.gif')
        self.attack_effect_thunder = QMovie('./image/Effect/thunder_effect.gif')
        self.attack_effect_bow = QMovie('./image/Effect/bow_effect_1.gif')
        self.effect_heal = QMovie('./image/Effect/heal_effect_1.gif')
        self.effect_buff = QMovie('./image/Effect/heal_effect_2.gif')
        self.effect_widget_list = [self.Effect_Widget_1, self.Effect_Widget_2,
                                   self.Effect_Widget_3, self.Effect_Widget_4,
                                   self.Effect_Widget_5, self.Effect_Widget_6,
                                   self.Effect_Widget_7, self.Effect_Widget_8,
                                   self.Effect_Widget_9, self.Effect_Widget_10]



    def attack_effect(self, num):
        self.effect_widget_list[num].show()
        self.effect_widget_list[num].setScaledContents(True)
        self.effect_widget_list[num].setAlignment(Qt.AlignCenter)
        self.effect_widget_list[num].setMovie(self.attack_effect_normal)
        self.attack_effect_timer.start(500)
        self.attack_effect_normal.start()
        self.attack_effect_timer.timeout.connect(lambda y=num: self.normal_close(y))

    def normal_close(self, num):
        self.attack_effect_timer.stop()
        self.attack_effect_normal.stop()
        self.effect_widget_list[num].close()

    def show_ending(self):
        """엔딩페이지 보여주는 곳"""
        self.StackWidget_Field.setCurrentIndex(0) #일반필드로 옮겨주고
        hide_list = [self.Character_QLabel_2, self.entrance, self.boss_monster,
                     self.portal_sample,self.Character_QLabel ]

        # 라벨리스트를 숨겨준다.
        for label in hide_list:
            label.hide()

        #영상의 경로를 불러온다
        self.movie_1 = QMovie('./video/boss_ending.gif', bytearray(), self)
        self.movie_2 = QMovie('./video/boki_endingcredits.gif', bytearray(), self)

        self.ending_timer = QTimer()
        self.ending_timer_2 = QTimer()

        self.ending_timer.timeout.connect(self.play_second_gif)
        self.ending_timer_2.timeout.connect(self.ending_message)
        self.play_first_gif()

    def play_first_gif(self):
        self.BackGround_Nomal.setMovie(self.movie_1)
        self.movie_1.start()
        self.ending_timer.start(130000)

    def play_second_gif(self):
        self.ending_timer.stop()
        self.BackGround_Nomal.setMovie(self.movie_2)
        self.movie_1.stop()
        self.movie_2.start()
        self.ending_timer_2.start(16000)
    def ending_message(self):
        self.close()
        self.show_messagebox("게임이 종료되었습니다.\n플레이 해 주셔서 감사합니다!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow_2 = WindowClass()
    myWindow = Boki_Opening()
    myWindow.show()
    app.exec_()