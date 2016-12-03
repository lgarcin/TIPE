from random import uniform, choice, random
from math import exp

nbobjects = 1000
objects = {k: {'value': uniform(40, 50), 'weight': uniform(1, 5)} for k in range(nbobjects)}
max_weight = 100
sack = {}
o = objects.copy()
s = sack.copy()

T = 10
value = 0
while T > .01:
    i = choice(list(objects.keys()))
    sack[i] = objects.pop(i)
    j = None
    while sum([sack[k]['weight'] for k in sack if k != j]) > max_weight:
        j = choice(list(sack.keys()))
    if j is not None:
        objects[j] = sack.pop(j)
    v = sum([sack[k]['value'] for k in sack])
    if random() > exp((v - value) / T):
        if i != j:
            objects[i] = sack.pop(i)
            sack[j] = objects.pop(j)
    else:
        value = v
    T *= .999

print(value)

objects = o
sack = s
T = 10
value = 0
while T > .01:
    i = choice(list(objects.keys()))
    sack[i] = objects.pop(i)
    j = None
    while sum([sack[k]['weight'] for k in sack if k != j]) > max_weight:
        j = choice(list(sack.keys()))
    if j is not None:
        objects[j] = sack.pop(j)
    v = sum([sack[k]['value'] for k in sack])
    if v - value < 0:
        if i != j:
            objects[i] = sack.pop(i)
            sack[j] = objects.pop(j)
    else:
        value = v
    T *= .999

print(value)
