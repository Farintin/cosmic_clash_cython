import pygame
import display



cdef int vw = display.view_width
cdef int vh = display.view_height

cdef tuple pt
cdef int rect_w


cdef object surf = pygame.Surface((vw, vh))
surf = surf.convert_alpha()
surf.set_colorkey((0,0,0,0))
class Bullet:
    def __init__(self):
        cdef object mask
        cdef list outline, outline_pos
        cdef bint exist

        self.mask = pygame.mask.from_surface(surf)

        self.outline = []
        for pt in self.mask.outline():
            self.outline.append((pt[0], pt[1]))
        self.outline_pos = []
        
        self.exist = True


cdef class Craft1Bullet:
    cdef public int power, rad, rad_init
    cdef public tuple vel, color
    cdef public object mask, rect
    cdef public list pos, pos_init, outline, outline_pos
    cdef public bint exist, puffed

    def __init__(self, list pos, int rad, int power, surf = surf):
        self.exist = True
        self.power = power
        self.pos_init = pos
        self.pos = pos*1
        self.vel = (0,-5)
        self.color = (255, 205, 55, 255)
        self.rad = rad
        self.rad_init = 2
        self.puffed = False
        
        surf.fill((0,0,0,0))
        #pygame.draw.circle(surf, (255,255,255,255), (self.rad, self.rad), self.rad)
        if self.rad > self.rad_init:
            pygame.draw.circle(surf, (255,255,255,255), (self.rad, self.rad), self.rad)
        else:
            pygame.draw.circle(surf, (255,255,255,255), (self.rad_init, self.rad_init), self.rad_init)
        '''if self.rad > 2:
            rect_w = round(self.rad / 2)
        else:
            rect_w = 1
        self.rect = pygame.Rect(0,0, rect_w, self.rad * 8)'''
        self.rect = pygame.Rect(0,0, 1, self.rad_init * 8)

        self.mask = pygame.mask.from_surface(surf)
        self.outline = []
        for pt in self.mask.outline():
            self.outline.append((pt[0], pt[1]))
        self.update_outline()
        
    cpdef void draw(self, object bg_obj):
        if self.puffed:
            pygame.draw.circle(bg_obj, self.color, self.pos, self.rad)
        else:
            pygame.draw.circle(bg_obj, self.color, self.pos, self.rad_init)

    cpdef void draw_outline(self, object bg_obj):
        pygame.draw.lines(bg_obj, (255,255,255), True, self.outline_pos)
        pygame.draw.rect(bg_obj, (255,0,0), self.rect, 1)
    
    cpdef void move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if not self.puffed and (self.rad > self.rad_init) and (self.pos[1] + self.rad < self.pos_init[1] - 40):
            self.rect = pygame.Rect(0,0, round(self.rad / 2), self.rad * 8)
            self.puffed = True
        self.rect.midtop = self.pos

    cpdef void update_outline(self):
        self.outline_pos = []
        for pt in self.outline:
            self.outline_pos.append( [self.pos[0] + pt[0] - self.rad, self.pos[1] + pt[1] -self.rad] )