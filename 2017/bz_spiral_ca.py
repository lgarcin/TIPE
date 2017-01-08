from numpy.random import random, randint
from scipy.ndimage.filters import laplace
from matplotlib.pyplot import imshow, show, figure, axis
from matplotlib.animation import ArtistAnimation, writers
from numpy import ndarray, zeros, mgrid, logical_and, roll

size = (256, 256)
a, b, c = random(size), random(size), random(size)
alpha, beta, gamma = 1., 1., 1.

ims = []
fig = figure(figsize=(4, 4))
axis('off')


def avg(v):
    return (v + roll(v, 1, 0) + roll(v, -1, 0) + roll(v, 1, 1) + roll(v, -1, 1) + roll(roll(v, 1, 0), 1, 1) + roll(
        roll(v, -1, 0), 1, 1) + roll(roll(v, 1, 0), -1, 1) + roll(roll(v, -1, 0), -1, 1)) / 9.


def constrain(v):
    v[v < 0.] = 0.
    v[v > 1.] = 1.
    return v


N = 200
for ind in range(N):
    aa, bb, cc = avg(a), avg(b), avg(c)
    a = constrain(aa + aa * (alpha * bb - gamma * cc))
    b = constrain(bb + bb * (beta * cc - alpha * aa))
    c = constrain(cc + cc * (gamma * aa - beta * bb))
    print(str(ind) + "/" + str(N))
    ims.append([imshow(a, vmin=0., vmax=1.)])

ani = ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
Writer = writers['ffmpeg']
writer = Writer(fps=20, metadata=dict(artist='Laurent Garcin'), bitrate=18000)
ani.save('bz.mp4', writer=writer)
print(writer.frame_size)
show()
