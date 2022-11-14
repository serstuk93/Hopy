import pygame

ZERO_POS = (0, 0)
GAME_RES = (1920, 1080)
RESOLUTIONS_LIST = ((1280, 720), (1920, 1080), (3840, 2160))
GAME_FPS = 60
MOVE_PER_FRAME = 2

COLOR_PICKER = {"red": (157, 0, 9),
                "orange red": (255, 69, 0),
                "gold": (255, 215, 0),
                "lawn green": (124, 252, 0),
                "aqua": (0, 255, 255),
                "dark blue": (0, 87, 255),
                "blue violet": (138, 43, 226),
                "deep pink": (255, 20, 147),
                "light yellow": (255, 255, 224),
                "gray": (128, 128, 128),
                "olive": (128, 128, 0),
                "white": (255, 255, 255)
                }
PLAYER_COLOR = []
for p_color, p_value in COLOR_PICKER.items():
    x = pygame.Color(p_value)
    PLAYER_COLOR.append(x)


PLAYER_POSITIONS = {
    "p1": (GAME_RES[0] / 2 - 75, 0 + 60),
    "p2": (GAME_RES[0] - 400, (GAME_RES[1] / 2)),
    "p3": (GAME_RES[0] / 2 - 75, GAME_RES[1] - 60),
    "p4": (0 + 60, (GAME_RES[1] / 2)),
    "p5": (GAME_RES[0] / 2 - 200 - 75, 0 + 60),
    "p6": (GAME_RES[0] - 400, (GAME_RES[1] / 2 - 200)),
    "p7": (GAME_RES[0] / 2 - 200, GAME_RES[1] - 60),
    "p8": (0 + 60, (GAME_RES[1] / 2 - 200)),
    "p9": (GAME_RES[0] / 2 + 200, 0 + 60),
    "p10": (GAME_RES[0] - 400, (GAME_RES[1] / 2 + 200)),
    "p11": (GAME_RES[0] / 2 + 200, GAME_RES[1] - 60),
    "p12": (0 + 60, (GAME_RES[1] / 2 + 200)),
}

PLAYER_ROTATIONS = {
    "p1": 180,
    "p2": 90,
    "p3": 0,
    "p4": 270,
    "p5": 180,
    "p6": 90,
    "p7": 0,
    "p8": 270,
    "p9": 180,
    "p10": 90,
    "p11": 0,
    "p12": 270,
}
WORM_SIZE = 32
START_GAME = False
START_ORIENTATION = ["UP", "DOWN", "LEFT", "RIGHT"]

KEYBOARD_CONTROLS = {"p1": [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP],
                     "p2": [pygame.K_a, pygame.K_d, pygame.K_w],
                     "p3": [pygame.K_j, pygame.K_l, pygame.K_i],
                     "p4": [pygame.K_KP4, pygame.K_KP6, pygame.K_KP8]
                     }

P1_CONTROL = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP]
P2_CONTROL = [pygame.K_a, pygame.K_d, pygame.K_w]
P3_CONTROL = [pygame.K_j, pygame.K_l, pygame.K_i]
P4_CONTROL = [pygame.K_KP4, pygame.K_KP6, pygame.K_KP8]

# TODO
# zvysovat rychlost po case
# nechat ten bunnyhopping ako featuru ktoru budu moct pouzivat aj AI
# moznost zapauzovat hru

# na konci ked bude skoro hotove vymenit vykreslovanie clankov rect za vykreslovanie obrazkov
# aby neboli zubky


# INFO CLICKER IMG POSITIONS FHD

# ZVUK
# 1620,20
# 1690,75

# MUSIC
# 1700,15
# 1750,75
#
# Restart
# 1775,15
# 1850,75
#
# QUIT
# 1855,15
# 1910, 75

# MENU
# 1620,90
# 1690,160


# SCORETABLE
#
# 1600, 0
# 1920,1080


# OPTIONS MENU
#x0=735 x1 = 850
#item  height = 120

# X = 735
# Y1 = 70
# Y2 = 230
# Y3 = 390
# Y4 = 552
# Y5 = 705
# Y6 = 865

SCORE_POSITIONS = {
    "1": (1715,265-30),
    "2": (1680, 315-30),
    "3": (1680, 365-30),
    "4": (1680, 415-30),
    "5": (1680, 470-30),
    "6": (1680, 520-30),
    "7": (1680,  575-30),
    "8": (1680, 625-30),
    "9": (1680,675-30),
    "10": (1680,725-30),
    "11": (1680, 785-30),
    "12": (1680,835-30),
}