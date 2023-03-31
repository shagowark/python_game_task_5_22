import tkinter as tk
from tkinter import filedialog
import random


# Класс для отрисовки клеток игрового поля
class Cell:
    def __init__(self, canvas, x, y, size, color="black"):
        self.canvas = canvas
        self.color = color
        self.rect = canvas.create_rectangle(x, y, x + size, y + size, fill=color)

    # Инверсия цвета клетки
    def invert(self):
        self.color = "white" if self.color == "black" else "black"
        self.canvas.itemconfig(self.rect, fill=self.color)


# Класс для отрисовки игрового поля
class LightsOut:
    def __init__(self, root):
        self.root = root
        self.cells = []
        self.width = 5
        self.height = 5
        self.cell_size = 50
        self.create_board()

    # Создание игрового поля
    def create_board(self):
        canvas = tk.Canvas(self.root, width=self.width * self.cell_size, height=self.height * self.cell_size)
        canvas.pack()
        for i in range(self.height):
            row = []
            for j in range(self.width):
                cell = Cell(canvas, j * self.cell_size, i * self.cell_size, self.cell_size)
                row.append(cell)
            self.cells.append(row)
        self.load_board("board.txt")

    # Загрузка игрового поля из txt файла
    def load_board(self, filename):
        try:
            with open(filename, "r") as f:
                data = f.read().strip().split("\n")
                for i in range(len(data)):
                    for j in range(len(data[i])):
                        if data[i][j] == "1":
                            self.switch(i, j)
        except FileNotFoundError:
            print("Файл не найден")

    # Смена цвета клеток
    def switch(self, i, j):
        self.cells[i][j].invert()
        if i > 0:
            self.cells[i - 1][j].invert()
        if i < self.height - 1:
            self.cells[i + 1][j].invert()
        if j > 0:
            self.cells[i][j - 1].invert()
        if j < self.width - 1:
            self.cells[i][j + 1].invert()


# Создание окна и запуск игры
def choose_level():
    filename = filedialog.askopenfilename()
    if filename:
        game.load_board(filename)


root = tk.Tk()
root.title("Выключи свет")
game = LightsOut(root)

# Создание кнопки "Выбрать уровень"
level_button = tk.Button(root, text="Выбрать уровень", command=choose_level)
level_button.pack()

root.mainloop()