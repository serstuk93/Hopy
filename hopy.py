import copy
import pygame
import pygame.freetype
import random
import sys
import time
import itertools

from resources.basic_handler import Basic
from resources.button import Button
from resources.player import Player
from resources.AI import AI
from config import config


# sounds
crash_sound = ""



# initialize pygame
pygame.init()
clock = pygame.time.Clock()

active_players = 1  # active players number
ai_players = 3  # AI players number
dead_players = 0  # number of dead_players
dead_ai = 0

soundObj = "resources/kim-lightyear-legends-109307.mp3"
soundObj1 = "resources/birdies-in-my-headroom.mp3"
soundObj2 = "resources/life-of-a-wandering-wizard-15549.mp3"
soundObj3 = "resources/mechropolis-110848.mp3"
soundObj4 = "resources/neonon-109616.mp3"
soundObj5 = "resources/pandemic-7749.mp3"
soundObj6 = "resources/techno-future-drone-main-9724.mp3"
music_list = [
    soundObj,
    soundObj1,
    soundObj2,
    soundObj3,
    soundObj4,
    soundObj5,
    soundObj6,
]
music_list_temp = copy.deepcopy(music_list)
random.shuffle(music_list)


def start_playlist(play_list_atr):
    play_list = play_list_atr
    if len(play_list_atr) == 0:
        play_list = copy.deepcopy(music_list_temp)
    pygame.mixer.music.load(play_list.pop())
    pygame.mixer.music.queue(play_list.pop())
    pygame.mixer.music.set_endevent(pygame.USEREVENT + 3)
    pygame.mixer.music.play()


pygame.mixer.music.set_volume(0.1)

jump_sound1 = pygame.mixer.Sound("resources/hopy1x2.mp3")
jump_sound2 = pygame.mixer.Sound("resources/hopy2x2.mp3")
jump_sounds = [jump_sound1, jump_sound2]

jump_sound = pygame.mixer.Sound("resources/hopy1x2.mp3")
jump_sound.set_volume(1)
# window create
display1 = pygame.display.set_mode(config.GAME_RES)
pygame.display.set_caption("Hoppy Worms")
Icon = pygame.image.load("resources/pythonik2.jpg").convert_alpha()
menu_image = pygame.image.load("resources/intro/0400.jpg").convert()
options_menu_image = pygame.image.load("resources/options_menu_backgr.jpg").convert()
menu_image = pygame.transform.scale(
    menu_image, (config.GAME_RES[0], config.GAME_RES[1])
)
endimage = pygame.image.load("resources/game_over_img.png").convert()
endimage = pygame.transform.scale(endimage, (config.GAME_RES[0], config.GAME_RES[1]))
startup_image = pygame.image.load("resources/startup_img2.jpg").convert()
startup_image = pygame.transform.scale(
    startup_image, (config.GAME_RES[0], config.GAME_RES[1])
)
keyboard_img = pygame.image.load("resources/Keyboard.png").convert()
keyboard_img = pygame.transform.scale(
    keyboard_img, (config.GAME_RES[0], config.GAME_RES[1])
)
pygame.display.set_icon(Icon)



BACKGROUND_IMG_PATH = [
    "resources/basic.jpg",
    "resources/abstract.png",
    "resources/fractals.jpg",
]
BACKGROUND_IMG_PATH_TEMP = copy.deepcopy(BACKGROUND_IMG_PATH)

# for bg in RAW_BACKGROUND_PATH:
#     background_image = pygame.image.load(bg).convert()
#     BACKGROUND_IMG_PATH.append(background_image)

pl_head_imgs_list = []  # load images of heads of players
for _ in range(1, 13): # TODO  change it back to 13 when fix of animation is finished 
    PLAYER_HEAD_IMG = pygame.image.load(f"resources/SnakeHead({_}).png").convert_alpha()
    PLAYER_HEAD_IMG = pygame.transform.rotate(
        PLAYER_HEAD_IMG, config.PLAYER_ROTATIONS[f"p{_}"]
    )
    pl_head_imgs_list.append(PLAYER_HEAD_IMG)
SCORE_IMG = pygame.image.load("resources/Untitled.png").convert_alpha()
SCORE_IMG = pygame.transform.scale(SCORE_IMG, config.GAME_RES)

background = Basic(config.ZERO_POS, BACKGROUND_IMG_PATH[0], False)  # create background
background.draw(display1)

