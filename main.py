import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np

# Constants
BOARD_SIZE = 10
CELL_SIZE = 40
EMPTY, HUMAN, AI = 0, 1, 2
MAX_DEPTH = 2
MAX = AI
MIN = HUMAN

# Game State
board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = HUMAN
mode = None
human_name = "Human"
last_move = (-1, -1)

def load_images():
    global black_stone, white_stone
    try:
        black_stone = ImageTk.PhotoImage(Image.open("AI_Gomoku/black.png").resize((36, 36)))
        white_stone = ImageTk.PhotoImage(Image.open("AI_Gomoku/white.png").resize((36, 36)))
    except:
        black_stone = white_stone = None

def draw_stone(x, y, player):
    if player == HUMAN and black_stone:
        canvas.create_image(x, y, anchor=tk.CENTER, image=black_stone)
    elif player == AI and white_stone:
        canvas.create_image(x, y, anchor=tk.CENTER, image=white_stone)
    else:
        color = "black" if player == HUMAN else "white"
        canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill=color)

def click(event):
    global current_player, last_move
    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE

    if not is_valid_move(board, row, col):
        return

    board[row][col] = current_player
    last_move = (row, col)
    draw_stone(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2, current_player)

    if check_winner(current_player, row, col):
        messagebox.showinfo("Game Over", f"{human_name if current_player == HUMAN else 'AI'} wins!")
        canvas.unbind("<Button-1>")
        status_label.config(text="Game Over")
        return

    if is_board_full():
        messagebox.showinfo("Game Over", "It's a draw!")
        canvas.unbind("<Button-1>")
        status_label.config(text="Game Over")
        return

    current_player = AI if current_player == HUMAN else HUMAN
    if mode == "HumanvsAI" and current_player == AI:
        status_label.config(text="AI is thinking...")
        root.after(100, ai_turn)
    elif mode == "AIvsAI":
        root.after(500, ai_turn)

def ai_turn():
    global current_player, last_move
    move = ai_move()
    if move:
        r, c = move
        board[r][c] = current_player
        last_move = (r, c)
        draw_stone(c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2, current_player)

        if check_winner(current_player, r, c):
            messagebox.showinfo("Game Over", f"{'AI 1' if current_player == HUMAN else 'AI 2'} wins!")
            canvas.unbind("<Button-1>")
            status_label.config(text="Game Over")
            return

        if is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            status_label.config(text="Game Over")
            return

        current_player = HUMAN if current_player == AI else AI
        if mode == "AIvsAI":
            root.after(500, ai_turn)
        elif mode == "HumanvsAI":
            status_label.config(text="Your turn!")

def start_game():
    global canvas, root, status_label
    canvas_size = CELL_SIZE * BOARD_SIZE
    root = tk.Tk()
    root.title("Gomoku")

    frame = tk.Frame(root)
    frame.pack()
    canvas = tk.Canvas(frame, width=canvas_size, height=canvas_size, bg='#E6B88C')
    canvas.pack()
    status_label = tk.Label(frame, text="Your turn!", font=("Arial", 12))
    status_label.pack(pady=5)

    for i in range(BOARD_SIZE):
        canvas.create_line(0, CELL_SIZE * i, canvas_size, CELL_SIZE * i)
        canvas.create_line(CELL_SIZE * i, 0, CELL_SIZE * i, canvas_size)

    load_images()
    if mode == "HumanvsAI":
        canvas.bind("<Button-1>", click)
    elif mode == "AIvsAI":
        # Start AI vs AI game after window initialization
        root.after(500, ai_turn)
    root.mainloop()

def select_mode(selected_mode):
    global mode, human_name
    mode = selected_mode
    if mode == "HumanvsAI":
        name = simpledialog.askstring("Enter Name", "Enter your name:")
        human_name = name if name else "Human"
    start_window.destroy()
    start_game()

def check_winner(player, row, col):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for direction in [1, -1]:
            r, c = row, col
            while True:
                r += dr * direction
                c += dc * direction
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                    count += 1
                else:
                    break
        if count >= 5:
            return True
    return False

