import tkinter as tk
from tkinter import messagebox

# Constants for representing the players and empty cells
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = " "

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board = [EMPTY] * 9
        self.current_player = PLAYER_X
        self.buttons = []
        self.player_x_wins = 0
        self.player_o_wins = 0
        self.ties = 0
        self.round_count = 1
        self.create_board()
        self.create_statistics_labels()
        self.create_round_label()
        self.create_reset_button()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.master, text="", font=('Arial', 30), width=5, height=2,
                                   command=lambda i=i, j=j: self.on_button_click(i, j))
                button.grid(row=i, column=j)
                self.buttons.append(button)

    def create_statistics_labels(self):
        self.label_player_x = tk.Label(self.master, text=f"Player X Wins: {self.player_x_wins}")
        self.label_player_x.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        self.label_player_o = tk.Label(self.master, text=f"Player O Wins: {self.player_o_wins}")
        self.label_player_o.grid(row=4, column=0, columnspan=3)
        self.label_ties = tk.Label(self.master, text=f"Ties: {self.ties}")
        self.label_ties.grid(row=5, column=0, columnspan=3)

    def create_round_label(self):
        self.label_round = tk.Label(self.master, text=f"Round {self.round_count}: Player {self.current_player} goes first")
        self.label_round.grid(row=6, column=0, columnspan=3, pady=(10, 0))

    def update_statistics_labels(self):
        self.label_player_x.config(text=f"Player X Wins: {self.player_x_wins}")
        self.label_player_o.config(text=f"Player O Wins: {self.player_o_wins}")
        self.label_ties.config(text=f"Ties: {self.ties}")

    def update_round_label(self):
        self.label_round.config(text=f"Round {self.round_count}: Player {self.current_player} goes first")

    def on_button_click(self, row, col):
        index = 3 * row + col
        if self.board[index] == EMPTY:
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Winner", f"Player {self.current_player} wins!")
                if self.current_player == PLAYER_X:
                    self.player_x_wins += 1
                else:
                    self.player_o_wins += 1
                self.update_statistics_labels()
                self.reset_board()
                return
            elif self.check_draw():
                messagebox.showinfo("Draw", "It's a draw!")
                self.ties += 1
                self.update_statistics_labels()
                self.reset_round()
                return
            self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
            self.update_round_label()

    def check_winner(self):
        win_patterns = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                        [0, 3, 6], [1, 4, 7], [2, 5, 8],
                        [0, 4, 8], [2, 4, 6]]

        for pattern in win_patterns:
            if self.board[pattern[0]] == self.board[pattern[1]] == self.board[pattern[2]] != EMPTY:
                return True
        return False

    def check_draw(self):
        return all(cell != EMPTY for cell in self.board) and not self.check_winner()

    def create_reset_button(self):
        reset_button = tk.Button(self.master, text="Reset Game", command=self.reset_round)
        reset_button.grid(row=7, column=0, columnspan=3, pady=(10, 0))

    def reset_board(self):
        for i in range(9):
            self.board[i] = EMPTY
            self.buttons[i].config(text="")
        self.round_count += 1
        self.current_player = PLAYER_X if self.round_count % 2 == 1 else PLAYER_O
        self.update_round_label()

    def reset_round(self):
        for i in range(9):
            self.board[i] = EMPTY
            self.buttons[i].config(text="")
        self.current_player = PLAYER_X if self.round_count % 2 == 1 else PLAYER_O
        self.update_round_label()

def main():
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
