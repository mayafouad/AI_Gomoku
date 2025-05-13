import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np
import math
import random

# Constants
BOARD_SIZE = 10
CELL_SIZE = 40
EMPTY, HUMAN, AI = 0, 2, 1
MAX_DEPTH = 2
MAX = AI
AI1 , AI2 = 3 , 4
MIN = HUMAN
N, M = BOARD_SIZE, BOARD_SIZE
current_player = HUMAN
last_move = (-1, -1)

firstPlayer , secondPlayer = HUMAN, AI
mode = None
human_name = "Human"


# Game State
board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def select_mode(selected_mode):
    global mode, human_name
    mode = selected_mode
    if mode == "HumanvsAI":
        root = tk.Tk()
        root.withdraw()
        dialog = CustomNameDialog(root, title="Enter Name")
        name = dialog.result
        human_name = name if name else "Human"
    start_game(mode)


def start_game(mode):
    global canvas, root, status_label , firstPlayer , secondPlayer , MIN , MAX , current_player
    canvas_size = CELL_SIZE * BOARD_SIZE
    root = tk.Tk()
    if mode == "HumanvsAI" :
        root.title("Gomoku (Human Vs AI) ")
    else :
        root.title("Gomoku (AI Vs AI)")


    frame = tk.Frame(root)
    frame.pack()
    canvas = tk.Canvas(frame, width=canvas_size, height=canvas_size, bg='#E6B88C')
    canvas.pack()
    if mode == "HumanvsAI" :
        status_label = tk.Label(frame, text="Your turn!", font=("Arial", 12))
        status_label.pack(pady=5)

    for i in range(BOARD_SIZE):
        canvas.create_line(0, CELL_SIZE * i, canvas_size, CELL_SIZE * i)
        canvas.create_line(CELL_SIZE * i, 0, CELL_SIZE * i, canvas_size)

    load_images()
    if mode == "HumanvsAI":
        firstPlayer , secondPlayer = HUMAN , AI
        current_player = firstPlayer
        MIN ,MAX  = HUMAN , AI
        canvas.bind("<Button-1>", click)
    elif mode == "AIvsAI":
        firstPlayer , secondPlayer = AI1 , AI2
        current_player = AI1
        MIN ,MAX = AI1 , AI2
        status_label = tk.Label(frame, text="AI1 is Thinking", font=("Arial", 12))
        status_label.pack(pady=5)
        root.after(500, ai_turn)
    root.mainloop()



def load_images():
    global black_stone, white_stone
    try:
        black_stone = ImageTk.PhotoImage(Image.open("AI_Gomoku/black.png").resize((36, 36)))
        white_stone = ImageTk.PhotoImage(Image.open("AI_Gomoku/white.png").resize((36, 36)))
    except:
        black_stone = white_stone = None

def draw_stone(x, y, player):
    if player == firstPlayer and black_stone:
        canvas.create_image(x, y, anchor=tk.CENTER, image=black_stone)
    elif player == secondPlayer and white_stone:
        canvas.create_image(x, y, anchor=tk.CENTER, image=white_stone)
    else:
        color = "black" if player == HUMAN or player == AI1 else "white"
        canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill=color)

def click(event):
    global firstPlayer, last_move,current_player , status_label
    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE

    if not is_valid_move(board, row, col):
        return

    board[row][col] = current_player
    last_move = (row, col)
    draw_stone(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2, current_player)

    if check_winner(current_player, row, col):
        messagebox.showinfo("Game Over", f"{human_name if current_player == HUMAN else 'AI'} wins!")
        if mode == "HumanvsAI" :
            canvas.unbind("<Button-1>")
        status_label.config(text="Game Over")
        return

    if is_board_full():
        messagebox.showinfo("Game Over", "It's a draw!")
        if mode == "HumanvsAI" :
            canvas.unbind("<Button-1>")
        status_label.config(text="Game Over")
        return
    if current_player == firstPlayer :
        current_player = secondPlayer
    else :
        current_player = firstPlayer
    if mode == "HumanvsAI" and current_player == AI:
        status_label.config(text="AI is thinking...")
        root.after(100, ai_turn)

yet = False
def ai_turn():
    global current_player, last_move , mode , yet , status_label
    if mode == "AIvsAI" and yet == False :
        yet =  True
        x = random.randint(0, BOARD_SIZE - 1)
        y = random.randint(0, BOARD_SIZE - 1)
        move = (x , y)
    else :
        move = ai_move()

        # Check if the AI move is valid or not as the board is full
    if move is None:
        print("No valid move returned by ai_move in its window search size.")
        if is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            status_label.config(text="Game Over")
        return
    else:
        r, c = move
        board[r][c] = current_player
        last_move = (r, c)
        draw_stone(c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2, current_player)

        if check_winner(current_player, r, c):
            if mode == "AIvsAI" :
                messagebox.showinfo("Game Over", f"{'AI 1' if current_player == AI1 else 'AI 2'} wins!")
            else :
                messagebox.showinfo("Game Over", f"{'AI' if current_player == AI else human_name} wins!")
            if mode == "HumanvsAI" :
                canvas.unbind("<Button-1>")
            status_label.config(text="Game Over")
            return

        if is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            status_label.config(text="Game Over")
            return
        current_player = secondPlayer if current_player == firstPlayer else firstPlayer
        if mode == "HumanvsAI":
            status_label.config(text="Your turn!")
        else :
            status_label.config(text="AI2 is thinking...")
            root.after(100 , ai2_turn)




