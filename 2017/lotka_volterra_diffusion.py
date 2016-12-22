from numpy.random import random, normal
from numpy import ndarray
from scipy.ndimage.filters import laplace
from matplotlib.pyplot import imshow, show, figure, axis, subplot
from matplotlib.animation import ArtistAnimation, writers

a = 1.
b = 0.1
c = 1.5
d = 0.75

size = (256, 256)
# u, v = 10 + (2 * random(size) - 1) * .05, 5 + (2 * random(size) - 1) * .05
u, v = normal(10, 1, size), normal(5, 1, size)

# D, k = 0.516, 2.
D, k = 1., 1.

dt = .001

ims = []
fig = figure()
subplot(121)
axis('off')
subplot(122)
axis('off')

N = 20000
for ind in range(N):
    u, v = u + (D * d * laplace(u, mode='wrap') + a * u - b * u * v) * dt, v + (
        k * laplace(v, mode='wrap') - c * v + d * b * u * v) * dt
    if ind % 10 == 0:
        print(str(ind) + "/" + str(N))
        subplot(121)
        imu = imshow(u)
        subplot(122)
        imv = imshow(v)
        ims.append([imu, imv])

ani = ArtistAnimation(fig, ims, interval=10, blit=True, repeat_delay=1000)
Writer = writers['ffmpeg']
writer = Writer(fps=100, metadata=dict(artist='Laurent Garcin'), bitrate=18000)
ani.save('lotka_volterra_diffusion.mp4', writer=writer)
show()
