import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont, QFontDatabase

app = QApplication(sys.argv)

# TTF 파일을 추가합니다.
QFontDatabase.addApplicationFont('neodgm.ttf')

# QFont 객체를 만듭니다. 폰트 이름은 TTF 파일에서 확인할 수 있습니다.
font = QFont('Neo둥근모', 12)

# QLabel 위젯을 만듭니다.
label = QLabel('Hello, World!')
label.setFont(font)

label_ = QLabel('Hello, python!')





# QVBoxLayout을 만들고 label 위젯을 추가합니다.
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(label_)

# QWidget 위젯을 만들고 QVBoxLayout을 적용합니다.
widget = QWidget()
widget.setLayout(layout)
self.setStyleSheet(font)
widget.resize(250, 150)
widget.show()

sys.exit(app.exec_())
