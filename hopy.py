import pygame
import random
import sys
import numpy as np
import time

from resources.basic_handler import Basic
from resources.button import Button
from resources.player import Player
from config import config
from pygame import mixer
from numba import jit

# sounds
crash_sound = ""
# initialize sound mixer

# initialize pygame

pygame.init()
clock = pygame.time.Clock()

soundObj = pygame.mixer.music.load('resources/kim-lightyear-legends-109307.mp3')

pygame.mixer.music.set_volume(0.1)
jump_sound = pygame.mixer.Sound('resources/mixkit-player-jumping-in-a-video-game-2043.wav')
jump_sound.set_volume(0.1)
# window create
display1 = pygame.display.set_mode(config.GAME_RES)
pygame.display.set_caption('Cerviky')
Icon = pygame.image.load('resources/pythonik2.jpg').convert_alpha()
menu_image = pygame.image.load('resources/intro/0400.jpg').convert()
options_menu_image = pygame.image.load('resources/options_menu_backgr.jpg').convert()
menu_image = pygame.transform.scale(menu_image, (config.GAME_RES[0], config.GAME_RES[1]))
endimage = pygame.image.load("resources/end_img.jpg")
endimage = pygame.transform.scale(endimage, (config.GAME_RES[0], config.GAME_RES[1]))
startup_image = pygame.image.load("resources/startup_img2.jpg")
startup_image = pygame.transform.scale(startup_image, (config.GAME_RES[0], config.GAME_RES[1]))
pygame.display.set_icon(Icon)

# active players number
active_players = 4

# number of dead_players
player1_dead = False
player2_dead = False
player3_dead = False
player4_dead = False
dead_players = 0

# AI players number
ai_players = 4
BACKGROUND_IMG_PATH = "resources/background.jpg"  # background image

pl_head_imgs_list = []  #load images of heads of players
for _ in range(0, active_players):
    PLAYER_HEAD_IMG = pygame.image.load(f'resources/SnakeHead({_+1}).png').convert_alpha()
    #PLAYER_HEAD_IMG = pygame.transform.scale(PLAYER_HEAD_IMG, (config.GAME_RES[0], config.GAME_RES[1]))
    PLAYER_HEAD_IMG = pygame.transform.rotate(PLAYER_HEAD_IMG, 180)
    pl_head_imgs_list.append(PLAYER_HEAD_IMG)

SCORE_IMG = pygame.image.load("resources/untitled.png").convert_alpha()
SCORE_IMG = pygame.transform.scale(SCORE_IMG, config.GAME_RES)

# create background
background = Basic(config.ZERO_POS, BACKGROUND_IMG_PATH, False)
background.draw(display1)

# game over text
game_font = pygame.font.SysFont("comicsans", 90, True, True)

# dt = The clock.tick returns the time since the last call to clock.tick.
# Use that value and multiply all your speeds with it when you move
# dt = clock.tick(60)

# create playable players
if active_players >= 1:
    player1 = Player(config.PLAYER_COLOR, config.PLAYER_POSITIONS["p1"], config.MOVE_PER_SECOND, pl_head_imgs_list[0],
                     config.WORM_SIZE, config.GAME_RES, 0, "p1")
    if active_players >= 2:
        player2 = Player(config.PLAYER_COLOR2, config.PLAYER_POSITIONS["p2"], config.MOVE_PER_SECOND,
                         pl_head_imgs_list[1],
                         config.WORM_SIZE, config.GAME_RES, 0, "p2")
        if active_players >= 3:
            player3 = Player(config.PLAYER_COLOR3, config.PLAYER_POSITIONS["p3"], config.MOVE_PER_SECOND,
                             pl_head_imgs_list[2],
                             config.WORM_SIZE, config.GAME_RES, 0, "p3")
            if active_players >= 4:
                player4 = Player(config.PLAYER_COLOR4, config.PLAYER_POSITIONS["p4"], config.MOVE_PER_SECOND,
                                 pl_head_imgs_list[3],
                                 config.WORM_SIZE, config.GAME_RES, 0, "p4")
AI1, AI2, AI3, AI4, AI5, AI6, AI7, AI8 = 0, 0, 0, 0, 0, 0, 0, 0
PLAYER_LIST = [player1, player2, player3, player4]
AI_LIST = [AI1, AI2, AI3, AI4, AI5, AI6, AI7, AI8]

AIs = []  # generate multiple AIs
for ai_num in range(1, ai_players + 1):
    AIs.append(
        Player(config.PLAYER_COLOR, config.PLAYER_POSITIONS[f"p{ai_num}"], config.MOVE_PER_SECOND, pl_head_imgs_list[0],
               config.WORM_SIZE, config.GAME_RES, 0, f"p{ai_num}"))
# PLAYER_LIST = [player1]

# starting direction for move velocity
direction = 0
angle = 0

