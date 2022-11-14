import pygame


class Basic_Player(pygame.sprite.Sprite):
    def __init__(self, pl_color, pl_pos, pl_speed, pl_head_img_path, pl_size, game_res, angle, player_id, destination):
        pygame.sprite.Sprite.__init__(self)
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
        
        self.trn = 0
        self.jump = False
        self.head_image_position = []
        self.head_rect = self.head_image.get_rect()
        self.drawn_trail = False
        self.playerid = player_id
        self.player_name = str("Player"+str(player_id[1:]))
        self.player_collided = False
        self.trail = [[self.position, angle]]

        self.c = 0
        self.turned = False

        # create surface from draw rect
        self.surface_trail = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.surface_trail.fill((255,255,255,0)) 
        #self.surface_trail.fill(self.color)
        pygame.draw.circle(self.surface_trail, self.color, (5, 5), 5)
        self.masktrail = pygame.mask.from_surface(self.surface_trail)
        self.trail_allow = True
        self.seconds = 0
        self.jump_time = 0
        self.jumped_already = False
        self.destinate = destination
        self.score = 0
        self.player_dead = False
        self.front_predict_jump = []


        self.debug_center = pygame.Surface((5, 5))
        self.debug_center.fill((0, 0, 139,0))
        self.mask_center =  pygame.mask.from_surface(self.debug_center)

        from test_area_nogit import spritesheet
        #trail
        BG = (50, 50, 50)
        BLACK = (0, 0, 0)
      #  trail_sheet_image = pygame.image.load('test_area_nogit/trail.png').convert_alpha()

      #  trail_sheet = spritesheet.SpriteSheet(trail_sheet_image)
     #   self.trail_img = trail_sheet.get_image(0, 5, 5, 1, BLACK)


        #head
        sprite_sheet_image = pygame.image.load('test_area_nogit/worm.png').convert_alpha()
       # print(sprite_sheet_image)
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
       # print(sprite_sheet)





        # animation for sprite
        self.animations = {"move": None,
                    "jump": None,
                    }
        self.update_time = pygame.time.get_ticks()
        run_animation_list = []
        run_animation_frames = 4 
        jump_animation_list = []
        jump_animation_frames = 13
        self.trail_animation_list = []
        update_tick = pygame.time.get_ticks()
        update_cooldown = 100
        self.frame =0
        self.action = "move"

       

        for i in range(run_animation_frames):
            tmp_img = sprite_sheet.get_image(i, 32, 32, 1, BLACK)
            tmp_img = pygame.transform.rotate(
            tmp_img, angle)
            run_animation_list.append(tmp_img)


        for i in range(run_animation_frames,run_animation_frames+jump_animation_frames):
            tmp_img = sprite_sheet.get_image(i, 32, 32, 1, BLACK)
            tmp_img = pygame.transform.rotate(
            tmp_img, angle)
            jump_animation_list.append(tmp_img)

     #   for i in range(2):
      #      tmp_img = trail_sheet.get_image(i, 5, 5, 1, BLACK)
      #      tmp_img = pygame.transform.rotate(
      ##      tmp_img, angle)
     #       self.trail_animation_list.append(tmp_img)

        self.animations["move"] = run_animation_list
        self.animations["jump"] = jump_animation_list
        self.image = self.animations[self.action][self.frame]


        self.rect = self.image.get_rect()
       # self.rect.center = (100, 100)








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
        self.trail = [[self.position, self.angle]]
        self.trn = 0
        self.jump = False
        self.head_image_position = [[None,None]]
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
      #  print(self.head_image_position)
       # if self.head_image_position:
         #   self.head_image_position.pop()
        self.head_image_position[0] = self.position
         #update rectangle position
        self.rect.x += self.position[0]
        self.rect.y += self.position[1]

    def rotation(self, angle):
        self.rot = (self.rot - angle) % 360
        #self.head_image_copy = pygame.transform.rotate(self.head_image, self.rot)
        self.head_image_copy = pygame.transform.rotate(self.animations[self.action][self.frame], self.rot)
        self.head_rect = self.head_image_copy.get_rect()

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 75
        if self.jumped_already:
            self.action = "jump"
           # self.frame = 0
        else:
            self.action = "move"
        #update image depending on current frame
        
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame += 1

        #if the animation has run out the reset back to the start
        if self.frame >= len(self.animations[self.action]):
            self.frame = 0

        self.image = self.animations[self.action][self.frame]
      #  print("frame", self.frame)
        
        self.head_image_copy = pygame.transform.rotate(self.animations[self.action][self.frame], self.rot)
        
        # TODO improve performance by not calling function everytime only every 100 ms in main function

    def draw_player(self):
        self.front_position_sensor()
        self.drawn_player = True
        
        if self.head_image_copy is None:
            self.destinate.blit(self.animations[self.action][self.frame], self.front_predict_position)
        else:
            self.head_image_copy.set_alpha(255)

            current_img_height = self.head_image_copy.get_height()
            current_img_width = self.head_image_copy.get_width()
            half_height = int(current_img_height /2) 
            half_width = int(current_img_width /2) 
            self.destinate.blit(self.head_image_copy, (self.front_predict_position[0]-half_width, self.front_predict_position[1]-half_height))
      #  self.destinate.blit(self.animations["move"][self.frame],self.position)

    #  @print_durations()
    def create_trail(self):
        # TODO check collision as arrays not points ie range(x-10:10+x,1) in x and the same in y for array creation 
        if self.previous_vel == self.velocity:
          #  if self.turned == True:
             #   self.c = 5
            #    self.turned = False 
          #  else:
            self.c += 2
            if self.c >= 5:
                self.trail.append([self.position, self.rot])
                self.c = 0
                

        if not self.previous_vel == self.velocity:
         #   if self.turned == False: 
            #    self.c = 5
           # else:
                #self.turned = True
            self.c += 2
            if self.c >= 5:
                self.trail.append([self.position, self.rot])
                self.c = 0
        if self.jump and not self.jumped_already:
            self.c = 5
       # print("CT",self.trail)
        self.drawn_trail = False
        self.previous_vel = self.velocity

    def draw_trail(self, trail_list):
        # TODO ked si dam print trail list tak ono stale bezi
        # ten draw trail niekolko krat aj ked sa nepridava nova hodnota
        # original WORKING iterator
        for j in trail_list[:]:

            self.destinate.blit(self.surface_trail, (j[0][0]-5,j[0][1]-5))
          #  self.trail_img_copy = pygame.transform.rotate(self.trail_animation_list[j[2]], j[1])
          #  self.trail_img_copy.set_alpha(255)
        #    self.destinate.blit(self.trail_img_copy,j[0])                                  
        
    def player_score(self):
        self.score = len(self.trail)


    def get_pixel_color(self):
        self.front_position_sensor()
        self.pixel_color_point = pygame.Surface((4, 4))
        self.pixel_color_point.fill((255, 255, 255,0))
        self.rounded_pos = (int(self.front_predict[-1][0]-2),int(self.front_predict[-1][1]-2))
        self.pixel_color = self.destinate.get_at(self.rounded_pos) 
        self.destinate.blit(self.pixel_color_point,(self.rounded_pos))
        return self.pixel_color


    def front_position_sensor(self):
        self.front_predict = []
        self.front_movement_angle = 0
        self.front_predict_steps = 5
        self.front_predict_velocity = self.velocity
        self.front_predict_position = self.position
        for i in range(0, self.front_predict_steps):
            self.front_predict_velocity = self.vel(self.front_predict_velocity, self.front_movement_angle)

            self.front_predict_position = [round((self.front_predict_position[0] + self.front_predict_velocity[0]), 2),
                                     round((self.front_predict_position[1] + self.front_predict_velocity[1]), 2)]
            self.front_predict.append(self.front_predict_position)
        
        
        self.front_predict_jump = self.front_predict_position
        for i in range(0, 5):
            self.front_predict_jump = [round((self.front_predict_jump[0] + self.front_predict_velocity[0]), 2),
                                     round((self.front_predict_jump[1] + self.front_predict_velocity[1]), 2)]
            self.front_predict_jump = [int(i) for i in self.front_predict_jump]
