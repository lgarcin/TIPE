from numpy.random import random, randint
from numpy import ndarray, logical_and, array_equal, where, zeros, uint8
from matplotlib.pyplot import imshow, show, axis, imsave, subplot, savefig, title, suptitle, subplots_adjust, figure
from scipy.ndimage.morphology import binary_dilation
from matplotlib.animation import ArtistAnimation, writers

N = 256
p = .6

grid = random((N, N)) < p
access = ndarray((N, N))
access.fill(False)
a = access.copy()
im = zeros((N, N, 3), dtype=uint8)
im[where(grid)] = [0, 0, 255]

# x, y = where(grid)
# n = randint(len(x))
# i, j = x[n], y[n]
# a[i, j] = grid[i, j]

a[0, :] = grid[0, :]

ims = []
fig = figure()
axis('off')

while not array_equal(access, a):
    access = a.copy()
    a = logical_and(binary_dilation(a), grid)
    im = im.copy()
    im[where(a)] = [255, 0, 0]
    # ims.append([imshow(access, cmap='gray')])
    ims.append([imshow(im)])

ani = ArtistAnimation(fig, ims, interval=10, blit=True, repeat_delay=1000)
Writer = writers['ffmpeg']
writer = Writer(fps=100, metadata=dict(artist='Laurent Garcin'), bitrate=18000)
ani.save('perco_site.mp4', writer=writer)
show()
