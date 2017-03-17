import sys, pygame

pygame.init()
clock = pygame.time.Clock()

size = width, height = 600, 600
black = 0, 0, 0

screen = pygame.display.set_mode(size)

from numpy import array
from numpy.linalg import norm


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


boids = Boid(array([0., 0.]), array([0., 0.]), 4., 10.)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)
    boids.seek(array(pygame.mouse.get_pos()))
    boids.update()
    x, y = boids.position[0], boids.position[1]
    pygame.draw.circle(screen, (60, 60, 100), (int(x), int(y)), 10)
    clock.tick(30)
    pygame.display.flip()
