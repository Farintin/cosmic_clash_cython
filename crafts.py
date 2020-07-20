import pygame
import display, colors, controls
from bullets import *
from explode import *



vw = display.view_width
vh = display.view_height
FPS = display.FPS

lifeGem = pygame.image.load('img/item/gem.png').convert_alpha()
lifeGem = pygame.transform.scale(lifeGem, (25,25)).convert_alpha()


class Craft:
    life_bar_w = 6
    life_bar_g = 5
    life_bar_h = 15

    def __init__(self):
        self.DIM = (self.image.get_width(), self.image.get_height())
        self.center = (self.DIM[0] / 2, self.DIM[1] / 2)
        self.pos = [int(display.view_center[0] - self.center[0]), int(display.view_height - self.center[1] - 60)]

        self.shoots = []
        self.rapid_strike_timer = 0

        self.dx = 0

        self.mask = pygame.mask.from_surface(self.image)
        self.outline = []
        for pt in self.mask.outline():
            self.outline.append([pt[0], pt[1]])
        self.outline_pos = []
        self.outline_color = colors.RED

        self.collide = False
        self.collided = False

    def collision_actions(self, bg_obj):
        if self.collide:
            self.collided = True
            self.collide = False
            self.collided_blink_counter = 0
            self.blink_outline_timer = 0

        if self.collided:
            if self.blink_outline_timer <= 1/16:
                self.draw_outline(bg_obj)
            if self.blink_outline_timer >= 1/8:
                self.blink_outline_timer = 0
                self.collided_blink_counter += 1

            if self.collided_blink_counter >= 4:
                self.draw_outline(bg_obj)
                self.collided = False
                self.collided_blink_counter = 1
            else:
                self.blink_outline_timer += 1 / FPS

    def draw_outline(self, bg_obj):
        if self.outline_pos:
            pygame.draw.polygon(bg_obj, self.outline_color, self.outline_pos)

    def load_bullets(self):
        shoot = []
        for pt in self.mozzles:
            shoot.append( Craft1Bullet( [self.pos[0] + pt[0], self.pos[1] + pt[1]] ) )
        self.shoots.append(shoot)

    def nav(self):
        self.pos[0] += self.dx
        if self.pos[0] <= 0:
            self.pos[0] = 0
        elif self.pos[0] + self.DIM[0] >= display.view_width:
            self.pos[0] = display.view_width - self.DIM[0]
        self.rect.left = self.pos[0] + int(self.DIM[0] * 0.22)
    
    def rapid_strike(self, bg_obj):
        if self.rapid_strike_timer >= 0.1:
            self.load_bullets()
            self.rapid_strike_timer = 0

        if self.shoots:
            self.shoot(bg_obj)

        self.rapid_strike_timer += 1/display.FPS

    def shoot(self, bg_obj):
        for shoot in self.shoots:
            if shoot:
                for bullet in shoot:
                    if not bullet.exist:
                        shoot.remove(bullet)
            else:
                self.shoots.remove(shoot)
        for shoot in self.shoots:
            if shoot:
                for bullet in shoot:
                    bullet.update_outline()
                    bullet.draw(bg_obj)
                    #bullet.draw_outline(bg_obj)
                    bullet.move()

                    if bullet.pos[1] < -10: # Top display bound bullet termination 
                        bullet.exist = False
                
                for bullet in shoot:
                    if not bullet.exist:
                        shoot.remove(bullet)
            else:
                self.shoots.remove(shoot)

    def show_bounds(self, bg_obj):
        pygame.draw.rect(bg_obj, colors.RED, self.rect, 1)

        for pt in self.mozzles:
            mozzle_pos = (self.pos[0] + pt[0], self.pos[1] + pt[1])
            pygame.draw.circle(bg_obj, colors.RED, mozzle_pos, 2)
    
    def show_life(self, bg_obj):
        if self.life <= 1:
            self.life_color = colors.RED
        else:
            self.life_color = colors.WHITE
        for n in range(0, self.life):
            x = (Craft.life_bar_w * n + Craft.life_bar_g * (n + 1)) + (lifeGem.get_width() / 2) + 25
            y = 10
            w = Craft.life_bar_w
            h = Craft.life_bar_h
            pygame.draw.rect(bg_obj, self.life_color, (x, y, w, h))
        bg_obj.blit(lifeGem, (20,5))
    
    def update_outline(self):
        self.outline_pos = []
        for pt in self.outline:
            self.outline_pos.append( [self.pos[0] + pt[0] , self.pos[1] + pt[1]] )


class Craft1(Craft):
    def __init__(self, **kwargs):
        self.image = pygame.image.load('img/craft/space_craft.png').convert_alpha()
        super().__init__()
        self.rect = pygame.Rect(self.pos[0] + int(self.DIM[0] * 0.22), self.pos[1] + int(self.DIM[1] * 0.15), int(self.DIM[0] * 0.58), int(self.DIM[1] * 0.68))

        self.prop = {'pt': (26,62),
                        'acce': (0,0.1)
                        }
        self.props = {'rad_range': range(4,6),
                        'vel': ({'min': -0.5, 'max': 0.5}, 2),
                        'redux_rate': 0.6,
                        'const_color_range': ((245,256),(245,256),(245,256)),
                        'color_range': ((233,256),(233,256),(0,102))
                        }

        self.flame = Flame(self.prop, self.props)

        self.mozzles = ((15,20), (36,20))

        self.life = 3

    def propel(self, bg_alpha):
        self.flame.combust(bg_alpha, self.pos)






def action(bg_obj, bg_alpha, craft):
    craft.nav()
    craft.propel(bg_alpha)

    if controls.actions['auto_shoot']:
        craft.rapid_strike(bg_obj)
    else:
        craft.shoot(bg_obj)

    bg_obj.blit(craft.image, (craft.pos[0], craft.pos[1]))
    #craft.update_bounds()
    craft.show_bounds(bg_alpha)
    craft.update_outline()

    craft.collision_actions(bg_obj)