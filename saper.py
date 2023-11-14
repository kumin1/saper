import tkinter as tk
from tkinter import messagebox
import random

class Saper:
    def __init__(self, master, rows, cols, mines):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flags = [[False for _ in range(cols)] for _ in range(rows)]

        self.timer_running = False
        self.time = 0

        self.create_board()
        self.place_mines()
        self.calculate_numbers()

        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]

        self.create_menu()
        self.create_buttons()
        self.create_timer()

    def create_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        game_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='gra', menu=game_menu)
        game_menu.add_command(label='nowa gra', command=self.new_game)
        game_menu.add_separator()
        game_menu.add_command(label='wyjdz', command=self.master.destroy)

    def create_board(self):
        for i in range(self.mines):
            row, col = divmod(i, self.cols)
            self.board[row][col] = 'M'

    def place_mines(self):
        flat_board = [cell for row in self.board for cell in row]
        random.shuffle(flat_board)
        self.board = [flat_board[i:i + self.cols] for i in range(0, len(flat_board), self.cols)]

    def calculate_numbers(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 'M':
                    self.increment_numbers(i - 1, j - 1)
                    self.increment_numbers(i - 1, j)
                    self.increment_numbers(i - 1, j + 1)
                    self.increment_numbers(i, j - 1)
                    self.increment_numbers(i, j + 1)
                    self.increment_numbers(i + 1, j - 1)
                    self.increment_numbers(i + 1, j)
                    self.increment_numbers(i + 1, j + 1)

    def increment_numbers(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols and self.board[row][col] != 'M':
            self.board[row][col] += 1

    def create_buttons(self):
        for i in range(self.rows):
            for j in range(self.cols):
                btn = tk.Button(self.master, width=2, height=1, relief=tk.RAISED, command=lambda i=i, j=j: self.click(i, j))
                btn.grid(row=i, column=j)
                btn.bind('<Button-3>', lambda event, i=i, j=j: self.right_click(event, i, j))
                self.buttons[i][j] = btn

    def create_timer(self):
        self.timer_label = tk.Label(self.master, text="Czas: 0")
        self.timer_label.grid(row=self.rows, columnspan=self.cols)

    def update_timer(self):
        if self.timer_running:
            self.time += 1
            self.timer_label.config(text=f"Czas: {self.time}")
            self.master.after(1000, self.update_timer)

    def new_game(self):
        self.timer_running = False
        self.time = 0
        self.timer_label.config(text="Czas: 0")
        self.reset_board()

    def reset_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].config(text='', state=tk.NORMAL, relief=tk.RAISED)
                self.revealed[i][j] = False
                self.flags[i][j] = False

        self.create_board()
        self.place_mines()
        self.calculate_numbers()

    def click(self, row, col):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

        if not self.revealed[row][col] and not self.flags[row][col]:
            self.revealed[row][col] = True

            if self.board[row][col] == 'M':
                self.buttons[row][col].config(text='*', background='red', state='disabled')
                self.game_over()
            elif self.board[row][col] == 0:
                self.buttons[row][col].config(text='', state='disabled', relief=tk.SUNKEN)
                self.reveal_empty(row, col)
            else:
                self.buttons[row][col].config(text=self.board[row][col], state='disabled', relief=tk.SUNKEN)

    def reveal_empty(self, row, col):
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < self.rows and 0 <= j < self.cols and not self.revealed[i][j]:
                    self.click(i, j)

    def right_click(self, event, row, col):
        if not self.revealed[row][col]:
            if not self.flags[row][col]:
                self.buttons[row][col].config(text='F', relief=tk.RAISED, background='red')
                self.flags[row][col] = True
            else:
                self.buttons[row][col].config(text='', relief=tk.RAISED, background='SystemButtonFace')
                self.flags[row][col] = False

    def game_over(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 'M':
                    self.buttons[i][j].config(text='M', state='disabled', background='SystemButtonFace')

        messagebox.showinfo('Przegrales','klikneles mine')


def main():
    root = tk.Tk()
    root.title('Saper')

    rows = 8
    cols = 8
    mines = 10

    saper = Saper(root, rows, cols, mines)

    root.mainloop()


if __name__ == '__main__':
    main()
