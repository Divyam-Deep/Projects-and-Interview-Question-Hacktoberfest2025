🧠 1. N-Queens Problem
def solveNQueens(n):
    res = []
    board = [["."] * n for _ in range(n)]

    def is_safe(r, c):
        for i in range(r):
            if board[i][c] == "Q": return False
        i, j = r - 1, c - 1
        while i >= 0 and j >= 0:
            if board[i][j] == "Q": return False
            i -= 1; j -= 1
        i, j = r - 1, c + 1
        while i >= 0 and j < n:
            if board[i][j] == "Q": return False
            i -= 1; j += 1
        return True

    def backtrack(r):
        if r == n:
            res.append(["".join(row) for row in board])
            return
        for c in range(n):
            if is_safe(r, c):
                board[r][c] = "Q"
                backtrack(r + 1)
                board[r][c] = "."

    backtrack(0)
    return res

print(solveNQueens(4))

🐀 2. Rat in a Maze
def ratInMaze(maze, n):
    res, path = [], []

    def solve(x, y):
        if x == n - 1 and y == n - 1:
            res.append("".join(path))
            return
        if not (0 <= x < n and 0 <= y < n) or maze[x][y] == 0:
            return
        maze[x][y] = 0
        for move, dx, dy in [('D', 1, 0), ('L', 0, -1), ('R', 0, 1), ('U', -1, 0)]:
            path.append(move)
            solve(x + dx, y + dy)
            path.pop()
        maze[x][y] = 1

    solve(0, 0)
    return res

maze = [[1, 0, 0], [1, 1, 0], [1, 1, 1]]
print(ratInMaze(maze, 3))

🔢 3. Subset Sum / Subsets
def subsets(nums):
    res, subset = [], []

    def backtrack(i):
        if i == len(nums):
            res.append(subset[:])
            return
        subset.append(nums[i])
        backtrack(i + 1)
        subset.pop()
        backtrack(i + 1)

    backtrack(0)
    return res

print(subsets([1, 2, 3]))

🔄 4. Permutations
def permute(nums):
    res = []

    def backtrack(start):
        if start == len(nums):
            res.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]

    backtrack(0)
    return res

print(permute([1, 2, 3]))

🎯 5. Combination Sum
def combinationSum(candidates, target):
    res, comb = [], []

    def backtrack(start, total):
        if total == target:
            res.append(comb[:])
            return
        if total > target:
            return
        for i in range(start, len(candidates)):
            comb.append(candidates[i])
            backtrack(i, total + candidates[i])
            comb.pop()

    backtrack(0, 0)
    return res

print(combinationSum([2, 3, 6, 7], 7))

🔤 6. Word Search
def exist(board, word):
    rows, cols = len(board), len(board[0])
    path = set()

    def dfs(r, c, i):
        if i == len(word): return True
        if (r < 0 or c < 0 or r >= rows or c >= cols or 
            word[i] != board[r][c] or (r, c) in path):
            return False
        path.add((r, c))
        res = (dfs(r+1,c,i+1) or dfs(r-1,c,i+1) or 
               dfs(r,c+1,i+1) or dfs(r,c-1,i+1))
        path.remove((r, c))
        return res

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0): return True
    return False

board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
print(exist(board, "ABCCED"))

💎 7. Palindrome Partitioning
def partition(s):
    res, part = [], []

    def is_palindrome(sub):
        return sub == sub[::-1]

    def backtrack(start):
        if start == len(s):
            res.append(part[:])
            return
        for end in range(start + 1, len(s) + 1):
            if is_palindrome(s[start:end]):
                part.append(s[start:end])
                backtrack(end)
                part.pop()

    backtrack(0)
    return res

print(partition("aab"))

🧮 8. Sudoku Solver
def solveSudoku(board):
    def is_valid(r, c, ch):
        for i in range(9):
            if board[r][i] == ch or board[i][c] == ch:
                return False
        box_r, box_c = 3 * (r // 3), 3 * (c // 3)
        for i in range(box_r, box_r + 3):
            for j in range(box_c, box_c + 3):
                if board[i][j] == ch:
                    return False
        return True

    def backtrack():
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    for ch in "123456789":
                        if is_valid(r, c, ch):
                            board[r][c] = ch
                            if backtrack():
                                return True
                            board[r][c] = "."
                    return False
        return True

    backtrack()
    return board

☎️ 9. Letter Combinations of a Phone Number
def letterCombinations(digits):
    if not digits: return []
    phone = {'2':'abc','3':'def','4':'ghi','5':'jkl','6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}
    res = []

    def backtrack(i, cur):
        if i == len(digits):
            res.append(cur)
            return
        for ch in phone[digits[i]]:
            backtrack(i+1, cur + ch)

    backtrack(0, "")
    return res

print(letterCombinations("23"))

🧩 10. Generate Parentheses
def generateParenthesis(n):
    res = []

    def backtrack(openN, closeN, cur):
        if openN == closeN == n:
            res.append(cur)
            return
        if openN < n:
            backtrack(openN + 1, closeN, cur + "(")
        if closeN < openN:
            backtrack(openN, closeN + 1, cur + ")")

    backtrack(0, 0, "")
    return res

print(generateParenthesis(3))
