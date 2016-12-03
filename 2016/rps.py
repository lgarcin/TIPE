import random
from collections import defaultdict

ORDER = 6


class RPSEngine(object):
    RPS = {
        "R": "P",
        "P": "S",
        "S": "R",
    }

    def __init__(self):
        self.db = defaultdict(lambda: {"R": 0, "P": 0, "S": 0})
        self.state = []

    def learn(self, inp):
        if len(self.state) == ORDER:
            self.db[tuple(self.state)][inp] += 1
            del self.state[0]
        self.state.append(inp)

    def decide(self):
        if len(self.state) == ORDER:
            possible = sorted(self.db[tuple(self.state)].items(), key=lambda i: i[1], reverse=True)
            if possible[0][1] == 0:
                return random.choice(list(self.RPS.keys()))
            else:
                return self.RPS[possible[0][0]]
        else:
            return random.choice(list(self.RPS.keys()))


class Player(object):
    def play(self):
        while True:
            inp = input("Votre choix : ")
            if inp in ("R", "P", "S"):
                break
        return inp


rpsengine = RPSEngine()
player = Player()

while True:
    inp = player.play()
    out = rpsengine.decide()
    print(out)
    rpsengine.learn(inp)
