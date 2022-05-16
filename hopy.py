import pygame
import random
import sys
import numpy as np
import time

from resources.basic_handler import Basic
from resources.button import Button
from resources.player import Player
from resources.AI import AI
from config import config
from pygame import mixer
from numba import jit

# sounds
crash_sound = ""
# initialize sound mixer

# initialize pygame

pygame.init()
clock = pygame.time.Clock()

soundObj = 'resources/kim-lightyear-legends-109307.mp3'
soundObj1 = 'resources/birdies-in-my-headroom.mp3'
soundObj2 = 'resources/life-of-a-wandering-wizard-15549.mp3'
soundObj3 = 'resources/mechropolis-110848.mp3'
soundObj4 = 'resources/neonon-109616.mp3'
soundObj5 = 'resources/pandemic-7749.mp3'
soundObj6 = 'resources/techno-future-drone-main-9724.mp3'
music_list = [soundObj, soundObj1 ,soundObj2 ,soundObj3,soundObj4 ,soundObj5 ,soundObj6]
music_list_temp = music_list
random.shuffle(music_list)

def start_playlist(playList):
    if len(playList) ==0:
        playList = music_list_temp
    pygame.mixer.music.load(music_list.pop())
    pygame.mixer.music.queue(music_list.pop())
    pygame.mixer.music.set_endevent(pygame.USEREVENT+3)
    pygame.mixer.music.play()

pygame.mixer.music.set_volume(0.1)

jump_sound1 = pygame.mixer.Sound('resources/hopy1x2.mp3')
jump_sound2 = pygame.mixer.Sound('resources/hopy2x2.mp3')
jump_sounds =[jump_sound1,jump_sound2]

jump_sound = pygame.mixer.Sound('resources/hopy1x2.mp3')
jump_sound.set_volume(1)
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
ai_players = 1
BACKGROUND_IMG_PATH = "resources/background.jpg"  # background image

pl_head_imgs_list = []  # load images of heads of players
for _ in range(0, active_players):
    PLAYER_HEAD_IMG = pygame.image.load(f'resources/SnakeHead({_ + 1}).png').convert_alpha()
    # PLAYER_HEAD_IMG = pygame.transform.scale(PLAYER_HEAD_IMG, (config.GAME_RES[0], config.GAME_RES[1]))
    PLAYER_HEAD_IMG = pygame.transform.rotate(PLAYER_HEAD_IMG, 180)
    pl_head_imgs_list.append(PLAYER_HEAD_IMG)

SCORE_IMG = pygame.image.load("resources/untitled.png").convert_alpha()
SCORE_IMG = pygame.transform.scale(SCORE_IMG, config.GAME_RES)

# create background
background = Basic(config.ZERO_POS, BACKGROUND_IMG_PATH, False)
background.draw(display1)

# game over text
game_font = pygame.font.SysFont("comicsans", 90, True, True)

# score text for scoretable
score_font = pygame.font.SysFont("comicsans", 30, True, True)

# player name and color text for scoretable
player_font = pygame.font.SysFont("comicsans", 30, True, True)

# draw current time of gameplay
gameplay_time_font = pygame.font.SysFont("comicsans", 40, True, True)

# dt = The clock.tick returns the time since the last call to clock.tick.
# Use that value and multiply all your speeds with it when you move
# dt = clock.tick(60)

# create playable players
if active_players >= 1:
    player1 = Player(config.PLAYER_COLOR, config.PLAYER_POSITIONS["p1"], config.MOVE_PER_SECOND, pl_head_imgs_list[0],
                     config.WORM_SIZE, config.GAME_RES, 0, "p1", display1)
    if active_players >= 2:
        player2 = Player(config.PLAYER_COLOR2, config.PLAYER_POSITIONS["p2"], config.MOVE_PER_SECOND,
                         pl_head_imgs_list[1],
                         config.WORM_SIZE, config.GAME_RES, 0, "p2", display1)
        if active_players >= 3:
            player3 = Player(config.PLAYER_COLOR3, config.PLAYER_POSITIONS["p3"], config.MOVE_PER_SECOND,
                             pl_head_imgs_list[2],
                             config.WORM_SIZE, config.GAME_RES, 0, "p3", display1)
            if active_players >= 4:
                player4 = Player(config.PLAYER_COLOR4, config.PLAYER_POSITIONS["p4"], config.MOVE_PER_SECOND,
                                 pl_head_imgs_list[3],
                                 config.WORM_SIZE, config.GAME_RES, 0, "p4", display1)
