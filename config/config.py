import pygame

ZERO_POS = (0, 0)
GAME_RES = (1920, 1080)
RESOLUTIONS_LIST = ((1280, 720), (1920, 1080), (3840, 2160))
GAME_FPS = 60
MOVE_PER_SECOND = 2

COLOR_PICKER = {"red": (157, 0, 9),
                "orange red": (255, 69, 0),
                "gold": (255, 215, 0),
                "lawn green": (124, 252, 0),
                "aqua": (0, 255, 255),
                "dark blue": (0, 0, 139),
                "blue violet": (138, 43, 226),
                "deep pink": (255, 20, 147),
                "light yellow": (255, 255, 224),
                "gray": (128, 128, 128),
                "olive": (128, 128, 0),
                "black": (0, 0, 0)
                }

PLAYER_COLOR = pygame.Color(COLOR_PICKER["red"])
PLAYER_COLOR2 = pygame.Color(COLOR_PICKER["orange red"])
PLAYER_COLOR3 = pygame.Color(COLOR_PICKER["gold"])
PLAYER_COLOR4 = pygame.Color(COLOR_PICKER["lawn green"])
PLAYER_COLOR5 = pygame.Color(COLOR_PICKER["aqua"])
PLAYER_POSITIONS = {
    "p1": [GAME_RES[0] - (GAME_RES[0]) + 100, 0 + 50],
    "p2": (GAME_RES[0] - (GAME_RES[0]) + 300, 0 + 50),
    "p3": (GAME_RES[0] - (GAME_RES[0]) + 500, 0 + 50),
    "p4": (GAME_RES[0] - (GAME_RES[0]) + 700, 0 + 50),
    "p5": (GAME_RES[0] - (GAME_RES[0]) + 800, 0 + 50),
    "p6": (GAME_RES[0] - (GAME_RES[0]) + 1200, 0 + 50),
    "p7": (GAME_RES[0], GAME_RES[1] - round(GAME_RES[1] * 0.7)),
    "p8": (GAME_RES[0], GAME_RES[1] - round(GAME_RES[1] * 0.4)),
    "p9": (0, GAME_RES[1]),
    "p10": (GAME_RES[0] - round(GAME_RES[0] * 0.7), GAME_RES[1]),
    "p11": (GAME_RES[0] - round(GAME_RES[0] * 0.4), GAME_RES[1]),
    "p12": (GAME_RES[0], GAME_RES[1]),
}

PLAYER_ROTATIONS = {
    "p1": 180,
    "p2": 270,
    "p3": 0,
    "p4": 90,
    "p5": 180,
    "p6": 270,
    "p7": 0,
    "p8": 90,
    "p9": 180,
    "p10": 270,
    "p11": 0,
    "p12": 90,
}
WORM_SIZE = 50
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
# pridat skore tabulku
# skore ratat podla poctu prvkov v liste suradnic
# nechat ten bunnyhopping ako featuru ktoru budu moct pouzivat aj AI
# vypisovat na tabulke skore aj aktualny uplynuty cas v sekundach
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