def is_board_full():
    return all(cell != EMPTY for row in board for cell in row)

def is_valid_move(board, row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == EMPTY

def evaluate_board(current_player):
    weights = {1: 1, 2: 10, 3: 100, 4: 1000}  # Scores for chain lengths
    open_bonus = {3: 500, 4: 5000}  # Bonuses for open or gapped chains
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, vertical, diagonal, anti-diagonal

    if last_move != (-1, -1):
        start_row = max(0, last_move[0] - 4)
        end_row = min(BOARD_SIZE, last_move[0] + 5)
        start_col = max(0, last_move[1] - 4)
        end_col = min(BOARD_SIZE, last_move[1] + 5)
    else:
        start_row, end_row, start_col, end_col = 0, BOARD_SIZE, 0, BOARD_SIZE

    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if board[r][c] == EMPTY:
                continue
            current = board[r][c]
            for dr, dc in directions:
                # Prevent double-counting
                prev_r, prev_c = r - dr, c - dc
                if 0 <= prev_r < BOARD_SIZE and 0 <= prev_c < BOARD_SIZE and board[prev_r][prev_c] == current:
                    continue
                chain_length = 0
                gaps = 0
                open_start = False
                open_end = False
                nr, nc = r, c
                # Check for open start
                if 0 <= r - dr < BOARD_SIZE and 0 <= c - dc < BOARD_SIZE and board[r - dr][c - dc] == EMPTY:
                    open_start = True
                # Count stones and up to 1 gap
                while (start_row <= nr < end_row and start_col <= nc < end_col and
                       0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE):
                    if board[nr][nc] == current:
                        chain_length += 1
                    elif board[nr][nc] == EMPTY and gaps == 0:
                        gaps += 1
                        chain_length += 1
                    else:
                        break
                    nr += dr
                    nc += dc
                # Check for open end
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == EMPTY:
                    open_end = True
                # Handle winning condition (5+ stones, no gaps) ->  { * * * * * }
                if chain_length >= 5 and gaps == 0:
                    if current == current_player:
                        return 100000
                    else:
                        return -100000
                # remove the gap from the chain length -> { * * * 0 * } chain_length = 5 so we need to remove 1 from the chain length
                if gaps == 1:
                    chain_length -= 1
                # Score non-winning chains
                if chain_length in weights:
                    chain_score = weights[chain_length]
                    if chain_length in open_bonus and (open_start or open_end or gaps > 0):
                        chain_score += open_bonus[chain_length]
                    if current == current_player:
                        score += chain_score
                    else:
                        score -= chain_score
    return score

def minimax(board, depth, is_maximizing,current_player):

    if depth == 0 or is_board_full():
        return evaluate_board(current_player)

    if last_move != (-1, -1):
        start_row = max(0, last_move[0] - 2)
        end_row = min(BOARD_SIZE, last_move[0] + 3)
        start_col = max(0, last_move[1] - 2)
        end_col = min(BOARD_SIZE, last_move[1] + 3)
    else:
        start_row, end_row, start_col, end_col = 0, BOARD_SIZE, 0, BOARD_SIZE
    if is_maximizing:
        max_eval = -np.inf
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                if board[r][c] == EMPTY:
                    board[r][c] = current_player
                    eval = minimax(board, depth - 1, False,current_player)
                    board[r][c] = EMPTY
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = np.inf
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                if board[r][c] == EMPTY:
                    board[r][c] = firstPlayer if current_player == secondPlayer else secondPlayer
                    eval = minimax(board, depth - 1, True,current_player)
                    board[r][c] = EMPTY
                    min_eval = min(min_eval, eval)
        return min_eval

def ai_move():
    best_score = -np.inf
    best_move = None
    global last_move, current_player
    # Define ±5 window for instant win/loss check
    if last_move != (-1, -1):
        win_start_row = max(0, last_move[0] - 5)
        win_end_row = min(BOARD_SIZE, last_move[0] + 6)
        win_start_col = max(0, last_move[1] - 5)
        win_end_col = min(BOARD_SIZE, last_move[1] + 6)

        # Check for instant win (can AI1 win with one move?)
        for r in range(win_start_row, win_end_row):
            for c in range(win_start_col, win_end_col):
                if board[r][c] == EMPTY:
                    board[r][c] = current_player
                    if check_winner(current_player, r, c):
                        board[r][c] = EMPTY
                        return (r, c)  # Win found
                    board[r][c] = EMPTY
        # Check if opponent can win on the next move
        for r in range(win_start_row, win_end_row):
            for c in range(win_start_col, win_end_col):
                if board[r][c] == EMPTY:
                    opponent = firstPlayer if current_player == secondPlayer else secondPlayer
                    board[r][c] = opponent
                    if check_winner(opponent, r, c):
                        board[r][c] = EMPTY
                        return (r, c)  # Block the win
                    board[r][c] = EMPTY

                    # Initial search window (±2 cells around last move)
    if last_move != (-1, -1):
        start_row = max(0, last_move[0] - 2)
        end_row = min(BOARD_SIZE, last_move[0] + 3)
        start_col = max(0, last_move[1] - 2)
        end_col = min(BOARD_SIZE, last_move[1] + 3)
    else:
        start_row, end_row, start_col, end_col = 0, BOARD_SIZE, 0, BOARD_SIZE

    valid_moves = []
    # Get all valid moves in the initial window
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if board[r][c] == EMPTY:
                valid_moves.append((r, c))

    # If no valid moves in the initial window, search the entire board
    if not valid_moves:
        print("No valid moves in initial window, searching entire board...")
        start_row, end_row, start_col, end_col = 0, BOARD_SIZE, 0, BOARD_SIZE
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                if board[r][c] == EMPTY:
                    valid_moves.append((r, c))

    # Evaluate each valid move
    for r, c in valid_moves:
        board[r][c] = current_player
        score = minimax(board, MAX_DEPTH, False, current_player)
        board[r][c] = EMPTY
        if score > best_score:
            best_score = score
            best_move = (r, c)

    # If no move improved best_score, select a random move
    if best_move is None and valid_moves:
        print("No move improved best_score, selecting random move")
        best_move = random.choice(valid_moves)
        best_score = -np.inf

    return best_move




class CustomNameDialog(simpledialog.Dialog):
    def body(self, master):
        self.configure(bg="#E6B88C")
        self.geometry("400x200")

        tk.Label(master, text="Enter your name:", bg="#E6B88C", font=("Arial", 14)).pack(pady=20)
        self.entry = tk.Entry(master, font=("Arial", 14), width=30)
        self.entry.pack()
        return self.entry

    def apply(self):
        self.result = self.entry.get()



############################## Alpha-Beta ##############################3

######################################################################################

def BlockedNums(grid, turn):
    blocked = 0
    dx = [-1, 1, 0, 0, 1, -1, -1, 1]
    dy = [0,  0, -1, 1, 1, -1, 1, -1]

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            for k in range(8):
                x, y = i, j
                curCnt = 0
                while IsValid(x, y):
                    if grid[x][y] == turn or grid[x][y] == 0:
                        curCnt += 1
                        x += dx[k]
                        y += dy[k]
                    else:
                        if 1 <= curCnt < 5:
                            blocked += curCnt * 100
                        break
    return blocked


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
            if  board[x][y] == val:
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
        row =  lastMove.x + dx[k]
        col =  lastMove.y + dy[k]

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
    return UtilityFunctionInner(curgrid, secondPlayer) - UtilityFunctionInner(curgrid,  firstPlayer) + (BlockedNums(curgrid,secondPlayer))
#####################################################################################3

def ai2_turn():
    global last_move , current_player , status_label
    move = ai2_move()
    if move:
        r, c = move
        board[r][c] = current_player
        last_move = (r, c)
        draw_stone(c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2,  current_player)

        if check_winner(current_player, r, c):
            messagebox.showinfo("Game Over", f"{'AI 1' if  current_player ==  AI1 else 'AI 2'} wins!")
            status_label.config(text="Game Over")
            return

        if is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            status_label.config(text="Game Over")
            return

        if  current_player ==  firstPlayer :
            current_player =  secondPlayer
        else :
            current_player =  firstPlayer
        if mode == "AIvsAI":
            status_label.config(text="AI1 is thinking...")
            root.after(100 ,  ai_turn)


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


def alphabeta(board, depth, is_maximizing, last_x, last_y, alpha, beta):

    if depth == 0 or is_board_full():
        return (UtilityFunction(board), (last_x, last_y))

    best_x, best_y = -1, -1
    best = float('-inf') if is_maximizing else float('inf')
    children = getNeighbors(board)


    if is_maximizing:
        for r, c in children:
            if  board[r][c] == EMPTY:
                board[r][c] =  secondPlayer
                if IsWinner(board, secondPlayer, Move(r, c)):
                    board[r][c] = EMPTY
                    return (float('inf'), (r, c))

                eval = alphabeta(board, depth - 1, False, r, c, alpha, beta)
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
                board[r][c] = firstPlayer
                if IsWinner(board,firstPlayer, Move(r, c)):
                    board[r][c] = EMPTY
                    return (float('-inf'), (r, c))

                eval = alphabeta(board, depth - 1, True, r, c, alpha, beta)
                if eval[0] <= best:
                    best_x, best_y = r, c
                    best = eval[0]
                beta = min(beta, best)
                board[r][c] = EMPTY
                if alpha >= beta:
                    break

    return (best, (best_x, best_y))

def ai2_move():

    res = alphabeta(board, MAX_DEPTH, True, last_move[0] , last_move[1], float('-inf'), float('inf'))
    return res[1]