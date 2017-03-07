from numpy import array
from numpy.linalg import norm
from matplotlib.pyplot import plot, show, xlim, ylim, figure, gca
from random import random


class Boid:
    def __init__(self, pos, vel, max_speed, max_force):
        self.position = pos
        self.velocity = vel
        self.acceleration = array([0., 0.])
        self.max_speed = max_speed
        self.max_force = max_force
        self.r = 2
        self.p, = plot([], [], 'go')

    def update(self):
        self.velocity += self.acceleration
        ns = norm(self.velocity)
        if ns > self.max_speed:
            self.velocity /= ns
            self.velocity *= self.max_speed
        self.position += self.velocity
        self.acceleration = array([0., 0.])
        self.p.set_data(self.position[0], self.position[1])

    def applyForce(self, force):
        self.acceleration += force

    def seek(self, target):
        desired = target - self.position
        nd = norm(desired)
        if nd > 0:
            desired = desired / nd * self.max_speed
            steer = desired - self.velocity
            ns = norm(steer)
            if ns > self.max_force:
                steer /= ns
                steer *= self.max_force
            self.applyForce(steer)

    def separate(self, boids):
        desiredseparation = self.r * 2
        sum = array([0., 0.])
        count = 0;
        for b in boids:
            d = norm(self.position - b.position)
            if d > 0 and d < desiredseparation:
                diff = self.position - b.position
                diff /= norm(diff)
                diff /= d
                sum += diff
                count += 1
        if count > 0:
            sum /= count
            sum /= norm(sum)
            sum *= self.max_speed
            steer = sum - self.velocity
            ns = norm(steer)
            if ns > self.max_force:
                steer /= ns
                steer *= self.max_force
            self.applyForce(steer)


fig = figure()
xlim([0, 100])
ylim([0, 100])
gca().set_aspect('equal', adjustable='box')

test = [Boid(array([random() * 100., random() * 100]), array([0., 0.]), 1., .1) for _ in range(100)]
target = array([40., 40.])
p, = plot([], [], 'ro')


def update():
    for t in test:
        t.seek(target)
        t.separate(test)
        t.update()
    p.set_data(target[0], target[1])
    fig.canvas.draw()


def update_target(event):
    global target
    if event.xdata and event.ydata:
        target = [event.xdata, event.ydata]


def add_boid(event):
    global test
    test.append(Boid(array([event.xdata, event.ydata]), array([0., 0.]), 1., .1))


timer = fig.canvas.new_timer(interval=10)
timer.add_callback(update)
timer.start()

fig.canvas.mpl_connect("motion_notify_event", update_target)
fig.canvas.mpl_connect('button_press_event', add_boid)

show()
