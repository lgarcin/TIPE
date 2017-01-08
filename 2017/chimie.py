from numpy.random import random, randint
from scipy.ndimage.filters import laplace, convolve
from matplotlib.pyplot import imshow, show, figure, axis
from matplotlib.animation import ArtistAnimation, writers
from numpy import ndarray, zeros, mgrid, array


def laplacian(arrays):
    kernel = [[1, 1, 1], [1, -8, 1], [1, 1, 1]]
    return array([convolve(a, kernel) for a in arrays])
    return array([laplace(a) for a in arrays])


def brusselator(arrays, params):
    x, y = arrays[0], arrays[1]
    a, b = params
    return array([x ** 2 * y - (b + 1) * x + a, -x * 2 * y + b * x])
    # return array([1 - (b + 1) * x + a * x ** 2 * y, b * x - a * x ** 2 * y])


def oregonator(arrays, params):
    x, y = arrays[0], arrays[1]
    e, f, q = params
    return array([(x * (1. - x) - (x - q) / (x + q) * f * y) / e, x - y])


def ball(arrays, params):
    x, y, z = arrays[0], arrays[1], arrays[2]
    a, b, c = params
    return array([x * (a * y - c * z), y * (b * z - a * x), z * (c * x - b * y)])


def constrain(arrays):
    arrays[arrays < 0.] = 0.
    arrays[arrays > 1.] = 1.


def simul(init, N, f, D=None, dt=1.):
    arrays = init
    ims = []
    fig = figure()
    axis('off')

    if D == None:
        D = [1. for _ in range(len(init))]
    for ind in range(N):
        arrays += (f(arrays) + array([a * d for a, d in zip(laplacian(arrays), D)])) * dt
        constrain(arrays)
        if ind % 10 == 0:
            print(str(ind) + "/" + str(N))
            ims.append([imshow(arrays[0].copy(), vmin=0., vmax=1.)])

    ani = ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
    Writer = writers['ffmpeg']
    writer = Writer(fps=100, metadata=dict(artist='Laurent Garcin'), bitrate=18000)
    ani.save('bz.mp4', writer=writer)
    show()


size = (256, 256)
f = lambda arrays: oregonator(arrays, (.3, 1, 2e-2))
# init = array([random(size), random(size), random(size)])
init = array([zeros(size), zeros(size)])
for _ in range(50):
    init[0, randint(size[0]), randint(size[1])] = 1
simul(init, 10000, f, [.1, .0], dt=.005)
