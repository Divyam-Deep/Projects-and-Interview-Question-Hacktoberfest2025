# Read input (single integer on a line)
n = input().strip()

# Check adjacent digits
is_cookie = True
for i in range(len(n) - 1):
    if n[i] == n[i+1]:
        is_cookie = False
        break

print("Yes" if is_cookie else "No")