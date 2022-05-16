import pygame

import numpy as np
import random

from Hopy.config import config
from Hopy.resources.basic_players_handler import Basic_Player

class AI(Basic_Player):
    def __init__(self,pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id, destination ):
        super().__init__(pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id, destination)
        self.ai_movement = 0
        self.predict_trail = []
        self.predict_position = None
        self.predict_trajectory = None
        self.predict_velocity = None

    def random_movement(self):
        self.velocity = self.vel(self.velocity, self.ai_movement)
        self.ai_movement = random.choice([10, 0, -10])
        self.rotation(self.ai_movement)
        self.get_vector()
        self.move(self.velocity[0], self.velocity[1])

    def position_awarness(self):
        self.predict_trail = []
        self.predict_velocity = self.velocity
        ai_old_x, ai_old_y = self.position
        for i in range(0,5):
            self.predict_velocity = self.vel(self.predict_velocity, self.ai_movement)
          #  self.predict_trajectory = self.move(self.predict_velocity[0], self.predict_velocity[1])
            self.predict_position = [round((ai_old_x + self.predict_velocity[0]), 2), round((ai_old_y +self.predict_velocity[1]), 2)]
            self.predict_trail.append(self.predict_position)


    def ai_jumping(self):
        self.jump = random.choices([True,False], weights=[0.1, 1000], k=1)

    def handle_keys(self):
        pass


