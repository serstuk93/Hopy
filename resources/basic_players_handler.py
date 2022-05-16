import pygame
import numpy as np

class Basic_Player():
    def __init__(self, pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id):
        self.color = pl_color
        self.position = pl_pos
        self.position_temp = pl_pos
        self.speed = pl_speed
        self.head_image = pl_head_img_path
        self.size = pl_size
        self.game_res = game_res
        self.velocity = pygame.math.Vector2(0, pl_speed)
        self.vel = pygame.math.Vector2.rotate
        self.angle = angle
        self.angle_temp = angle
        self.rot = 0
        self.head_image_copy = None
        #   print(self.position)
        self.trail = []
        self.trail_num = np.array([])
        #  self.trail.append(self.position)
        self.trn = 0
        self.jump = False
        self.head_image_position = []
        #    print(self.position)
        self.head_rect = self.head_image.get_rect()
        self.drawn_trail = False
        self.playerid = player_id
        self.player_collided = False

        # create surface from draw rect
        self.surface_trail = pygame.Surface((5, 5))
        self.surface_trail.fill(self.color)
        self.masktrail = pygame.mask.from_surface(self.surface_trail)
        self.trail_allow = True
        self.seconds = 0
        self.jump_time = 0
        self.jumped_already = False

        self.reset()

    def reset(self):
        self.position = self.position_temp
        self.vel = pygame.math.Vector2.rotate
        self.velocity = pygame.math.Vector2(0, self.speed)
        self.rot = 0
        self.head_image_copy = None
        self.trail = []
        self.trn = 0
        self.jump = False
        self.head_image_position = []
        self.drawn_trail = False
        self.player_collided = False
        self.angle = self.angle_temp
        self.trail_allow = True
        self.seconds = 0
        self.jump_time = 0
        self.jumped_already = False

    def move(self, offsetx, offsety):
        old_x, old_y = self.position
        self.position = [round((old_x + offsetx), 2), round((old_y + offsety), 2)]
        if self.head_image_position:
            self.head_image_position.pop()
        self.head_image_position.append(self.position)

    def get_vector(self):
        vector1 = pygame.Vector2(0, 0)
        vector1.from_polar((1, self.rot))
        vector1.x, vector1.y = vector1.y, vector1.x
        return vector1

    def rotation(self, angle):
        self.rot = (self.rot - angle) % 360
        self.head_image_copy = pygame.transform.rotate(self.head_image, self.rot)
        self.head_rect = self.head_image_copy.get_rect()

        # disable multiple side  keys at once
        keys_multiple = pygame.key.get_pressed()

    def draw_player(self, destination):
        self.drawn_player = True
        self.destinate = destination
        if self.head_image_copy is None:
            self.destinate.blit(self.head_image, (self.position[0] - int(self.head_image.get_width() / 2),
                                                  self.position[1] - int(self.head_image.get_height() / 2)))
        else:
            self.destinate.blit(self.head_image_copy, (self.position[0] - int(self.head_image_copy.get_width() / 2),
                                                       self.position[1] - int(self.head_image_copy.get_height() / 2)))

    def create_trail(self):
        self.trail.append(self.position)
        self.drawn_trail = False


    def draw_trail(self, trail_list):
        for j in trail_list:
            self.destinate.blit(self.surface_trail, (j[0] - int(self.head_image.get_width() / 3 - 3),
                                                     j[1] - int(self.head_image.get_height() / 3 - 3)))