AI1, AI2, AI3, AI4, AI5, AI6, AI7, AI8 = 0, 0, 0, 0, 0, 0, 0, 0
PLAYER_LIST = [player1, player2, player3, player4]
# AI_LIST = [AI1, AI2, AI3, AI4, AI5, AI6, AI7, AI8]


AIs = []  # generate multiple AIs

for ai_num in range(5, 5 + ai_players):
    AIs.append(
        AI(config.PLAYER_COLOR5, config.PLAYER_POSITIONS[f"p{ai_num}"], config.MOVE_PER_SECOND, pl_head_imgs_list[0],
           config.WORM_SIZE, config.GAME_RES, 0, "p4", display1))

    # AI(config.PLAYER_COLOR, config.PLAYER_POSITIONS[f"p{ai_num}"], config.MOVE_PER_SECOND, pl_head_imgs_list[0],
    #    config.WORM_SIZE, config.GAME_RES, 0, f"p{ai_num}"))
# PLAYER_LIST = [player1]

# for ai in AIs: # append AI to player list
#     PLAYER_LIST.append(ai)


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

game_state = ["welcome_intro", "running", "menu", "options", "score_screen", "end_screen"]
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
        ANIMATION_COOLDOWN = 10  # define animation cooldown
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


def check_collision(pl):  # check collisions for selected player
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
                x_off = trail_step[0] - pl.head_image_position[0][0]
                y_off = trail_step[1] - pl.head_image_position[0][1]
                if pl.mask1.overlap(others.masktrail, (x_off, y_off)) and not pl.jump:
                    pl.player_collided = True
                    # return pretoze nechcem aby potom slo dalej este ked uz bude veidet ze bola kolizia
                if pl.mask1.overlap(others.masktrail, (x_off, y_off)) and pl.jump:
                    pl.player_collided = False
    for others in AIs:
        if len(others.trail) <= 30:
            pl.player_collided = False
        else:
            for trail_step in (others.trail[0:-30]):
                x_off = trail_step[0] - pl.head_image_position[0][0]
                y_off = trail_step[1] - pl.head_image_position[0][1]
                if pl.mask1.overlap(others.masktrail, (x_off, y_off)) and not pl.jump:
                    pl.player_collided = True
                    # return pretoze nechcem aby potom slo dalej este ked uz bude veidet ze bola kolizia
                if pl.mask1.overlap(others.masktrail, (x_off, y_off)) and pl.jump:
                    pl.player_collided = False

def predict_collision(pl):
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
            for trail_step in (others.trail[0:-15]):
                x_off = trail_step[0] - pl.predict_position[0]
                y_off = trail_step[1] - pl.predict_position[1]
                if pl.mask1.overlap(others.masktrail, (x_off, y_off)) and not pl.jump:
                    ai_jump_handler(ai)
                    print("skok")
                    # return pretoze nechcem aby potom slo dalej este ked uz bude veidet ze bola kolizia
                if pl.mask1.overlap(others.masktrail, (x_off, y_off)) and pl.jump:
                    pl.player_collided = False
    for others in AIs:
        print(others.predict_trail)
        if len(others.predict_trail) <= 30:
            pl.player_collided = False
        else:
            for trail_step in (others.predict_trail[0:-15]):
                x_off = trail_step[0] - pl.predict_position[0]
                y_off = trail_step[1] - pl.predict_position[1]
                if pl.mask1.overlap(others.masktrail, (x_off, y_off)) and not pl.jump:
                    ai_jump_handler(ai)
                    print("skokAI")
                 #   pl.player_collided = True
                    # return pretoze nechcem aby potom slo dalej este ked uz bude veidet ze bola kolizia
                if pl.mask1.overlap(others.masktrail, (x_off, y_off)) and pl.jump:
                    pl.player_collided = False


# TODO niekedy po par sekundach a po par preskokoch nejaky cervik potom prechadza cez vsetky ciarky
# a este potom po restarte pri jeho smrti je hned game over aj ked ostatni ziju


