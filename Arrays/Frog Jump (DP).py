import sys
sys.setrecursionlimit(1000000)
def frogJump(h):
    memo={}
    n=len(h)
    def f(i):
        if i in memo:
            return memo[i]
        if i==n-1:
            return 0
        
        if i==n-2:
            return abs(h[i]-h[i+1])
        c1=abs(h[i]-h[i+1])+f(i+1)
        c2=abs(h[i]-h[i+2])+f(i+2)

        memo[i]=min(c1,c2)
        return min(c1,c2)
    return f(0)




























#code 2
# def frogJump(heights):
    
#     n = len(heights)
#     if n==1:
#         return 0
    
#     prev1=0
#     prev2=abs(heights[0]-heights[1])

#     for i in range(2,n):
#         jump1=prev2 + abs(heights[i]-heights[i-1])
#         jump2=prev1 + abs(heights[i]-heights[i-2])
#         curr=min(jump1,jump2)

#         prev1,prev2=prev2,curr
#     return prev2
