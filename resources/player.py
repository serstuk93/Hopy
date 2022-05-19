from Hopy.config import config
from Hopy.resources.basic_players_handler import Basic_Player


class Player(Basic_Player):
    def __init__(self, pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id, destination):
        super().__init__(pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id, destination)

    def handle_keys(self, keys):

        if keys[config.KEYBOARD_CONTROLS[self.playerid][0]] and keys[config.KEYBOARD_CONTROLS[self.playerid][1]]:
            return

        if keys[config.KEYBOARD_CONTROLS[self.playerid][0]]:
            self.velocity = self.vel(self.velocity, -10)
            self.rotation(-10)
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
        # keys_multiple = pygame.key.get_pressed()