def players_handler(pl):
    if not pl.player_collided:
        check_collision(pl)
        # hodnota 320 je sirka skore tabulky , treba preprogramovat na prisposobovatelne podla rozlisenia
        if 0 + pl.head_image.get_width() / 2 >= pl.position[0] or pl.position[0] >= config.GAME_RES[0] - 320 or \
                0 + pl.head_image.get_height() / 2 >= pl.position[1] or \
                pl.position[1] >= config.GAME_RES[1] - pl.head_image.get_height() / 2:
            pl.player_collided = True
        pl.handle_keys(keys)
        pl.move(pl.velocity[0], pl.velocity[1])
        if pl.trail_allow:
            pl.create_trail()
        pl.draw_trail(pl.trail)
        pl.draw_player()
        pl.player_score()
    else:
        pl.draw_trail(pl.trail)
        pl.draw_player()

    # jumping_handler


def ai_players_handler(ai):
    if not ai.player_collided:
        ai.position_awarness()
        predict_collision(ai)
        check_collision(ai)
        # hodnota 320 je sirka skore tabulky , treba preprogramovat na prisposobovatelne podla rozlisenia
        if 0 + ai.head_image.get_width() / 2 >= ai.position[0] or ai.position[0] >= config.GAME_RES[0] - 320 or \
                0 + ai.head_image.get_height() / 2 >= ai.position[1] or \
                ai.position[1] >= config.GAME_RES[1] - ai.head_image.get_height() / 2:
            ai.player_collided = True
        ai.random_movement()
        # ai.move(ai.velocity[0], ai.velocity[1])
        if ai.trail_allow:
            ai.create_trail()
        ai.draw_trail(ai.trail)
        ai.draw_player()
    else:
        ai.draw_trail(ai.trail)
        ai.draw_player()
  #  print(ai.player_collided)

# jumping_handler
def players_jump_handler(pl):
    pl.seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if pl.jump and pl.jumped_already == False:
        random_sound = random.choice(jump_sounds)
        random_sound.play()
        pl.jumped_already = True

        if pl.jump_time == 0:
            pl.jump_time = pl.seconds
        pl.trail_allow = False

    if pl.seconds - pl.jump_time >= 0.5 and pl.jumped_already == True:
        pl.trail_allow = True
        pl.jump_time = 0
        pl.jumped_already = False
        pl.jump = False

# jumping_handler
def ai_jump_handler(ai):
    ai.seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if not ai.jump:
        ai.ai_jumping()
    if ai.jump and ai.jumped_already == False:
        random_sound = random.choice(jump_sounds)
        random_sound.play()
        ai.jumped_already = True

        if ai.jump_time == 0:
            ai.jump_time = pl.seconds
        ai.trail_allow = False

    if ai.seconds - ai.jump_time >= 0.5 and ai.jumped_already == True:
        print("hopy")
        ai.trail_allow = True
        ai.jump_time = 0
        ai.jumped_already = False
        ai.jump = False


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

start_playlist(music_list)

movement_event = pygame.USEREVENT + 2
pygame.time.set_timer(movement_event, 1000)