game_font = pygame.font.SysFont("comicsans", 90, True, True)  # game over text
opt_fps_font = pygame.font.SysFont("comicsans", 45, True, True)  # options fps font
opt_map_font = pygame.font.SysFont("comicsans", 25, True, True)
font_file = pygame.font.match_font("Arial", False, True)
font_f = pygame.font.Font(font_file, 30)
score_font = pygame.font.SysFont(
    "comicsans", 30, True, True
)  # score text for scoretable

player_font = pygame.font.SysFont(
    "comicsans", 30, True, True
)  # player name and color text for scoretable
gameplay_time_font = pygame.font.SysFont(
    "comicsans", 40, True, True
)  # draw current time of gameplay

PLAYER_LIST = []


# AI_LIST = [AI1, AI2, AI3, AI4, AI5, AI6, AI7, AI8]
def player_generator():
    for pl_num in range(1, active_players + 1):
        str_pl = f"PLAYER_COLOR{pl_num}"
        PLAYER_LIST.append(
            Player(
                config.PLAYER_COLOR[pl_num - 1],
                config.PLAYER_POSITIONS[f"p{pl_num}"],
                config.MOVE_PER_FRAME,
                pl_head_imgs_list[pl_num - 1],
                config.WORM_SIZE,
                config.GAME_RES,
                config.PLAYER_ROTATIONS[f"p{pl_num}"],
                f"p{pl_num}",
                display1,
            )
        )


AIs = []  # generate multiple AIs


def ai_player_generator():
    for ai_num in range(5, 5 + ai_players):
        AIs.append(
            AI(
                config.PLAYER_COLOR[ai_num - 1],
                config.PLAYER_POSITIONS[f"p{ai_num}"],
                config.MOVE_PER_FRAME,
                pl_head_imgs_list[ai_num - 1],
                config.WORM_SIZE,
                config.GAME_RES,
                config.PLAYER_ROTATIONS[f"p{ai_num}"],
                f"p{ai_num}",
                display1,
            )
        )


player_generator()
ai_player_generator()
# music and sound
played_jump_sound = False
paused_music = False
paused_sounds = False

# counter for drawing trail every second not every frame
time_delay = 200
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, time_delay)
start_ticks = pygame.time.get_ticks()

font = pygame.font.SysFont("Arial", 18)


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, True, pygame.Color("coral"))
    return fps_text


def strike_text(text):
    result = ""
    for c in text:
        result = "\u0336".join(text) + "\u0336"
    return result


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
    display1.blit(
        intro_text,
        (
            (config.GAME_RES[0] * 0.8 - int(intro_text.get_width() / 3)),
            (config.GAME_RES[1] / 5 - int(intro_text.get_size()[1] / 2) - 150),
        ),
    )
    pygame.display.update()

intro_animation_list = []

for num_frame in range(1, 401):
    anim = pygame.image.load(f"resources/intro/{num_frame:04d}.jpg").convert()
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

        self.anim_img = self.animations[
            self.frame_index
        ]  # update image depending on current action
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(
            self.animations
        ):  # if the animation has run out then reset back to the start
            self.frame_index = 0
            self.game_st = "menu"
        display1.blit(self.anim_img, self.anim_rect)


intro = Intro()
all_players_list = PLAYER_LIST + AIs


