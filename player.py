# each player has a name, a rating, which has a default value of ___ if they do not have a fargo rating, and isBye
# by default isBye is set to false, but if a player is high enough seeded it will be True
class Player:
    def __init__(self, name, rating=300, state="USA"):
        self.name = name
        self.rating = rating
        self.state = state
        self.isBye = False

    def __str__(self):
        if self.rating == -1 or self.rating == 0:
            return f"{self.name}"
        else:
            return f"{self.name}, {self.rating}"



