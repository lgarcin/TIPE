from numpy import array
from numpy.linalg import norm
from matplotlib.pyplot import plot, show, xlim, ylim, figure, gca, cla
from random import random


class Boid:
    def __init__(self, pos, vel, max_speed, max_force):
        self.position = pos
        self.velocity = vel
        self.acceleration = array([0., 0.])
        self.max_speed = max_speed
        self.max_force = max_force
        self.r = 2
        self.p, = plot([self.position[0]], [self.position[1]], 'go')

    def update(self):
        self.velocity += self.acceleration
        ns = norm(self.velocity)
        if ns > self.max_speed:
            self.velocity /= ns
            self.velocity *= self.max_speed
        self.position += self.velocity
        self.acceleration = array([0., 0.])
        self.p.set_data(self.position[0], self.position[1])

    def apply_force(self, force):
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
            self.apply_force(steer)

    def separate(self, boids):
        desired_separation = self.r * 2
        s = array([0., 0.])
        count = 0;
        for b in boids:
            d = norm(self.position - b.position)
            if 0 < d < desired_separation:
                diff = self.position - b.position
                diff /= norm(diff)
                diff /= d
                s += diff
                count += 1
        if count > 0:
            s /= count
            n = norm(s)
            if n > 0:
                s /= norm(s)
                s *= self.max_speed
                steer = s - self.velocity
                ns = norm(steer)
                if ns > self.max_force:
                    steer /= ns
                    steer *= self.max_force
                self.apply_force(steer)

    def bounce(self, x_bounds, y_bounds, dist):
        if self.position[0] < x_bounds[0] + dist:
            desired = array([self.max_speed, self.velocity[1]])
            steer = desired - self.velocity
            ns = norm(steer)
            if ns > self.max_force:
                steer /= ns
            steer *= self.max_force
            self.apply_force(steer)
        if self.position[0] > x_bounds[1] - dist:
            desired = array([-self.max_speed, self.velocity[1]])
            steer = desired - self.velocity
            ns = norm(steer)
            if ns > self.max_force:
                steer /= ns
            steer *= self.max_force
            self.apply_force(steer)
        if self.position[1] < y_bounds[0] + dist:
            desired = array([self.velocity[0], self.max_speed])
            steer = desired - self.velocity
            ns = norm(steer)
            if ns > self.max_force:
                steer /= ns
            steer *= self.max_force
            self.apply_force(steer)
        if self.position[1] > y_bounds[1] - dist:
            desired = array([self.velocity[0], -self.max_speed])
            steer = desired - self.velocity
            ns = norm(steer)
            if ns > self.max_force:
                steer /= ns
            steer *= self.max_force
            self.apply_force(steer)


fig = figure()
xlim([0, 100])
ylim([0, 100])
gca().set_aspect('equal', adjustable='box')

boids = [Boid(array([random() * 100., random() * 100]), array([0., 0.]), 1., .1) for _ in range(10)]
target = array([40., 40.])
p, = plot([], [], 'ro')
mouse_down = False


def update():
    for t in boids:
        t.seek(target)
        t.separate(boids)
        t.bounce((0, 100), (0, 100), 10)
        t.update()
    p.set_data(target[0], target[1])
    fig.canvas.draw()


def update_target(event):
    global target, boids
    if event.xdata and event.ydata:
        target = [event.xdata, event.ydata]
    if mouse_down:
        boids.append(Boid(array([event.xdata, event.ydata]), array([0., 0.]), 1., .1))


def toggle_add(event):
    global mouse_down
    mouse_down = not mouse_down


def remove(event):
    global boids, p
    if event.key == 'escape':
        boids = []
        cla()
        xlim([0, 100])
        ylim([0, 100])
        gca().set_aspect('equal', adjustable='box')
        p, = plot([], [], 'ro')


timer = fig.canvas.new_timer(interval=10)
timer.add_callback(update)
timer.start()

fig.canvas.mpl_connect("motion_notify_event", update_target)
fig.canvas.mpl_connect('button_press_event', toggle_add)
fig.canvas.mpl_connect('button_release_event', toggle_add)
fig.canvas.mpl_connect('key_press_event', remove)

show()
