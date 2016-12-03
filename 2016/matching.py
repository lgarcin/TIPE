from numpy import mean, ones, mat
from numpy.random import uniform, normal
from numpy.linalg import qr, svd, det, norm

nb = 30
n = 2

X = mat(uniform(10, 20, (n, nb)))
A = uniform(10, 20, (n, n))
R = qr(A)[0]
T = uniform(-1, 1, (n, 1))
Y = R.dot(X) + T.dot(ones((1, nb))) + normal(0, .1, (n, nb))
X0 = mean(X, 1)
Y0 = mean(Y, 1)
XX = X - X0.dot(ones((1, nb)))
YY = Y - Y0.dot(ones((1, nb)))
u, s, v = svd(YY.dot(XX.T))
RR = u.dot(v)
TT = Y0 - R.dot(X0)
print(norm(Y - RR.dot(X) - TT.dot(ones((1, nb)))))
