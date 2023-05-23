import os
import random
import sys
import time

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import uic, Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QMovie, QFontDatabase, QFont
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

        # 폰트 지정
        # TTF 파일을 추가
        QFontDatabase.addApplicationFont('neodgm.ttf')

        # QFont 객체를 만든다.
        font = QFont('Neo둥근모', 12)
        font_style = 'font-family: Neo둥근모;'
        self.setStyleSheet(font_style)


        # 클래스 값 넣어줄 리스트 mp / hp
        self.class_hp_mp_present_value_list = [
            [self.Status1_2_HpValue, self.Status1_3_MpValue],
            [self.Status2_2_HpValue, self.Status2_3_MpValue],
            [self.Status3_2_HpValue, self.Status3_3_MpValue],
            [self.Status4_2_HpValue, self.Status4_3_MpValue],
            [self.Status5_2_HpValue, self.Status5_3_MpValue],
        ]


        # 일단 임시로 옮겨놓음
        # for i in range(1, 6):
        #     getattr(self, f"Status{i}_Action1_Attack").clicked.connect(lambda : self.attack_function(i))

        self.Status1_Action1_Attack.clicked.connect(lambda: self.attack_function(1))
        self.Status2_Action1_Attack.clicked.connect(lambda: self.attack_function(2))
        self.Status3_Action1_Attack.clicked.connect(lambda: self.attack_function(3))
        self.Status4_Action1_Attack.clicked.connect(lambda: self.attack_function(4))
        self.Status5_Action1_Attack.clicked.connect(lambda: self.attack_function(5))

        # 몬스터 버튼 클릭하면 몬스터 공격 함수로 넘어감
        # for j in range(1, 11):
        #     getattr(self, f"Monster_{j}_QButton").clicked.connect(lambda: self.monster_got_damage(j))
        self.Monster_1_QButton.clicked.connect(lambda x: self.monster_got_damage(1))
        self.Monster_2_QButton.clicked.connect(lambda x: self.monster_got_damage(2))
        self.Monster_3_QButton.clicked.connect(lambda x: self.monster_got_damage(3))
        self.Monster_4_QButton.clicked.connect(lambda x: self.monster_got_damage(4))
        self.Monster_5_QButton.clicked.connect(lambda x: self.monster_got_damage(5))
        self.Monster_6_QButton.clicked.connect(lambda x: self.monster_got_damage(6))
        self.Monster_7_QButton.clicked.connect(lambda x: self.monster_got_damage(7))
        self.Monster_8_QButton.clicked.connect(lambda x: self.monster_got_damage(8))
        self.Monster_9_QButton.clicked.connect(lambda x: self.monster_got_damage(9))
        self.Monster_10_QButton.clicked.connect(lambda x: self.monster_got_damage(10))

        # 공격 타입 구분 초기 설정값
        self.attackType = 0

        #
        self.stop_the_loop = False

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
        self.guardLevel = 1

        self.guardoption()  # 캐릭터 생성해줌
        self.StautsHpall = []
        self.StautsMpall = []
        self.Statusclass = []

        # 리스트를 셔플로 돌려줌
        # 위 self.guardoption()에서 생성한 클래스 캐릭터들의 값총 6개-(전체정보/최대hp/최대mp)저장
        random.shuffle(self.list_class)

        # 유저 체력을 리스트에 담아준다. 응애2
        self.class_hp_dict = {}
        self.class_mp_dict = {}
        for i in range(1, 5 + 1):  # 서플로 돌려준 클래스유저들의 체력/마나를 빈 딕셔너리에 1부터 5까지 담아줌
            self.class_hp_dict[i] = self.list_class[i - 1][1]  # hp 담기
            self.class_mp_dict[i] = self.list_class[i - 1][2]  # mp 담기
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

        # ++ keypressevent 함수에 추가로 추합
        # ==================================================================================================================

        # 몬스터 상속 - 몬스터 필드/ 이름/ 이미지/ 레벨/ hp/ 공격력(임시로100)
        self.nomalfield_fire_monster1 = MonsterOption("불의 지역", "불타는 나무정령", "character_1.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.nomalfield_fire_monster2 = MonsterOption("불의 지역", "불의 정령", "character_2.png", 1,
                                                      random.randrange(200, 1000), 50)
        self.nomalfield_fire_monster3 = MonsterOption("불의 지역", "불타는 골렘", "character_3.png", 1,
                                                      random.randrange(200, 1000), 50)
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

        # 클래스 스킬 버튼들 리스트화 /
        # #미하일 도발스킬 / #루미너스 스킬: 힐, 그레이트힐, 힐올, 공격력업, 방어력업, 맵핵 / #알렉스 스킬: 파이어볼, 파이어월, 블리자드, 썬더브레이커 / # 메르데스 집중타, 듀얼샷, 마스터샷 / #샐리멘더 힐, 그레이트힐, 힐올, 파이어볼 파이어월, 블리자드 썬더브레이커
        self.pushbox = [self.Class1_Skill1_Btn, self.Class2_Skill1_Btn, self.Class2_Skill2_Btn, self.Class2_Skill3_Btn,
                        self.Class2_Skill4_Btn, self.Class2_Skill5_Btn, self.Class2_Skill6_Btn,
                        self.Class3_Skill1_Btn, self.Class3_Skill2_Btn, self.Class3_Skill3_Btn, self.Class3_Skill4_Btn,
                        self.Class4_Skill1_Btn, self.Class4_Skill2_Btn, self.Class4_Skill3_Btn,
                        self.Class4_Skill4_Btn, self.Class4_Skill5_Btn, self.Class4_Skill6_Btn, self.Class4_Skill7_Btn,
                        self.Class5_Skill1_Btn, self.Class5_Skill2_Btn, self.Class5_Skill3_Btn,
                        self.Class6_Skill1_Btn]  # 강타

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

    # 신규함수 ========================================================================================================================

    # 몬스터가 랜덤 등장하는 부분
    def Add_Monster_info(self):
        # 몬스터 랜덤 등장 구현
        self.j = 1
        monster_random_num = random.randrange(2, 11)  # 몬스터 랜덤 등장 숫자
        self.monster_hp_dict = {}  # 빈 딕셔너리에 몬스터 체력 담기

        for num in range(1, monster_random_num):
            getattr(self, f'Monster_{num}_Name').setText(getattr(self, f'nomalfield_fire_monster{1}').name)  # 몬스터 이름
            getattr(self, f'Monster_{num}_Name').setStyleSheet("Color : white")
            getattr(self, f'Monster_{num}_QLabel').setPixmap(
                QPixmap(getattr(self, f'nomalfield_fire_monster{1}').image))  # 몬스터 이미지
            getattr(self, f'Monster_{num}_QProgressBar').setMaximum(
                getattr(self, f'nomalfield_fire_monster{1}').hp)  # 몬스터 체력
            self.monster_hp_dict[num] = getattr(self, f'nomalfield_fire_monster{1}').hp  # 몬스터 체력 더하기
            getattr(self, f'Monster_{num}_QProgressBar').setValue(
                getattr(self, f'nomalfield_fire_monster{1}').hp)  # 몬스터 체력
            getattr(self, f'Monster_{num}_QButton').setEnabled(False)
            getattr(self, f'Monster_{num}_Name').show()
            getattr(self, f'Monster_{num}_QLabel').show()
            getattr(self, f'Monster_{num}_QButton').show()
            getattr(self, f'Monster_{num}_QProgressBar').show()

            if self.j < 3:
                self.j += 1
            else:
                self.j = 1
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
        if self.go_to_normalfield() == 'out':
            return
        print('유저턴일때 처음hp', self.class_hp_dict)

        ############################일반필드나가기 ####################################
        print("함수 유저턴")


        ## 유저 턴 확인
        print('유저턴', self.user_turn)

        if self.user_turn >= 5:  # 만약 유저 턴이 5보다 크다면
            self.user_turn = 1  # 1로 만들어준다.
            self.monster_attack_users()  # 이거 여기다 넣으니까 (동시 다발적으로 캐릭터가 죽으면 턴이 넘어가도 몬스터가 공격을안함) 이 현상이 해결됨..
            print('여기서죽음 1')
            if self.go_to_normalfield() == 'out':
                return
        else:
            self.user_turn += 1  # 그렇지 않다면 턴 더해주기
        print('User_Turn 함수/현재 턴은: ', self.user_turn)  # 확인용

        if self.go_to_normalfield() == 'out':
            return

        # 유저턴 hp 0 이상이면 활성화 / 아니면 다음 턴으로 넘어감
        selected_character_hp = self.class_hp_dict[self.user_turn]  # 선택된 캐릭터의 hp
        if selected_character_hp > 0:
            self.active_class_frame(self.user_turn)  # 해당 클래스 버튼들 활성화 및 다른 프레임 버튼들 비활성화
        else:
            self.User_Turn()  # 0보다 작으면 다시 User_Turn 돌아감 (재귀함수)

    def go_to_normalfield(self):
        # 사용하면 됨 / # 만약 모든 유저 hp가 0이면 일반필드로 나가게 함
        # 이 함수 수정함 / 이 함수 나오는 모든 부분 수정필요 **응애**

        # 클래스들의 체력이 모두 0일 때 경우
        if all(h == 0 for h in self.class_hp_dict.values()):
            self.class_turn = [1, 2, 3, 4, 5]
            print("유저체력 부족해서 죽은 경우")
            self.Log_textEdit.append('유저 체력이 부족하여 후퇴합니다... 한 발자국만 움직여 보자...')
            self.set_actions_enabled(5, False)  # 클래스들의 모든 버튼 비활성화 시켜줌 <= 지금 작동 안함 살려조ㅁ
            self.current_index = 0
            self.StackWidget_Field.setCurrentIndex(0)  # 일반필드로 이동
            print("여기서 User_turn 으로 이동하는 현상 발생")

            return 'out'

        # 몬스터들의 체력이 모두 0인 경우
        if all(v == 0 for v in self.monster_hp_dict.values()):
            self.user_turn = 0
            print("몬스터 체력이 0입니다.")  # 확인용
            self.Log_textEdit.append('몬스터를 모두 처치했습니다....')
            self.set_actions_enabled(5, False)  # 클래스들의 모든 버튼 비활성화 시켜줌 <= 지금 작동 안함 살려조ㅁ
            self.current_index = 0
            self.StackWidget_Field.setCurrentIndex(0)  # 일반필드로 이동
            return 'out'
        return 'not_out'

    def attack_function(self, num):
        """공격 함수(공격버튼 외 다른 버튼 비활성화, 몬스터 공격버튼 활성화)"""
        self.Log_textEdit.append(f"클래스 {num}번이 공격버튼을 선택했습니다.")

        # 공격 버튼 외에 다른 버튼 비활성화
        getattr(self, f'Status{num}_Action2_Skill').setEnabled(False)
        getattr(self, f'Status{num}_Action3_Item').setEnabled(False)
        getattr(self, f'Status{num}_Action4_Run').setEnabled(False)

        # 몬스터 공격 버튼 활성화
        self.monster_btn_active(True)

    def monster_got_damage(self, num):
        """몬스터 데미지 입는 함수"""

        self.monster_hp_dict[num] -= 100  # 임시로 몬스터 체력에는 100씩 데미지 입힘
        print(f'{num}번 몬스터의 맞은 후 체력: {self.monster_hp_dict[num]}')  # 확인용

        if self.go_to_normalfield() == 'out':  # 일반필드 나가기
            return
        # 체력 0인 얘들은 안보여주기
        for m, n in self.monster_hp_dict.items():
            if n < 0:
                print(f'{m}번 몬스터를 처치했습니다.')  # 콘솔 확인용
                self.Log_textEdit.append(f'{m}번 몬스터를 처치했습니다.')
                self.monster_hp_dict[m] = 0  # 몬스터 체력 0 만들어주기

                # 죽은 몬스터 구성들은 숨겨주기
                getattr(self, f'Monster_{m}_Name').hide()
                getattr(self, f'Monster_{m}_QLabel').hide()
                getattr(self, f'Monster_{m}_QButton').hide()
                getattr(self, f'Monster_{m}_QProgressBar').hide()


        # 프로그래스바에 유저가 때린 몬스터 체력 넣어주기
        getattr(self, f'Monster_{num}_QProgressBar').setValue(self.monster_hp_dict[num])  # 몬스터 체력

        # 몬스터 버튼 비활성화
        self.monster_btn_active(False)

        # 공격 버튼 비활성화
        getattr(self, f'Status{self.user_turn}_Action1_Attack').setEnabled(False)

        print(f'다음 턴으로 넘어가야됨=========================(지금 유저턴{self.user_turn})')

        #####################추가 항목#########################################
        # self.cnt = 0  # 클래스 체력이 0이 아닌 유저들을 카운트해서 현재 살아남은 유저 수를 기준으로 카운트가 초기화됨 좀더물어보장
        # for hp in self.class_hp_dict.values():
        #     if hp != 0:
        #         self.cnt += 1

        if self.user_turn == 5:
            self.user_turn = 0  # 유저 턴 0으로 만들어주고 다른 버튼들 비활성화 시켜줌(나중에 단축시킬 것)
            self.set_actions_enabled(5, False)  # 5명 모두 비활성화 시켜주고

            ### 몬스터 공격 함수로 넘어가야됨
            self.monster_attack_users()

        else:  # 유저턴이 5 미만이면 다시 유저턴으로 돌아감
            ################################### 다음 턴으로 넘어가기 몬스터 턴에서 더해주기!!!!!!!!!!!! ########################################
            print("몬스터가 데미지 입고 유저턴으로 갑니다")
            self.User_Turn()

    def monster_attack_users(self):
        """몬스터가 유저 랜덤으로 때리는 함수"""
        # 살아있는 몬스터가 돌아가면서 랜덤으로 유저 때림
        # 유저hp가 0이 되면 패스
        # 살아있는 몬스터 수 세기(죽으면 hide() 시켜줌)

        self.alive_monster = []  # 살아있는 몬스터 리스트에 담아주기
        for i, j in self.monster_hp_dict.items():  # 몬스터 체력 딕셔너리는 몬스터 호출 함수 Add_Monster_info 에 있음. 여기서 체력을 가져와줌
            print(i, j)  # 확인용
            if j > 0:  # 만약 몬스터 체력이 0 이상이면
                self.alive_monster.append(i)  # 빈 리스트에 더해준다.
                pass
            elif j == 0:  # 만약 몬스터 체력이 0 이면
                pass
            else:  # 만약 몬스터 체력이 0 미만이면
                print("패스")
                pass

        print('살아있는 몬스터 리스트는', self.alive_monster)

        # 살아있는 클래스 수 세기
        self.alive_class = [key for key, value in self.class_hp_dict.items() if value > 0]

        # 어떤 클래스 때릴지 랜덤으로 리스트에 추가 - 몬스터 갯수만큼 세주기
        attacked_class_list = []
        for i in range(1, len(self.alive_monster) + 1):
            attacked_class_list.append(random.choice(self.alive_class))
        print("attacked_class_list", attacked_class_list)

        # 클래스의 hp 깎아준다 <============여기 수정함 응애3


        # 클래스 라벨들
        class_label_list = [self.Class_1_QLabel, self.Class_2_QLabel, self.Class_3_QLabel, self.Class_4_QLabel,
                            self.Class_5_QLabel]

        death_class = []
        for m in range(1, len(self.alive_monster) + 1):
            self.Log_textEdit.append(f"{m}번째 몬스터가 {attacked_class_list[m - 1]}번 클래스를 100만큼 때립니다...")
            print(f"{m}번째 몬스터가 {attacked_class_list[m - 1]}번 클래스를 100만큼 때립니다...")
            self.class_hp_dict[attacked_class_list[m - 1]] -= 100  # 임시로 100씩 때린다
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
        # 비석
        for j in death_class:
            class_label_list[j - 1].setPixmap(QtGui.QPixmap('비석.png'))

        for i in range(1, 6):
            self.class_hp_mp_present_value_list[i - 1][0].setText(
                f'{self.class_hp_dict[i]}/{self.Statusclass[i - 1].get_maxhp()}')  # hp판에 변경된 값 넣어주기
            self.class_hp_mp_present_value_list[i - 1][1].setText(
                f'{self.class_mp_dict[i]}/{self.Statusclass[i - 1].get_maxmp()}')  # mp판에 변경된 값 넣어주기

        print("몬스터 공격이 종료되었습니다.")
        if self.go_to_normalfield() == 'out':
            print("여기서 오류가 나는 듯@@@@")
            return
        else:
            print("몬스터 공격이 종료 후 user_turn", self.user_turn)
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

    def set_actions_enabled(self, status_count, enabled):  ##########
        """클래스 프레임 활성화/비활성화 시키기"""
        for i in range(1, status_count + 1):
            getattr(self, f'Status{i}_Action1_Attack').setEnabled(enabled)
            getattr(self, f'Status{i}_Action2_Skill').setEnabled(enabled)
            getattr(self, f'Status{i}_Action3_Item').setEnabled(enabled)
            getattr(self, f'Status{i}_Action4_Run').setEnabled(enabled)

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

    def keyPressEvent(self, event):

        # 소연 keypressevent 함수 내 수정(current_index값 받아오기)===========================================================

        # 현재 스택위젯 값 가져오기 # 응애7(current_index에 self붙여줌)
        self.current_index = self.StackWidget_Field.currentIndex()

        ## 일반필드일 때
        if self.current_index == 0:
            self.return_user_state()

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
                        print("전투필드로 이동하고 적 생성합니다.")
                        self.StackWidget_Field.setCurrentIndex(2)  # 전투필드로 이동

                        self.Add_Monster_info()
                        print("키프레스 이벤트 값 속의 유저턴입니당")
                        self.User_Turn()
                        """
                        적을 만났을 때 설정값
                        """

                    else:
                        self.Log_textEdit.append("타 수호대를 만났습니다.")


                elif rand_event > 7:
                    self.Log_textEdit.append("아이템을 획득하였습니다.")
                    """
                    길준 : 여기를 채워주세요
                    """
            # 왼쪽 상단에 변경된 죄표 값 출력
            self.TopUI_Coordinate_Label.setText(f"x좌표: {lab_x_} y좌표: {lab_y_}")

        ## 던전필드일때
        elif self.current_index == 1:
            pass
        else:
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
