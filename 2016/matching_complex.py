from numpy import mean, linspace, absolute, angle, exp
from numpy.random import uniform, normal
from matplotlib.pyplot import scatter, show, figure
from matplotlib.animation import ArtistAnimation

nb = 10
z = uniform(-3, 3, nb) + 1j * uniform(-3, 3, nb)
a = 2 + 2j
b = 3 - 2j
Z = a * (z + normal(0, .01) + 1j * normal(0, .01)) + b
z0 = mean(z)
Z0 = mean(Z)
zz = z - z0
ZZ = Z - Z0
aa = sum(zz.conjugate() * ZZ) / sum(zz * zz.conjugate())
bb = Z0 - aa * z0

center = bb / (1 - aa)
mod = absolute(aa)
arg = angle(aa)

fig = figure()
ims = []
for t in linspace(0, 1, 100):
    m = (1 - t) + t * mod
    a = t * arg
    a_current = m * exp(1j * a)
    current = center + a_current * (z - center)
    # current = (1 - t) * z + t * (aa * z + bb)
    ims.append((scatter(z.real, z.imag, color='blue'), scatter(Z.real, Z.imag, color='red'),
                scatter(current.real, current.imag)))
im_ani = ArtistAnimation(fig, ims, interval=50, repeat_delay=3000, blit=True)
im_ani.save('test.mp4')
show()
