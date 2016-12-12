from numpy.random import random
from numpy import ndarray
from matplotlib.pyplot import imshow, show, axis, imsave, subplot, savefig, title, suptitle, subplots_adjust
import sys

sys.setrecursionlimit(10000)
N = 256
p = .6


def simul(N, p):
    grid = random((N, N)) < p
    access = ndarray((N, N))
    access.fill(False)
    visit = ndarray((N, N))
    visit.fill(False)

    def flow(i, j):
        if grid[i][j]:
            access[i][j] = True
            visit[i][j] = True
            if i < N - 1 and not visit[i + 1][j]:
                flow(i + 1, j)
            if i > 0 and not visit[i - 1][j]:
                flow(i - 1, j)
            if j < N - 1 and not visit[i][j + 1]:
                flow(i, j + 1)
            if j > 0 and not visit[i][j - 1]:
                flow(i, j - 1)

    for j in range(N):
        flow(0, j)
    subplot(121)
    axis('off')
    imshow(grid, cmap='gray')
    title('Sites')
    subplot(122)
    axis('off')
    imshow(access, cmap='gray')
    title('Chemins')
    subplots_adjust(top=1.2)
    result = any(access[-1, :])
    if result:
        suptitle('Dernière ligne atteinte' + ' p=' + str(p))
    else:
        suptitle('Dernière ligne non atteinte' + ' p=' + str(p))
    savefig('perco.jpeg', bbox_inches='tight')
    return result


print(simul(N, p))

# nb = 1000
# print(sum([simul(N, p) for _ in range(nb)]) / nb)