score_table_dict = {}
start_time = time.time()
while True:  # creating a running loop

    for event in pygame.event.get():  # creating a loop to check events that are occurring
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.USEREVENT:  # A track has ended
            if (len(music_list) > 0):  # If there are more tracks in the queue...
                pygame.mixer.music.queue(music_list.pop())  # queue a sound file to follow the current

        if event.type == pygame.MOUSEBUTTONDOWN and game_status == "score_screen":
            game_status = "end_screen"

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
                start_time = time.time()
                for ai in AIs:
                    ai.reset()
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
                    jump_sound.set_volume(1)
                    paused_sounds = False
                else:
                    jump_sound.set_volume(0.0)
                    paused_sounds = True

            # MAIN MENU BUTTON
            if 1620 <= mpos[0] <= 1690 and 90 <= mpos[1] <= 160 and mpress[
                0] == True:  # if you want user to do right click on mouse
                game_status = "menu"
                player1.reset()
                player2.reset()
                player3.reset()
                player4.reset()
                for ai in AIs:
                    ai.reset()
        if event.type == movement_event and game_status == "running":
            for ai in AIs:
                if not ai.player_collided:
                    # po urcitom case automaticky skoci ak je povoleny jump handler
                 #   ai.random_movement()
                    pass
                   # ai_jump_handler(ai)

    # launched game
    if game_status == "running":  # clear display with fresh background
        background.draw(display1)
        display1.blit(SCORE_IMG, (0, 0))  # scoretable
        display1.blit(update_fps(), (10, 0))  # fps show
        keys = pygame.key.get_pressed()  # movement of players

        # draw current gameplay time
        elapsed_time = time.time() - start_time
        current_time = time.strftime("%M:%S", time.gmtime(elapsed_time))
        gameplay_time = gameplay_time_font.render(f'{current_time}', True, (255, 255, 255))
        display1.blit(gameplay_time,
                      (config.GAME_RES[0] * 0.95 - gameplay_time.get_width() / 2,
                       config.GAME_RES[1] * 0.115 - gameplay_time.get_height() / 2))

        # players collisions
        for pl in PLAYER_LIST:
            players_handler(pl)
            score_value = score_font.render(f'{pl.score}', True, (255, 255, 255))
            display1.blit(score_value,
                          (config.GAME_RES[0] *0.93 - score_value.get_width() / 2,
                           config.GAME_RES[1] * 0.28 - score_value.get_height() / 2))
        for ai in AIs:
            ai_players_handler(ai)


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


        if dead_players == active_players:
            end_text = game_font.render(f"Game over", True, (255, 255, 255))
            display1.blit(end_text,
                          (config.GAME_RES[0] // 2 - end_text.get_width() / 2,
                           config.GAME_RES[1] * 0.4 - end_text.get_height() / 2))

            guide_text = game_font.render(f"Click mouse for continue", True, (255, 255, 255))
            display1.blit(guide_text,
                          (config.GAME_RES[0] // 2 - guide_text.get_width() / 2,
                           config.GAME_RES[1] * 0.6 - guide_text.get_height() / 2))

            game_status = "score_screen"

    if game_status == "welcome_intro":
        intro.udpate_anim()
        DrawBar(barPos, barSize, borderColor, barColor, intro.frame_index / max_a)
        welcome_text = game_font.render(f"Loading...", True, (0, 0, 0))

        display1.blit(welcome_text, ((config.GAME_RES[0] * 0.8 - int(welcome_text.get_width() / 3)),
                                     (config.GAME_RES[1] / 5 - int(welcome_text.get_size()[1] / 2) - 150)))
        game_status = intro.game_st

    if game_status == "menu":  # menu
        display1.blit(menu_image, (0, 0))
        display1.blit(title_menu, (0, 0))
        if start_button.draw(display1):
            game_status = "running"
        if exit_button.draw(display1):
            pygame.quit()
            sys.exit()
        if options_button.draw(display1):
            game_status = "options"

    if game_status == "options":
        display1.blit(options_menu_image, (0, 0))
        display1.blit(options_menu, (0, 0))
        if menu_button.draw(display1):
            game_status = "menu"
        if exit_button.draw(display1):
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
            pygame.quit()
            sys.exit()

        if menu_button.draw(display1):
            game_status = "menu"

        if restart_button.draw(display1):
            start_time = time.time()
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
            for ai in AIs:
                ai.reset()
            game_status = "running"

    pygame.display.update()  # updating the display
    clock.tick(config.GAME_FPS)

# TODO
# pri skoku zvacsit obrazok hlavy aby sa vytvoril akoze efekt skoku, hlava sa bude zvacsovat do stredu skoku a v druhej
# polovici sa bude znizovat do klasickej velkosti

# TODO ak je hrac mrtvy necheckovat koliziu ani nepridavat novy tail len opakovane zobrazit
# pridat powerup dlhsi  skok ktory sa bude nacitvat pri skorebare pre kazdeho hraca
# pri nacitani zmenit farbu hlavy hada


# TODO
# skusit namiesto float trail suradnic suradnice INT, mozno to usetri pamat alebo bude lepsie kreslit stvorceky
# specialne ked je rec o draw polygons


# TODO
# pri umrti vsetkych hracov najprv zamrazit obrazovku  a napisat ze prehral a az tak po stlaceni tlacidla dajakeho dat na menu s hlasenim ze som prehral

# TODO
# pridat pociatocnu rotaciu hlavy pre zaciatok hry aby sa obrazok cez transform rotate otocil namiesto sucasneho
# klasickeho zadania uhlu ako parameter pre player

# TODO
# AI nech ma novy py subor ktory dedicnostou prevezme player class a prida k nej AI funkcie