# TODO zamenit for loop za while a pridat step alebo cez np
def check_collision():  # check collisions for selected player
    # TODO mixkit-player-jumping-in-a-video-game-2043.wav ako death sound
    for player in all_players_list:
        if not player.player_collided:
            player.predict_jump_checker = False
            for pl in all_players_list:
                
                if pl == player:
                    if len(player.trail) <= 11:
                        player.player_collided = False
                    else:
                        if player.jumped_already:
                            stp = -1
                        else:
                            stp = -10
                        
                        for trail_step in pl.trail[:stp]:
                            if player.predict_jump_checker == True:
                                break 
                            x_off = trail_step[0][0] - player.position[0]
                            y_off = trail_step[0][1] - player.position[1]
                            if hasattr(player, "predict_position"):
                                for i in itertools.chain(player.predict_trail,player.predict_trail_around):
                                    pre_x_off = trail_step[0][0] - i[0]
                                    pre_y_off = trail_step[0][1] - i[1]
                                    if (
                                        player.mask_center.overlap(
                                            pl.masktrail, (pre_x_off, pre_y_off)
                                        )
                                        and not player.jumped_already
                                    ):
                                        player.predict_jump_checker = True # TODO predict jump checker find another way how to inplement it 
                                        player.player_collided = False
                                        break
                                    elif (
                                        player.mask_center.overlap(
                                            pl.masktrail, (pre_x_off, pre_y_off)
                                        )
                                        and player.jumped_already
                                    ):
                                    #    player.drop_collision_handler()
                                        player.incoming_drop_collision = True 
                                        player.predict_jump_checker = False
                                        player.player_collided = False
                                        break 
                            if (
                                player.mask_center.overlap(pl.masktrail, (x_off, y_off))
                                and not player.jumped_already
                            ):
                                player.player_collided = True
                                break
                            if (
                                player.mask_center.overlap(pl.masktrail, (x_off, y_off))
                                and player.jumped_already
                            ):
                                player.incoming_drop_collision = True 
                                player.predict_jump_checker = True
                                player.player_collided = False
                                break 
                else:
                    for trail_step in pl.trail:
                        if player.predict_jump_checker == True:
                            break 

                      #  print("HI",player.head_image_position)
                       # print("TS",trail_step)
                        x_off = trail_step[0][0] - player.position[0]
                        y_off = trail_step[0][1] - player.position[1]
                        if hasattr(player, "predict_position"):
                            for i in itertools.chain(player.predict_trail,player.predict_trail_around):
                                pre_x_off = trail_step[0][0] - i[0]
                                pre_y_off = trail_step[0][1] - i[1]
                                if (
                                    player.mask_center.overlap(
                                        pl.masktrail, (pre_x_off, pre_y_off)
                                    )
                                    and not player.jumped_already
                                ):
                                    player.predict_jump_checker = True
                                    player.player_collided = False
                                    break
                                elif (
                                    player.mask_center.overlap(
                                        pl.masktrail, (pre_x_off, pre_y_off)
                                    )
                                    and player.jumped_already
                                ):
                                    player.predict_jump_checker = False
                                    player.incoming_drop_collision = True 
                                    player.player_collided = False
                                    break 
                        if (
                            player.mask_center.overlap(pl.masktrail, (x_off, y_off))
                            and not player.jumped_already
                        ):
                            player.player_collided = True
                            break
                        if (
                            player.mask_center.overlap(pl.masktrail, (x_off, y_off))
                            and player.jumped_already
                        ):
                            player.incoming_drop_collision = True 
                            player.predict_jump_checker = True
                            player.player_collided = False
                            break 


# TODO optimalizacia - skore tabulka aj hodnoty skore a cas aktualizovat iba po 1 sekunde a nie kazdy frame
# TODO stale sa trail tvori v strede hlavy,pretvorit aby sa tvoril vzadu

time_elapsed = 0 

def players_handler(pl,time_el):
    time_elapsed = time_el
    if not pl.player_collided:
        players_jump_handler(pl)
        # TODO hodnota 320 je sirka skore tabulky , treba preprogramovat na prisposobovatelne podla rozlisenia
        if (
            0 + pl.head_image.get_width() / 2 >= pl.position[0]
            or pl.position[0] >= config.GAME_RES[0] - 320
            or 0 + pl.head_image.get_height() / 2 >= pl.position[1]
            or pl.position[1] >= config.GAME_RES[1] - pl.head_image.get_height() / 2
        ):
            pl.player_collided = True
        
        pl.move(pl.velocity[0], pl.velocity[1])
       # ttt = clock.tick() 
      #  print(pl.velocity)
       # time_elapsed += ttt
       # print(time_elapsed)
        # dt is measured in milliseconds, therefore 250 ms = 0.25 seconds
      #  if time_elapsed > 3:
            
            
       #     time_elapsed = 0 # reset it to 0 so you can count again
        pl.handle_keys(keys)
        if pl.trail_allow:
            pl.create_trail()
        pl.draw_trail(pl.trail)
        pl.draw_player()
        pl.player_score()
    else:
        # TODO preprogramovat aby chvost sa objavoval az za hlavou,
        #  potom nebudme musiet mat v kolizii vynechane 20 body trailu
        pl.draw_trail(pl.trail)
        pl.draw_player()


