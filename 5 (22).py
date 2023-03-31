import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QColor


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
        self.field = Field(self.__WIDTH, self.__HEIGHT)

    def trigger_cell(self, i, j):
        for k in range(-1, 2):
            for h in range(-1, 2):
                if k == 0 or h == 0:
                    if 0 <= i + k < self.field.height and 0 <= j + h < self.field.width:
                        self.field.change_cell_color(i + k, j + h)

    # def get_colors(self):
    #     colors = []
    #     for arr in self.field.get_cells():
    #         colors.append([cell.get_color() for cell in arr])
    #     return colors

    def get_color_of_cell(self, i, j):
        return self.field.cells[i][j].color

    @property
    def width(self):
        return self.__WIDTH

    @property
    def height(self):
        return self.__HEIGHT





class WindowApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Задаем размеры окна и заголовок
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle("Выключить свет!")

        # Создаем виджет и размещаем его на главном окне
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Создаем вертикальный и горизонтальный слои
        self.vertical_layout = QVBoxLayout()
        self.horizontal_layout = QHBoxLayout()

        # Создаем кнопку "Начать игру"
        self.start_button = QPushButton("Начать игру")
        self.start_button.clicked.connect(self.start_game)

        # Добавляем кнопку в горизонтальный слой
        self.horizontal_layout.addWidget(self.start_button)

        # Добавляем горизонтальный слой в вертикальный
        self.vertical_layout.addLayout(self.horizontal_layout)

        # Устанавливаем вертикальный слой в качестве основного
        self.central_widget.setLayout(self.vertical_layout)

    def start_game(self):
        # Удаляем содержимое вертикального слоя
        for i in reversed(range(self.vertical_layout.count())):
            self.vertical_layout.itemAt(i).widget().setParent(None)

        # Задаем параметры игры
        game = Game()
        cell_size = 50

        # Создаем виджет для отрисовки игрового поля
        canvas = GameCanvas(game, cell_size)

        # Добавляем виджет в вертикальный слой
        self.vertical_layout.addWidget(canvas)

        # Обновляем виджет
        canvas.update()


class GameCanvas(QWidget):
    def __init__(self, game, cell_size):
        super().__init__()

        # Сохраняем параметры игры и размер клетки
        self.game = game
        self.cell_size = cell_size

        # Задаем размеры виджета
        self.setFixedSize(self.game.width * self.cell_size, self.game.height * self.cell_size)

    def paintEvent(self, event):
        # Создаем объект QPainter для рисования
        painter = QPainter(self)

        # Отрисовываем каждую клетку
        for i in range(self.game.height):
            for j in range(self.game):
                color = self.game.get_color_of_cell(i, j)
                painter.fillRect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size, QColor(*color))

                # Рисуем контур клетки
                painter.setPen(QColor(255, 255, 255))
                painter.drawRect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)


if __name__ == '__main__':
    t = {1: 1, 2: 2, 3: 3, '4': 2}
    print(t['4'])
    # app = QApplication(sys.argv)
    # window = WindowApp()
    # window.show()
    # sys.exit(app.exec_())
