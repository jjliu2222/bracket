import keyboard

matches = [("Alex", "Andrei"), ("Bart", "Ryan"), ("Paul", "Dmitri"), ("Grigor", "John")]
winners = []

i = 0  # index of current match
while i < len(matches):
    print(f"Match {i+1}: {matches[i][0]} vs {matches[i][1]}")
    while True:
        if keyboard.is_pressed("f"):
            i += 1
            break
        elif keyboard.is_pressed("b"):
            i -= 1
            break
        elif keyboard.is_pressed("1"):
            winners.append(matches[i][0])
            i += 1
            break
        elif keyboard.is_pressed("2"):
            winners.append(matches[i][1])
            i += 1
            break

for w in winners:
    print(winners)