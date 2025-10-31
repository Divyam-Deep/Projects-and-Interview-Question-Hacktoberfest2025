MOD = 10**9 + 7
def mazeObstacles(m, n, obstacleGrid):
    if obstacleGrid[0][0]==1 and obstacleGrid[m - 1][n - 1]==1:
        return 0
    dp = [0] * n
    dp[0] = 1
    for i in range(m):
        for j in range(n):
            if obstacleGrid[i][j]==1:
                dp[j] = 0
            elif j>0:
                dp[j] = (dp[j] + dp[j - 1]) % MOD
    return dp[-1]
