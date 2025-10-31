def maxProfit(k, prices):
    n = len(prices)
    if n == 0:
        return 0

    memo = {}

    def helper(index, buy, cap):
        # base cases
        if index == n or cap == 0:
            return 0

        if (index, buy, cap) in memo:
            return memo[(index, buy, cap)]

        if buy:
            # choose to buy or skip
            ans = max(
                -prices[index] + helper(index + 1, False, cap),  # buy
                helper(index + 1, True, cap)                     # skip
            )
        else:
            # choose to sell or skip
            ans = max(
                prices[index] + helper(index + 1, True, cap - 1),  # sell (one transaction done)
                helper(index + 1, False, cap)                      # skip
            )

        memo[(index, buy, cap)] = ans
        return ans

    return helper(0, True, k)
