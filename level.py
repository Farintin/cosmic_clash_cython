import pygame
import pygame.gfxdraw
import display
from dom import *
from math import *
import db


vw = display.view_width
vh = display.view_height



surf = pygame.Surface((vw, vh))
surf = surf.convert_alpha()
surf.set_colorkey((0,0,0,0))
class Level:
    def __init__(self, n, x, y, attacks = 0):
        self.n = n
        self.dom_obj = Circle((255,255,255), 25, (x, y))
        children = (Circle((255,255,255,155), 15, (x, y)), Text(str(self.n), color = (155,155,155), font_size = 14))
        for child in children:
            child.id = 'sub_icon'
        self.dom_obj.addChildren( children )

        self.attacks = attacks

        self.bodys_prob = db.document['levels']['body_prob'][str(n)]

    def draw(self, bg_alpha):
        self.dom_obj.show(bg_alpha)

    def update(self):
        current = db.document['levels']['current']
        if self.n <= current:
            self.unlocked = True
        else:
            self.unlocked = False

        if self.n == current:
            self.current = True
        else:
            self.current = False





def set_grids(n_levels = 100):
    levels = []

    w_vec = -1
    w = round(vw * 0.5)
    h = round(vh * 0.15)

    grid_h = h * (n_levels + 2)
    
    gridFrame = Rect((0, 0, vw, grid_h), bgColor = (0,0,0,155))
    x = round(vw * 0.25)
    #y = round(vh * 0.85)
    y = grid_h - h

    ### Attacks preparation
    
    attacks = [5,10,15]
    for n in range(1, n_levels + 1):
        if len(attacks) < n_levels:
            if n > 3 and n <= 50:
                attacks += [n * 5] * 5
            elif n > 50:
                attacks += [n * 5] * 6
        else:
            break

    for n in range(1, n_levels + 1):
        attack = attacks[n - 1]
        lvl = Level(n, x, y, attacks = attack)
        lvl.dom_obj.offSet = (x, y)
        #lvl.dom_obj.state['bg'] = False
        #lvl.dom_obj.hovering['bg'] = True
        levels.append(lvl)
        gridFrame.addChild(lvl.dom_obj)

        x += w * (w_vec ** (n + 1))
        y -= h
    
    return levels, gridFrame, grid_h


def show_grids(bg_alpha, gridFrame):
    w = round(vw * 0.5)
    h = round(vh * 0.15)
    diag = sqrt(w ** 2 + h ** 2)
    sin = h / diag
    cos = w / diag

    rad = gridFrame.children[0].getChildBy('name', 'circle').radius
    dx = cos * rad
    dy = sin * rad

    i = 0
    slope_vec = -1
    for lvl_icon in gridFrame.children:
        if i > 0:
            vec = slope_vec ** (i + 1)
            
            centerx1, centery1 = gridFrame.children[i - 1].rect.center
            centerx2, centery2 = lvl_icon.rect.center
            if vec == 1:
                pt1 = (centerx1 + dx, centery1 - dy)
                pt2 = (centerx2 - dx, centery2 + dy)
            elif vec == -1:
                pt1 = (centerx1 - dx, centery1 - dy)
                pt2 = (centerx2 + dx, centery2 + dy)

            pygame.draw.aaline(bg_alpha, (255,255,255), pt1, pt2)
            
        i += 1

selected = None