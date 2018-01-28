from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from matplotlib.collections import PatchCollection

ims = []


def plot_config(config):
    plt.gca().axis([-N, 5 * N, 0, N])
    patches = []
    for piquet in Piquet.A, Piquet.B, Piquet.C:
        if piquet == Piquet.A:
            x = 0
        elif piquet == Piquet.B:
            x = 2 * N
        elif piquet == Piquet.C:
            x = 4 * N
        y = 0
        for anneau in config[piquet]:
            patches.append(plt.Rectangle((x - anneau, y), anneau * 2, 1))
            y += 1
    ims.append(
        (plt.gca().add_collection(PatchCollection(patches)),
         plt.text(-N + 1, N - 1, 'Itération ' + ' ' + str(config['iter']))))


class Piquet(Enum):
    A = 1
    B = 2
    C = 3


N = 7

config = {
    'iter': 0,
    Piquet.A: list(range(N, 0, -1)),
    Piquet.B: [],
    Piquet.C: []
}

fig = plt.figure()
plot_config(config)


def hanoi(n, A, B, C):
    if n > 0:
        hanoi(n - 1, A, C, B)
        config[A].pop()
        config[C].append(n)
        config['iter'] += 1
        plot_config(config)
        hanoi(n - 1, B, A, C)


hanoi(N, Piquet.A, Piquet.B, Piquet.C)
im_ani = ArtistAnimation(fig, ims, interval=50, repeat_delay=1000, blit=True)
im_ani.save('hanoi.mp4')
plt.show()
