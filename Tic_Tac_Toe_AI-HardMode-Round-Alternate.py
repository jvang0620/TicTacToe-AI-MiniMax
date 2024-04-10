import tkinter as tk
from tkinter import messagebox

# Initialize the empty board
board = [
    ['_', '_', '_'],
    ['_', '_', '_'],
    ['_', '_', '_']
]

# Initialize counts
user_wins = 0
computer_wins = 0
ties = 0

# Variable to keep track of current player (0 for human, 1 for computer)
current_player = 0

# Function to print the current board
def print_board():
    for row in board:
        print(' '.join(row))
    print()

# Function to check if the game is over
def is_game_over():
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '_':
            return True
        if board[0][i] == board[1][i] == board[2][i] != '_':
            return True
    if board[0][0] == board[1][1] == board[2][2] != '_':
        return True
    if board[0][2] == board[1][1] == board[2][0] != '_':
        return True
    
    # Check for a tie
    if all(cell != '_' for row in board for cell in row):
        return True
    
    return False

# Function to evaluate the current board
def evaluate():
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == 'X':
            return 1
        if board[0][i] == board[1][i] == board[2][i] == 'X':
            return 1
        if board[i][0] == board[i][1] == board[i][2] == 'O':
            return -1
        if board[0][i] == board[1][i] == board[2][i] == 'O':
            return -1
    if board[0][0] == board[1][1] == board[2][2] == 'X':
        return 1
    if board[0][2] == board[1][1] == board[2][0] == 'X':
        return 1
    if board[0][0] == board[1][1] == board[2][2] == 'O':
        return -1
    if board[0][2] == board[1][1] == board[2][0] == 'O':
        return -1
    
    return 0  # Tie

# Minimax algorithm
def minimax(depth, is_maximizing):
    if is_game_over() or depth == 0:
        return evaluate()
    
    if is_maximizing:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'X'
                    eval = minimax(depth - 1, False)
                    board[i][j] = '_'
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'O'
                    eval = minimax(depth - 1, True)
                    board[i][j] = '_'
                    min_eval = min(min_eval, eval)
        return min_eval

# Function to make the best move using Minimax
def make_best_move():
    best_eval = float('-inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = 'X'
                eval = minimax(5, False)  # Depth set to 5 for demo purposes
                board[i][j] = '_'
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    board[best_move[0]][best_move[1]] = 'X'
    update_gui()

# Function to handle player's move
def player_move(row, col):
    global current_player
    if board[row][col] == '_':
        board[row][col] = 'O'
        update_gui()
        if not is_game_over():
            current_player = 1
            computer_move()
        else:
            end_game()
    else:
        messagebox.showinfo("Invalid Move", "That cell is already occupied. Try again.")

# Function to handle computer's move
def computer_move():
    make_best_move()
    if not is_game_over():
        current_player = 0
    else:
        end_game()

# Function to update GUI based on current board
def update_gui():
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                buttons[i][j].config(text='X', state='disabled')
            elif board[i][j] == 'O':
                buttons[i][j].config(text='O', state='disabled')
    if is_game_over():
        end_game()

# Function to display game result and ask for rematch
def end_game():
    global user_wins, computer_wins, ties
    result = evaluate()
    if result == 1:
        messagebox.showinfo("Game Over", "Sorry, you lose. Better luck next time!")
        user_wins += 1
    elif result == -1:
        messagebox.showinfo("Game Over", "Congratulations! You win!")
        computer_wins += 1
    else:
        messagebox.showinfo("Game Over", "It's a tie!")
        ties += 1
    update_counters()
    play_again = messagebox.askyesno("Play Again?", "Do you want to play again?")
    if play_again:
        reset_game()
    else:
        root.destroy()

# Function to update counters in GUI
def update_counters():
    user_wins_label.config(text=f"X Wins: {user_wins}")
    computer_wins_label.config(text=f"O Wins: {computer_wins}")
    ties_label.config(text=f"Ties: {ties}")

# Function to reset the game
def reset_game():
    global board, current_player
    board = [
        ['_', '_', '_'],
        ['_', '_', '_'],
        ['_', '_', '_']
    ]
    current_player = 0
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text='', state='active')

# Create GUI
root = tk.Tk()
root.title("Tic-Tac-Toe")

buttons = [[None]*3 for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text='', font=('Arial', 20), width=5, height=2,
                                   command=lambda row=i, col=j: player_move(row, col))
        buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

# Create counters
user_wins_label = tk.Label(root, text=f"X Wins: {user_wins}")
user_wins_label.grid(row=3, column=0, padx=5, pady=5)

computer_wins_label = tk.Label(root, text=f"O Wins: {computer_wins}")
computer_wins_label.grid(row=3, column=1, padx=5, pady=5)

ties_label = tk.Label(root, text=f"Ties: {ties}")
ties_label.grid(row=3, column=2, padx=5, pady=5)

# Start the game
reset_game()

root.mainloop()