def is_board_full():
    return all(cell != EMPTY for row in board for cell in row)

def is_valid_move(board, row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == EMPTY

def evaluate_board():
    # Evaluation function that assigns scores based on contiguous chains for both players.
   
    weights = {1: 1, 2: 10, 3: 100, 4: 1000}
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    if last_move != (-1, -1):
        start_row = max(0, last_move[0] - 3)
        end_row = min(BOARD_SIZE, last_move[0] + 4)
        start_col = max(0, last_move[1] - 3)
        end_col = min(BOARD_SIZE, last_move[1] + 4)
    else:
        start_row, end_row, start_col, end_col = 0, BOARD_SIZE, 0, BOARD_SIZE

    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if board[r][c] == EMPTY:
                continue
            current = board[r][c]
            for dr, dc in directions:
                # Check if this cell is the beginning of a chain in direction (dr, dc)
                prev_r, prev_c = r - dr, c - dc
                if 0 <= prev_r < BOARD_SIZE and 0 <= prev_c < BOARD_SIZE and board[prev_r][prev_c] == current:
                    continue  # already counted in previous cell
                chain_length = 0
                nr, nc = r, c
                while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == current:
                    chain_length += 1
                    nr += dr
                    nc += dc
                if chain_length >= 5:
                    # Very high value for winning move
                    if current == AI:
                        return 100000
                    else:
                        return -100000
                if chain_length in weights:
                    if current == AI:
                        score += weights[chain_length]
                    else:
                        score -= weights[chain_length]
    return score

def minimax(board, depth, is_maximizing):
    # If game over or maximum depth reached, return evaluation
    if depth == 0 or is_board_full():
        return evaluate_board()

    # Check for a winning state immediately within a 6x6 grid around the last move
    if last_move != (-1, -1):
        start_row = max(0, last_move[0] - 3)
        end_row = min(BOARD_SIZE, last_move[0] + 4)
        start_col = max(0, last_move[1] - 3)
        end_col = min(BOARD_SIZE, last_move[1] + 4)
    else:
        start_row, end_row, start_col, end_col = 0, BOARD_SIZE, 0, BOARD_SIZE

    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if board[r][c] != EMPTY:
                if check_winner(board[r][c], r, c):
                    if board[r][c] == AI:
                        return 100000 - depth
                    else:
                        return -100000 + depth

    if is_maximizing:
        max_eval = -np.inf
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == EMPTY:
                    board[r][c] = AI
                    eval = minimax(board, depth - 1, False)
                    board[r][c] = EMPTY
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = np.inf
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == EMPTY:
                    board[r][c] = HUMAN
                    eval = minimax(board, depth - 1, True)
                    board[r][c] = EMPTY
                    min_eval = min(min_eval, eval)
        return min_eval

def ai_move():
    best_score = -np.inf
    best_move = None
    if last_move != (-1, -1):
        start_row = max(0, last_move[0] - 3)
        end_row = min(BOARD_SIZE, last_move[0] + 4)
        start_col = max(0, last_move[1] - 3)
        end_col = min(BOARD_SIZE, last_move[1] + 4)
    else:
        start_row, end_row, start_col, end_col = 0, BOARD_SIZE, 0, BOARD_SIZE

    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if board[r][c] == EMPTY:
                board[r][c] = AI
                score = minimax(board, MAX_DEPTH, False)
                board[r][c] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    return best_move

# Mode selection window
start_window = tk.Tk()
start_window.title("Gomoku Mode Selection")
start_window.geometry("300x200")

label = tk.Label(start_window, text="Choose Game Mode:", font=("Arial", 14))
label.pack(pady=20)

btn1 = tk.Button(start_window, text="Human vs AI", command=lambda: select_mode("HumanvsAI"), width=20)
btn1.pack(pady=10)

btn2 = tk.Button(start_window, text="AI vs AI", command=lambda: select_mode("AIvsAI"), width=20)
btn2.pack(pady=10)

start_window.mainloop()
