from numpy.random import randint
from numpy import bitwise_xor, argmax


def nim_sum():
    return bitwise_xor.reduce(tas)


tas = randint(1, 20, 5)


# while nim_sum() != 0:
#     tas = randint(1, 20, 5)


def random_turn():
    while True:
        t = randint(len(tas))
        if tas[t] != 0:
            break
    n = randint(1, tas[t] + 1)
    tas[t] -= n


def best_turn():
    s = nim_sum()
    l = bitwise_xor(tas, s)
    i = argmax(tas - l)
    if tas[i] > l[i]:
        tas[i] = l[i]
    else:
        random_turn()


print(nim_sum())
j = 0
while sum(tas) != 0:
    best_turn()
    print(j, tas)
    j = (j + 1) % 2

