import pygame

ZERO_POS = (0, 0)
GAME_RES = (1280, 720)
RESOLUTIONS_LIST = ((1280, 720), (1920, 1080), (3840, 2160))
GAME_FPS = 60
MOVE_PER_SECOND = 1

COLOR_PICKER = {"red": (255, 0, 0),
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
PLAYER_POSITIONS = {
    "p1": [GAME_RES[0]- (GAME_RES[0])+400, 0+400],
    "p2": (GAME_RES[0] - round(GAME_RES[0] * 0.7 +50), 0),
    "p3": (GAME_RES[0] - round(GAME_RES[0] * 0.4+50 ), 0),
    "p4": (GAME_RES[0], 0),
    "p5": (0, GAME_RES[1] - round(GAME_RES[1] * 0.7)),
    "p6": (0, GAME_RES[1] - round(GAME_RES[1] * 0.4)),
    "p7": (GAME_RES[0], GAME_RES[1] - round(GAME_RES[1] * 0.7)),
    "p8": (GAME_RES[0], GAME_RES[1] - round(GAME_RES[1] * 0.4)),
    "p9": (0, GAME_RES[1]),
    "p10": (GAME_RES[0] - round(GAME_RES[0] * 0.7), GAME_RES[1]),
    "p11": (GAME_RES[0] - round(GAME_RES[0] * 0.4), GAME_RES[1]),
    "p12": (GAME_RES[0], GAME_RES[1]),
}
WORM_SIZE = 50
START_GAME = False
START_ORIENTATION = ["UP", "DOWN", "LEFT", "RIGHT"]

# background image
BACKGROUND_IMG_PATH = "resources/background.jpg"
PLAYER_HEAD_IMG = pygame.image.load("resources/headred.png")

#TODO
#zvysovat rychlost po case
#pridat skore tabulku
#skore ratat podla poctu prvkov v liste suradnic
#nechat ten bunnyhopping ako featuru ktoru budu moct pouzivat aj AI
#vypisovat na tabulke skore aj aktualny uplynuty cas v sekundach
#moznost zapauzovat hru

# na konci ked bude skoro hotove vymenit vykreslovanie clankov rect za vykreslovanie obrazkov
#aby neboli zubky

