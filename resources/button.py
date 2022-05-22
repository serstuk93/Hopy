import pygame
from Hopy.config import config


# button
class Button:
    def __init__(self, image, image_selected):
        # self.image = pygame.transform.scale(image, (config.GAME_RES[0], config.GAME_RES[1]))
        self.image = image

        self.image_temp = image
        self.selected_image = image_selected
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image_temp.get_rect(center=(config.GAME_RES[0] / 2, config.GAME_RES[1] / 2))
        self.clicked = False
        self.bwidth = image.get_width()
        self.bheight = image.get_height()

    def draw(self, surface):
        action = False
        self.image = self.image_temp

        # return to basic scale
        #  scale=1
        # self.image = pygame.transform.scale(self.image, (int(self.bwidth * scale), (int(self.bheight * scale))))

        # get mouse position
        position_mouse = pygame.mouse.get_pos()
        # position in mask
        pos_in_mask = position_mouse[0] - self.rect.x, position_mouse[1] - self.rect.y

        # check mouseover and clicked conditions

        if self.rect.collidepoint(position_mouse) and self.mask.get_at(pos_in_mask):
            self.image = self.selected_image

            # zmeni farbu a zvacsi tlacidlo
            # scale = 1.1
            # self.image = pygame.image.load("crosshairActive.png").convert_alpha()
            # self.image = pygame.transform.scale(self.image, (int(self.bwidth * scale), (int(self.bheight * scale))))

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        surface.blit(self.image, (0, 0))

        return action
