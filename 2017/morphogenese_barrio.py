from numpy.random import random
from scipy.ndimage.filters import laplace
from matplotlib.pyplot import imshow, show, figure, axis
from matplotlib.animation import ArtistAnimation, writers

size = (256, 256)
u, v = (2 * random(size) - 1) * .05, (2 * random(size) - 1) * .05

# D, a, b, c, d, r1, r2 = 0.516, 0.899, -.91, -.899, 2., 2., 0.
D, a, b, c, d, r1, r2 = 0.516, 0.899, -.91, -.899, 2., 2., .367

dt = .1

ims = []
fig = figure()
axis('off')

N = 10000
for ind in range(N):
    u, v = u + (D * d * laplace(u, mode='wrap') + a * u * (1 - r1 * v ** 2) + v * (1 - r2 * u)) * dt, v + (
        d * laplace(v, mode='wrap') + v * (b + a * r1 * u * v) + u * (c + r2 * v)) * dt
    if ind % 10 == 0:
        print(str(ind) + "/" + str(N))
        ims.append([imshow(u)])

ani = ArtistAnimation(fig, ims, interval=10, blit=True, repeat_delay=1000)
Writer = writers['ffmpeg']
writer = Writer(fps=100, metadata=dict(artist='Laurent Garcin'), bitrate=18000)
ani.save('morpho.mp4', writer=writer)
show()
