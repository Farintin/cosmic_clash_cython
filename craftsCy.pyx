import pygame
import display, colors, controls
from bulletsCy import *
from explodeCy import *
import db



cdef int vw = display.view_width
cdef int vh = display.view_height
cdef tuple vc = display.view_center
cdef float FPSsec = display.FPSsec

cdef list shoot, blit
cdef tuple pt
cdef bint collide

class Craft:
    def __init__(self):
        cdef bint collide, collided, bubble_collide

        self.center = (self.DIM[0] / 2, self.DIM[1] / 2)
        self.surf_rect = pygame.Rect(vc[0], 0, self.DIM[0], self.DIM[1])
        self.surf_rect.centery = vh - 60
        self.pos = [self.surf_rect.left, self.surf_rect.top]
        self.craft_rect = pygame.Rect(0,0, self.surf_rect.width * 0.65, self.surf_rect.height * 0.9)
        self.craft_rect.center = self.surf_rect.center

        self.shoots = []
        self.shooting = False

        self.defaults = {
            'rapid_load_period_stamp': 0.1
        }
        self.rapid_strike = False
        self.rapid_strike_timer = 0
        self.rapid_load_period_stamp = self.defaults['rapid_load_period_stamp']

        self.dx = 0

        self.mask = pygame.mask.from_surface(self.image)
        self.outline = []
        for pt in self.mask.outline():
            self.outline.append( (pt[0], pt[1]) )
        self.outline_color = colors.RED

        self.collide = False
        self.collided = False

        self.units = 0
        self.items = []
        self.periodic_items = ['puffy','rapid','magnet','bubble']
        self.magnet = False

        self.bubble = False
        self.bubble_rad = self.inner_width * 2
        self.bubble_color = colors.AQUABLUE + [255]
        self.bubble_surf = pygame.Surface((self.bubble_rad * 2, self.bubble_rad * 2))
        self.bubble_surf.convert_alpha()
        self.bubble_surf.set_colorkey((0,0,0,0))
        self.bubble_surf.fill((0,0,0,0))
        self.bubble_rect = pygame.Rect(0,0, self.bubble_rad * 2, self.bubble_rad * 2)
        self.bubble_collide = False

        while self.bubble_rad > 0:
            if self.bubble_color[3] < 1:
                self.bubble_color[3] = 1
            pygame.gfxdraw.circle(self.bubble_surf, self.bubble_rect.centerx, self.bubble_rect.centery, int(self.bubble_rad - 1), self.bubble_color)
            self.bubble_rad -= 1
            self.bubble_color[3] -= 12
        
        self.bubble_mask = pygame.mask.from_surface(self.bubble_surf)
        self.bubble_outline = []
        for pt in self.bubble_mask.outline():
            self.bubble_outline.append( (pt[0], pt[1]) )

        self.update_outline()

    def action(self, object bg_obj, object bg_alpha):
        self.items_state()
        self.nav()
        self.propel(bg_alpha)
        self.strike(bg_obj)
        #self.show_bounds(bg_alpha)
        self.update_outline()
        #self.draw_bubble_outline(bg_alpha)
        self.show(bg_obj)
        self.collide_indication(bg_obj)

    def body_collision(self, object body, list explosions):
        collide = False
        if self.bubble and body.bottom >= self.bubble_rect.top:
            for pt in body.outline_pos:
                if pt in self.bubble_outline_pos:
                    self.bubble_collide = True
                    break
        elif body.bottom >= self.rect.top:
            for pt in body.outline_pos:
                if pt[0] in range(self.rect.left, self.rect.right) and pt[1] in range(self.rect.top, self.rect.bottom):
                    self.outline_color = colors.RED
                    collide = True
                    break

        if collide or self.bubble_collide:
            if body.rotation:
                explode_pos = [body.smoothed_rot_x + body.ROT_DIM[0] / 2, body.smoothed_rot_y + body.ROT_DIM[1] / 2]
            else:
                explode_pos = body.rect.center
            ripple = body.ripple
            ripple.set_pos(explode_pos)
            scatter = body.scatter
            scatter.set_pos(explode_pos)
            scatter.gen()
            explosions.append(ripple)
            explosions.append(scatter)

            body.exist = False
            self.bubble_collide = False
        if collide:
            if db.document["item"]["items"]["shield"]["bought"]:
                if body.power > db.document["item"]["items"]["shield"]["bought"]:
                    body.power = abs(db.document["item"]["items"]["shield"]["bought"] - body.power)
                    db.document["item"]["items"]["shield"]["bought"] = 0
                elif body.power == db.document["item"]["items"]["shield"]["bought"]:
                    body.power = 0
                    db.document["item"]["items"]["shield"]["bought"] = 0
                else:
                    db.document["item"]["items"]["shield"]["bought"] -= body.power
                    body.power = 0
            self.shield -= body.power
            self.collide = True

    def collect(self, object item):
        name = item.name
        if name == 'shield':
            self.shield += 1
        elif name == 'rapid':
            self.rapid_strike = True
            self.rapid_load_period_stamp = self.defaults['rapid_load_period_stamp'] / item.multi
        elif name == 'puffy':
            self.puff_bullet(item)
        elif name == 'magnet':
            self.magnet = True
        elif name == 'bubble':
            self.bubble = True

        if name in self.periodic_items:
            item.img = pygame.transform.scale(item.img, (16, round(16 / item.imgAR)))
            for i in self.items:
                if i.name == name:
                    self.items.remove(i)
            self.items.append(item)

    def collide_indication(self, object bg_obj):
        if self.collide:
            self.collided = True
            self.collide = False
            self.collided_blink_counter = 0
            self.blink_outline_timer = 0

        if self.collided:
            if self.blink_outline_timer <= 0.1:
                self.draw_outline(bg_obj)
            if self.blink_outline_timer >= 0.15:
                self.blink_outline_timer = 0
                self.collided_blink_counter += 1

            if self.collided_blink_counter >= 4:
                self.draw_outline(bg_obj)
                self.collided = False
            else:
                self.blink_outline_timer += FPSsec

    def draw_outline(self, object bg_obj):
        pygame.draw.polygon(bg_obj, self.outline_color, self.outline_pos)
    
    def draw_bubble_outline(self, object bg_alpha):
        pygame.draw.lines(bg_alpha, colors.RED, True, self.bubble_outline_pos)

    def item_collision(self, object item):
        if item.rect.bottom >= self.rect.top:
            if pygame.sprite.collide_rect(item, self):
                if item.name == 'unit':
                    self.units += item.multi
                else:
                    self.collect(item)
                item.exist = False
                self.outline_color = item.collected_color
                self.collide = True

    def items_state(self):
        for item in self.items:
            if item.timer <= 0:
                self.items.remove(item)
                name = item.name
                if name == 'puffy':
                    self.bullet_rad = self.defaults['bullet_rad']
                elif name == 'rapid':
                    self.rapid_strike = False
                    self.rapid_load_period_stamp = self.defaults['rapid_load_period_stamp']
                elif name == 'magnet':
                    self.magnet = False
                elif name == 'bubble':
                    self.bubble = False

    def load_bullets(self):
        shoot = []
        for pt in self.mozzles:
            shoot.append( self.bullet([self.pos[0] + pt[0], self.pos[1] + pt[1]], self.bullet_rad, self.bullet_power) )
        self.shoots.append(shoot)

    def nav(self):
        self.pos[0] += self.dx
        if self.pos[0] <= 0:
            self.pos[0] = 0
        elif self.pos[0] + self.DIM[0] >= vw:
            self.pos[0] = vw - self.DIM[0]
        self.rect.left = self.pos[0] + int(self.DIM[0] * 0.22)
        self.surf_rect.center = self.craft_rect.center = self.rect.center
        if self.bubble:
            self.bubble_rect.center = self.rect.center
    
    def rapid_shoots(self, object bg_obj):
        if self.rapid_strike_timer >= self.rapid_load_period_stamp:
            self.load_bullets()
            self.rapid_strike_timer = 0
        else:
            self.rapid_strike_timer += FPSsec

        if self.shoots:
            self.shoot(bg_obj)

    def shoot(self, object bg_obj):
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

    def show(self, object bg_obj):
        bg_obj.blit(self.image, (self.pos[0], self.pos[1]))
        if self.bubble:
            bg_obj.blit(self.bubble_surf, (self.bubble_rect.left, self.bubble_rect.top))

    def show_bounds(self, object bg_obj):
        pygame.draw.rect(bg_obj, colors.RED, self.rect, 1)
        pygame.draw.rect(bg_obj, colors.GREEN, self.craft_rect, 1)
        pygame.draw.rect(bg_obj, colors.BLUE, self.surf_rect, 1)
        for pt in self.mozzles:
            mozzle_pos = (self.pos[0] + pt[0], self.pos[1] + pt[1])
            pygame.draw.circle(bg_obj, colors.RED, mozzle_pos, 2)

    def strike(self, object bg_obj):
        if self.rapid_strike and self.shooting:
            self.rapid_shoots(bg_obj)
        else:
            self.shoot(bg_obj)
    
    def update_bullet(self, int multi):
        self.bullet_rad = m

    def update_outline(self):
        self.outline_pos = []
        for pt in self.outline:
            self.outline_pos.append( [self.pos[0] + pt[0] , self.pos[1] + pt[1]] )
        if self.bubble:
            self.bubble_outline_pos = []
            for pt in self.bubble_outline:
                self.bubble_outline_pos.append( [self.bubble_rect.left + pt[0], self.bubble_rect.top + pt[1]] )


