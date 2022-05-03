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

#active players number
active_players = 4

#number of dead_players
player1_dead=False
player2_dead=False
player3_dead=False
player4_dead=False
dead_players = 0

#AI players number
ai_players = 8

#game over text
game_font = pygame.font.SysFont("comicsans", 60)

# create playable players
if active_players>=1:
    player1 = Player(config.PLAYER_COLOR, config.PLAYER_POSITIONS["p1"], config.MOVE_PER_SECOND, config.PLAYER_HEAD_IMG,
                     config.WORM_SIZE, config.GAME_RES, 0, "p1")
    if active_players >= 2:
        player2 = Player(config.PLAYER_COLOR2, config.PLAYER_POSITIONS["p2"], config.MOVE_PER_SECOND, config.PLAYER_HEAD_IMG,
                 config.WORM_SIZE, config.GAME_RES, 0, "p2")
        if active_players >= 3:
            player3 = Player(config.PLAYER_COLOR3, config.PLAYER_POSITIONS["p3"], config.MOVE_PER_SECOND, config.PLAYER_HEAD_IMG,
                 config.WORM_SIZE, config.GAME_RES, 0 ,"p3")
            if active_players >= 4:
                player4 = Player(config.PLAYER_COLOR4, config.PLAYER_POSITIONS["p4"], config.MOVE_PER_SECOND, config.PLAYER_HEAD_IMG,
                 config.WORM_SIZE, config.GAME_RES, 0 ,"p4")

PLAYER_LIST = [player1,player2,player3,player4]

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

    # clear display with fresh background
    background.draw(display1)
    # movement of players
    keys = pygame.key.get_pressed()
    # draw player
    player1.draw_player(display1)
    player2.draw_player(display1)
    player3.draw_player(display1)
    player4.draw_player(display1)

    #players collisions

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

    #check collisions
    def check_collision():
        for pl in PLAYER_LIST:
            #TODO it is checking only when image head is rotated
            if pl.head_image_copy:
                pl.mask1 = pygame.mask.from_surface(pl.head_image_copy)
                # it is checking all players including itself
                for others in PLAYER_LIST:
                    print(pl.head_image_position)
                    for trail_step in others.trail[:-20]:
                        x_off = trail_step[0] - pl.head_image_position[0][0]
                        y_off = trail_step[1] - pl.head_image_position[0][1]
                        if pl.mask1.overlap(others.masktrail, (x_off, y_off)):
                            pl.player_collided = True

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
        player1_dead=True
    if player2.player_collided and not player2_dead:
        dead_players += 1
        player2_dead = True
    if player3.player_collided and not player3_dead:
        dead_players += 1
        player3_dead = True
    if player4.player_collided and not player4_dead:
        dead_players += 1
        player4_dead = True





    print("dead",dead_players)

    #draw trails
    player1.draw_trail(player1.trail)
    player2.draw_trail(player2.trail)
    player3.draw_trail(player3.trail)
    player4.draw_trail(player4.trail)





    #scoretable
    display1.blit(config.SCORE_IMG, (0,
                                    0))
    if dead_players == active_players:
        print("koniec")
        end_text = game_font.render(f"Game over", True, (255, 255, 255))
        display1.blit(end_text, (config.GAME_RES[0]//2- end_text.get_width()  , config.GAME_RES[1]//2 - end_text.get_height()/2 ))
    # updating the display
    pygame.display.update()
    clock.tick(config.GAME_FPS)
#  pygame.display.flip()
