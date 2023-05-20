import sys
import random
from PyQt5.Qt import *

from bottomUi import Ui_Maingame as maingame

from PyQt5.QtWidgets import *


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


class MainGame(QMainWindow, maingame):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.Widget_Skill.hide()    # 위젯 스킬 창 투명화

        self.user_turn = 0      # 유저 턴에 대한 초기 설정
        self.run_random = 0     # 유저 도망 선택 확률에 대한 초기 설정
        self.color = 0

        self.btn_clicked = -1       # 하단 ui 버튼에 대한 초기 설정
        self.timer_1 = QTimer()
        self.timer_1.setInterval(400)
        self.timer_1.timeout.connect(self.change_btn_color)
        self.timer_1.start()

        self.item_btn_clicked = -1  # 인벤토리 버튼에 대한 초기 설정
        self.timer_2 = QTimer()
        self.timer_2.setInterval(400)
        self.timer_2.timeout.connect(self.change_item_btn_color)
        self.timer_2.start()

        # 캐릭터 별 프레임
        self.frame_class_list = [self.Frame_Class1_Status, self.Frame_Class2_Status,
                                 self.Frame_Class3_Status, self.Frame_Class4_Status, self.Frame_Class5_Status]
        # 하단 ui 버튼 리스트
        self.btn_list = [self.Status1_Action1_Attack, self.Status2_Action1_Attack, self.Status3_Action1_Attack,
                            self.Status4_Action1_Attack, self.Status5_Action1_Attack,
                         self.Status1_Action2_Skill, self.Status2_Action2_Skill, self.Status3_Action2_Skill,
                          self.Status4_Action2_Skill, self.Status5_Action2_Skill,
                         self.Status1_Action3_Item, self.Status2_Action3_Item, self.Status3_Action3_Item,
                          self.Status4_Action3_Item, self.Status5_Action3_Item,
                         self.Status1_Action4_Run, self.Status2_Action4_Run, self.Status3_Action4_Run,
                          self.Status4_Action4_Run, self.Status5_Action4_Run]

        # 오른쪽 인벤토리 버튼 리스트
        self.item_list = [self.Btn_Equip, self.Btn_Portion]

        # 몬스터 버튼 리스트
        self.mon_list = [self.Monster_1_QButton, self.Monster_2_QButton, self.Monster_3_QButton, self.Monster_4_QButton,
                        self.Monster_5_QButton, self.Monster_6_QButton, self.Monster_7_QButton, self.Monster_8_QButton,
                        self.Monster_9_QButton, self.Monster_10_QButton]


        # 해당 인스턴스에 캐릭터 정보 저장
        class_1 = Status('전사', '미하일', 300, 0, 1)
        class_2 = Status('백법사', '루미너스', 200, 150, 1)
        class_3 = Status('흑법사', '알렉스', 200, 150, 1)
        class_4 = Status('적법사', '샐러맨더', 150, 150, 1)
        class_5 = Status('궁수', '메르데스', 150, 150, 1)
        class_6 = Status('검사', '랜슬롯', 150, 150, 1)

        # 인스턴스 리스트화
        list_class = [class_1, class_2, class_3, class_4, class_5, class_6]

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

        # 삭제 가능한 부분
        self.StackWidget_Field.setCurrentWidget(self.Page_Nomal_Field)        # 일반 필드 작업하려고 둔 것
        self.StackWidget_Field.setCurrentIndex(2)
        self.page = self.StackWidget_Field.currentIndex()

        # ====/일반 필드 페이지/=============================================================================================================

        if self.page == 0:
            print('일반필드 페이지입니다.')

            # ui 하단 버튼 비활성화
            for btn in self.btn_list:
                btn.setEnabled(False)

            # ui 오른쪽 인벤토리 선택 버튼 선택 시 스타일 넣기
            for idx, btn in enumerate(self.item_list):
                btn.clicked.connect(lambda x=None, y=idx: self.item_btn_clicked_fuc(y))

            self.Btn_Portion.clicked.connect(lambda :self.StackWidget_Item.setCurrentWidget(self.Page_Use))
            self.Btn_Equip.clicked.connect(lambda : self.StackWidget_Item.setCurrentWidget(self.Page_Equip))

        # ====/전투 및 던전 페이지/=============================================================================================================

        elif (self.page == 1) or (self.page == 2):
            print('전투 페이지 겸 던전 페이지 입니다.')

            # 캐릭터 창 초기 [0] 빼고 비활성화 상태
            for FCS in self.frame_class_list[1:]:
                FCS.setEnabled(False)

            # 몬스터 초기 전체 비활성화 상태
            for mon_btn in range(10):
                getattr(self, f'Monster_{mon_btn + 1}_QButton').setEnabled(False)

            # 스킬창 모두 비활성화
            for skill in range(5):
                getattr(self, f'Frame_Class{skill + 1}').setEnabled(False)

            # 인벤토리의 창을 소비 아이템 창으로 변경
            self.StackWidget_Item.setCurrentWidget(self.Page_Use)

            # 인벤토리 선택 버튼 및 소비 아이템 버튼 비활성화
            self.Btn_Equip.setEnabled(False)
            self.Btn_Portion.setEnabled(False)

            for btn in range(11):
                getattr(self, f'Portion_{btn + 1}_Btn').setEnabled(False)

            # 버튼 선택에 대한 시그널 연결
            for btn in range(5):
                getattr(self, f'Status{btn + 1}_Action1_Attack').clicked.connect(self.Attack_btn)
                getattr(self, f'Status{btn + 1}_Action3_Item').clicked.connect(self.Item_btn)
                getattr(self, f'Status{btn + 1}_Action4_Run').clicked.connect(self.Run_btn)

            # 몬스터 버튼 선택에 대한 시그널 연결
            for mon_btn in self.mon_list:
                mon_btn.clicked.connect(self.user_Turn)

            name_text = self.Status1_1_Name.text()
            name_text2 = self.Status2_1_Name.text()
            name_text3 = self.Status3_1_Name.text()
            name_text4 = self.Status4_1_Name.text()
            name_text5 = self.Status5_1_Name.text()

            skills = {'미하일': 1, '루미너스': 2, '알렉스': 3, '샐러맨더': 4, '메르데스': 5,'랜슬롯': 6}  # 각 이름에 대한 인덱스를 찾아서 람다 함수 내에서 스킬 버튼을 연결

            self.Status1_Action2_Skill.clicked.connect(lambda x, index=skills.get(name_text): self.skill_btn(index))
            self.Status2_Action2_Skill.clicked.connect(lambda x, index=skills.get(name_text2): self.skill_btn(index))
            self.Status3_Action2_Skill.clicked.connect(lambda x, index=skills.get(name_text3): self.skill_btn(index))
            self.Status4_Action2_Skill.clicked.connect(lambda x, index=skills.get(name_text4): self.skill_btn(index))
            self.Status5_Action2_Skill.clicked.connect(lambda x, index=skills.get(name_text5): self.skill_btn(index))

            # 하단 ui 버튼 클릭 시 다른 버튼 비활성화 시키기
            for btn in range(5):
                getattr(self, f'Status{btn + 1}_Action1_Attack').clicked.connect(lambda: self.change('1'))
                getattr(self, f'Status{btn + 1}_Action2_Skill').clicked.connect(lambda: self.change('2'))
                getattr(self, f'Status{btn + 1}_Action3_Item').clicked.connect(lambda: self.change('3'))
                getattr(self, f'Status{btn + 1}_Action4_Run').clicked.connect(lambda: self.change('4'))

            # 버튼 색상 적용해주는 함수
            for idx, btn in enumerate(self.btn_list):
                btn.clicked.connect(lambda x=None, y=idx: self.btn_clicked_fuc(y))
            # self.btn_list[0].clicked.connect(lambda: self.btn_clicked_fuc(0))



