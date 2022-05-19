import pygame
import numpy as np

from funcy import *


class Basic_Player:
    def __init__(self, pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id, destination):
        self.color = pl_color
        self.position = pl_pos
        self.position_temp = pl_pos
        self.speed = pl_speed
        self.head_image = pl_head_img_path
        self.size = pl_size
        self.game_res = game_res
        self.vel = pygame.math.Vector2.rotate
        self.angle = angle
        self.angle_temp = angle
        self.rot = 0
        if self.angle_temp == 180:
            self.velocity = pygame.math.Vector2(0, self.speed)
        elif self.angle_temp == 90:
            self.velocity = pygame.math.Vector2(-self.speed, 0)
        elif self.angle_temp == 0:
            self.velocity = pygame.math.Vector2(0, - self.speed)
        elif self.angle_temp == 270:
            self.velocity = pygame.math.Vector2(+ self.speed, 0)
        self.head_image_copy = None
        self.trail = [self.position]
        self.trail_num = np.array([])
        self.trn = 0
        self.jump = False
        self.head_image_position = []
        self.head_rect = self.head_image.get_rect()
        self.drawn_trail = False
        self.playerid = player_id
        self.player_collided = False
        self.c = 0

        # create surface from draw rect
        self.surface_trail = pygame.Surface((10, 10))
        self.surface_trail.fill(self.color)
        self.masktrail = pygame.mask.from_surface(self.surface_trail)
        self.trail_allow = True
        self.seconds = 0
        self.jump_time = 0
        self.jumped_already = False
        self.destinate = destination
        self.score = 0
        self.player_dead = False
        self.a2D = np.array([[self.position[0], self.position[1]]])

        if self.head_image_copy is None:
            self.mask1 = pygame.mask.from_surface(self.head_image)
        else:
            self.mask1 = pygame.mask.from_surface(self.head_image_copy)
        self.seconds_temp = 0
        self.previous_vel = [0, 0]




        self.reset()

    def reset(self):
        self.position = self.position_temp
        self.vel = pygame.math.Vector2.rotate
        if self.angle_temp == 180:
            self.velocity = pygame.math.Vector2(0, self.speed)
        elif self.angle_temp == 90:
            self.velocity = pygame.math.Vector2(-self.speed, 0)
        elif self.angle_temp == 0:
            self.velocity = pygame.math.Vector2(0, -self.speed)
        elif self.angle_temp == 180:
            self.velocity = pygame.math.Vector2(- self.speed, 0)
        self.rot = 0
        self.head_image_copy = None
        self.trail = [self.position]
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
        self.score = 0
        self.player_dead = False
        self.head_rect = None
        self.previous_vel = [0, 0]
        self.c = 0
        self.seconds_temp = 0

    def move(self, offsetx, offsety):
        old_x, old_y = self.position
        self.position = [round((old_x + offsetx), 2), round((old_y + offsety), 2)]
        if self.head_image_position:
            self.head_image_position.pop()
        self.head_image_position.append(self.position)

    # def get_vector(self):
    #     vector1 = pygame.Vector2(0, 0)
    #     vector1.from_polar((0, self.rot))
    #     vector1.x, vector1.y = vector1.y, vector1.x
    #     return vector1

    def rotation(self, angle):
        self.rot = (self.rot - angle) % 360
        self.head_image_copy = pygame.transform.rotate(self.head_image, self.rot)
        self.head_rect = self.head_image_copy.get_rect()

    def draw_player(self):
        self.drawn_player = True
        if self.head_image_copy is None:
            self.destinate.blit(self.head_image, (self.position[0] - int(self.head_image.get_width() / 4),
                                                  self.position[1] - int(self.head_image.get_height() / 4)))
        else:
            self.destinate.blit(self.head_image_copy, (self.position[0] - int(self.head_image.get_width() / 4),
                                                       self.position[1] - int(self.head_image.get_height() / 4)))

    #  @print_durations()
    def create_trail(self):
        # print("CTA",self.trail)
        if self.previous_vel == self.velocity:
            self.c += 1
            if self.c == 5:
                self.trail.append(self.position)
                self.c = 0

        if not self.previous_vel == self.velocity:
            self.trail.append(self.position)
        #     print("CT", self.trail)
        if self.jump and not self.jumped_already:
            self.c = 4

        self.drawn_trail = False
        self.previous_vel = self.velocity
        #  print("createtrail", self.trail)

    #   self.a2D = np.asarray(self.trail)

    def draw_trail(self, trail_list):
      #  print("TL",trail_list)

        #TODO ked si dam print trail list tak ono stale bezi ten draw trail niekolko krat aj ked sa nepridava nova hodnota

        # original WORKING iterator
        for j in trail_list:
            self.destinate.blit(self.surface_trail, (j[0],
                                                     j[1]))
        # numpy experimental iterator
        # numpy is SLOWER here !!!
        # for j in np.array(self.a2D):
        #     self.destinate.blit(self.surface_trail, (j[0] - int(self.head_image.get_width() / 3 - 3),
        #                                              j[1] - int(self.head_image.get_height() / 3 - 3)))
        # for i in trail_list:
        #   #  print("i", i)
        #     if len(i) <= 2:
        #         pass
        #     else:
        #         pygame.draw.lines(self.destinate,self.color,False, i,10 )


    def player_score(self):
        self.score = len(self.trail)
