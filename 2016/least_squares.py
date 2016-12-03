from matplotlib.pyplot import plot, show
from numpy import exp, log, array, vstack, ones
from numpy.linalg import lstsq

t = array([1790, 1800, 1810, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890, 1900, 1910])
P = array([3929, 5308, 7240, 9638, 12866, 17069, 23192, 31443, 38558, 50156, 62948, 75995, 91972])
K = 197273
PP = P / K
ch = log(PP / (1 - PP))
A = vstack([t, ones(len(t))]).T
m, c = lstsq(A, ch)[0]
print(lstsq(A, ch)[1])
print(m, c)
plot(t, P)
plot(t, K / (1 + exp(-m * t - c)))
show()