# ====== 함수 ============================================================================================================

    # ui 하단 선택 버튼 클릭 시 스타일 설정 =============================================================================================

    def btn_clicked_fuc(self, idx):
        self.btn_clicked = idx
        for i, a in enumerate(self.btn_list):
            if idx != i:
                a.setStyleSheet("")

    # ui 하단 색상 적용해주는 함수
    def change_btn_color(self):
        if self.btn_clicked == -1:
            return
        print(self.btn_clicked)
        if self.color == 0:
            self.btn_list[self.btn_clicked].setStyleSheet('border-style: solid; border-width: 5px; '
                                                          'border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, '
                                                          'stop:0 rgba(10, 242, 251, 255), stop:1 rgba(224, 6, 159, 255));')
        else:
            self.btn_list[self.btn_clicked].setStyleSheet('border-style: solid; border-width: 2px; border-color: black;')
        self.color += 1
        if self.color == 2:
            self.color = 0

    # ui 오른쪽 인벤토리 선택 버튼 클릭 시 스타일 설정 ======================================================================================

    def item_btn_clicked_fuc(self, idx):
        self.item_btn_clicked = idx
        for i, a in enumerate(self.item_list):
            if idx != i:
                a.setStyleSheet("")

    def change_item_btn_color(self):
        if self.item_btn_clicked == -1:
            return
        print(self.item_btn_clicked)
        if self.color == 0:
            self.item_list[self.item_btn_clicked].setStyleSheet('border-style: solid; border-width: 5px; '
                                                          'border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, '
                                                          'stop:0 rgba(10, 242, 251, 255), stop:1 rgba(224, 6, 159, 255));')
        else:
            self.item_list[self.item_btn_clicked].setStyleSheet('border-style: solid; border-width: 2px; border-color: blac\;')
        self.color += 1
        if self.color == 2:
            self.color = 0

    # 하단 ui 버튼 클릭 시 다른 버튼 비활성화 함수 =========================================================================================

    def change(self, get):
        if get == '1':
            for i in range(5):
                getattr(self, f'Status{i + 1}_Action1_Attack').setEnabled(True)
                getattr(self, f'Status{i + 1}_Action2_Skill').setDisabled(True)
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

    # 공격 버튼 시 몬스터 버튼 활성화 =========================================================================================

    def Attack_btn(self):
        for mon in range(10):
            getattr(self, f'Monster_{mon + 1}_QButton').setEnabled(True)

    # 스킬 버튼 시 캐릭터명에 맞는 스킬 창 활성화 ===============================================================================
    # 스킬번호 받아서 스킬창 활성화/비활성화 하는 함수
    def skill_btn(self, index_):
        self.Widget_Skill.show()
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
                frame.setEnabled(True) # 해당 스킬 프레임만 활성화
            else:
                frame.setEnabled(False) # 그 이외는 비활성화
        self.Attack_btn()
        print('skill')

    # 아이템 버튼 시 인벤토리 활성화 ==========================================================================================

    def Item_btn(self):
        self.Btn_Portion.setEnabled(True)       # 소비 아이템 버튼 활성화

        self.Btn_Portion.setStyleSheet('border: 5px solid qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955, '
                                       'stop:0 rgba(10, 242, 251, 255), stop:1 rgba(224, 6, 159, 255));')
        # 소비 아이템으로 페이지 옮김
        self.StackWidget_Item.setCurrentWidget(self.Page_Use)

        # 소비 아이템 버튼들 활성화
        for btn in range(11):
            getattr(self, f'Portion_{btn + 1}_Btn').setEnabled(True)

        # 삭제 가능
        self.Attack_btn()  # 도망을 눌러도 우선 턴을 넘길 수 있도록 넣어둔 것
        print('Item')

    def Run_btn(self):
        self.run_random = random.randint(1,10)

        if self.run_random < 4:
                self.Log_textEdit.append('적에게 쫄아서 숨었습니다.')
        else:
            self.Log_textEdit.append('적이 무서워 도망가다 넘어졌습니다.')

        # 삭제 가능
        self.Attack_btn()   # 도망을 눌러도 우선 턴을 넘길 수 있도록 넣어둔 것
        print('Run')

    # 턴 변경 시 함수 =====================================================================================================

    def user_Turn(self):    # 몬스터 공격 버튼 눌렀을 때 함수
        self.user_turn += 1

        if self.user_turn >= len(self.frame_class_list):    #6번 돌리면 초기화 해줌 if self.user_turn >= 6:
            self.user_turn = 0

        for idx, FCS in enumerate(self.frame_class_list):   # 턴에 따른 버튼 활성화
            if self.user_turn == idx:
                FCS.setEnabled(True)
                # print('유저 활성화')
                for btn in range(5):    # 턴 변경에 따른 하단 ui 버튼 모두 활성화
                    getattr(self, f'Status{btn + 1}_Action1_Attack').setEnabled(True)
                    getattr(self, f'Status{btn + 1}_Action1_Attack').setStyleSheet('')  # 버튼 스타일 디폴트로 다시 변경
                    getattr(self, f'Status{btn + 1}_Action2_Skill').setEnabled(True)
                    getattr(self, f'Status{btn + 1}_Action2_Skill').setStyleSheet('')
                    getattr(self, f'Status{btn + 1}_Action3_Item').setEnabled(True)
                    getattr(self, f'Status{btn + 1}_Action3_Item').setStyleSheet('')
                    getattr(self, f'Status{btn + 1}_Action4_Run').setEnabled(True)
                    getattr(self, f'Status{btn + 1}_Action4_Run').setStyleSheet('')
                    self.btn_clicked = -1
            else:
                FCS.setEnabled(False)
                # print('유저 비활성화')

            self.mon_Turn()
            self.portion_reset()

    # 몬스터 버튼 비활성화
    def mon_Turn(self):
        for mon in range(10):   #몬스터 버튼 비활성화
            getattr(self, f'Monster_{mon + 1}_QButton').setEnabled(False)

        self.skill_hide()

    # 스킬창 숨김
    def skill_hide(self):
        self.Widget_Skill.hide()    # 스킬창 숨김

    # 턴 변경에 따른 소비 아이템 인벤토리 버튼 초기화
    def portion_reset(self):
        self.Btn_Portion.setStyleSheet('')
        self.Btn_Portion.setEnabled(False)
        for btn in range(11):
            getattr(self, f'Portion_{btn + 1}_Btn').setEnabled(False)




class MainGame(QMainWindow, maingame):
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = MainGame()
        ex.show()
        app.exec_()