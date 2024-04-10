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
        self.board = [[EMPTY] * 3 for _ in range(3)]
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
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.master, text="", font=('Arial', 30), width=5, height=2,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def create_statistics_labels(self):
        self.label_player_x = tk.Label(self.master, text=f"Player X Wins: {self.player_x_wins}")
        self.label_player_x.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        self.label_player_o = tk.Label(self.master, text=f"Player O Wins: {self.player_o_wins}")
        self.label_player_o.grid(row=4, column=0, columnspan=3)
        self.label_ties = tk.Label(self.master, text=f"Ties: {self.ties}")
        self.label_ties.grid(row=5, column=0, columnspan=3)

    def update_statistics_labels(self):
        self.label_player_x.config(text=f"Player X Wins: {self.player_x_wins}")
        self.label_player_o.config(text=f"Player O Wins: {self.player_o_wins}")
        self.label_ties.config(text=f"Ties: {self.ties}")

    def create_reset_button(self):
        reset_button = tk.Button(self.master, text="Reset Board", command=self.reset_board)
        reset_button.grid(row=6, column=0, columnspan=3, pady=(10, 0))

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = EMPTY
                self.buttons[i][j].config(text="")
        self.current_player = PLAYER_X
        if self.current_player == PLAYER_O:
            self.ai_move()

    def on_button_click(self, row, col):
        if self.board[row][col] == EMPTY:
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
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
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    self.board[i][j] = PLAYER_O
                    score = self.minimax(5, False)  # Adjust depth as needed
                    self.board[i][j] = EMPTY
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        row, col = best_move
        self.board[row][col] = PLAYER_O
        self.buttons[row][col].config(text=PLAYER_O)
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

    def minimax(self, depth, is_maximizing):
        result = self.evaluate()
        if result != 0:
            return result * depth  # Incorporate depth for better performance

        if is_maximizing:
            max_eval = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == EMPTY:
                        self.board[i][j] = PLAYER_X
                        eval = self.minimax(depth - 1, False)
                        self.board[i][j] = EMPTY
                        max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == EMPTY:
                        self.board[i][j] = PLAYER_O
                        eval = self.minimax(depth - 1, True)
                        self.board[i][j] = EMPTY
                        min_eval = min(min_eval, eval)
            return min_eval

    def evaluate(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != EMPTY:
                if self.board[i][0] == PLAYER_X:
                    return 1
                else:
                    return -1
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != EMPTY:
                if self.board[0][i] == PLAYER_X:
                    return 1
                else:
                    return -1
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != EMPTY:
            if self.board[0][0] == PLAYER_X:
                return 1
            else:
                return -1
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != EMPTY:
            if self.board[0][2] == PLAYER_X:
                return 1
            else:
                return -1
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    return 0  # Game is not over yet, return 0 for tie
        return 0  # Game is a tie

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != EMPTY:
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != EMPTY:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != EMPTY:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != EMPTY:
            return True
        return False

    def check_draw(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    return False
        return True

def main():
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
