import pygame
import random
import sys

from resources.basic_handler import Basic
from resources.button import Button
from resources.player import Player
from config import config
from pygame import mixer

# sounds
crash_sound = ""
# initialize sound mixer

# initialize pygame

pygame.init()
clock = pygame.time.Clock()

soundObj = pygame.mixer.music.load('resources/kim-lightyear-legends-109307.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
jump_sound = pygame.mixer.Sound('resources/mixkit-player-jumping-in-a-video-game-2043.wav')
jump_sound.set_volume(0.1)
# window create
display1 = pygame.display.set_mode(config.GAME_RES)
pygame.display.set_caption('Cerviky')
Icon = pygame.image.load('resources/pythonik2.jpg').convert_alpha()
menu_image = pygame.image.load('resources/intro/0400.jpg').convert()
menu_image = pygame.transform.scale(menu_image, (config.GAME_RES[0], config.GAME_RES[1]))
pygame.display.set_icon(Icon)

# images loading
# background image
BACKGROUND_IMG_PATH = "resources/background.jpg"
PLAYER_HEAD_IMG = pygame.image.load("resources/SnakeHead(1).png").convert_alpha()
PLAYER_HEAD_IMG = pygame.transform.rotate(PLAYER_HEAD_IMG, 180)
PLAYER_HEAD_IMG2 = pygame.image.load("resources/SnakeHead(1).png").convert_alpha()
PLAYER_HEAD_IMG2 = pygame.transform.rotate(PLAYER_HEAD_IMG2, 180)
PLAYER_HEAD_IMG3 = pygame.image.load("resources/SnakeHead(1).png").convert_alpha()
PLAYER_HEAD_IMG3 = pygame.transform.rotate(PLAYER_HEAD_IMG3, 180)
PLAYER_HEAD_IMG4 = pygame.image.load("resources/SnakeHead(1).png").convert_alpha()
PLAYER_HEAD_IMG4 = pygame.transform.rotate(PLAYER_HEAD_IMG4, 180)
SCORE_IMG = pygame.image.load("resources/untitled.png").convert_alpha()
SCORE_IMG = pygame.transform.scale(SCORE_IMG, config.GAME_RES)

# create background
background = Basic(config.ZERO_POS, BACKGROUND_IMG_PATH, False)
background.draw(display1)

# active players number
active_players = 4

# number of dead_players
player1_dead = False
player2_dead = False
player3_dead = False
player4_dead = False
dead_players = 0

# AI players number
ai_players = 8

# game over text
game_font = pygame.font.SysFont("comicsans", 90, True, True)

# dt = The clock.tick returns the time since the last call to clock.tick.
# Use that value and multiply all your speeds with it when you move
# dt = clock.tick(60)

# main
# if __name__ == "__main__":


# create playable players
if active_players >= 1:
    player1 = Player(config.PLAYER_COLOR, config.PLAYER_POSITIONS["p1"], config.MOVE_PER_SECOND, PLAYER_HEAD_IMG,
                     config.WORM_SIZE, config.GAME_RES, 0, "p1")
    if active_players >= 2:
        player2 = Player(config.PLAYER_COLOR2, config.PLAYER_POSITIONS["p2"], config.MOVE_PER_SECOND,
                         PLAYER_HEAD_IMG2.convert_alpha(),
                         config.WORM_SIZE, config.GAME_RES, 0, "p2")
        if active_players >= 3:
            player3 = Player(config.PLAYER_COLOR3, config.PLAYER_POSITIONS["p3"], config.MOVE_PER_SECOND,
                             PLAYER_HEAD_IMG3.convert_alpha(),
                             config.WORM_SIZE, config.GAME_RES, 0, "p3")
            if active_players >= 4:
                player4 = Player(config.PLAYER_COLOR4, config.PLAYER_POSITIONS["p4"], config.MOVE_PER_SECOND,
                                 PLAYER_HEAD_IMG4.convert_alpha(),
                                 config.WORM_SIZE, config.GAME_RES, 0, "p4")

PLAYER_LIST = [player1, player2, player3, player4]
# PLAYER_LIST = [player1]

player1.draw_player(display1)

# starting direction for move velocity
direction = 0
angle = 0

# music and sound
played_jump_sound = False
paused_music = False
paused_sounds = False

# counter for drawing trail every second not every frame
time_delay = 1000
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, time_delay)
jump_time = 0
jumped_already = False
start_ticks = pygame.time.get_ticks()
seconds = 0
trail_allow = True

