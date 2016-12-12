from numpy.random import random
from numpy import zeros
from scipy.ndimage.filters import laplace
from matplotlib.pyplot import imshow, show, figure, axis
from matplotlib.animation import ArtistAnimation, writers

size = (256, 256)
u, v = zeros(size), zeros(size)
u[...] = 1
r = 20
u[size[0] // 2 - r:size[0] // 2 + r, size[1] // 2 - r:size[1] // 2 + r] = .5
v[size[0] // 2 - r:size[0] // 2 + r, size[1] // 2 - r:size[1] // 2 + r] = .25
u += random(size) * .05
v += random(size) * .05

params = []
params.append((0.16, 0.08, 0.035, 0.065))  # Bacteria 1
params.append((0.14, 0.06, 0.035, 0.065))  # Bacteria 2
params.append((0.16, 0.08, 0.060, 0.062))  # Coral
params.append((0.19, 0.05, 0.060, 0.062))  # Fingerprint
params.append((0.10, 0.10, 0.018, 0.050))  # Spirals
params.append((0.12, 0.08, 0.020, 0.050))  # Spirals Dense
params.append((0.10, 0.16, 0.020, 0.050))  # Spirals Fast
params.append((0.16, 0.08, 0.020, 0.055))  # Unstable
params.append((0.16, 0.08, 0.050, 0.065))  # Worms 1
params.append((0.16, 0.08, 0.054, 0.063))  # Worms 2
params.append((0.16, 0.08, 0.035, 0.060))  # Zebrafish
(du, dv, f, k) = params[1]

dt = 1.

ims = []
fig = figure()
axis('off')

N = 20000
for ind in range(N):
    u, v = u + (du * laplace(u, mode='wrap') - u * v ** 2 + f * (1. - u)) * dt, v + (
        dv * laplace(v, mode='wrap') + u * v ** 2 - (k + f) * v) * dt
    if ind % 10 == 0:
        print(str(ind) + "/" + str(N))
        ims.append([imshow(v)])

ani = ArtistAnimation(fig, ims, interval=10, blit=True, repeat_delay=1000)
Writer = writers['ffmpeg']
writer = Writer(fps=100, metadata=dict(artist='Laurent Garcin'), bitrate=18000)
ani.save('morpho.mp4', writer=writer)
show()
