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
        self.create_board()
        self.create_statistics_labels()
        self.create_reset_button()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.master, text="", font=('Arial', 30), width=5, height=2,
                                   command=lambda i=i, j=j: self.on_button_click(i, j))
                button.grid(row=i, column=j)
                self.buttons.append(button)

    def create_statistics_labels(self):
        label_player_x = tk.Label(self.master, text=f"Player X Wins: {self.player_x_wins}")
        label_player_x.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        label_player_o = tk.Label(self.master, text=f"Player O Wins: {self.player_o_wins}")
        label_player_o.grid(row=4, column=0, columnspan=3)
        label_ties = tk.Label(self.master, text=f"Ties: {self.ties}")
        label_ties.grid(row=5, column=0, columnspan=3)

    def update_statistics_labels(self):
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()
        self.create_statistics_labels()

    def create_reset_button(self):
        reset_button = tk.Button(self.master, text="Reset Board", command=self.reset_board)
        reset_button.grid(row=6, column=0, columnspan=3, pady=(10, 0))

    def reset_board(self):
        for i in range(9):
            self.board[i] = EMPTY
            self.buttons[i].config(text="")
        self.current_player = PLAYER_X
        if self.current_player == PLAYER_O:
            self.ai_move()

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
                self.reset_board()
                return
            self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
            if self.current_player == PLAYER_O:
                self.ai_move()

    def ai_move(self):
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if self.board[i] == EMPTY:
                self.board[i] = PLAYER_O
                score = self.minimax(self.board, 0, False)
                self.board[i] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = i
        self.board[best_move] = PLAYER_O
        self.buttons[best_move].config(text=PLAYER_O)
        if self.check_winner():
            messagebox.showinfo("Winner", f"Player {PLAYER_O} wins!")
            self.player_o_wins += 1
            self.update_statistics_labels()
            self.reset_board()
        elif self.check_draw():
            messagebox.showinfo("Draw", "It's a draw!")
            self.ties += 1
            self.update_statistics_labels()
            self.reset_board()
        else:
            self.current_player = PLAYER_X

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner():
            return -1 if is_maximizing else 1
        elif self.check_draw():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == EMPTY:
                    board[i] = PLAYER_O
                    score = self.minimax(board, depth + 1, False)
                    board[i] = EMPTY
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == EMPTY:
                    board[i] = PLAYER_X
                    score = self.minimax(board, depth + 1, True)
                    board[i] = EMPTY
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self):
        win_patterns = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                        [0, 3, 6], [1, 4, 7], [2, 5, 8],
                        [0, 4, 8], [2, 4, 6]]

        for pattern in win_patterns:
            if self.board[pattern[0]] == self.board[pattern[1]] == self.board[pattern[2]] != EMPTY:
                return True
        return False

    def check_draw(self):
        return all(cell != EMPTY for cell in self.board)

def main():
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
