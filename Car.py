import pygame

from settings import *


class Car:
    def __init__(self, name, x=None, lane=1, vx=None):
        self.name = name
        if x == None:
            self.x = np.random.rand() * 2000
        else:
            self.x = x
        self.lane = lane
        if x == None:
            self.vx = np.random.rand() * 19 + 6
        else:
            self.vx = vx

        self.ax = 0
        self.length = 4
        if use_pygame:
            self.font = pygame.font.SysFont("arial", 12)

    def update(self, dt):
        self.vx += self.ax * dt
        self.x += self.vx * dt

    def draw(self, screen):
        if use_pygame:
            # pygame.draw.circle(screen, (255, 255, 255), (int(self.lane * 20 + 10), 500 - int(self.x)), 6, 2)
            scoretext = self.font.render(self.name, 1, (255, 255, 255))
            screen.blit(scoretext, (int(self.lane * 20 + 10) - 3, 500 - int(self.x / 4) - 4))

    def get_distance_from(self, car):
        distance = self.x - car.x
        if distance < self.length and distance > -car.length:
            distance = 0
        elif distance >= self.length:
            distance -= self.length
        else:  # distance <= -car.length
            distance += car.length
        return distance
