def calculate_score(speed, strength):
    if speed > 0 and speed % 2 == 0:
        speed = speed * 3
    elif speed > 0 and speed % 2 != 0:  
        speed = speed * 2
    elif speed < 0:
        speed = abs(speed) * 2
    else:
        speed = 0
    if strength % 2 == 0:
        strength = strength * 4
    else:
        strength = strength * 3

    return speed + strength
g1_speed, g1_strength = map(int, input().split())
g2_speed, g2_strength = map(int, input().split())

g1_score = calculate_score(g1_speed, g1_strength)
g2_score = calculate_score(g2_speed, g2_strength)

if g1_score > g2_score:
    print("GAMER 1 WINS")
elif g2_score > g1_score:
    print("GAMER 2 WINS")
else:
    print("DRAW")