class Craft1(Craft):
    def __init__(self):
        self.image = pygame.image.load('img/craft/space_craft.png').convert_alpha()
        self.DIM = (self.image.get_width(), self.image.get_height())
        self.inner_width = self.DIM[0] * 0.64
        super().__init__()
        self.rect = pygame.Rect(0, 0, int(self.surf_rect.width * 0.58), int(self.surf_rect.height * 0.68) + 10)
        self.rect.center = self.craft_rect.center
        self.rect.centery += 5

        self.prop = {'pt': (26,64),
                        'acce': (0,0.1)
                        }
        self.props = {'rad_range': list(range(6,7)),
                        'vel': ({'min': -0.2, 'max': 0.2}, 1.5),
                        'redux_rate': 0.6,
                        'const_color_range': ((245,256),(245,256),(245,256)),
                        'color_range': ((233,256),(233,256),(0,102)),
                        'alpha_frac': 1
                        }
        self.flame = Flame(self.prop, self.props)

        self.mozzles = ((15,20), (36,20))
        self.bullet = Craft1Bullet

        self.defaults.update({
            'bullet_rad': 2,
            'bullet_power': 1,
            'shield': 3
        })
        self.bullet_rad = self.defaults['bullet_rad']
        self.bullet_power = self.defaults['bullet_power']
        self.shield = self.defaults['shield']

    def propel(self, object bg_alpha):
        self.flame.combust(bg_alpha, self.pos)

    def puff_bullet(self, object item):
        self.bullet_rad = item.half_w
        self.bullet_power = self.defaults['bullet_power'] * item.multi