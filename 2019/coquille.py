import numpy as np

N1 = 1000
N2 = 2000

s = np.linspace(0, 2 * np.pi, N1)
t = np.linspace(0, 6 * np.pi, N2)

S, T = np.meshgrid(s, t)

D = 1
A = 90
alpha = 86 * np.pi / 180
beta = 10 * np.pi / 180
mu = 5 * np.pi / 180
Omega = 1 * np.pi / 180
phi = -45 * np.pi / 180
a = 20
b = 20


def re(s):
    return ((np.cos(s) / a) ** 2 + (np.sin(s) / b) ** 2) ** (-1 / 2)


X = D * (A * np.sin(beta) * np.cos(T) + np.cos(S + phi) * np.cos(T + Omega) * re(S) - np.sin(mu) * np.sin(
    S + phi) * np.sin(T + Omega) * re(S)) * np.exp(T / np.tan(alpha))

Y = (A * np.sin(beta) * np.sin(T) + np.cos(S + phi) * np.sin(T + Omega) * re(S) + np.sin(mu) * np.sin(
    S + phi) * np.cos(T + Omega) * re(S)) * np.exp(T / np.tan(alpha))

Z = (-A * np.cos(beta) + np.cos(mu) * np.sin(S + phi) * re(S)) * np.exp(T / np.tan(alpha))

from scipy.ndimage.filters import laplace


def laplacien(x):
    # return laplace(x, mode='wrap')
    return np.roll(x, 1) + np.roll(x, -1) - 2 * x


def evol1(a, s, dt, N):
    la = []
    ls = []
    mu = .01
    rho0 = .0025
    sigma = (1 + np.sin(np.linspace(0, 10 * np.pi, N1))) / 2 * .11
    # sigma = .015
    nu = .002
    Da = .01
    Ds = .05
    kappa = .5
    rho = .1 * (1 + np.random.uniform(-.025, .025, N1))
    step = 10
    for n in range(N * step):
        a2 = a ** 2 / (1 + kappa * a ** 2) + rho0
        da = rho * s * a2 - mu * a + Da * laplacien(a)
        ds = sigma - rho * s * a2 - nu * s + Ds * laplacien(s)
        a += da * dt
        s += ds * dt
        if n % step == 0:
            la.append(a.copy())
            ls.append(s.copy())
    return np.array(la), np.array(ls)


# def evol2(a, h, dt, N):
#     la = []
#     lh = []
#     mu = .05
#     rho0 = .02
#     rho1 = .0075
#     nu = .03
#     Da = .1
#     Dh = .0
#     kappa = .0004
#     rho = .05 + np.random.uniform(-.05, .05) * 15 / 100
#     step = 1
#     for n in range(N * step):
#         a2 = a ** 2 / (1 + kappa * a ** 2)
#         da = rho * (a2 + rho0) / h - mu * a + Da * laplacien(a)
#         dh = rho * a2 - nu * h + Dh * laplacien(h) + rho1
#         a += da * dt
#         h += dh * dt
#         if n % step == 0:
#             la.append(a.copy())
#             lh.append(h.copy())
#     return np.array(la), np.array(lh)


a = np.ones(N1) * 0
s = np.ones(N1) * 0
la, ls = evol1(a, s, .1, N2)
la /= la.max(axis=0)[np.newaxis, :]
ls /= ls.max(axis=0)[np.newaxis, :]

# a = np.random.uniform(.1, .2, N1)
# h = np.random.uniform(.1, .2, N1)
# la, lh = evol2(a, h, 1, N2)


from mayavi import mlab

mesh = mlab.mesh(X, Y, Z, scalars=ls, colormap='autumn')
mlab.show()
