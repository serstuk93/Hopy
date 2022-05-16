import pygame

import numpy as np
import random

from Hopy.config import config
from Hopy.resources.basic_players_handler import Basic_Player

class AI(Basic_Player):
    def __init__(self,pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id, destination ):
        super().__init__(pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id, destination)
        self.ai_movement = 0

    def random_movement(self):
        self.velocity = self.vel(self.velocity, self.ai_movement)
        self.ai_movement = random.choice([10, 0, -10])
        self.rotation(self.ai_movement)

        self.get_vector()
        self.move(self.velocity[0], self.velocity[1])

    def position_awarness(self):
        pass
    def ai_jumping(self):
        pass

    def handle_keys(self):
        pass


