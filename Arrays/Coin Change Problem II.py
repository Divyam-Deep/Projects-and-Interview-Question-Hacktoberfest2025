def count(coins, N, target):
    memo={}
    coins.sort()
    def f(i,target):
        if target==0:
            return 1
        if i==len(coins) or coins[i]>target:
            return 0
        if (i,target) in memo:
            return memo[(i,target)]
        

        take =f(i,target-coins[i])
        nottake=f(i+1,target)
        memo[(i,target)]=take + nottake
        return memo[(i,target)]
    return f(0,target)
