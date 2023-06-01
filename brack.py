# Each player can receive a maximum of 1 bye! This means that if there are 9 players
# #in the tournament, top 7 ranked will receive a bye and the lowest 2
# ranked will play a play-in game for the 8th spot

import os
import math
import random
import player
import csv

class BracketRules:
    def __init__(self, players, format):
        self.players = players
        self.format = format
        self.matches = []
        self.matchesRaw = []
        self.numRounds = 0
        self.numPlayers = len(players)
        self.makeSingleBracket()


    def makeSingleBracket(self):
        if self.format == 0:
            # sort if tournament is seeded
            self.players.sort(key=lambda x: x.rating, reverse=True)


        print("There are", len(self.players), "players in the tournament.")
        # calculate number of rounds
        self.numRounds = int(math.ceil(math.log2(self.numPlayers)))

        # initializing round
        self.round = 0
        # number of byes ITFR
        self.numByes = 2 ** self.numRounds - self.numPlayers
        if self.numByes < 0:
            self.numByes = 0

        if self.numByes != 0 and self.format == 0:
            print("There are ", self.numByes," byes in the tournament given to the top ",self.numByes, " ranked player(s).")
        else:
            print("There are",self.numByes,"byes in the tournament.")


        if self.format == 1:
            # shuffle players if unseeded
            random.shuffle(self.players)





        for i in range(self.numByes):
            if self.numByes != 0:
                # Give the top i rated players in the player pool a bye
                # if unseeded, then just give the first i players in the shuffled list a bye
                self.players[i].isBye = True
                # For every player that is given a bye, create a placeholder bye player in order to make total players an even number
                myPlay = player.Player("BYE", 0)
                # placeholder player
                myPlay.isBye = True
                self.players.append(myPlay)


        # shuffle bracket players
        random.shuffle(self.players)
        # number of matches in the first round
        self.numMatches = len(self.players) / 2

        for i in range(int(self.numMatches)):
            p1 = self.players.pop()
            # non-placeholder player who receives a bye
            if p1.isBye == True and p1.rating != 0:
                p2 = None  # initialize p2
                for p in self.players:
                    # finding a placeholder bye player to match up with bona fide bye receiver
                    if p.isBye == True and p.rating == 0:
                        p2 = p
                        self.players.remove(p) # remove placeholder from player list
                        break
                # add bye match to list of matches
                # self.matches contains the string representation of the player objects!
                self.matches.append((p1.__str__(), p2.__str__()))
                self.matchesRaw.append((p1, p2))
            elif p1.isBye == True and p1.rating == 0: # if player is a placeholder:
                p2 = None  # initialize p2
                for p in self.players:
                    if p.isBye == True and p.rating != 0: # finding a bona fide bye receiver
                        p2 = p
                        self.players.remove(p)
                        break
                self.matches.append((p2.__str__(), p1.__str__()))
                self.matchesRaw.append((p2, p1))
            else:
                p2 = None  # initialize p2
                for p in self.players:
                    if p.isBye == False: # finding first non-bye player to match up against
                        p2 = p
                        self.players.remove(p)
                        break
                self.matches.append((p1.__str__(), p2.__str__()))
                self.matchesRaw.append((p1, p2))
        self.round += 1




    def printMatches(self):
        if self.round == self.numRounds + 1:
            print("Winner:", self.matchesRaw[0].__str__())
        else:
            print("Round",self.round)
            for m in self.matches:
                print(m)

        self.writetolog(self.log)

    def advanceTourney(self, b):
        # b: existing bracket
        # clear matches list
        self.matches = []

        # create a temporary list that will contain player string representations
        self.temp = []
        for match in b:
            for player in match:
                playerString = player.__str__()
                self.temp.append(playerString)

        # turning a list of players into a list of tuples, each with size 2 that represent matchups
        if len(self.temp) > 1:
            for i in range(0, len(self.temp), 2):
                self.matches.append((self.temp[i], self.temp[i + 1]))

        # set raw matches equal to passed argument
        self.matchesRaw = b

        # increment round number by 1
        self.round += 1

        # print the round and matches
        self.printMatches()

    def writetolog(self, filename):

        with open(filename, mode='a') as file:
            file.write("")

            if self.round == self.numRounds + 1:
                file.write("\n" + "Winner: " + self.matchesRaw[0].__str__() + "\n")
            else:
                file.write("Round " + str(self.round) + "\n")
                file.write("")
                for m in self.matchesRaw:
                    file.write(m[0].__str__() + " vs " + m[1].__str__() + "\n")

            # save what is currently written to disk

            file.flush()
            os.fsync(file.fileno())

    def iter_through_matches(self, mode):
        if mode == "f":
            self.currentMatch += 1
        else:
            self.currentMatch -= 1









































