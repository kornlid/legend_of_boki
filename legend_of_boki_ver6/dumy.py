# import sys
# import random
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.Qt import *
#
# from maingame_2 import Ui_Maingame as maingame
#
#
# class MainGame(QMainWindow, maingame):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#
#         self.user_turn = 0
#         self.mon_turn = 0
#
#         # 캐릭터 별 프레임
#         self.frame_class_list = [self.Frame_Class1_Status, self.Frame_Class2_Status,
#                                  self.Frame_Class3_Status, self.Frame_Class4_Status, self.Frame_Class5_Status]
#         # MonsterImage 버튼
#         self.pushButton_list = [self.pushButton_1, self.pushButton_2, self.pushButton_3,
#                                 self.pushButton_4, self.pushButton_5, self.pushButton_6]
#         # MonsterImage 버튼 가져오기
#         self.Action_btn_set = self.MainFrame_Bottom.findChildren(QPushButton)
#         # 캐릭터 창 초기 [0] 빼고 비활성화 상태
#         for FCS in self.frame_class_list[1:]:
#             FCS.setEnabled(False)
#         # MonsterImage 초기 전체 비활성화 상태
#         for PB in self.pushButton_list:
#             PB.setEnabled(False)
#         # 공격 버튼 선택에 대한 시그널 연결
#         for Attack in range(5):
#             getattr(self, f'Status{Attack + 1}_Action1_Attack').clicked.connect(self.print_atk)
#             print(getattr(self, f'Status{Attack + 1}_Action1_Attack'))
#         # MonsterImage 버튼 선택에 대한 시그널 연결
#         for mon in self.pushButton_list:
#             mon.clicked.connect(self.Turn)
#
#     def print_atk(self):
#         self.Log_textEdit.append("공격")
#         for mon in self.pushButton_list:
#             mon.setEnabled(True)
#
#     def Turn(self):
#         self.user_turn += 1  # 유저 턴에 대한 초기 설정
#         self.mon_turn += 1
#
#         for mon in self.pushButton_list:
#             mon.setEnabled(True)
#
#         if self.user_turn >= len(self.frame_class_list):
#             self.user_turn = 0
#
#         for idx, FCS in enumerate(self.frame_class_list):
#             if self.user_turn == idx:
#                 FCS.setEnabled(True)
#                 print('유저 활성화')
#             else:
#                 FCS.setEnabled(False)
#                 print('유저 비활성화')
#         for mon in self.pushButton_list:
#             mon.setEnabled(False)
#
#     def mon_False(self):
#         self.mon_turn = 0
#
#         for i in range(6):
#             if self.mon_turn == 0:
#                 getattr(self, f'pushButton_{i + 1}').setEnabled(False)
#
#
# class MainGame(QMainWindow, maingame):
#     if __name__ == '__main__':
#         app = QApplication(sys.argv)
#         ex = MainGame()
#         ex.show()
#         app.exec_()

class num:
    def __init__(self):
        self.num_1 = 1
        self.num_2 = 2
        self.num_3 = 3
        self.num_4 = 4
        for i in range(1, 5):
            getattr(self, f'num_{i}')
num()