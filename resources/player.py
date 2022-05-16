import pygame

from Hopy.config import config
from Hopy.resources.basic_players_handler import Basic_Player

class Player(Basic_Player):
    def __init__(self, pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id, destination):
        super().__init__(pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id, destination)

    # def rotation(self, angle):
    #     self.rot += angle % 360
    #     self.head_image_copy = pygame.transform.rotate(self.head_image, self.rot)
    #     self.head_rect = self.head_image_copy.get_rect()

    def handle_keys(self, keys):
        # self.jump = False
        # if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
        #     return(print("si kokot "))

        if keys[config.KEYBOARD_CONTROLS[self.playerid][0]] and keys[config.KEYBOARD_CONTROLS[self.playerid][1]]:
            return (print("si  "))

        if keys[config.KEYBOARD_CONTROLS[self.playerid][0]]:
            #  self.velocity = self.vel(self.velocity, 10)
            #  self.angle =self.angle % 360  # I can't test right now so if this doesn't work switch -angle with abs(angle)
            self.velocity = self.vel(self.velocity, -10)
            self.rotation(-10)
            print(self.rot)
            self.get_vector()
            self.move(self.velocity[0], self.velocity[1])
        if keys[config.KEYBOARD_CONTROLS[self.playerid][1]]:
            self.velocity = self.vel(self.velocity, 10)
            self.rotation(+10)
            self.get_vector()
            self.move(self.velocity[0], self.velocity[1])
        if keys[config.KEYBOARD_CONTROLS[self.playerid][2]]:
            self.jump = True

        # disable multiple side  keys at once
        keys_multiple = pygame.key.get_pressed()

