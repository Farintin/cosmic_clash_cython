import pygame
import display



cdef int vw = display.view_width
cdef int vh = display.view_height

cdef tuple pt


cdef object surf = pygame.Surface((vw, vh))
surf = surf.convert_alpha()
surf.set_colorkey((0,0,0,0))
class Bullet():
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
    cdef public int power, rad
    cdef public tuple vel, color
    cdef public object mask
    cdef public list pos, outline, outline_pos
    cdef public bint exist

    def __init__(self, list pos, int rad, int power, surf = surf):
        self.power = power
        self.pos = pos
        self.vel = (0,-5)
        self.color = (255, 205, 55, 255)
        self.rad = rad
        
        surf.fill((0,0,0,0))
        pygame.draw.circle(surf, (255,255,255,255), (self.rad, self.rad), self.rad)

        self.mask = pygame.mask.from_surface(surf)

        self.outline = []
        for pt in self.mask.outline():
            self.outline.append((pt[0], pt[1]))
        self.outline_pos = []
        
        self.exist = True

    cpdef void draw(self, object bg_obj):
        pygame.draw.circle(bg_obj, self.color, self.pos, self.rad)

    cpdef void draw_outline(self, object bg_obj):
        if self.outline_pos:
            pygame.draw.lines(bg_obj, (255,255,255), True, self.outline_pos)
    
    cpdef void move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
    
    cpdef void update_outline(self):
        self.outline_pos = []
        for pt in self.outline:
            self.outline_pos.append( [self.pos[0] + pt[0] - self.rad, self.pos[1] + pt[1] -self.rad] )