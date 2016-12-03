from numpy import zeros
from numpy.random import randint
from pprint import pprint

nbobjects = 1000
objects = [{'value': randint(10, 1000), 'weight': randint(1, 10)} for _ in range(nbobjects)]
max_weight = 100
sack = {}

t = zeros((nbobjects, max_weight + 1), dtype=int)
k = zeros((nbobjects, max_weight + 1), dtype=bool)

for w in range(max_weight + 1):
    t[0, w] = 0
for i in range(nbobjects):
    for w in range(max_weight + 1):
        if objects[i]['weight'] <= w and objects[i]['value'] + t[i - 1, w - objects[i]['weight']] > t[
                    i - 1, w]:
            t[i, w] = objects[i]['value'] + t[i - 1, max_weight - objects[i]['weight']]
            k[i, w] = True
        else:
            t[i, w] = t[i - 1, w]
            k[i, w] = False

print(t[-1, w])

sack = []
w = max_weight
for i in reversed(range(nbobjects)):
    if k[i, w]:
        sack.append(objects[i])
        w -= objects[i]['weight']

pprint(sack)
