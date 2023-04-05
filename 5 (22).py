import sys

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QFont


class Cell:

    def __init__(self, color):
        self.__color = color

    def change_color(self):
        if self.__color == "white":
            self.__color = "black"
        else:
            self.__color = "white"

    @property
    def color(self):
        return self.__color


class Field:

    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__cells = []

        for i in range(height):
            self.__cells.append([])
            for j in range(width):
                self.__cells[i].append(Cell("white"))

    def set_new_cells(self, new_cells):
        if len(new_cells) != self.__height:
            raise Exception("Неверный формат массива")

        for arr in new_cells:
            if len(arr) != self.__width:
                raise Exception("Неверный формат массива")

        self.__cells = new_cells

    def change_cell_color(self, i, j):
        self.__cells[i][j].change_color()

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def cells(self):
        return self.__cells.copy()


class Game:
    __WIDTH = 5
    __HEIGHT = 5

    def __init__(self):
        self.__field = Field(self.__WIDTH, self.__HEIGHT)

    def trigger_cell(self, i, j):
        for k in range(-1, 2):
            for h in range(-1, 2):
                if k == 0 or h == 0:
                    if 0 <= i + k < self.__field.height and 0 <= j + h < self.__field.width:
                        self.__field.change_cell_color(i + k, j + h)

    # def get_colors(self):
    #     colors = []
    #     for arr in self.field.get_cells():
    #         colors.append([cell.get_color() for cell in arr])
    #     return colors

    def get_color_of_cell(self, i, j):
        return self.__field.cells[i][j].color

    @property
    def width(self):
        return self.__WIDTH

    @property
    def height(self):
        return self.__HEIGHT


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__game_window = None
        self.__settings_window = None
        self.__rules_window = None

        self.__color_off = "black"
        self.__color_on = "white"
        self.__width = "500"
        self.__height = "500"

        self.init_ui()

    def init_ui(self):
        name_label = QLabel('Выключить свет!', self)
        font = QFont()
        font.setPointSize(18)
        name_label.setFont(font)
        name_label.setMaximumWidth(250)
        name_label.setMaximumHeight(20)

        play_button = QPushButton('Играть', self)
        play_button.setFixedWidth(200)
        play_button.clicked.connect(self.play_clicked)

        settings_button = QPushButton('Настройки', self)
        settings_button.setFixedWidth(200)
        settings_button.clicked.connect(self.settings_clicked)

        rules_button = QPushButton('Правила', self)
        rules_button.setFixedWidth(200)
        rules_button.clicked.connect(self.rules_clicked)

        layout = QVBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(play_button)
        layout.addWidget(settings_button)
        layout.addWidget(rules_button)
        self.setLayout(layout)

        self.setWindowTitle('Выключить свет!')
        self.setFixedSize(225, 200)

    def play_clicked(self):
        self.__game_window = GameWindow(self.__color_off, self.__color_on, int(self.__width), int(self.__height))
        self.__game_window.show()

    def settings_clicked(self):
        self.__settings_window = SettingsWindow()
        self.__settings_window.show()

        tpl = self.__settings_window.get_info()
        if tpl is not None:
            self.__color_off = tpl[0]
            self.__color_on = tpl[1]
            self.__width = tpl[2]
            self.__height = tpl[3]

    def rules_clicked(self):
        self.__rules_window = RulesWindow()
        self.__rules_window.show()


class GameWindow(QWidget):
    def __init__(self, color_off='black', color_on='white', width=500, height=500):
        super().__init__()

        self.__color_off = color_off
        self.__color_on = color_on
        self.__width = width
        self.__height = height

        self.__game = Game()

        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(self.__width)
        self.setFixedHeight(self.__height)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor('green'))

        cell_width = int(self.__width / self.__game.width)
        cell_height = int(self.__height / self.__game.height)

        self.__game.trigger_cell(0, 0)
        for i in range(self.__game.height):
            for j in range(self.__game.width):
                if self.__game.get_color_of_cell(i, j) == 'white':
                    color = self.__color_on
                else:
                    color = self.__color_off

                painter.fillRect(cell_width * j, cell_height * i, cell_width, cell_height, QColor(color))
                painter.fillRect(0, 0, 10, 10, QColor('black'))
                painter.drawRect(cell_width * j, cell_height * i, cell_width, cell_height)


        painter.end()


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.__color_off = ""
        self.__color_on = ""
        self.__width = ""
        self.__height = ""
        self.__button_pressed = False
        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(400)
        self.setFixedHeight(200)
        self.setWindowTitle("Настройки")

        horizontal_layout = QHBoxLayout(self)
        horizontal_layout.setContentsMargins(5, 5, 5, 5)
        horizontal_layout.setSpacing(10)

        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(10)

        label_color_off = QLabel("Цвет \"выкл.\"", self)
        label_color_on = QLabel("Цвет \"вкл.\"", self)
        label_width = QLabel("Ширина", self)
        label_height = QLabel("Высота", self)

        vertical_layout.addWidget(label_color_off)
        vertical_layout.addWidget(label_color_on)
        vertical_layout.addWidget(label_width)
        vertical_layout.addWidget(label_height)
        vertical_layout.addWidget(QLabel(""))
        horizontal_layout.addLayout(vertical_layout)

        vertical_layout_2 = QVBoxLayout(self)

        self.__input_color_off = QLineEdit(self)
        self.__input_color_on = QLineEdit(self)
        self.__input_width = QLineEdit(self)
        self.__input_height = QLineEdit(self)

        vertical_layout_2.addWidget(self.__input_color_off)
        vertical_layout_2.addWidget(self.__input_color_on)
        vertical_layout_2.addWidget(self.__input_width)
        vertical_layout_2.addWidget(self.__input_height)

        save_button = QPushButton('Сохранить', self)
        save_button.setGeometry(160, 260, 75, 23)
        save_button.clicked.connect(self.save_button_clicked)

        vertical_layout_2.addWidget(save_button)
        horizontal_layout.addLayout(vertical_layout_2)

    def save_button_clicked(self):
        self.__color_off = self.__input_color_off.text()
        self.__color_on = self.__input_color_on.text()
        self.__width = self.__input_width.text()
        self.__height = self.__input_height.text()
        self.__button_pressed = True

    def get_info(self):
        if self.__button_pressed:
            tpl = (self.__color_off, self.__color_on, self.__width, self.__height)
            self.__button_pressed = False
            return tpl
        else:
            return None


class RulesWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        with open('rules.txt', encoding='UTF-8') as f:
            text = f.read()

        label = QLabel(text, self)
        font = QFont()
        font.setPointSize(16)
        label.setFont(font)

        v_layout = QVBoxLayout(self)
        v_layout.addWidget(label)

        self.setWindowTitle('Правила')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
