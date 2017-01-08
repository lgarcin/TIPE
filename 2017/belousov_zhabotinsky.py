from numpy.random import random, randint
from scipy.ndimage.filters import laplace, convolve
from matplotlib.pyplot import imshow, show, figure, axis
from matplotlib.animation import ArtistAnimation, writers
from numpy import ndarray, zeros, mgrid, logical_and

size = (256, 256)
u, v = zeros(size), zeros(size)

for _ in range(20):
    u[randint(size[0]), randint(size[1])] = 1.

dt = .005
e, q, f = .3, 5e-3, 1.
Du, Dv = 0.1, 0.

kernel = [[1, 1, 1], [1, -8, 1], [1, 1, 1]]


def constrain(v):
    v[v < 0.] = 0.
    v[v > 1.] = 1.
    return v


ims = []
fig = figure()
axis('off')

N = 20000
for ind in range(N):
    # u, v = u + (Du * laplace(u) + (u * (1. - u) - (u - q) / (u + q) * f * v) / e) * dt, \
    #        v + (Dv * laplace(v) + u - v) * dt
    u, v = constrain(u + (Du * convolve(u, kernel) + (u * (1. - u) - (u - q) / (u + q) * f * v) / e) * dt), \
           constrain(v + (Dv * convolve(v, kernel) + u - v) * dt)
    if ind % 10 == 0:
        print(str(ind) + "/" + str(N))
        ims.append([imshow(u)])

ani = ArtistAnimation(fig, ims, interval=10, blit=True, repeat_delay=1000)
Writer = writers['ffmpeg']
writer = Writer(fps=100, metadata=dict(artist='Laurent Garcin'), bitrate=18000)
# ani.save('bz.mp4', writer=writer)
show()