# music and sound
played_jump_sound = False
paused_music = False
paused_sounds = False

# counter for drawing trail every second not every frame
time_delay = 0
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, time_delay)
start_ticks = pygame.time.get_ticks()

global game_status
game_status = "running"

game_state = ["welcome_intro", "running", "menu", "options" "end_screen"]
font = pygame.font.SysFont("Arial", 18)

def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


# load intro
# display1.blit(menu_image, (0, 0))

# power up bar

barSize = (200, 20)
barPos = (config.GAME_RES[0] / 2 - barSize[0] / 2, config.GAME_RES[1] * 0.95)
borderColor = (0, 0, 0)
barColor = (0, 128, 0)
max_a = 400

def DrawBar(pos, size, borderC, barC, progress):
    pygame.draw.rect(display1, borderC, (*pos, *size), 1)
    innerPos = (pos[0] + 3, pos[1] + 3)
    innerSize = ((size[0] - 6) * progress, size[1] - 6)
    pygame.draw.rect(display1, barC, (*innerPos, *innerSize))

if __name__ == "__main__":  # main
    display1.blit(startup_image, (0, 0))  # startupimage
    intro_text = game_font.render(f"Starting...", True, (0, 0, 0))

    display1.blit(intro_text, ((config.GAME_RES[0] * 0.8 - int(intro_text.get_width() / 3)),
                               (config.GAME_RES[1] / 5 - int(intro_text.get_size()[1] / 2) - 150)))
    pygame.display.update()

intro_animation_list = []

for num_frame in range(1, 401):
    anim = pygame.image.load(f'resources/intro/{num_frame:04d}.jpg').convert()
    anim = pygame.transform.scale(anim, (config.GAME_RES[0], config.GAME_RES[1]))
    intro_animation_list.append(anim)


