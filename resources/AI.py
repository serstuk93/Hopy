import pygame
import random

from Hopy.resources.basic_players_handler import Basic_Player


class AI(Basic_Player):
    def __init__(self, pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id, destination):
        super().__init__(pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id, destination)
        self.ai_movement = 0
        self.predict_steps = 5
        self.predict_trail = [[] for _ in range(self.predict_steps)]
        self.predict_position = self.position
        self.predict_trajectory = None
        self.predict_velocity = None
        self.predict_jump_checker = False
        self.last = pygame.time.get_ticks()
        self.cooldown = 60
        self.now = pygame.time.get_ticks()
        self.picked_rotation_side = False
        self.player_name = str("AI" + str(player_id[1:]))

    def reset(self):
        super().reset()
        self.ai_movement = 0
        self.predict_steps = 5
        self.predict_trail = [[] for _ in range(self.predict_steps)]
        self.predict_position = self.position
        self.predict_trajectory = None
        self.predict_velocity = None
        self.predict_jump_checker = False
        if self.angle_temp == 180:
            self.velocity = pygame.math.Vector2(0, self.speed)
        elif self.angle_temp == 90:
            self.velocity = pygame.math.Vector2(-self.speed, 0)
        elif self.angle_temp == 0:
            self.velocity = pygame.math.Vector2(0, - self.speed)
        elif self.angle_temp == 270:
            self.velocity = pygame.math.Vector2(+ self.speed, 0)
        self.picked_rotation_side = False

    def random_movement(self):
        if not self.predict_jump_checker:
            if self.position[0] < 50 or self.position[1] < 50 or self.position[0] > 1550 or self.position[1] > 1030:
                if not self.picked_rotation_side:
                    self.picked_rotation_side = random.choice(["R", "L"])
                    if self.picked_rotation_side == "R":
                        self.ai_movement = 8
                    else:
                        self.ai_movement = -8
            elif self.now - self.last >= self.cooldown and self.picked_rotation_side is False:
                self.last = self.now
                self.ai_movement = random.choice([10, 0, -10])
            else:
                self.ai_movement = 0
                self.picked_rotation_side = False
            self.velocity = self.vel(self.velocity, self.ai_movement)
            self.rotation(self.ai_movement)
        self.move(self.velocity[0], self.velocity[1])

    def position_awarness(self):
        # TODO pri predvidani sa hodnoty generuju do kruhu!!!
        # TODO stale skacu neskoro pred koliziou
        # TODO AI nech  predvida do kruhu aj dopredu a opravit zacyklenie pri kraji obrazovky
        self.predict_velocity = self.velocity
        self.predict_position = self.position
        # TODO predict velocity nerobi hodnoty ked ide cerv priamo rovno, iba ked uhluje
        for i in range(0, self.predict_steps):
            self.predict_velocity = self.vel(self.predict_velocity, self.ai_movement)

            self.predict_position = [round((self.predict_position[0] + self.predict_velocity[0]), 2),
                                     round((self.predict_position[1] + self.predict_velocity[1]), 2)]
            self.predict_trail[i] = self.predict_position

    def ai_jumping(self):
        # weights dava pravdepodobnost vyberu medzi moznostami
        self.jump = random.choices([True, False], weights=[1, 100], k=1)

    def handle_keys(self):
        pass
