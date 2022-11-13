import pygame
import random

from resources.basic_players_handler import Basic_Player


class AI(Basic_Player):
    def __init__(self, pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id, destination):
        super().__init__(pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id, destination)
        self.ai_movement = 0
        self.predict_steps = 20
        self.predict_trail = [[] for _ in range(self.predict_steps)]
        self.predict_trail_around = [[] for _ in range(4)]
        self.predict_position = self.position
        self.predict_trajectory = None
        self.predict_velocity = None
        self.predict_jump_checker = False
        self.last = pygame.time.get_ticks()
        self.cooldown = 60
        self.now = pygame.time.get_ticks()
        self.picked_rotation_side = False
        self.player_name = str("AI" + str(player_id[1:]))
        self.incoming_drop_collision = False


        self.debug_pos = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.debug_pos.fill((255,255,255,0)) 
        #self.surface_trail.fill(self.color)
        pygame.draw.circle(self.debug_pos, (255, 255, 255), (5, 5), 5)

    def reset(self):
        super().reset()
        self.ai_movement = 0
        self.predict_steps = 20
        self.predict_trail = [[] for _ in range(self.predict_steps)]
        self.predict_trail_around = [[] for _ in range(4)]
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
        self.incoming_drop_collision = False

    def random_movement(self):
        if self.predict_jump_checker == False:
            if self.position[0] < 75 or self.position[1] < 75 or self.position[0] > 1500 or self.position[1] > 900:
                if self.picked_rotation_side== False :
                    self.picked_rotation_side = random.choice(["R", "L"])
                    if self.picked_rotation_side == "R":
                        self.ai_movement = 5
                    else:
                        self.ai_movement = -5
                    self.picked_rotation_side== True
            elif self.now - self.last >= self.cooldown and self.picked_rotation_side is False:
                self.last = self.now
                self.ai_movement = random.choice([5, 0, -5])
            elif self.incoming_drop_collision == True and self.picked_rotation_side== True:
                self.ai_movement = self.ai_movement * -1 
                self.picked_rotation_side== True
            else:
                self.ai_movement = 0
                self.picked_rotation_side = False
        elif self.incoming_drop_collision == True and self.picked_rotation_side== True:
            self.ai_movement = self.ai_movement * -1 
            self.picked_rotation_side== False
        self.velocity = self.vel(self.velocity, self.ai_movement)
        self.rotation(self.ai_movement)
        self.move(self.velocity[0], self.velocity[1])

    def position_awarness(self):
        # TODO PROBLEM JE ASI V TOM ZE SA PREDIKUJE Z POZICIE HLAVY KTORA ZACINA VZDY PRI OBRAZKU v polohe 0,0, co znamena ze je to posunute o dost do strany, pREDIKCIA MA BYT Z POZICIE BODKY NAKONCI TRAILU 
        # TODO pri predvidani sa hodnoty generuju do kruhu!!!
        # TODO stale skacu neskoro pred koliziou
        # TODO AI nech  predvida do kruhu aj dopredu a opravit zacyklenie pri kraji obrazovky
        around_distance = 10
        self.predict_velocity = self.velocity
        self.predict_position = self.position
        # TODO predict velocity nerobi hodnoty ked ide cerv priamo rovno, iba ked uhluje
        for i in range(0, self.predict_steps):
            self.predict_velocity = self.vel(self.predict_velocity, self.ai_movement)

            self.predict_position = [round((self.predict_position[0] + self.predict_velocity[0]), 2),
                                     round((self.predict_position[1] + self.predict_velocity[1]), 2)]
            self.predict_trail[i] = self.predict_position
        # those 4 added values are for prediction points around worm...see debug prediction
        self.predict_trail_around[0]=(self.position[0]-around_distance,self.position[1]-around_distance)
        self.predict_trail_around[1]=(self.position[0]+around_distance,self.position[1]+around_distance)
        self.predict_trail_around[2]=(self.position[0]-around_distance,self.position[1]+around_distance)
        self.predict_trail_around[3]=(self.position[0]+around_distance,self.position[1]-around_distance)

    def drop_collision_handler(self):
        if self.picked_rotation_side == "R":
            self.ai_movement = 5
        else:
            self.ai_movement = -5
    def ai_jumping(self):

        # weights dava pravdepodobnost vyberu medzi moznostami
        self.jump = True 
     #   self.jump = random.choices([True, False], weights=[1, 100], k=1)

    def handle_keys(self):
        pass

    def debug_prediction(self):
      #  print("PT",self.predict_trail)
        for j in self.predict_trail:
         #   print("j",j)
            self.destinate.blit(self.debug_pos, (j))
          #  self.destinate.blit(self.debug_pos, (j[0], self.position[1]))
            #self.destinate.blit(self.debug_pos, (self.position[0],j[1]))

        for j in self.predict_trail_around:
            self.destinate.blit(self.debug_pos, (j))
        self.destinate.blit(self.debug_center, self.position)




    def debug_borders(self):
        self.destinate.blit(self.debug_pos, (50,50))
        self.destinate.blit(self.debug_pos, (1550,50))
        self.destinate.blit(self.debug_pos, (50,900))
        self.destinate.blit(self.debug_pos, (1550,1030))