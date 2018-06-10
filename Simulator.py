import pygame

from Controller import Controller
from FuzzyInferenceSystem import FuzzyInferenceSystem
from Model import Model
from settings import *


class Simulator:
    def __init__(self, fps):
        if use_pygame:
            pygame.init()

        self.fis = FuzzyInferenceSystem()
        self.controller = Controller()
        self.model = Model()

        self.fps = fps
        self.time_step = 1.0 / fps
        if use_pygame:
            self.screen = pygame.display.set_mode((40, int(self.model.road_length / 4)))

        self.collision = False

    def start(self, random_acc):
        end = False
        to_draw = False
        prev_time = time.clock()
        curr_time = 0
        delta_time = 0
        try:
            while not end:
                curr_time = time.clock()
                delta_time += curr_time - prev_time
                prev_time = curr_time
                if use_pygame:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            end = True
                while delta_time >= self.time_step:
                    delta_time -= self.time_step
                    signal = self.fis.generate_response(self.model)
                    self.controller.apply_signal(self.model.cars["A"], signal)
                    self.update(self.time_step * self.fps, random_acc)
                    end = self.check_end_conditions()
                    to_draw = True
                if to_draw:
                    self.draw()
                    to_draw = False
            pygame.quit()
        except SystemExit:
            pygame.quit()

    def update(self, dt, random_acc):
        self.model.update(dt, random_acc)

    def check_end_conditions(self):
        if self.model.cars["A"].x >= self.model.road_length:
            print("Car A reached end of the road")
            return True
        if self.model.cars["B"].x >= self.model.road_length:
            print("Car B reached end of the road")
            return True
        if self.check_collisions():
            print("Collision detected")
            self.collision = True
            return True
        return False

    def check_collisions(self):
        return self.model.check_collisions()

    def draw(self):
        if use_pygame:
            self.screen.fill((0, 0, 0))
            self.model.draw(self.screen)
            pygame.display.update()

    def load_initial_state(self, file_name):
        self.model.load_from_file(file_name)

    def save_state(self, file_name):
        finished_overtaking = 0
        if self.model.cars['A'].get_distance_from(self.model.cars['B']) > 0:
            finished_overtaking = 1
        collision = 0
        if self.collision:
            collision = 1
        output_file = open(file_name, 'a+')
        output_file.write(str(finished_overtaking) + ' ' + str(collision) + '\n')
        output_file.close()