def ai_players_handler(ai):
    if not ai.player_collided:
        ai.now = pygame.time.get_ticks()
        ai.position_awarness()
        ai.random_movement()
        # TODO hodnota 320 je sirka skore tabulky , treba preprogramovat na prisposobovatelne podla rozlisenia
        if (
            0 + ai.head_image.get_width() / 2 >= ai.position[0]
            or ai.position[0] >= config.GAME_RES[0] - 320
            or 0 + ai.head_image.get_height() / 2 >= ai.position[1]
            or ai.position[1] >= config.GAME_RES[1] - ai.head_image.get_height() / 2
        ):
            ai.player_collided = True
        if  ai.predict_jump_checker==True or ai.trail_allow==False:
            ai_jump_handler(ai)
        if ai.trail_allow:
            ai.create_trail()
        ai.draw_trail(ai.trail)
        ai.draw_player()
        ai.player_score()
    else:
        ai.draw_trail(ai.trail)
        ai.draw_player()


def ai_jump_handler(ai):  # ai jumping_handler
    ai.seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if not ai.jump:
        ai.ai_jumping()
    if ai.jump and ai.jumped_already == False and ai.seconds - pl.seconds_temp > 0.1:
        random_sound = random.choice(jump_sounds)
        random_sound.play()
        ai.jumped_already = True
        if ai.jump_time == 0:
            ai.jump_time = ai.seconds
        ai.trail_allow = False

    if ai.seconds - ai.jump_time >= 0.5 and ai.jumped_already == True:
        ai.trail_allow = True
        ai.jump_time = 0
        ai.jumped_already = False
        ai.jump = False
      #  ai.predict_jump_checker = False
        ai.seconds_temp = pl.seconds


def players_jump_handler(pl):  # jumping_handler
    pl.seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if pl.jump and pl.jumped_already == False and pl.seconds - pl.seconds_temp > 0.1:
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
        pl.seconds_temp = pl.seconds


# create buttons
start_button_img = pygame.image.load("resources/button_start.png").convert_alpha()
exit_button_img = pygame.image.load("resources/button_quit.png").convert_alpha()
restart_button_img = pygame.image.load("resources/button_restart.png").convert_alpha()
menu_button_img = pygame.image.load("resources/buttons_menu.png").convert_alpha()
options_button_img = pygame.image.load("resources/button_options.png").convert_alpha()

# selected buttons
start_button_selected_img = pygame.image.load(
    "resources/button_start_selected.png"
).convert_alpha()
exit_button_selected_img = pygame.image.load(
    "resources/button_quit_selected.png"
).convert_alpha()
restart_button_selected_img = pygame.image.load(
    "resources/button_restart_selected.png"
).convert_alpha()
menu_button_selected_img = pygame.image.load(
    "resources/buttons_menu_selected.png"
).convert_alpha()
options_button_selected_img = pygame.image.load(
    "resources/button_options_selected.png"
).convert_alpha()

title_menu = pygame.image.load("resources/title_menu.png").convert_alpha()
options_menu = pygame.image.load("resources/options_menu.png").convert_alpha()
options_menu_selections = pygame.image.load(
    "resources/options_menu_selections.png"
).convert_alpha()

# options selected buttons
opt_selected_buttons_list = []
for _ in range(0, 7):
    button_selected_img = pygame.image.load(
        f"resources/options_menu_selections_{_ + 1}.png"
    ).convert_alpha()
    opt_selected_buttons_list.append(button_selected_img)
opt_not_selected_buttons_list = []
for _ in range(0, 7):
    button_not_selected_img = pygame.image.load(
        f"resources/options_menu_selections{_}.png"
    ).convert_alpha()
    opt_not_selected_buttons_list.append(button_not_selected_img)
opt_buttons = []
for _ in range(0, 7):
    opt_button = Button(opt_not_selected_buttons_list[_], opt_selected_buttons_list[_])
    opt_buttons.append(opt_button)
opt_action_list = [True, False, +1, -1]
opt_arrows_list = []
for _ in range(1, 3):
    arrow_img = pygame.image.load(
        f"resources/options_menu_arrows{_}.png"
    ).convert_alpha()
    opt_arrows_list.append(arrow_img)
