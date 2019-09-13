from enum import Enum

import matplotlib.pyplot as plt


def plot_config(config):
    plt.clf()
    plt.gca().axis([-N, 5 * N, 0, N])
    for piquet in Piquet.A, Piquet.B, Piquet.C:
        if piquet == Piquet.A:
            x = 0
        elif piquet == Piquet.B:
            x = 2 * N
        elif piquet == Piquet.C:
            x = 4 * N
        y = 0
        for anneau in config[piquet]:
            plt.gca().add_patch(plt.Rectangle((x - anneau, y), anneau * 2, 1))
            y += 1


class Piquet(Enum):
    A = 1
    B = 2
    C = 3


N = 4

config = {
    Piquet.A: list(range(N, 0, -1)),
    Piquet.B: [],
    Piquet.C: []
}

plot_config(config)


def hanoi(n, A, B, C):
    if n > 0:
        hanoi(n - 1, A, C, B)
        config[A].pop()
        config[C].append(n)
        plt.waitforbuttonpress()
        plot_config(config)
        hanoi(n - 1, B, A, C)


hanoi(N, Piquet.A, Piquet.B, Piquet.C)
plt.show()