class Intro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.animations = intro_animation_list
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.anim_img = self.animations[self.frame_index]
        self.anim_rect = self.anim_img.get_rect()
        self.game_st = "welcome_intro"

    def udpate_anim(self):
        ANIMATION_COOLDOWN = 10 # define animation cooldown
        # update image depending on current action
        self.anim_img = self.animations[self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
            self.game_st = "menu"
        display1.blit(self.anim_img, self.anim_rect)

intro = Intro()

def check_collision():  # check collisions for selected player
    # TODO it is checking only when image head is rotated
    if pl.head_image_copy is None:
        pl.mask1 = pygame.mask.from_surface(pl.head_image)
    else:
        pl.mask1 = pygame.mask.from_surface(pl.head_image_copy)
        # it is checking all players including itself
    for others in PLAYER_LIST:
        if len(others.trail) <= 30:
            pl.player_collided = False
        else:
            for trail_step in (others.trail[0:-30]):
                #  print(trail_step)
                x_off = trail_step[0] - pl.head_image_position[0][0]
                y_off = trail_step[1] - pl.head_image_position[0][1]
                if pl.mask1.overlap(others.masktrail, (x_off, y_off)) and not pl.jump:
                    pl.player_collided = True
                    # return pretoze nechcem aby potom slo dalej este ked uz bude veidet ze bola kolizia
                if pl.mask1.overlap(others.masktrail, (x_off, y_off)) and pl.jump:
                    pl.player_collided = False


# TODO niekedy po par sekundach a po par preskokoch nejaky cervik potom prechadza cez vsetky ciarky
# a este potom po restarte pri jeho smrti je hned game over aj ked ostatni ziju

#
# def check_collision(number):
#         # TODO it is checking only when image head is rotated
#         if PLAYER_LIST[number].head_image_copy:
#             PLAYER_LIST[number].mask1 = pygame.mask.from_surface(PLAYER_LIST[number].head_image_copy)
#             # it is checking all players including itself
#             for others in PLAYER_LIST:
#                 for trail_step in others.trail[:-30]:
#
#                     x_off = trail_step[0] - PLAYER_LIST[number].head_image_position[0][0]
#                     y_off = trail_step[1] - PLAYER_LIST[number].head_image_position[0][1]
#                     if PLAYER_LIST[number].mask1.overlap(others.masktrail, (x_off, y_off)) and not PLAYER_LIST[number].jump:
#                         PLAYER_LIST[number].player_collided = True
#                     if PLAYER_LIST[number].mask1.overlap(others.masktrail, (x_off, y_off)) and PLAYER_LIST[number].jump:
#                         PLAYER_LIST[number].player_collided = False

def players_handler(pl):
    if not pl.player_collided:
        check_collision()
        # hodnota 320 je sirka skore tabulky , treba preprogramovat na prisposobovatelne podla rozlisenia
        if 0 + pl.head_image.get_width() / 2 >= pl.position[0] or pl.position[0] >= config.GAME_RES[0] - 320 or \
                0 + pl.head_image.get_height() / 2 >= pl.position[1] or \
                pl.position[1] >= config.GAME_RES[1] - pl.head_image.get_height() / 2:
            pl.player_collided = True
        pl.handle_keys(keys)
        pl.move(pl.velocity[0], pl.velocity[1])
        if pl.trail_allow:
            pl.create_trail()
        pl.draw_player(display1)
        pl.draw_trail(pl.trail)
    pl.draw_player(display1)
    pl.draw_trail(pl.trail)
    # jumping_handler

def players_jump_handler(pl):
    pl.seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if pl.jump and pl.jumped_already== False:
        jump_sound.play()
        pl.jumped_already = True

        # print(pl.seconds)  # calculate how many seconds
        if pl.jump_time == 0:
            pl.jump_time = pl.seconds
        pl.trail_allow = False

    if pl.seconds - pl.jump_time >= 0.5 and pl.jumped_already == True:
        # print("JF jump finish")
        # print(pl.seconds)
        # print("JT" ,pl.jump_time)
        pl.trail_allow = True
        pl.jump_time = 0
        pl.jumped_already = False
        pl.jump = False

# create buttons
start_button_img = pygame.image.load("resources/button_start.png").convert_alpha()
exit_button_img = pygame.image.load("resources/button_quit.png").convert_alpha()
restart_button_img = pygame.image.load("resources/button_restart.png").convert_alpha()
menu_button_img = pygame.image.load("resources/buttons_menu.png").convert_alpha()
options_button_img = pygame.image.load("resources/button_options.png").convert_alpha()

# selected buttons
start_button_selected_img = pygame.image.load("resources/button_start_selected.png").convert_alpha()
exit_button_selected_img = pygame.image.load("resources/button_quit_selected.png").convert_alpha()
restart_button_selected_img = pygame.image.load("resources/button_restart_selected.png").convert_alpha()
menu_button_selected_img = pygame.image.load("resources/buttons_menu_selected.png").convert_alpha()
options_button_selected_img = pygame.image.load("resources/button_options_selected.png").convert_alpha()

start_button = Button(start_button_img, start_button_selected_img)
options_button = Button(options_button_img, options_button_selected_img)
menu_button = Button(menu_button_img, menu_button_selected_img)
exit_button = Button(exit_button_img, exit_button_selected_img)
restart_button = Button(restart_button_img, restart_button_selected_img)

title_menu = pygame.image.load("resources/title_menu.png").convert_alpha()
options_menu = pygame.image.load("resources/options_menu.png").convert_alpha()

pygame.mixer.music.play(-1)

while True: # creating a running loop

    for event in pygame.event.get():  # creating a loop to check events that are occurring
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and game_status == "running":
            mpress = pygame.mouse.get_pressed()
            mpos = pygame.mouse.get_pos()

            # EXIT GAME BUTTON
            if 1855 <= mpos[0] <= 1910 and 15 <= mpos[1] <= 75 and mpress[
                0] == True:  # if you want user to do right click on mouse
                pygame.quit()
                sys.exit()
            # RESTART GAME BUTTON
            if 1775 <= mpos[0] <= 1850 and 15 <= mpos[1] <= 75 and mpress[
                0] == True:  # if you want user to do right click on mouse
                player1.reset()
                player2.reset()
                player3.reset()
                player4.reset()
                dead_players = 0
                jump_time = 0
                player1.jumped_already = False
                player2.jumped_already = False
                player3.jumped_already = False
                player4.jumped_already = False
                player1_dead = False
                player2_dead = False
                player3_dead = False
                player4_dead = False
            # MUSIC BUTTON
            if 1700 <= mpos[0] <= 1750 and 15 <= mpos[1] <= 75 and mpress[
                0] == True:  # if you want user to do right click on mouse
                if paused_music:
                    pygame.mixer.music.unpause()
                    paused_music = False
                else:
                    pygame.mixer.music.pause()
                    paused_music = True
            # SOUNDS  BUTTON
            if 1620 <= mpos[0] <= 1690 and 20 <= mpos[1] <= 75 and mpress[
                0] == True:  # if you want user to do right click on mouse
                if paused_sounds:
                    jump_sound.set_volume(0.1)
                    paused_sounds = False
                else:
                    jump_sound.set_volume(0.0)
                    paused_sounds = True
                    print("tlacidlo")

            # MAIN MENU BUTTON
            if 1620 <= mpos[0] <= 1690 and 90 <= mpos[1] <= 160 and mpress[
                0] == True:  # if you want user to do right click on mouse
                game_status = "menu"
                player1.reset()
                player2.reset()
                player3.reset()
                player4.reset()

    # launched game
    if game_status == "running":  # clear display with fresh background
        background.draw(display1)
        keys = pygame.key.get_pressed()  # movement of players
        # AI
        # for ai_act in AIs:
        #     ai_act.draw_player(display1)
        #     if not ai_act.player_collided:
        #       #  check_collision(8888)
        #         ai_act.handle_keys(keys)
        #         ai_act.move(ai_act.velocity[0], ai_act.velocity[1])
        #         if trail_allow:
        #             ai_act.create_trail()

        # players collisions
        for pl in PLAYER_LIST:
            players_handler(pl)
        if player1.player_collided and not player1_dead:
            dead_players += 1
            player1_dead = True
        if player2.player_collided and not player2_dead:
            dead_players += 1
            player2_dead = True
        if player3.player_collided and not player3_dead:
            dead_players += 1
            player3_dead = True
        if player4.player_collided and not player4_dead:
            dead_players += 1
            player4_dead = True

        for pl in PLAYER_LIST:
            players_jump_handler(pl)

        # TODO namiesto rect draw polygon pre usporenie pamate a viac fps
        # TODO pripadne spravit namiesto rect iba obrazky ktore sa budu pridavat
        # TODO bug pri preskakovani hned za hlavou protivnika..neni kolizia
        # POKLES FPS - poskles fps nevyrieseny convert() prikazom pri loadovani suboru
        # again draw player head becouse of trail visibility


        display1.blit(SCORE_IMG, (0, 0))   # scoretable
        display1.blit(update_fps(), (10, 0))  # fps show

        if dead_players == active_players:
            end_text = game_font.render(f"Game over", True, (255, 255, 255))
            display1.blit(end_text,
                          (config.GAME_RES[0] // 2 - end_text.get_width(),
                           config.GAME_RES[1] // 2 - end_text.get_height() / 2))

            # TODO pridat reset button
            game_status = "end_screen"

    if game_status == "welcome_intro":
        intro.udpate_anim()
        DrawBar(barPos, barSize, borderColor, barColor, intro.frame_index / max_a)
        welcome_text = game_font.render(f"Loading...", True, (0, 0, 0))

        display1.blit(welcome_text, ((config.GAME_RES[0] * 0.8 - int(welcome_text.get_width() / 3)),
                                     (config.GAME_RES[1] / 5 - int(welcome_text.get_size()[1] / 2) - 150)))
        game_status = intro.game_st

    if game_status == "menu":          # menu
        display1.blit(menu_image, (0, 0))
        display1.blit(title_menu, (0, 0))
        if start_button.draw(display1):
            game_status = "running"
            print("clicked start ")
        if exit_button.draw(display1):
            print("clicked quit ")
            pygame.quit()
            sys.exit()
        if options_button.draw(display1):
            print("clicked options ")
            game_status = "options"

    if game_status == "options":
        display1.blit(options_menu_image, (0, 0))
        display1.blit(options_menu, (0, 0))
        if menu_button.draw(display1):
            game_status = "menu"
            print("clicked menu ")
        if exit_button.draw(display1):
            print("clicked quit ")
            pygame.quit()
            sys.exit()

    if game_status == "end_screen":
        pygame.mixer.pause()
        score_text = game_font.render(f"skóre ", True, (0, 0, 0))
        display1.blit(endimage, (0, 0))

        display1.blit(score_text, (5, 0))
        end_text = game_font.render(f"Game over", True, (0, 0, 0))

        display1.blit(end_text, ((config.GAME_RES[0] * 0.8 - int(end_text.get_width() / 3)),
                                 (config.GAME_RES[1] / 5 - int(end_text.get_size()[1] / 2) - 150)))
        if exit_button.draw(display1):
            print("clicked quit ")
            pygame.quit()
            sys.exit()

        if menu_button.draw(display1):
            print("clicked menu ")
            game_status = "menu"

        if restart_button.draw(display1):
            print("clicked restart")
            dead_players = 0
            trail_allow = True
            jump_time = 0
            player1.jumped_already = False
            player1_dead = False
            player2_dead = False
            player3_dead = False
            player4_dead = False
            player1.reset()
            player2.reset()
            player3.reset()
            player4.reset()
            game_status = "running"

    pygame.display.update()  # updating the display
    clock.tick(config.GAME_FPS)
#  pygame.display.flip()

# TODO
# pri skoku zvacsit obrazok hlavy aby sa vytvoril akoze efekt skoku, hlava sa bude zvacsovat do stredu skoku a v druhej
# polovici sa bude znizovat do klasickej velkosti

# TODO ak je hrac mrtvy necheckovat koliziu ani nepridavat novy tail len opakovane zobrazit
# pridat powerup dlhsi  skok ktory sa bude nacitvat pri skorebare pre kazdeho hraca
# pri nacitani zmenit farbu hlavy hada


# TODO
# skusit namiesto float trail suradnic suradnice INT, mozno to usetri pamat alebo bude lepsie kreslit stvorceky
# specialne ked je rec o draw polygons
