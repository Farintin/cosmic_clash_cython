import pygame
import display



vw = display.view_width
vh = display.view_height


surf = pygame.Surface((vw, vh))
surf = surf.convert_alpha()
surf.set_colorkey((0,0,0,0))
class Bullet():
    def __init__(self):
        self.mask = pygame.mask.from_surface(surf)

        self.outline = []
        for pt in self.mask.outline():
            self.outline.append([pt[0], pt[1]])
        self.outline_pos = []
        
        self.exist = True

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]


class Craft1Bullet(Bullet):
    def __init__(self, pos):
        self.strength = 1
        self.pos = pos
        self.vel = (0,-5)
        self.color = (255, 205, 55, 255)
        self.rad = 2
        
        surf.fill((0,0,0,0))
        pygame.draw.circle(surf, (255,255,255,255), (self.rad, self.rad), self.rad)
        super().__init__()

    def draw(self, bg_obj):
        pygame.draw.circle(bg_obj, self.color, self.pos, self.rad)

    def draw_outline(self, bg_obj):
        if self.outline_pos:
            pygame.draw.lines(bg_obj, (255,255,255), True, self.outline_pos)
    
    def update_outline(self):
        self.outline_pos = []
        for pt in self.outline:
            self.outline_pos.append( [self.pos[0] + pt[0] - self.rad, self.pos[1] + pt[1] -self.rad] )