# opt1_button_selected_img = pygame.image.load("resources/options_menu_selections_1.png").convert_alpha()
# opt2_button_selected_img = pygame.image.load("resources/options_menu_selections_2.png").convert_alpha()
# opt3_button_selected_img = pygame.image.load("resources/options_menu_selections_3.png").convert_alpha()
# opt4_button_selected_img = pygame.image.load("resources/options_menu_selections_4.png").convert_alpha()
# opt5_button_selected_img = pygame.image.load("resources/options_menu_selections_5.png").convert_alpha()
# opt6_button_selected_img = pygame.image.load("resources/options_menu_selections_6.png").convert_alpha()


start_button = Button(start_button_img, start_button_selected_img)
options_button = Button(options_button_img, options_button_selected_img)
menu_button = Button(menu_button_img, menu_button_selected_img)
exit_button = Button(exit_button_img, exit_button_selected_img)
restart_button = Button(restart_button_img, restart_button_selected_img)

start_playlist(music_list)

score_table_dict = {}
start_time = time.time()

time_before = pygame.time.get_ticks()

game_state = [
    "welcome_intro",
    "running",
    "menu",
    "options",
    "keyboard",
    "score_screen",
    "end_screen",
]
global game_status
game_status = "running"
# TODO pridat obrazovku klavesnice s ovladanim

