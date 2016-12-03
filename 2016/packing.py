from random import uniform as ran, choice
import matplotlib.pyplot as plt
import matplotlib.animation as animation

L = [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)]
sigma = 0.15
delta = 0.15
square_x = [0, 1, 1, 0, 0];
square_y = [0, 0, 1, 1, 0]
number = 0

fig = plt.figure()
ims = []
for iter in range(100):
    a = choice(L)
    L.remove(a)
    b = (a[0] + ran(-delta, delta), a[1] + ran(-delta, delta))
    min_dist = min((b[0] - x[0]) ** 2 + (b[1] - x[1]) ** 2 for x in L)
    box_cond = min(b[0], b[1]) < sigma or max(b[0], b[1]) > 1 - sigma
    if box_cond or min_dist < 4 * sigma ** 2:
        L.append(a)
    else:
        L.append(b)
    if iter % 1 == 0:
        number += 1
        plt.axes()
        for x, y in L:
            cir = plt.Circle((x, y), radius=sigma, fc='r')
            plt.gca().add_patch(cir)
        plt.axis('equal')
        ims.append((plt.plot(square_x, square_y),))

im_ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=3000, blit=True)
plt.show()
