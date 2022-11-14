from config import config
from resources.basic_players_handler import Basic_Player


class Player(Basic_Player):
    def __init__(self, pl_color, pl_pos, pl_speed, pl_size, game_res, angle, player_id, destination):
        super().__init__(pl_color, pl_pos, pl_speed, pl_size, game_res, angle, player_id, destination)

    def handle_keys(self, keys):

        if keys[config.KEYBOARD_CONTROLS[self.playerid][0]] and keys[config.KEYBOARD_CONTROLS[self.playerid][1]]:
            return

        if keys[config.KEYBOARD_CONTROLS[self.playerid][0]]:
            self.velocity = self.vel(self.velocity, -5)
            self.rotation(-5)
       #     self.move(self.velocity[0], self.velocity[1])
        if keys[config.KEYBOARD_CONTROLS[self.playerid][1]]:
            self.velocity = self.vel(self.velocity, 5)
            self.rotation(+5)
        #    self.move(self.velocity[0], self.velocity[1])
        if keys[config.KEYBOARD_CONTROLS[self.playerid][2]]:
            self.jump = True
