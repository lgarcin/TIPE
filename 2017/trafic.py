from random import random
from matplotlib.pyplot import imshow, show, axis, subplot, title, savefig

evolution = {
    (True, True, True): True,
    (True, True, False): False,
    (True, False, True): True,
    (True, False, False): True,
    (False, True, True): True,
    (False, True, False): False,
    (False, False, True): False,
    (False, False, False): False
}

N = 512
nb = 128
i = 0
lp = (.25, .5, .75)
for p in lp:
    ca = [random() < p for _ in range(N)]
    im = []
    for _ in range(nb):
        ca = [True] + ca + [False]
        ca = [evolution[tuple(ca[m:m + 3])] for m in range(N - 2)]
        im.append(ca)
    i += 1
    subplot(len(lp), 1, i)
    imshow(im, cmap='gray_r')
    axis('off')
    title("Probabilité " + str(p))
savefig('trafic.jpeg', bbox_inches='tight', dpi=200)
show()
