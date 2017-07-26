# #! temp .py file to check some part of code

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QWidget, QGridLayout,
    QPushButton, QApplication)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.gui()

    def gui(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.test0 = []

        posmany = [(i, j) for i in range(4) for j in range(1)]
        for position in posmany:
            entry = QLineEdit()
            grid.addWidget(entry, *position)
            self.test0.append(entry)

        butt = QPushButton()
        grid.addWidget(butt, 5, 5)
        butt.clicked.connect(self.print0)

        self.move(300, 150)
        self.setWindowTitle('test')
        self.show()

    def print0(self):
        test20 = []
        for i in self.test0:
            test20.append(i)
        print(test20)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
