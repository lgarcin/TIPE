from numpy import array
from numpy.linalg import norm
from matplotlib.pyplot import plot, show, figure, xlim, ylim
from matplotlib.animation import FuncAnimation


class Boid:
    def __init__(self, pos, vel, max_speed, max_force):
        self.position = pos
        self.velocity = vel
        self.acceleration = array([0., 0.])
        self._max_speed = max_speed
        self._max_force = max_force

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        self._position = pos

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, vel):
        self._velocity = vel

    @property
    def acceleration(self):
        return self._acceleration

    @velocity.setter
    def acceleration(self, acc):
        self._acceleration = acc

    def update(self):
        self.velocity += self.acceleration
        ns = norm(self.velocity)
        if ns > self._max_speed:
            self.velocity /= ns
            self.velocity *= self._max_speed
        self.position += self.velocity
        self.acceleration = array([0., 0.])

    def applyForce(self, force):
        self.acceleration += force

    def seek(self, target):
        desired = target - self.position
        desired = desired / norm(desired) * self._max_speed
        steer = desired - self.velocity
        ns = norm(steer)
        if ns > self._max_force:
            steer /= ns
            steer *= self._max_force
        self.applyForce(steer)


boids = Boid(array([0., 0.]), array([2., -2.]), 1., .1)
l = []
target = array([40., 40.])
N = 100
for _ in range(N):
    l.append(boids.position.copy())
    # target += array([.1, .1])
    boids.seek(target)
    boids.update()

l = array(l)
# print(l)
# plot(l[:, 0], l[:, 1])

fig = figure()

xlim(min(l[:, 0]), max(l[:, 0]))
ylim(min(l[:, 1]), max(l[:, 1]))
p, = plot([], [], 'g-')


def animate(i):
    p.set_data(l[:i, 0], l[:i, 1])
    return p,


ani = FuncAnimation(fig, animate, range(N), interval=10, blit=True)
show()
