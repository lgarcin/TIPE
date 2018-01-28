import numpy as np
import matplotlib.pyplot as plt


class Transport1D:
    def __init__(self):
        N = 200
        self.dx = 1. / N
        cfl = .1
        self.c = 100.
        self.dt = cfl * self.dx / self.c
        self.t = 0
        self.x = np.linspace(0, 1, N)
        self.u = np.sin(2 * np.pi * self.x) * 0
        self.u[0] = 1
        self.fig = plt.figure()
        self.line, = plt.plot(self.x, self.u)
        self.timer = self.fig.canvas.new_timer(interval=1)
        self.timer.add_callback(self.update)
        self.timer.start()
        plt.show()

    def update(self):
        self.t += self.dt
        if 100 * self.t - np.floor(100 * self.t) < 1 / 5:
            self.u[0] = 1
        else:
            self.u[0] = 0
        self.u[1:] -= self.c * (1 - self.u[1:]) * (self.u[1:] - self.u[:-1]) / self.dx * self.dt
        self.line.set_ydata(self.u)
        plt.draw()


from matplotlib.animation import FuncAnimation, writers


class Transport1DAnimate:
    def __init__(self):
        N = 200
        self.dx = 1. / N
        cfl = .1
        self.c = 100.
        self.dt = cfl * self.dx / self.c
        self.t = 0
        self.x = np.linspace(0, 1, N)
        self.u = np.sin(2 * np.pi * self.x) * 0
        self.u[0] = 1
        self.fig = plt.figure()
        self.line, = plt.plot(self.x, self.u)
        ani = FuncAnimation(self.fig, self.update, range(10000), interval=10, blit=True)
        Writer = writers['ffmpeg']
        writer = Writer(fps=100, metadata=dict(artist='Laurent Garcin'), bitrate=18000)
        ani.save('transport.mp4', writer=writer)
        plt.show()

    def update(self, i):
        self.t += self.dt
        if 100 * self.t - np.floor(100 * self.t) < 1 / 5:
            self.u[0] = 1
        else:
            self.u[0] = 0
        self.u[1:] -= self.c * (1 - self.u[1:]) * (self.u[1:] - self.u[:-1]) / self.dx * self.dt
        self.line.set_ydata(self.u)
        return self.line,


tr = Transport1DAnimate()
