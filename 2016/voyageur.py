from itertools import combinations, permutations
from random import sample, random, randint, uniform
from math import exp, sqrt, log
from matplotlib.pyplot import plot, show, figure, axis


def distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


xmin, xmax, ymin, ymax = -10, 10, -10, 10

# villes = ["Paris", "Lyon", "Marseille", "Tombouctou", "Bangkok"]
villes = list(range(30))
locations = {ville: (uniform(xmin, xmax), uniform(ymin, ymax)) for ville in villes}
distances = {pair: distance(locations[pair[0]], locations[pair[1]]) for pair in combinations(villes, 2)}


def longueur(chemin):
    l = 0
    n = len(chemin)
    for k in range(n):
        if (chemin[k], chemin[(k + 1) % n]) in distances:
            l += distances[chemin[k], chemin[(k + 1) % n]]
        else:
            l += distances[chemin[(k + 1) % n], chemin[k]]
    return l


c = villes.copy()
best_c = villes.copy()
l = longueur(c)
best_l = l
n = len(villes)
li = [l]
T = 100
nb = 0
while T > .001:
    i, j = sample(range(n), 2)
    c[i], c[j] = c[j], c[i]
    ll = longueur(c)
    # if random() > exp((l - ll) / T):
    p = random()
    if log(p) > (l - ll) / T:
        c[i], c[j] = c[j], c[i]
    else:
        l = ll
    if l < best_l:
        best_l = l
        best_c = c.copy()
    T *= .99999
    # nb += 1
    # if nb % 1000 == 0:
    #     l = best_l
    #     c = best_c.copy()
    li.append(l)
# print(min([longueur(c) for c in permutations(villes)]))
l = best_l
c = best_c.copy()
print(c, longueur(c))

chemin = c + [c[0]]
figure()
axis([xmin, xmax, ymin, ymax])
plot([locations[ville][0] for ville in chemin], [locations[ville][1] for ville in chemin], marker='.')
figure()
plot(li)
show()
