import pygame
import math

from Hopy.config import config

class Player():
    def __init__(self, pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle):
        self.color = pl_color
        self.position = pl_pos
        self.speed = pl_speed
        self.head_image = pl_head_img_path
        self.size = pl_size
        self.game_res = game_res
        self.velocity = pygame.math.Vector2(0, pl_speed)
        self.vel = pygame.math.Vector2.rotate
        self.angle = angle
        self.rot= 0
        self.head_image_copy=None
        self.trail = []
        self.jump = False
        self.head_image_position = []
        print(self.position)
        self.head_rect = self.head_image.get_rect()
        self.drawn_trail = False


        # create surface from draw rect
        surface_trail = pygame.Surface((10, 10))
        self.masktrail = pygame.mask.from_surface(surface_trail)


    def move(self, offsetx,offsety):
        old_x, old_y = self.position
        self.position = [round((old_x + offsetx),2), round((old_y + offsety),2)]
        if self.head_image_position:
            self.head_image_position.pop()
        self.head_image_position.append(self.position)


    # def rotateitem(self):
    #     self.head_image = pygame.transform.rotate(self.head_image, self.angle)
    #     imageRect = self.head_image.get_rect(center=(self.position[0], self.position[1]))
    #     self.destinate.blit(self.head_image, imageRect)

    def get_vector(self):
        vector1 = pygame.Vector2(0, 0)
        vector1.from_polar((1, self.rot))
        vector1.x, vector1.y = vector1.y, vector1.x
      #  print("V",vector1)
        return vector1

    def rotation(self, angle):

        self.head_image = pygame.image.load("resources/headred.png").convert_alpha()
        self.rot += angle % 360
        self.head_image_copy = pygame.transform.rotate(self.head_image,  self.rot)
     #   print(self.head_image_copy.get_size())
        self.head_rect = self.head_image_copy.get_rect()
    #    self.destinate.blit(self.head_image_copy, (self.position[0] - int(self.head_image_copy.get_width() / 2), self.position[1] - int(self.head_image_copy.get_height() / 2)))

       # self.destinate.blit(self.head_image_copy, self.position)

    def handle_keys(self, keys):
       # self.jump = False
        self.jump_effect_launch = False
        if keys[pygame.K_LEFT]:

          #  self.velocity = self.vel(self.velocity, 10)
          #  self.angle =self.angle % 360  # I can't test right now so if this doesn't work switch -angle with abs(angle)

            self.velocity = self.vel(self.velocity, -10)
            self.rotation(+10)
            # print(self.position)
            # print(self.velocity)
            self.get_vector()
            self.move(self.velocity[0], self.velocity[1])
        if keys[pygame.K_RIGHT]:
            self.velocity = self.vel(self.velocity, 10)
            self.rotation(-10)
            # print(self.position)
            # print(self.velocity)
            self.get_vector()
            self.move(self.velocity[0],self.velocity[1])
        if keys[pygame.K_UP]:
            self.jump_effect_launch = True
            self.jump=True


    def sound_effects(self):
        pass
     #   if self.jump_effect_launch:
          #  jump_sound.play()

    def draw_player(self,destination):
        self.drawn_player=True
        self.destinate= destination
        if self.head_image_copy is None:
            self.destinate.blit( self.head_image,(self.position[0] - int(self.head_image.get_width() /2),
                                               self.position[1] - int(self.head_image.get_height() / 2)))
        else:
            self.destinate.blit(self.head_image_copy, (self.position[0] - int(self.head_image_copy.get_width()/ 2 ),
                                                   self.position[1] - int(self.head_image_copy.get_height()/ 2)))

    def create_trail(self):
        self.trail.append(self.position)
        self.drawn_trail = False
    def draw_trail(self, trail_list):
        for j in trail_list[:]:
            surface_trail = pygame.Surface((5, 5))
            surface_trail.fill(config.PLAYER_COLOR)
            self.destinate.blit(surface_trail,(j[0] - int(self.head_image.get_width() / 3),
                                               j[1] - int(self.head_image.get_height() / 3)))
            # pygame.draw.rect(self.destinate, config.PLAYER_COLOR,
            #                  pygame.Rect(j[0], j[1], 5,
            #                             5))



    def check_collision(self):
        if self.head_image_copy:
            self.mask1 = pygame.mask.from_surface(self.head_image_copy)
            print(self.head_image_position)
           # print((self.trail))
            # print("len",len(self.trail))
            for trail_step in self.trail[:-20]:
                x_off = trail_step[0] - self.head_image_position[0][0]
                y_off = trail_step[1] - self.head_image_position[0][1]
                if self.mask1.overlap(self.masktrail, (x_off, y_off)):
                   # pass
                    print("KOLIZIA")
            #
            # print("P", self.position)
            # print("MT", self.masktrail.get_size())

            #
            # point = pygame.mouse.get_pos()
            # collide = rect.collidepoint(point)
            # color = (255, 0, 0) if collide else (255, 255, 255)
            #   print( self.head_image_position[0][0])

        #         pos_in_mask = trail_step[0] - self.head_image_position[0][0], trail_step[1] - self.head_image_position[0][1]
        #         touching = self.head_rect.collidepoint(*trail_step) and self.mask.get_at(pos_in_mask)
        #         if touching:
        #             print("KOLIZIA")
        # if (pygame.sprite.spritecollide(maze, alien_group, False, collided=pygame.sprite.collide_mask)):
        #     # returned list is not empty
        #     background = FIREY_RED