# menu,start,restart
global game_status
game_status = "welcome"

game_state = ["welcome", "running", "menu", "end_screen"]
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
        self.game_st = "welcome"

    def udpate_anim(self):

        # define animation cooldown
        ANIMATION_COOLDOWN = 1
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


# check collisions
def check_collision():
    for pl in PLAYER_LIST:
        # TODO it is checking only when image head is rotated
        if pl.head_image_copy:
            pl.mask1 = pygame.mask.from_surface(pl.head_image_copy)
            # it is checking all players including itself
            for others in PLAYER_LIST:
                for trail_step in others.trail[:-20]:
                    x_off = trail_step[0] - pl.head_image_position[0][0]
                    y_off = trail_step[1] - pl.head_image_position[0][1]
                    if pl.mask1.overlap(others.masktrail, (x_off, y_off)) and not pl.jump:
                        pl.player_collided = True
                    if pl.mask1.overlap(others.masktrail, (x_off, y_off)) and pl.jump:
                        pl.player_collided = False


# create buttons
start_button_img = pygame.image.load("resources/startbutton.png").convert()
exit_button_img = pygame.image.load("resources/exitbutton.png").convert()
restart_button_img = pygame.image.load("resources/restartbutton.png").convert()
start_button = Button(config.GAME_RES[0] * 0.8, config.GAME_RES[1] * 0.35, start_button_img, 1)
exit_button = Button(config.GAME_RES[0] * 0.8, config.GAME_RES[1] * 0.55, exit_button_img, 1)
restart_button = Button(config.GAME_RES[0] // 2 - restart_button_img.get_size()[1] - 100,
                        config.GAME_RES[1] // 2 + 100, restart_button_img, 1)

# creating a running loop
while True:
    print(game_status)
    # print(player1.jump)
    # creating a loop to check events that are occurring
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
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
                if active_players >= 1:
                    player1 = Player(config.PLAYER_COLOR, config.PLAYER_POSITIONS["p1"], config.MOVE_PER_SECOND,
                                     PLAYER_HEAD_IMG,
                                     config.WORM_SIZE, config.GAME_RES, 0, "p1")
                    if active_players >= 2:
                        player2 = Player(config.PLAYER_COLOR2, config.PLAYER_POSITIONS["p2"], config.MOVE_PER_SECOND,
                                         PLAYER_HEAD_IMG2.convert_alpha(),
                                         config.WORM_SIZE, config.GAME_RES, 0, "p2")
                        if active_players >= 3:
                            player3 = Player(config.PLAYER_COLOR3, config.PLAYER_POSITIONS["p3"], config.MOVE_PER_SECOND,
                                             PLAYER_HEAD_IMG3.convert_alpha(),
                                             config.WORM_SIZE, config.GAME_RES, 0, "p3")
                            if active_players >= 4:
                                player4 = Player(config.PLAYER_COLOR4, config.PLAYER_POSITIONS["p4"],
                                                 config.MOVE_PER_SECOND,
                                                 PLAYER_HEAD_IMG4.convert_alpha(),
                                                 config.WORM_SIZE, config.GAME_RES, 0, "p4")
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
                pygame.quit()
                sys.exit()

        # check position out of map
        # for pl in PLAYER_LIST:
        #     if pl.head_image_position[0] <=

    # launched game
    if game_status == "running":

        # jumping_handler
        if player1.jump and (jumped_already == False):
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds
            if jump_time == 0:
                jump_time = seconds
            print(seconds)
            trail_allow = False

        if seconds - jump_time >= 0.5 and player1.jump:
            print("jump finish")
            trail_allow = True
            jump_time = 0
            jumped_already = False
            player1.jump = False

        # clear display with fresh background
        background.draw(display1)
        # movement of players
        keys = pygame.key.get_pressed()
        # draw player
        player1.draw_player(display1)
        player2.draw_player(display1)
        player3.draw_player(display1)
        player4.draw_player(display1)

        # players collisions

        if not player1.player_collided:
            player1.handle_keys(keys)
            player1.move(player1.velocity[0], player1.velocity[1])

        if not player2.player_collided:
            player2.handle_keys(keys)
            player2.move(player2.velocity[0], player2.velocity[1])

        if not player3.player_collided:
            player3.handle_keys(keys)
            player3.move(player3.velocity[0], player3.velocity[1])

        if not player4.player_collided:
            player4.handle_keys(keys)
            player4.move(player4.velocity[0], player4.velocity[1])

        # sound
        if player1.jump_effect_launch and not played_jump_sound:
            jump_sound.play()
            played_jump_sound = True

        if not player1.jump_effect_launch:
            played_jump_sound = False

        # trail create
        if trail_allow and not player1.player_collided:
            player1.create_trail()
        if trail_allow and not player2.player_collided:
            player2.create_trail()
        if trail_allow and not player3.player_collided:
            player3.create_trail()
        if trail_allow and not player4.player_collided:
            player4.create_trail()

        check_collision()
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

        #  print("dead", dead_players)

        # draw trails
        player1.draw_trail(player1.trail)
        player2.draw_trail(player2.trail)
        player3.draw_trail(player3.trail)
        player4.draw_trail(player4.trail)
        # TODO namiesto rect draw polygon pre usporenie pamate a viac fps
        # TODO pripadne spravit namiesto rect iba obrazky ktore sa budu pridavat
        # TODO bug pri preskakovani hned za hlavou protivnika..neni kolizia
        # POKLES FPS - poskles fps vyrieseny convert() prikazom pri loadovani suboru
        # again draw player head becouse of trail visibility
        player1.draw_player(display1)
        player2.draw_player(display1)
        player3.draw_player(display1)
        player4.draw_player(display1)

        # scoretable
        display1.blit(SCORE_IMG, (0, 0))

        # fps show
        display1.blit(update_fps(), (10, 0))

        if dead_players == active_players:
            print("koniec")
            end_text = game_font.render(f"Game over", True, (255, 255, 255))
            display1.blit(end_text,
                          (config.GAME_RES[0] // 2 - end_text.get_width(),
                           config.GAME_RES[1] // 2 - end_text.get_height() / 2))

    if game_status == "welcome":
        intro.udpate_anim()
        DrawBar(barPos, barSize, borderColor, barColor, intro.frame_index / max_a)
        game_status = intro.game_st

    if game_status == "menu":
        # menu
        display1.blit(menu_image, (0, 0))
        if start_button.draw(display1):
            game_status = "running"
        if exit_button.draw(display1):
            pygame.quit()
            sys.exit()
        startuptext = game_font.render(f"Hoppy Worms ", True, (0, 0, 0))
        display1.blit(startuptext, ((config.GAME_RES[0] * 0.8 - int(startuptext.get_width() / 2)),
                                    (config.GAME_RES[1] / 5 - int(startuptext.get_size()[1] / 2) - 150)))

    if game_status == "end_screen":
        pass

    # updating the display
    pygame.display.update()
    clock.tick(config.GAME_FPS)
#  pygame.display.flip()


# TODO
# pri skoku zvacsit obrazok hlavy aby sa vytvoril akoze efekt skoku, hlava sa bude zvacsovat do stredu skoku a v druhej
# polovici sa bude znizovat do klasickej velkosti

#TODO ak je hrac mrtvy necheckovat koliziu ani nepridavat novy tail len opakovane zobrazit
# pridat powerup dlhsi  skok ktory sa bude nacitvat pri skorebare pre kazdeho hraca
# pri nacitani zmenit farbu hlavy hada