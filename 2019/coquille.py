import numpy as np

N1 = 1000
N2 = 6000

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


def laplacien(x):
    return np.roll(x, 1) + np.roll(x, -1) - 2 * x


mu = .1
rho0 = .004
sigma = np.linspace(0.012, 0.038, N1)
nu = 0
Da = .1
Ds = .1
kappa = 1
rho = .5
step = 1


def evol(a, s, dt, N):
    la = []
    ls = []
    for n in range(N):
        a2 = a ** 2 / (1 + kappa * a ** 2) + rho0
        da = rho * s * a2 - mu * a + Da * laplacien(a)
        ds = sigma - rho * s * a2 - nu * s + Ds * laplacien(s)
        a += da * dt
        s += ds * dt
        if n % step == 0:
            la.append(a.copy())
            ls.append(s.copy())
    return np.array(la), np.array(ls)


a = np.ones(N1) * 0
s = np.ones(N1) * 0
la, ls = evol(a, s, 1, step * N2)

from mayavi import mlab

print(X.shape, la.shape)

mesh = mlab.mesh(X, Y, Z, scalars=ls, colormap='autumn')
mlab.show()
