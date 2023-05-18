wall_list = {
    1: [(899, 908, 131, 338), #던전 맵 1
        (522, 638, 412, 420),
        (660, 680, 490, 700),
        (829, 1091, 488, 496),],
    2: [(800, 820, 117, 341), #던전 맵 2
        (509, 962, 486, 500)],
}

for key, value in wall_list.items():
    for i in value:

        if i[0] < new_position.x() < i[1] and i[2] < new_position.y() < i[3]:
            self.Character_QLabel_2.setGeometry(previous_position)

# if self.dungeon_number == 1:  # 15*15 사이즈 맵에 들어갔을 때
#     # 던전 벽을 벗어나지 못하게 함
#     if not ((self.map_size[1][0] <= new_position.x() <= self.map_size[1][1]) and (
#             self.map_size[1][2] < new_position.y() < self.map_size[1][3])):  # 미궁 x값, 미궁 y값 설정
#         self.Character_QLabel_2.setGeometry(previous_position)
#     # 던전 내에 위치한 벽을 벗어나지 못하게 함
#     for key, value in wall_dict.items():
#         if value[0][0] < new_position.x() < value[1] and value[2] < new_position.y() < value[3]:
#             self.Character_QLabel_2.setGeometry(previous_position)
#             break