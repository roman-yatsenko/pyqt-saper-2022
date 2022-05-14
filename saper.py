"""
Игра "Сапер" на PyQt5
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import random
import time

from numpy import outer

LEVELS = (
    (8, 10),
    (16, 40),
    (24, 99)
)

IMG_BOMB = QImage('./images/bomb.png')
IMG_CLOCK = QImage('./images/clock.png')
IMG_START = QImage('./images/rocket.png')


class Cell(QWidget):
    """
    Клетка игрового поля
    """

    def __init__(self, x, y, *args, **kwargs):
        """
        Конструктор клекти игровго поля
        """
        super().__init__(*args, **kwargs)
        self.setFixedSize(20, 20)

        self.x = x
        self.y = y

    def reset(self):
        """
        Сброс клетки
        """
        self.is_start = False
        self.is_mine = False
        self.mines_around = 0
        self.is_revealed = False
        self.is_flagged = 0
        self.is_end = False
        self.update()

    def paintEvent(self, event):
        """
        Событие перерисовки клетки
        """
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = event.rect()
        outer, inner = Qt.gray, Qt.lightGray
        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_revealed:
            if self.is_mine:
                p.drawPixmap(r, QPixmap(IMG_BOMB))
            elif self.is_start:
                p.drawPixmap(r, QPixmap(IMG_START))
            elif self.mines_around > 0:
                pen = QPen(Qt.black)
                p.setPen(pen)
                f = p.font()
                f.setBold(True)
                p.setFont(f)
                p.drawText(r, Qt.AlignCenter, str(self.mines_around))

    def click(self):
        """
        Обработка клика по клетке
        """
        if not self.is_revealed and not self.is_flagged:
            self.reveal()

    def reveal(self):
        """
        Открытие клетки
        """
        if not self.is_revealed:
            self.reveal_self()

    def reveal_self(self):
        """
        Открыть только эту клетку
        """
        self.is_revealed = True
        self.update()


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
        self.initUI()
        self.init_map()
        self.reset_map()

        self.setFixedSize(self.sizeHint())
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

    def init_map(self):
        """
        Инициализация игрового поля
        """
        for x in range(self.board_size):
            for y in range(self.board_size):
                w = Cell(x, y)
                self.grid.addWidget(w, x, y)

    def reset_map(self):
        self.n_mines = LEVELS[self.level][1]
        self.mines.setText(f'{self.n_mines:03d}')
        self.clock.setText('000')

        for _, _, cell in self.get_all_cells():
            cell.reset()

        self.set_mines()
        self.calc_mines()
        self.set_start()

    def get_all_cells(self):
        """
        Возвращает все клетки
        """
        for x in range(self.board_size):
            for y in range(self.board_size):
                yield (x, y, self.grid.itemAtPosition(x, y).widget())

    def set_mines(self):
        """
        Установка мин на игровое поле
        """
        positions = []
        while len(positions) < self.n_mines:
            x = random.randint(0, self.board_size - 1)
            y = random.randint(0, self.board_size - 1)
            if (x, y) not in positions:
                self.grid.itemAtPosition(x, y).widget().is_mine = True
                positions.append((x, y))
        
    def calc_mines(self):
        """
        Подсчет количества мин
        """
        for x, y, cell in self.get_all_cells():
            cell.mines_around = self.get_mines_around(x, y)

    def get_mines_around(self, x, y):
        """
        Подсчет количества мин вокруг клетки (x, y)
        """
        cells = [cell for _, _, cell in self.get_around_cells(x, y)]
        return sum(1 if cell.is_mine else 0 for cell in cells)

    def get_around_cells(self, x, y):
        """
        Получить список клеток вокруг клетки (x, y)
        """
        positions = []
        for xi in range(max(0, x-1), min(x+2, self.board_size)):
            for yi in range(max(0, y-1), min(y+2, self.board_size)):
                positions.append((xi, yi, self.grid.itemAtPosition(xi, yi).widget()))
        return positions

    def set_start(self):
        """
        Выбор начальной клетки
        """
        empty_cells = [cell
                       for x, y, cell
                       in self.get_all_cells()
                       if cell.mines_around == 0 and not cell.is_mine
                      ]
        start_cell = empty_cells[random.randint(0, len(empty_cells)-1)]
        start_cell.is_start = True

        for _, _, cell in self.get_around_cells(start_cell.x, start_cell.y):
            if not cell.is_mine:
                cell.click()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()
