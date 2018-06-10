import numpy as np
import pygame

from Car import Car


class Model:
    def __init__(self):
        self.road_length = 2000
        self.cars = {"A": Car("A"), "B": Car("B"), "C": Car("C")}
        self.cars["A"].x = 0
        self.cars["B"].x = np.random.randint(0, self.road_length - self.cars["B"].vx * self.road_length / 25)
        self.cars["C"].vx *= -1
        self.cars["C"].lane = 0

    def update(self, dt, random_acc=False):
        if random_acc:
            if np.random.random() <= 0.1:
                if np.random.random() <= 0.5:
                    self.cars["B"].ax += 0.5
                else:
                    self.cars["B"].ax -= 0.5
            if np.random.random() <= 0.1:
                if np.random.random() <= 0.5:
                    self.cars["C"].ax += 0.5
                else:
                    self.cars["C"].ax -= 0.5
        for key in self.cars:
            self.cars[key].update(dt)
        if random_acc:
            self.cars["B"].ax = 0
            self.cars["C"].ax = 0
            if self.cars["B"].vx > 25:
                self.cars["B"].vx = 25
            elif self.cars["B"].vx < 6:
                self.cars["B"].vx = 6
            if self.cars["C"].vx > 25:
                self.cars["C"].vx = 25
            elif self.cars["C"].vx < 6:
                self.cars["C"].vx = 6

    def check_collisions(self):
        collision = False
        for key1 in self.cars:
            for key2 in self.cars:
                if key1 != key2:
                    if self.cars[key1].lane == self.cars[key2].lane:
                        if abs(self.cars[key1].get_distance_from(self.cars[key2])) < 0.000001:
                            print("Collision between car " + key1 + " and car " + key2)
                            collision = True
        return collision

    def draw(self, screen):
        for i in range(0, self.road_length, 50):
            pygame.draw.line(screen, (255, 255, 255), (20, i), (20, i + 25), 3)
        for key in self.cars:
            self.cars[key].draw(screen)

    def load_from_file(self, file_name):
        with open(file_name) as input_file:
            lines = input_file.readlines()
            input_file.close()
        for line in lines:
            values = line.split()
            self.cars[values[0]] = Car(values[0], float(values[1]), float(values[2]), float(values[3]))
