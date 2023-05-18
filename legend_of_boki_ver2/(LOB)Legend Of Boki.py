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

    # 캐릭터 방향키로 움직이기===============================================================================================
    def keyPressEvent(self, event):
        if self.HoldSwitch == 0:
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
                        self.StackWidget_Field.setCurrentIndex(2)
                        self.MainFrame_Bottom.setEnabled(True)
                        self.Page_Use.setEnabled(False)
                        self.StackWidget_Item.setCurrentWidget(self.Page_Use)
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
                        self.HoldSwitch = 1  # 스택 위젯 페이지 이동후에도 캐릭터 이동하는 현상 예외처리
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

            # (미궁 포탈 위치 - 캐릭터 위치)를 절대값으로 만듬
            if ((abs(self.Potal_QLabel.pos().x() - self.Character_QLabel.pos().x()) < 20)
                    and (abs(self.Potal_QLabel.pos().y() - self.Character_QLabel.pos().y()) < 20)):
                # 미궁 이동
                self.StackWidget_Field.setCurrentIndex(1)
                self.Log_textEdit.append("포탈을 탔습니다.")  # 미궁 이동시 출력문
                self.HoldSwitch = 1  # 스택 위젯 페이지 이동후에도 캐릭터 이동하는 현상 예외처리
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
