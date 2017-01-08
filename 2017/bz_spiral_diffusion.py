from numpy.random import random, randint
from scipy.ndimage.filters import laplace, convolve
from matplotlib.pyplot import imshow, show, figure, axis
from matplotlib.animation import ArtistAnimation, writers
from numpy import ndarray, zeros, mgrid, logical_and, roll

size = (256, 256)
a, b, c = random(size), random(size), random(size)
alpha, beta, gamma = 1., 1., 1.
Da, Db, Dc = .1, .1, .1

ims = []
fig = figure(figsize=(4, 4))
axis('off')

kernel = [[1, 1, 1], [1, -8, 1], [1, 1, 1]]


def constrain(v):
    v[v < 0.] = 0.
    v[v > 1.] = 1.
    return v


N = 500
for ind in range(N):
    a, b, c = constrain(a + Da * convolve(a, kernel) + a * (alpha * b - gamma * c)), \
              constrain(b + Db * convolve(b, kernel) + b * (beta * c - alpha * a)), \
              constrain(c + Dc * convolve(c, kernel) + c * (gamma * a - beta * b))
    print(str(ind) + "/" + str(N))
    ims.append([imshow(a, vmin=0., vmax=1.)])

ani = ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
Writer = writers['ffmpeg']
writer = Writer(fps=20, metadata=dict(artist='Laurent Garcin'), bitrate=18000)
ani.save('bz.mp4', writer=writer)
show()
