def maxProfit(prices):
    # Write your code here
    mini=prices[0]
    ans=0
    for i in range(1,len(prices)):
        # print(mini)
        if prices[i]-mini>ans:
            ans=prices[i]-mini
        elif prices[i]-mini<0:
            mini=prices[i]
    return ans
