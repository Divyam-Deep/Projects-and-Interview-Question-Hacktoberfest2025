import numpy as np

# Grid world: 0 = empty, -1 = wall, +10 = goal
env = np.array([
    [0, 0, 0, 10],
    [0, -1, 0, -1],
    [0, 0, 0, 0]
])

n_rows, n_cols = env.shape
actions = [(0,1), (0,-1), (1,0), (-1,0)]  # right, left, down, up
Q = np.zeros((n_rows, n_cols, len(actions)))

alpha, gamma, episodes = 0.1, 0.9, 500

def valid(r, c):
    return 0 <= r < n_rows and 0 <= c < n_cols and env[r, c] != -1

for _ in range(episodes):
    r, c = 2, 0  # start bottom-left
    while env[r, c] != 10:
        a = np.random.randint(0, 4)
        dr, dc = actions[a]
        nr, nc = r + dr, c + dc
        if not valid(nr, nc):
            reward, nr, nc = -5, r, c
        else:
            reward = env[nr, nc]
        Q[r, c, a] += alpha * (reward + gamma * np.max(Q[nr, nc]) - Q[r, c, a])
        r, c = nr, nc

# Derive optimal policy
policy = np.full((n_rows, n_cols), ' ')
dirs = ['→','←','↓','↑']
for r in range(n_rows):
    for c in range(n_cols):
        if env[r,c] == -1: policy[r,c] = 'X'
        elif env[r,c] == 10: policy[r,c] = '🏁'
        else: policy[r,c] = dirs[np.argmax(Q[r,c])]
print(policy)
