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

soundObj = pygame.mixer.Sound('resources/kim-lightyear-legends-109307.mp3')
soundObj.set_volume(0.1)
soundObj.play(loops=-1)
jump_sound = pygame.mixer.Sound('resources/mixkit-player-jumping-in-a-video-game-2043.wav')
jump_sound.set_volume(0.1)
# window create
display1 = pygame.display.set_mode(config.GAME_RES)
pygame.display.set_caption('Cerviky')
Icon = pygame.image.load('resources/pythonik2.jpg')
pygame.display.set_icon(Icon)

# create background
background = Basic(config.ZERO_POS, config.BACKGROUND_IMG_PATH, False)
background.draw(display1)

# create player
player1 = Player(config.PLAYER_COLOR, config.PLAYER_POSITIONS["p1"], config.MOVE_PER_SECOND, config.PLAYER_HEAD_IMG,
                 config.WORM_SIZE, config.GAME_RES, 0)
player1.draw_player(display1)
# starting direction for move velocity
direction = 0
angle = 0

# music and sound
played_jump_sound = False

# counter for drawing trail every second not every frame
time_delay = 1000
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, time_delay)
jump_time = 0
jumped_already = False
start_ticks = pygame.time.get_ticks()
seconds = 0
trail_allow = True
# creating a running loop
while True:



    # print(player1.jump)
    # creating a loop to check events that are occurring
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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

        #      player1.jump=False

        # if jump_time <= 1 and event.type == timer_event and player1.jump:
        #     jump_time += 1
        #     #     print(counter)
        #     trail_allow = False
        #     counter = 0

    # clear display with fresh background
    background.draw(display1)
    # movement of player 1
    keys = pygame.key.get_pressed()
    player1.handle_keys(keys)
    # draw player
    player1.draw_player(display1)
    player1.move(player1.velocity[0], player1.velocity[1])

    # sound
    if player1.jump_effect_launch and not played_jump_sound:
        jump_sound.play()
        played_jump_sound = True

    if not player1.jump_effect_launch:
        played_jump_sound = False

    # trail draw
    if trail_allow:
        player1.create_trail()

    player1.draw_trail(player1.trail)
    player1.check_collision()

    for trail_step in player1.trail:
        if player1.head_image_position in trail_step:
            print("Collision")
            break
        # if check_colision(ship_mask, meteor["mask"], (ship_coordsx, ship_coordsy), (meteor["x"], meteor["y"])):
        #     end = True

    # updating the display
    pygame.display.update()
    clock.tick(config.GAME_FPS)
#  pygame.display.flip()
