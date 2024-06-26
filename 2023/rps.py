import random
from collections import defaultdict


class RPSEngine:
    RPS = {
        "R": "P",
        "P": "S",
        "S": "R",
    }

    def __init__(self, order=6):
        self.order = order
        self.db = defaultdict(lambda: {"R": 0, "P": 0, "S": 0})
        self.state = []

    def learn(self, player_input):
        if len(self.state) == self.order:
            self.db[tuple(self.state)][player_input] += 1
            del self.state[0]
        self.state.append(player_input)

    def decide(self):
        if len(self.state) == self.order:
            possible = sorted(self.db[tuple(self.state)].items(), key=lambda i: i[1], reverse=True)
            if possible[0][1] == 0:
                return random.choice(list(self.RPS.keys()))
            else:
                return self.RPS[possible[0][0]]
        else:
            return random.choice(list(self.RPS.keys()))


class Player(object):
    @staticmethod
    def play():
        while True:
            player_input = input("Votre choix : R(ock), P(aper), S(scissors) ou Q(uitter) ")
            if player_input in ("R", "P", "S", "Q"):
                break
        return player_input


rps_engine = RPSEngine()
player = Player()

player_score = 0
engine_score = 0
while True:
    inp = player.play()
    if inp == "Q":
        break
    out = rps_engine.decide()
    print(out)
    rps_engine.learn(inp)
    if rps_engine.RPS[inp] == out:
        engine_score += 1
    if rps_engine.RPS[out] == inp:
        player_score += 1
    print(f"Player score : {player_score} / Engine score : {engine_score}")
