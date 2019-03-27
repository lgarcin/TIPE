from math import sqrt, hypot, atan2, asin, sin
import matplotlib.pyplot as plt

dt = .001
V = 1
Vc = .2


def naive():
    x, y = 0, 0
    t = 0
    X, Y = [x], [y]
    Vx, Vy = [], []
    while y < 1:
        n = sqrt(x ** 2 + (1 - y) ** 2)
        vx = -V * x / n
        vy = V * (1 - y) / n
        Vx.append(vx)
        Vy.append(vy)
        x += (vx + Vc) * dt
        y += vy * dt
        t += dt
        X.append(x)
        Y.append(y)
    Vx.append(0)
    Vy.append(0)
    return X, Y, Vx, Vy, t


def clever():
    x, y = 0, 0
    t = 0
    X, Y = [x], [y]
    vx = -Vc
    vy = sqrt(V ** 2 - vx ** 2)
    Vx, Vy = [vx], [vy]
    while y < 1:
        x += (vx + Vc) * dt
        y += vy * dt
        t += dt
        X.append(x)
        Y.append(y)
        Vx.append(vx)
        Vy.append(vy)
    return X, Y, Vx, Vy, t


def adapt():
    x, y = 0, 0
    t = 0
    X, Y = [x], [y]
    est_vx, est_vy = 0, 0
    while y < 1:
        vx = vx
        vy = vy
        n_est, ang_est = hypot(est_vx, est_vy), atan2(est_vx, est_vy)
        dir = atan2(-x, 1 - y)
        ang = asin(n_est / V * sin(dir - ang_est))


def plot(X, Y, Vx, Vy):
    plt.axis('equal')
    plt.plot(X, Y)
    step = 100
    plt.quiver(X[::step], Y[::step], Vx[::step], Vy[::step])
    plt.show()


plot(*naive()[:-1])
plot(*clever()[:-1])
