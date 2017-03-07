from scipy.integrate import odeint
from numpy import array, linspace, meshgrid
from matplotlib.pyplot import figure, plot, grid, legend, xlabel, ylabel, suptitle, show, xlim, ylim, subplot, \
    tight_layout, gca, quiver
from matplotlib.animation import FuncAnimation, writers

a = 1.
b = 0.1
c = 1.5
d = 0.75


def diff(X, t=0):
    return array([a * X[0] - b * X[0] * X[1], -c * X[1] + d * b * X[0] * X[1]])


t = linspace(0, 30, 2000)
X0 = array([10, 5])

X, infodict = odeint(diff, X0, t, full_output=True)
proies, predateurs = X.T
x, y = meshgrid(linspace(0, max(proies) * 1.1, 20), linspace(0, max(predateurs) * 1.1, 20))
dx, dy = a * x - b * x * y, -c * y + d * b * x * y

fig = figure()
# suptitle('Evolution des populations')

subplot(211)
grid()
xlim([min(t), max(t)])
ylim([0, max(max(proies), max(predateurs)) * 1.1])
xlabel('Temps')
ylabel('Population')
p1, = plot([], [], 'r-', label='Proies')
p2, = plot([], [], 'b-', label='Prédateurs')
legend()

subplot(212)
grid()
gca().set_aspect('equal', adjustable='box')
xlim([0, max(proies) * 1.1])
ylim([0, max(predateurs) * 1.1])
xlabel('Proies')
ylabel('Prédateurs')
p3, = plot([], [], 'g-')
p4, = plot([], [], 'go')
quiver(x, y, dx, dy)

tight_layout()


def animate(i):
    p1.set_data(t[:i], proies[:i])
    p2.set_data(t[:i], predateurs[:i])
    p3.set_data(proies[:i], predateurs[:i])
    p4.set_data(proies[i], predateurs[i])
    return p1, p2, p3, p4


ani = FuncAnimation(fig, animate, range(len(t)), interval=10, blit=True)
Writer = writers['ffmpeg']
writer = Writer(fps=100, metadata=dict(artist='Laurent Garcin'), bitrate=18000)
ani.save('test.mp4', writer=writer)

show()
