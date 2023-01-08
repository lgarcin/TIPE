from numpy.random import randint
from numpy import bitwise_xor, argmax


class NimGame:
    def __init__(self):
        self.tas = randint(1, 20, 5)

    def nim_sum(self):
        return bitwise_xor.reduce(self.tas)

    def random_turn(self):
        while True:
            t = randint(len(self.tas))
            if self.tas[t] != 0:
                break
        n = randint(1, self.tas[t] + 1)
        self.tas[t] -= n
        print("Prend ", n, " allumettes dans le tas ", t)

    def best_turn(self):
        s = self.nim_sum()
        l = bitwise_xor(self.tas, s)
        i = argmax(self.tas - l)
        if self.tas[i] > l[i]:
            print("Prend ", self.tas[i] - l[i], " allumettes dans le tas ", i)
            self.tas[i] = l[i]
        else:
            self.random_turn()

    def play(self):
        print(self.nim_sum())
        j = 0
        while sum(self.tas) != 0:
            print("Joueur ", j)
            print("Tas", self.tas)
            self.best_turn()
            j = (j + 1) % 2
            print("\n")


nim_game = NimGame()
nim_game.play()
