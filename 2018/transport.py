from numpy import roll, pi, sin, cos, linspace
from matplotlib.pyplot import plot, show, figure, draw
from matplotlib.animation import FuncAnimation


class Transport1D:
    def __init__(self):
        N = 100
        self.dx = 1. / N
        cfl = .01
        self.c = 100.
        self.dt = cfl * self.dx / self.c
        self.t = 0
        x = linspace(0, 1, N)
        self.u = sin(2 * pi * x)
        self.fig = figure()
        self.line, = plot(x, self.u)
        self.timer = self.fig.canvas.new_timer(interval=1)
        self.timer.add_callback(self.update)
        self.timer.start()
        show()

    def update(self):
        self.t += self.dt
        self.u += self.c * (roll(self.u, 1) - roll(self.u, -1)) / (2 * self.dx) * self.dt
        self.line.set_ydata(self.u)
        draw()


tr = Transport1D()
