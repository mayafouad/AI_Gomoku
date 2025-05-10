
N = 15
M = 15


def PrintGrid(curgrid):
    for i in range(len(curgrid)):
        for j in range(len(curgrid[0])):
            print(curgrid[i][j], end=" ")
        print()


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
class Move:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Move({self.x}, {self.y})"


def IsValid(x, y):
    return x >= 0 and x < N and y >= 0 and y < M

def getNeighbors(grid, radius):
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
def CalcWinPossibility(startX, startY, grid, val):
    waysToWin = 0
    dx = [-1, 1, 0, 0, 1, -1, -1, 1]
    dy = [0, 0, -1, 1, 1, -1, 1, -1]

    for i in range(8):
        curCnt = 0
        x = startX
        y = startY

        while IsValid(x, y) and (grid[x][y] == val or grid[x][y] == 0):
            curCnt += 1
            x += dx[i]
            y += dy[i]

        if curCnt >= 5:
            waysToWin += min(1, int(curCnt / 5))

    return waysToWin

def UtilityFunctionInner(curgrid, symbol):
    ways = 0
    for i in range(N):
        for j in range(M):
            if curgrid[i][j] == 0:
                ways += CalcWinPossibility(i, j, curgrid, symbol)
    return ways


def UtilityFunction(curgrid):
    return UtilityFunctionInner(curgrid, 1) - UtilityFunctionInner(curgrid, 2)


def AlphaBeta(grid, IsMaximize, turn, depth, alpha, beta):
    if depth == 0:
        return (UtilityFunction(grid), Move(-1, -1))

    cur_best = float('-inf') if IsMaximize else float('inf')
    best_move = Move(-1, -1)
    candidates = getNeighbors(grid,1)
    finished = False
    for i ,j in candidates:

            if grid[i][j] == 0:
                grid[i][j] = turn
                if IsWinner(grid, turn, Move(i, j)):
                    grid[i][j] = 0
                    if IsMaximize:
                        return (float('inf'), Move(i, j))
                    else:
                        return (float('-inf'), Move(i, j))

                res = AlphaBeta(grid, not IsMaximize, 3 - turn, depth - 1, alpha, beta)

                if IsMaximize:
                    if res[0] > cur_best:
                        cur_best = res[0]
                        best_move = Move(i, j)
                    alpha = max(alpha, res[0])
                else:
                    if res[0] < cur_best:
                        cur_best = res[0]
                        best_move = Move(i, j)
                    beta = min(beta, res[0])

                grid[i][j] = 0
                if alpha >= beta:
                    return (cur_best, best_move)
                if finished:
                    break;
    return (cur_best, best_move)


def Main():
    turn = 1
    grid = [[0 for _ in range(M)] for _ in range(N)]
    i = 0
    print("Center:", CalcWinPossibility(4, 4, grid, 1))
    print("Top First:", CalcWinPossibility(0, 0, grid, 1))
    while i < 255:
        PrintGrid(grid)
        print("Entered turn:", turn)
        res = AlphaBeta(grid, turn == 1, turn, 2, float('-inf'), float('inf'))
        print("Chosen Value:", res[0], res[1].x, res[1].y)
        grid[res[1].x][res[1].y] = turn
        turn = 3 - turn
        i += 1


Main()


