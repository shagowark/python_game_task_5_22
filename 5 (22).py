import sys

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QLineEdit, QMessageBox
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

    @color.setter
    def color(self, value):
        self.__color = value


class Field:

    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__cells = []

        for i in range(height):
            self.__cells.append([])
            for j in range(width):
                self.__cells[i].append(Cell("black"))

    def set_new_cells(self, new_cells):
        if len(new_cells) != self.__height:
            raise Exception("Неверный формат массива")

        for arr in new_cells:
            if len(arr) != self.__width:
                raise Exception("Неверный формат массива")

        for i in range(len(new_cells)):
            for j in range(len(new_cells[0])):
                x = new_cells[i][j]
                if x == 1:
                    self.__cells[i][j].color = 'white'
                else:
                    self.__cells[i][j].color = 'black'

    def change_cell_color(self, i, j):
        self.__cells[i][j].change_color()

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def get_cell_color(self, i, j):
        return self.__cells[i][j].color


class Game:
    __WIDTH = 5
    __HEIGHT = 5

    def __init__(self):
        self.__field = Field(self.__WIDTH, self.__HEIGHT)
        self.__game_ended = False

    def trigger_cell(self, i, j):
        for k in range(-1, 2):
            for h in range(-1, 2):
                if k == 0 or h == 0:
                    if 0 <= i + k < self.__field.height and 0 <= j + h < self.__field.width:
                        self.__field.change_cell_color(i + k, j + h)
        self.check_end()

    def check_end(self):
        win = True
        for i in range(self.__WIDTH):
            for j in range(self.__HEIGHT):
                if self.get_color_of_cell(i, j) == 'white':
                    win = False
                    break
        self.__game_ended = win

    def get_color_of_cell(self, i, j):
        return self.__field.get_cell_color(i, j)

    @property
    def width(self):
        return self.__WIDTH

    @property
    def height(self):
        return self.__HEIGHT

    @property
    def game_ended(self):
        return self.__game_ended

    def set_field(self, value):
        self.__field.set_new_cells(value)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__game_window = GameWindow()
        self.__level_window = LevelWindow()
        self.__settings_window = SettingsWindow()
        self.__rules_window = RulesWindow()

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

        level_button = QPushButton('Выбрать уровень', self)
        level_button.setFixedWidth(200)
        level_button.clicked.connect(self.level_clicked)

        settings_button = QPushButton('Настройки', self)
        settings_button.setFixedWidth(200)
        settings_button.clicked.connect(self.settings_clicked)

        rules_button = QPushButton('Правила', self)
        rules_button.setFixedWidth(200)
        rules_button.clicked.connect(self.rules_clicked)

        layout = QVBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(play_button)
        layout.addWidget(level_button)
        layout.addWidget(settings_button)
        layout.addWidget(rules_button)
        self.setLayout(layout)

        self.setWindowTitle('Выключить свет!')
        self.setFixedSize(225, 200)

    def play_clicked(self):
        tpl = self.__settings_window.get_info()
        if tpl is not None:
            if tpl[0] != "":
                self.__game_window.color_off = tpl[0]
            if tpl[1] != "":
                self.__game_window.color_on = tpl[1]
            if tpl[2] != "":
                self.__game_window.width = int(tpl[2])
            if tpl[3] != "":
                self.__game_window.height = int(tpl[3])

        lvl = self.__level_window.get_level()
        if lvl is None:
            self.show_no_lvl_err_msg()
        else:
            self.__game_window.set_lvl(lvl)
            self.__game_window.init_ui()
            self.__game_window.show()

    @staticmethod
    def show_no_lvl_err_msg():
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText("Выберите уровень!")
        msg.exec_()

    def level_clicked(self):
        self.__level_window.show()

    def settings_clicked(self):
        self.__settings_window.show()

    def rules_clicked(self):
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
        self.setWindowTitle("Выключить свет!")

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.draw_cells(painter)
        painter.end()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        i = int(y / self.__height // 0.2)
        j = int(x / self.__width // 0.2)
        self.__game.trigger_cell(i, j)
        self.update()
        if self.__game.game_ended:
            self.show_win_message()
            self.close()

    @staticmethod
    def show_win_message():
        msg = QMessageBox()
        msg.setWindowTitle("Ура!")
        msg.setText("Ура победа!!!!")
        msg.exec_()

    def draw_cells(self, painter):
        painter.setPen(QColor('green'))

        cell_width = int(self.__width / self.__game.width)
        cell_height = int(self.__height / self.__game.height)

        for i in range(self.__game.height):
            for j in range(self.__game.width):
                if self.__game.get_color_of_cell(i, j) == 'white':
                    color = self.__color_on
                else:
                    color = self.__color_off

                painter.fillRect(cell_width * j, cell_height * i, cell_width, cell_height, QColor(color))
                painter.drawRect(cell_width * j, cell_height * i, cell_width, cell_height)

    @property
    def color_off(self):
        return self.__color_off

    @color_off.setter
    def color_off(self, value):
        self.__color_off = value

    @property
    def color_on(self):
        return self.__color_on

    @color_on.setter
    def color_on(self, value):
        self.__color_on = value

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        self.__height = value

    def set_lvl(self, value):
        self.__game.set_field(value)


class LevelWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__lvl = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        lvl_1_button = QPushButton("Уровень 1")
        lvl_1_button.clicked.connect(self.lvl_1_clicked)
        layout.addWidget(lvl_1_button)

        lvl_2_button = QPushButton("Уровень 2")
        lvl_2_button.clicked.connect(self.lvl_2_clicked)
        layout.addWidget(lvl_2_button)

        lvl_3_button = QPushButton("Уровень 3")
        lvl_3_button.clicked.connect(self.lvl_3_clicked)
        layout.addWidget(lvl_3_button)

        self.setLayout(layout)

        self.setGeometry(100, 100, 200, 150)
        self.setWindowTitle("Уровни")

    def lvl_1_clicked(self):
        with open('level_01.txt', 'r') as f:
            temp = f.readlines()

        self.__lvl = [[int(x) for x in line.split()] for line in temp]
        self.close()

    def lvl_2_clicked(self):
        with open('level_02.txt', 'r') as f:
            temp = f.readlines()

        self.__lvl = [[int(x) for x in line.split()] for line in temp]
        self.close()

    def lvl_3_clicked(self):
        with open('level_03.txt', 'r') as f:
            temp = f.readlines()

        self.__lvl = [[int(x) for x in line.split()] for line in temp]
        self.close()

    def get_level(self):
        return self.__lvl


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.__input_color_off = QLineEdit(self)
        self.__input_color_on = QLineEdit(self)
        self.__input_width = QLineEdit(self)
        self.__input_height = QLineEdit(self)

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

        self.__input_color_off.setText(self.__color_off)
        self.__input_color_on.setText(self.__color_on)
        self.__input_width.setText(self.__width)
        self.__input_height.setText(self.__height)

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
        self.close()

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
