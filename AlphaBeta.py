import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np
import math

# Constants
BOARD_SIZE = 15
CELL_SIZE = 40
EMPTY, HUMAN, AI = 0, 2, 1
MAX_DEPTH = 2
MAX = AI
MIN = HUMAN
N, M = BOARD_SIZE, BOARD_SIZE

# Game State
board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = HUMAN
mode = None
human_name = "Human"
last_move = (-1, -1)


######################################################################################



def IsValid(x, y): 
    return x >= 0 and x < N and y >= 0 and y < M;

def CalcWinPossibility(startX, startY, grid, val):
    waysToWin = 0
    dx = [-1, 1, 0, 0, 1, -1, -1, 1]
    dy = [0,  0, -1, 1, 1, -1, 1, -1]
    player = 0
    opponent = 0
    
    sumi = 0
    for i in range(0, 8):
        curCnt = 0
        x = startX
        y = startY
         
        if not IsValid(x + dx[i] * 5, y + dy[i] * 5):
            continue

        cnt = 0
        while cnt < 5:
            if board[x][y] == val: 
                player += 1
            elif board[x][y] == (3 - val): 
                opponent += 1
            cnt += 1
            y += dy[i]
            x += dx[i]
        
        if opponent != 0:
             if opponent >= 4:
                  sumi -= 100000  
             elif opponent == 3:
                  sumi -= 1000     
             elif opponent == 2:
                  sumi -= 50   
        else:
            if player == 5: 
                sumi += 100000  
            elif player == 4: 
               
                if (IsValid(startX - dx[i], startY - dy[i]) and 
                   board[startX - dx[i]][startY - dy[i]] == EMPTY) or \
                   (IsValid(startX + dx[i], startY + dy[i]) and 
                   board[startX + dx[i]][startY + dy[i]] == EMPTY):
                    sumi += 100000  
                else:
                    sumi += 10000   
            elif player == 3:
                
                if (IsValid(startX - dx[i], startY - dy[i]) and 
                   board[startX - dx[i]][startY - dy[i]] == EMPTY) or \
                   (IsValid(x, y) and board[x][y] == EMPTY):
                    sumi += 1000  
                else:
                    sumi += 100   
            elif player == 2:
                
                if (IsValid(startX - dx[i], startY - dy[i]) and 
                   board[startX - dx[i]][startY - dy[i]] == EMPTY) or \
                   (IsValid(x, y) and board[x][y] == EMPTY):
                    sumi += 50   
                else:
                    sumi += 10   
        player = 0
        opponent = 0
    return sumi
class Move:
    def __init__(self, x, y):
        self.x = x;
        self.y = y
def IsWinner(curgrid, val, lastMove):
    dx = [1, 0, 1, 1]
    dy = [0, 1, 1, -1]
    for k in range(4):
        count = 1  
        row = lastMove.x + dx[k]
        col = lastMove.y + dy[k]
        
        while IsValid(row, col) and curgrid[row][col] == val:
            count += 1
            row += dx[k]
            col += dy[k]
        
        row = lastMove.x - dx[k]
        col = lastMove.y - dy[k]
        while IsValid(row, col) and curgrid[row][col] == val:
            count += 1
            row -= dx[k]
            col -= dy[k]
        
        if count >= 5:
            return True
    
    return False

def UtilityFunctionInner(curgrid, symbol):
    ways = 0
    for i in range(N):
        for j in range(M):
            if curgrid[i][j] == 0 or curgrid[i][j] == symbol:
                ways += CalcWinPossibility(i, j, curgrid, symbol)
    return ways

def UtilityFunction(curgrid):  
    return UtilityFunctionInner(curgrid, AI) - UtilityFunctionInner(curgrid, HUMAN)
#####################################################################################3
def load_images():
    global black_stone, white_stone
    try:
        black_stone = ImageTk.PhotoImage(Image.open("black_gm.jpg").resize((36, 36)))
        white_stone = ImageTk.PhotoImage(Image.open("white_gm.png").resize((36, 36)))
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
            return
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
        return
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
        for dir in [1, -1]:
            r, c = row, col
            while True:
                r += dr * dir
                c += dc * dir
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
def getNeighbors(grid, radius = 1):
    candidates = set()
    for i in range(N):
        for j in range(M):
            if grid[i][j] != 0:
                for di in range(-radius, radius + 1):
                    for dj in range(-radius, radius + 1):
                        ni, nj = i + di, j + dj
                        if IsValid(ni, nj) and grid[ni][nj] == 0:
                            candidates.add((ni, nj))
    return candidates
   

def AlphaBeta(board, depth, is_maximizing, last_x, last_y, alpha, beta):

    if depth == 0 or is_board_full():
        return (UtilityFunction(board), (last_x, last_y))
    
    best_x, best_y = -1, -1
    best = float('-inf') if is_maximizing else float('inf')
    children = getNeighbors(board)
   # print(children)
    
    if is_maximizing:
        for r, c in children:
            if board[r][c] == EMPTY:
                board[r][c] = AI
                if IsWinner(board,AI, Move(r, c)):
                    board[r][c] = EMPTY
                    return (float('inf'), (r, c))
                
                eval = AlphaBeta(board, depth - 1, False, r, c, alpha, beta)
                if eval[0] >= best:
                    best_x, best_y = r, c
                    best = eval[0]
                alpha = max(alpha, best)
                board[r][c] = EMPTY
                if alpha >= beta:
                    break  
    else:
        for r, c in children:
            if board[r][c] == EMPTY:
                board[r][c] = HUMAN
                if IsWinner(board, HUMAN, Move(r, c)):
                    board[r][c] = EMPTY
                    return (float('-inf'), (r, c))
                
                eval = AlphaBeta(board, depth - 1, True, r, c, alpha, beta)
                if eval[0] <= best:
                    best_x, best_y = r, c
                    best = eval[0]
                beta = min(beta, best)
                board[r][c] = EMPTY
                if alpha >= beta:
                    break  
                    
    return (best, (best_x, best_y))

def ai_move():
    
   res = AlphaBeta(board, MAX_DEPTH, True, -1, -1, float('-inf'), float('inf'))
   print(res)
   print("Utility: ", CalcWinPossibility(res[1][0], res[1][1], board, AI))
   return res[1]

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
