
class dbg:
    def __init__(self, screen, item):
        self.screen = screen
        self.item = item 
    def debug_borders(self):
        self.screen.blit(self.item, (50,50))
        self.screen.blit(self.item, (1550,50))
        self.screen.blit(self.item, (50,900))
        self.screen.blit(self.item, (1550,1030))

    def get_pixel_color(self):
        self.pixel_color = self.screen.get_at((52,52)) 
        print(self.pixel_color)
        return self.pixel_color