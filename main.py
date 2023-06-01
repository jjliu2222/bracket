import brack
import player
import csv
import datetime
import os
# How does this work?
# The program creates a single-elimination bracket of up to 128 players, each of which has a rating
# If a player does not have a rating they are given a default rating.
# If the number of players is not exactly 2,4,8,16, etc, byes are given to the highest seeded players to fill the bracket
# The rest of the bracket is randomly generated and lower seeded players play each other
# Starting from the second round play continues normally

# Upload a CSV of name, rating with Name, Rating title on the first line, if no rating then leave blank



timenow = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
players = []
while True:
    # Select a mode–either manually input players or upload from xl
    mode = input("Enter 'm' for manual mode and 'i' for import mode.")
    mode.lower()
    if mode == "i" or mode == "m":
        break
    else:
        print("Please enter a valid input.")
while True:
    isRanked = input("Is this tournament seeded? y/n: ")
    isRanked.lower()
    if isRanked == "y" or isRanked == "n":
        break
    else:
        print("Please enter a valid input.")


if mode == "m":

    # create a tournament log with current time as a csv file
    logName = f"tournamentlog_{timenow}.txt"
    with open(logName, "w", newline="") as file:

        if isRanked == "y":
            file.write("Name, Rating\n")
        else:
            file.write("Name\n")
        while True:
            name = input("Enter the player name (or done): ")
            if name == "done":
                break
            if isRanked == "y":
                while True:
                    rating = input("Enter the player's rating–blank for no ranking: ")
                    if rating == "":
                        break
                    try:
                        rating = int(rating)
                        break
                    except ValueError:
                        print("Please enter a valid input.")
                file.write(name + ", " + str(rating) + "\n") if rating != "" else file.write(name + ", unrated (300)\n")
                players.append(player.Player(name, int(rating))) if rating != "" else players.append(player.Player(name))

                file.flush()

            else:
                file.write(name + "\n")
                players.append(player.Player(name, -1))

                file.flush()
                os.fsync(file.fileno())

elif mode == "i" and isRanked == "y":
    while True:
        try:
            logName = input("Please enter the name of the file you would like to read from using a .csv format.")
            with open(logName, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    pName = row[0]
                    pRating = row[1] if len(row) > 1 else None

                    if pRating:
                        players.append(player.Player(pName, int(pRating)))
                    else:
                        players.append(player.Player(pName))
        except FileNotFoundError:
            print("File not found.")
        else:
            break

else:
    while True:
        try:
            logName = input("Please enter the name of the file you would like to read from using a .csv format.")
            with open(logName, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    pName = row[0]
                    players.append(player.Player(pName, -1))
        except FileNotFoundError:
            print("File not found.")
        else:
            break




if len(players) <= 1:
    print("There is no tournament.")
    quit()


if isRanked == "y":
    myBracket = brack.BracketRules(players, 0) # seeded
else:
    myBracket = brack.BracketRules(players, 1) # unseeded (completely randomly generated)


# if mode is manual, txt file already created, if not, create a txt file
if mode == "m":
    myBracket.log = logName
else:
    myBracket.log = logName[:-3] + "txt"

myBracket.printMatches()

# used to append matches later on

while myBracket.round < myBracket.numRounds + 1:
    nextRTemp = []
    matchNumbers = {}
    for match in myBracket.matchesRaw:
        # Index of the current match tuple
        myBracket.currentMatch = myBracket.matchesRaw.index(match)
        # each match's index is stored in a dictionary to be used later
        matchNumbers[match] = myBracket.currentMatch

        # if player has a bye, they are automatically moved on to the next round
        if match[0].isBye == True and match[0].rating != 0 and myBracket.round == 1:
            nextRTemp.append(match[0])
        else:
            while True:

                resulting = int(input("Enter 1 or 2 for the winner of" + " " + match[0].__str__() + " vs " + match[1].__str__() + ". "))
                if resulting == 1:
                    nextRTemp.append(match[0])
                    myBracket.currentMatch += 1
                    break
                elif resulting == 2:
                    nextRTemp.append(match[1])
                    myBracket.currentMatch += 1
                    break
                elif resulting == "":
                    myBracket.iter_through_matches("f")
                    break
                elif resulting.lower() == "b":
                    myBracket.iter_through_matches("b")
                    break
                else:
                    print("Not a valid input. Please try again.")



    nextR = []

    # creating a list of tuples of size 2 out of a list of players
    if len(nextRTemp) > 1:
        for i in range(0, len(nextRTemp), 2):
            nextR.append((nextRTemp[i], nextRTemp[i + 1]))
        myBracket.advanceTourney(nextR)
    else:
        myBracket.round += 1
        myBracket.matchesRaw = []
        myBracket.matchesRaw.append(nextRTemp[0])
        myBracket.printMatches()



