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

IMG_BOMB = QImage('./images/bomb.png')
IMG_CLOCK = QImage('./images/clock.png')


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

        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_BOMB))
        l.setAlignment(Qt.AlignCenter)
        hb.addWidget(l)

        hb.addWidget(self.mines)
        hb.addWidget(self.button)
        hb.addWidget(self.clock)

        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_CLOCK))
        l.setAlignment(Qt.AlignCenter)
        hb.addWidget(l)

        vb = QVBoxLayout()
        vb.addLayout(hb)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        vb.addLayout(self.grid)

        w.setLayout(vb)
        self.setCentralWidget(w)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()