while True:  # creating a running loop

    for pl in all_players_list:
        if not pl.player_collided:
            pl.update_animation()
    
    time_now = pygame.time.get_ticks()
    for (
        event
    ) in pygame.event.get():  # creating a loop to check events that are occurring
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.USEREVENT:  # A track has ended
            if len(music_list) > 0:  # If there are more tracks in the queue...
                pygame.mixer.music.queue(
                    music_list.pop()
                )  # queue a sound file to follow the current

        if event.type == pygame.MOUSEBUTTONDOWN and game_status == "score_screen":
            game_status = "end_screen"

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE and game_status == "keyboard":
                game_status = "options"
        if event.type == pygame.MOUSEBUTTONDOWN and game_status == "running":
            mpress = pygame.mouse.get_pressed()
            mpos = pygame.mouse.get_pos()

            # EXIT GAME BUTTON
            if 1855 <= mpos[0] <= 1910 and 15 <= mpos[1] <= 75 and mpress[0] == True:
                pygame.quit()
                sys.exit()
            # RESTART GAME BUTTON
            if 1775 <= mpos[0] <= 1850 and 15 <= mpos[1] <= 75 and mpress[0] == True:
                for pl in all_players_list:
                    pl.reset()
                start_time = time.time()
                dead_players = 0
                dead_ai = 0
                jump_time = 0

            # MUSIC BUTTON
            if 1700 <= mpos[0] <= 1750 and 15 <= mpos[1] <= 75 and mpress[0] == True:
                if paused_music:
                    pygame.mixer.music.unpause()
                    paused_music = False
                else:
                    pygame.mixer.music.pause()
                    paused_music = True
            # SOUNDS  BUTTON
            if 1620 <= mpos[0] <= 1690 and 20 <= mpos[1] <= 75 and mpress[0] == True:
                if paused_sounds:
                    jump_sound.set_volume(1)
                    paused_sounds = False
                else:
                    jump_sound.set_volume(0.0)
                    paused_sounds = True

            # MAIN MENU BUTTON
            if 1620 <= mpos[0] <= 1690 and 90 <= mpos[1] <= 160 and mpress[0] == True:
                game_status = "menu"
                for pl in all_players_list:
                    pl.reset()

        # if event.type == pygame.MOUSEBUTTONDOWN and game_status == "options":
        #     mpress = pygame.mouse.get_pressed()
        #     mpos = pygame.mouse.get_pos()
        #
        #     # OPT1
        #     for _ in range (0,6):
        #         if 735 <= mpos[0] <= 850 and 70+160*_ <= mpos[1] <= 190+160*_ and mpress[0] == True:
        #             display1.blit(opt_selected_buttons_list[_], (0, 0))

    if game_status == "running":  # launched game
        background.draw(display1)  # clear display with fresh background
        display1.blit(update_fps(), (10, 0))  # fps show
        keys = pygame.key.get_pressed()  # movement of players
        elapsed_time = time.time() - start_time
        current_time = time.strftime("%M:%S", time.gmtime(elapsed_time))
        gameplay_time = gameplay_time_font.render(
            f"{current_time}", True, (255, 255, 255)
        )
        display1.blit(SCORE_IMG, (0, 0))  # scoretable
        display1.blit(
            gameplay_time,
            (
                config.GAME_RES[0] * 0.95 - gameplay_time.get_width() / 2,
                config.GAME_RES[1] * 0.118 - gameplay_time.get_height() / 2,
            ),
        )

        for pl in PLAYER_LIST:
            players_handler(pl,0)

            if pl.player_collided and not pl.player_dead:
                dead_players += 1
                pl.player_dead = True

        for ai in AIs:
            ai_players_handler(ai)                    
            ai.debug_prediction()
            ai.debug_borders()
            if ai.player_collided and not ai.player_dead:
                dead_ai += 1
                ai.player_dead = True

        for numpl in range(0, len(all_players_list)):
            if all_players_list[numpl] in PLAYER_LIST:
                
                if not all_players_list[numpl].player_dead:
                    score_value = font_f.render(
                        f"PLAYER{numpl + 1} {all_players_list[numpl].score}",
                        True,
                        all_players_list[numpl].color,
                    )
                else:
                    t1 = strike_text(f"PLAYER{numpl + 1}")
                    writing = font_f.render(t1, True, (0, 0, 0))
                    score_value = font_f.render(
                        t1 + f" {all_players_list[numpl].score}",
                        True,
                        all_players_list[numpl].color,
                    )
            else:
                if not all_players_list[numpl].player_dead:
                    score_value = font_f.render(
                        f"AI{numpl - active_players + 1} {all_players_list[numpl].score}",
                        True,
                        all_players_list[numpl].color,
                    )
                else:
                    score_value = font_f.render(
                        strike_text(f"AI{numpl - active_players + 1}")
                        + f" {all_players_list[numpl].score}",
                        True,
                        all_players_list[numpl].color,
                    )
            display1.blit(score_value, (config.SCORE_POSITIONS[str(numpl + 1)]))

        if time_now - time_before >= time_delay:
            time_before = time_now
            check_collision() 

        # TODO namiesto rect draw polygon pre usporenie pamate a viac fps
        # TODO pripadne spravit namiesto rect iba obrazky ktore sa budu pridavat

        
        if (
            dead_players == active_players
            or dead_ai < ai_players
            and dead_players == active_players
            or active_players - dead_players == 1
            and dead_ai == ai_players
        ):
            end_text = game_font.render(f"Game over", True, (255, 255, 255))
            display1.blit(
                end_text,
                (
                    config.GAME_RES[0] // 2 - end_text.get_width() / 2,
                    config.GAME_RES[1] * 0.4 - end_text.get_height() / 2,
                ),
            )
            guide_text = game_font.render(
                f"dead ai:{dead_ai}, dead players:{dead_players}", True, (255, 255, 255)
            )
            guide_text1 = game_font.render(
                f"Click mouse for continue", True, (255, 255, 255)
            )
            display1.blit(
                guide_text,
                (
                    config.GAME_RES[0] // 2 - guide_text.get_width() / 2,
                    config.GAME_RES[1] * 0.6 - guide_text.get_height() / 2,
                ),
            )
            display1.blit(
                guide_text1,
                (
                    config.GAME_RES[0] // 2 - guide_text.get_width() / 2,
                    config.GAME_RES[1] * 0.7 - guide_text.get_height() / 2,
                ),
            )

            game_status = "score_screen"
        
    if game_status == "welcome_intro":
        intro.udpate_anim()
        DrawBar(barPos, barSize, borderColor, barColor, intro.frame_index / max_a)
        welcome_text = game_font.render(f"Loading...", True, (0, 0, 0))

        display1.blit(
            welcome_text,
            (
                (config.GAME_RES[0] * 0.8 - int(welcome_text.get_width() / 3)),
                (config.GAME_RES[1] / 5 - int(welcome_text.get_size()[1] / 2) - 150),
            ),
        )
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

        #   display1.blit(options_menu_image, (0, 0))
        for _ in range(0, 7):
            if opt_buttons[_].draw(display1):
                if _ == 0:
                    if active_players < 4:
                        active_players += 1
                    else:
                        active_players = 1
                    PLAYER_LIST = []
                    player_generator()
                    all_players_list = PLAYER_LIST + AIs
                if _ == 1:
                    if ai_players < 8:
                        ai_players += 1
                    else:
                        ai_players = 1
                    AIs = []
                    ai_player_generator()
                    all_players_list = PLAYER_LIST + AIs
                if _ == 2:
                    if config.GAME_FPS == 60:
                        config.GAME_FPS = 120
                        config.MOVE_PER_FRAME = config.MOVE_PER_FRAME / 2 
                    else:
                        config.GAME_FPS = 60
                        config.MOVE_PER_FRAME = 2
                    AIs = []
                    ai_player_generator()
                    PLAYER_LIST = []
                    player_generator()
                    all_players_list = PLAYER_LIST + AIs
                if _ == 3:
                    if paused_music:
                        pygame.mixer.music.unpause()
                        paused_music = False
                    else:
                        pygame.mixer.music.pause()
                        paused_music = True
                if _ == 4:
                    if len(BACKGROUND_IMG_PATH) == 1:
                        BACKGROUND_IMG_PATH = copy.deepcopy(BACKGROUND_IMG_PATH_TEMP)

                    else:
                        BACKGROUND_IMG_PATH.pop(0)
                    background = Basic(config.ZERO_POS, BACKGROUND_IMG_PATH[0], False)

                if _ == 5:
                    pass

                if _ == 6:
                    game_status = "keyboard"

        display1.blit(options_menu, (0, 0))
        player_num_text = game_font.render(str(active_players), True, (0, 0, 0))
        ai_num_text = game_font.render(str(ai_players), True, (0, 0, 0))
        fps_num_text = opt_fps_font.render(str(config.GAME_FPS), True, (0, 0, 0))
        music_status_text = opt_fps_font.render(
            str(not bool(paused_music)), True, (0, 0, 0)
        )
        map_status_text = opt_map_font.render(
            str(BACKGROUND_IMG_PATH[0][10:-4]), True, (0, 0, 0)
        )
        display1.blit(
            player_num_text,
            (
                795 - player_num_text.get_width() / 2,
                (130 - player_num_text.get_height() / 2),
            ),
        )
        display1.blit(
            ai_num_text,
            (795 - ai_num_text.get_width() / 2, (290 - ai_num_text.get_height() / 2)),
        )
        display1.blit(
            fps_num_text,
            (795 - fps_num_text.get_width() / 2, (450 - fps_num_text.get_height() / 2)),
        )
        display1.blit(
            music_status_text,
            (
                795 - music_status_text.get_width() / 2,
                (610 - music_status_text.get_height() / 2),
            ),
        )
        display1.blit(
            map_status_text,
            (
                795 - map_status_text.get_width() / 2,
                (760 - map_status_text.get_height() / 2),
            ),
        )

        if menu_button.draw(display1):
            game_status = "menu"
        if exit_button.draw(display1):
            pygame.quit()
            sys.exit()
    if game_status == "keyboard":
        display1.blit(keyboard_img, (0, 0))

    if game_status == "end_screen":
        pygame.mixer.pause()
        sorted_score = []
        for all in all_players_list:
            sorted_score.append([all.score, all.player_name])

        sort_final = sorted(sorted_score, key=lambda x: (x[0]))
        score_text = game_font.render(f"{sort_final[-1][1]}", True, (0, 0, 0))
        display1.blit(endimage, (0, 0))

        display1.blit(score_text, (50, 100))
        end_text = game_font.render(f"{sort_final[-1][0]} points", True, (0, 0, 0))

        display1.blit(end_text, (50, 200))
        if exit_button.draw(display1):
            pygame.quit()
            sys.exit()

        if menu_button.draw(display1):
            game_status = "menu"

        if restart_button.draw(display1):
            start_time = time.time()
            dead_players = 0
            dead_ai = 0
            jump_time = 0
            for pl in PLAYER_LIST:
                pl.reset()
            for ai in AIs:
                ai.reset()
            game_status = "running"
    
    pygame.display.flip()

 #   pygame.display.update()  # updating the display
    clock.tick(config.GAME_FPS)

# TODO
# pri skoku zvacsit obrazok hlavy aby sa vytvoril akoze efekt skoku, hlava sa bude zvacsovat do stredu skoku a v druhej
# polovici sa bude znizovat do klasickej velkosti

# TODO pridat powerup dlhsi  skok ktory sa bude nacitvat pri skorebare pre kazdeho hraca
#  TODOpri nacitani zmenit farbu hlavy hada


# # TODO skusit namiesto float trail suradnic suradnice INT, mozno to usetri pamat alebo bude lepsie kreslit stvorceky
# specialne ked je rec o draw polygons
