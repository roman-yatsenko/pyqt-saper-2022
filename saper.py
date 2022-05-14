"""
Игра "Сапер" на PyQt5
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import random
import time

LEVELS = (
    (8, 10),
    (16, 40),
    (24, 99)
)


class MainWindow(QMainWindow):
    """
    Главное окно программы
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор главного окна
        """
        super().__init__(*args, **kwargs)

        self.level = 0
        self.board_size, self.n_mines = LEVELS[self.level]

        self.setWindowTitle('Сапер')
        self.setFixedSize(300, 300)
        self.initUI()
        self.show()

    def initUI(self):
        """
        Настройка пользовательского интерфейса
        """
        w = QWidget()
        hb = QHBoxLayout()

        self.mines = QLabel(str(self.n_mines))
        self.mines.setAlignment(Qt.AlignCenter)

        self.clock = QLabel('000')
        self.clock.setAlignment(Qt.AlignCenter)

        f = self.mines.font()
        f.setPointSize(24)
        f.setWeight(75)
        self.mines.setFont(f)
        self.clock.setFont(f)

        self.button = QPushButton()
        self.button.setFixedSize(32, 32)
        self.button.setIconSize(QSize(32, 32))
        self.button.setIcon(QIcon('./images/smiley.png'))
        self.button.setFlat(True)

        hb.addWidget(self.mines)
        hb.addWidget(self.button)
        hb.addWidget(self.clock)

        vb = QVBoxLayout()
        vb.addLayout(hb)

        w.setLayout(vb)
        self.setCentralWidget(w)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()
