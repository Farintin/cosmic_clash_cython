import pygame
from display import view_width, view_height, FPSsec
from colors import RED, YELLOW
from items import *
from explode import Flame, Coma
import random


vw = view_width
vh = view_height

class Bodies:
    def __init__(self, level):
        self.level = level

        self.bodies = []
        '''self.body = Meteor( flame_glow = ((10,11),(116,136),(233,256)), alpha_frac = 0.8, vel = [0,1.7], mass = 2, shield = 24, strength = 3 )
        self.body.selc_item()'''
        '''self.body = Comet( mass = 0, shield = 32, strength = 6 )
        self.body.selc_item()
        self.bodies.append(self.body)'''

        self.init = True
        self.time_range = (2,3)
        self.time = random.randrange(self.time_range[0], self.time_range[1])
        self.timer = 0

        self.attacks_count = 0
        
    def next(self):
        self.timer += FPSsec

        if self.init == True:
            self.timer = self.time
            self.init = False

        if self.timer >= self.time:
            self.choice = random.choice(self.level.bodys_prob)
            
            ### invisble glow_const = ((211,214),(211,214),(211,214)), flame_glow = ((190,196),(190,196),(190,196)), alpha_frac = 0.15
            ### gold glow_const = ((255,256),(140,166),(0,1)), flame_glow = ((255,256),(215,223),(0,1)), alpha_frac = 0.88
            ### aqua-green glow_const = ((105,116),(105,116),(245,256)), flame_glow = ((0,1),(251,256),(250,256)), alpha_frac = 0.8
            ### blue-green glow_const = ((55,56),(55,56),(251,256)), flame_glow = ((1,3),(175,186),(1,3)), alpha_frac = 0.95
            ### violet ((181,190),(1,10),(231,240)), alpha_frac = 0.8
            ### white ((221,256),(221,256),(221,256)), alpha_frac = 0.9
            ###pink ((251,256),(51,56),(211,216)), alpha_frac = 0.85
            ### aqua ((0,10),(251,252),(191,192)), alpha_frac = 0.8
            ### green ((41,46),(251,256),(50,56)), alpha_frac = 0.8
            ### lemon ((171,180),(251,256),(0,10)), alpha_frac = 0.8
            # yellow ((251,256),(251,256),(0,6)), alpha_frac = 0.8
            ### orange ((233,256),(146,166),(30,31)), alpha_frac = 0.9
            ### red-orange ((233,256),(55,56),(10,11)), alpha_frac = 0.9
            ### red ((243,256),(16,26),(3,8)), alpha_frac = 0.8
            ### blue alpha_frac=0.8

            #vel_min = [0,1.5]
            I = int(str(self.choice).split('.')[0])
            dec = int(str(self.choice).split('.')[1])

            shield = 8 * I + 8 * dec
            strength = I + dec

            if I == 1:
                self.body = Meteorite(mass = dec, shield = shield, strength = strength)
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 2:
                self.body = Meteor(mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 3:### m blue
                self.body = Meteor( flame_glow = ((10,11),(116,136),(233,256)), alpha_frac = 0.8, vel = [0,1.7], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 4:### c 1
                self.body = Comet( mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 5:### m red
                self.body = Meteor( flame_glow = ((243,256),(16,26),(3,8)), alpha_frac = 0.8, vel = [0,1.9], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 6:### m red-orange
                self.body = Meteor( flame_glow = ((233,256),(55,56),(10,11)), alpha_frac = 0.9, vel = [0,2.1], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 7:### c 2
                self.body = Comet( vel = [0,2.4], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 8:### m orange
                self.body = Meteor( flame_glow = ((233,256),(146,166),(30,31)), alpha_frac = 0.9, vel = [0,2.3], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 9:### m lemon
                self.body = Meteor( flame_glow = ((171,180),(251,256),(0,10)), alpha_frac = 0.8, vel = [0,2.5], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 10:### c 3
                self.body = Comet( vel = [0,2.8], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 11:### m green
                self.body = Meteor( flame_glow = ((41,46),(251,256),(50,56)), alpha_frac = 0.8, vel = [0,2.7], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 12:### m aqua
                self.body = Meteor( flame_glow = ((0,10),(251,252),(191,192)), alpha_frac = 0.8, vel = [0,2.9], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 13:### c 4
                self.body = Comet( vel = [0,3.2], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 14:### m pink
                self.body = Meteor( flame_glow = ((251,256),(51,56),(211,216)), alpha_frac = 0.85, vel = [0,3.1], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 15:### m white
                self.body = Meteor( flame_glow = ((221,256),(221,256),(221,256)), alpha_frac = 0.9, vel = [0,3.3], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 16:### c 5
                self.body = Comet( vel = [0,3.6], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 17:### m violet
                self.body = Meteor( flame_glow = ((181,190),(1,10),(231,240)), alpha_frac = 0.8, vel = [0,3.5], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 18:### m aqua-green
                self.body = Meteor( glow_const = ((105,116),(105,116),(245,256)), flame_glow = ((0,1),(251,256),(250,256)), alpha_frac = 0.8, vel = [0,3.7], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 19:### c 6
                self.body = Comet( vel = [0,4], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 20:### m blue-green 
                self.body = Meteor( glow_const = ((55,56),(55,56),(251,256)), flame_glow = ((1,3),(175,186),(1,3)), alpha_frac = 0.95, vel = [0,3.9], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 21:### m gold
                self.body = Meteor( glow_const = ((255,256),(140,166),(0,1)), flame_glow = ((255,256),(215,223),(0,1)), alpha_frac = 0.88, vel = [0,4.1], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 22:### c 7
                self.body = Comet( vel = [0,4.4], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            elif I == 23:### m invisble
                self.body = Meteor( glow_const = ((211,214),(211,214),(211,214)), flame_glow = ((190,196),(190,196),(190,196)), alpha_frac = 0.15, vel = [0,4.3], mass = dec, shield = shield, strength = strength )
                self.body.selc_item()
                self.bodies.append(self.body)
            
            self.attacks_count += 1
            #print(self.attacks_count, level.attacks)
            self.time = random.randrange(self.time_range[0], self.time_range[1])
            self.timer = 0


class Body:
    def __init__(self, mass, shield, strength):
        self.surf_type = 'image'
        self.exist = True
        self.flaming = False

        self.rotation = True
        self.spin = {'angle': 0, 'rate': 1}

        self.item1= 'crafts_unit'
        self.items = []
        self.item2 = None

        if mass == 0:
            self.mass = 1
        elif mass == 1:
            self.mass = 1.3
        elif mass == 2:
            self.mass = 1.6

        self.shield = self.shieldMax = shield
        self.strength = strength

        self.explode_avg_rad = round(18 * self.mass)
        self.explode_alpha = 205

    def nav(self):
        self.pos[1] += self.vel[1]

    def rot(self):
        if self.spin['angle'] >= 359:
            self.spin['angle'] = 0
        else:
            self.spin['angle'] += self.spin['rate']

        self.img_rot, self.outline = self.rotated_sprites[int(self.spin['angle'] / self.spin['rate'])]
        
        self.img_rot_w = self.img_rot.get_width()
        self.img_rot_h = self.img_rot.get_height()

    def selc_item(self):
        '''prob_tot = 0
        choice_list = []

        if self.items:
            for choice in self.items:
                n = choice.inverse_prob_unpicked_rate
                prob_tot += n
                choice_list.append((choice.name, n))

            choice_list_inverse_n = []
            for name,n in choice_list:
                a = 1 - n / prob_tot
                b = prob_tot * a
                choice_list_inverse_n.append( (name, round(b)) )

            min_n = min( [n for name,n in choice_list_inverse_n] )
            choice_list_inverse_n_min = []
            for name,n in choice_list_inverse_n:
                choice_list_inverse_n_min.append( (name, n - min_n + 1) )

            pick_bucket_list = []
            for name,n in choice_list_inverse_n_min:
                for i in range(0, n):
                    pick_bucket_list.append(name)
        
            choice = random.choice(pick_bucket_list)
        else:
            choice = 'none'
            '''
        if self.items:
            choice = random.choice(self.items)
        else:
            choice = None
        '''if choice == 'none':
            self.item = None
        elif choice == 'auto_strike':
            self.item = None
        elif choice == 'life':
            self.item = Life()'''
        if choice == 'auto_strike':
            self.item2 = None
        elif choice == 'life':
            self.item2 = Life()
        else:
            choice = None
    
    def set_outline(self):
        #self.mask = pygame.mask.from_surface(self.img_rot)
        self.outline_pos = []
        for pt in self.outline:#self.mask.outline():
            self.outline_pos.append([self.smoothed_rot_x + pt[0], self.smoothed_rot_y + pt[1]])
        #self.outline_pos = list(map(lambda pt: [self.smoothed_rot_x + pt[0], self.smoothed_rot_y + pt[1]], self.mask.outline()))

    def show(self, bg_obj, bg_alpha):
        #bg_obj.blit(self.img_rot, (self.smoothed_rot_x, self.smoothed_rot_y))
        if self.flaming:
            self.combust(bg_alpha)
        return (self.img_rot, (self.smoothed_rot_x, self.smoothed_rot_y))
        '''
        if self.name == 'meteor':
            pygame.draw.line(bg_alpha, RED, (self.pos[0] - self.DIM[0] / 2, self.pos[1] + self.DIM[1] / 2), (self.pos[0] - self.DIM[0] / 2 + self.DIM[0], self.pos[1] + self.DIM[1] / 2))
        else:
            pygame.draw.line(bg_alpha, RED, (self.pos[0] - self.DIM[0] / 2, self.pos[1] + self.DIM[1] / 3), (self.pos[0] - self.DIM[0] / 2 + self.DIM[0], self.pos[1] + self.DIM[1] / 3))
                '''
    
    def show_life(self, bg_alpha):
        x = self.pos[0] + self.DIM[0] / 2
        y = self.pos[1] - 15
        pygame.draw.rect(bg_alpha, RED, (x, y, self.shieldMax + 2, 3))
        pygame.draw.rect(bg_alpha, YELLOW, (x + 1, y + 1, self.shield, 1))
    
    def show_outline(self, bg_obj):
        pygame.draw.lines(bg_obj, RED, True, self.outline_pos, 2)

    def terminate(self):
        # Terminate bodies out of view hieght
        if self.rotation:
            if self.smoothed_rot_y > vh:
                self.exist = False
        else:
            if self.pos[1] > vh or self.rect.top > vh:
                self.exist = False



meteorite_rotated_sprites1 = []
meteor_rotated_sprites1 = []
meteorite_rotated_sprites2 = []
meteor_rotated_sprites2 = []
meteorite_rotated_sprites3 = []
meteor_rotated_sprites3 = []
def load_rotated_sprites(img, rate):
    sprites = []
    while len(sprites) != int(360 / rate):
        for angle in range(0,360,rate):
            img_rot = pygame.transform.rotate(img, angle).convert_alpha()
            mask = pygame.mask.from_surface(img_rot)
            sprites.append( (img_rot, mask.outline()) )

    return sprites

meteorite = pygame.image.load('img/celest/meteorite.png').convert_alpha()
aspect_ratio = meteorite.get_width() / meteorite.get_height()
meteorite1 = pygame.transform.scale( meteorite, (55, round( 55 / aspect_ratio )) ).convert_alpha()
meteorite2 = pygame.transform.scale( meteorite1, (round(55 * 1.3), round( 55 / aspect_ratio * 1.3 )) ).convert_alpha()
meteorite3 = pygame.transform.scale( meteorite1, (round(55 * 1.6), round( 55 / aspect_ratio * 1.6 )) ).convert_alpha()
class Meteorite(Body):
    def __init__(self, mass = 1, shield = 8, strength = 1):
        super().__init__(mass, shield, strength)
        self.name = 'meteorite'

        if self.mass == 1:
            self.DIM = (meteorite1.get_width(), meteorite1.get_height())

            self.rotated_sprites = meteorite_rotated_sprites1
        elif self.mass == 1.3:
            self.DIM = (meteorite2.get_width(), meteorite2.get_height())

            self.rotated_sprites = meteorite_rotated_sprites2
        elif self.mass == 1.6:
            self.DIM = (meteorite3.get_width(), meteorite3.get_height())

            self.rotated_sprites = meteorite_rotated_sprites3
        
        self.pos = [random.randrange(0, vw - self.DIM[0]), -self.DIM[1]]
        self.vel = [0,1]
        self.bottom = self.pos[1] + self.DIM[1] / 3

        self.surf_colors = [(132,116,101), (84,71,63)]

    def nav(self):
        Body.nav(self)
        self.bottom = self.pos[1] + self.DIM[1] / 3

    def rot(self):
        Body.rot(self)
            
        self.smoothed_rot_x = round(self.pos[0]) - int(self.img_rot_w / 2)
        self.smoothed_rot_y = round(self.pos[1]) - round(self.img_rot_h / 2)

        self.ROT_DIM = (self.img_rot_w, self.img_rot_h)




meteor1 = pygame.image.load('img/celest/meteor.png').convert_alpha()
meteor2 = pygame.transform.scale( meteor1, (round(meteor1.get_width() * 1.3), round(meteor1.get_height() * 1.3)) ).convert_alpha()
meteor3 = pygame.transform.scale( meteor1, (round(meteor1.get_width() * 1.6), round(meteor1.get_height() * 1.6)) ).convert_alpha()
class Meteor(Body):
    def __init__(self, glow_const = ((245,256),(245,256),(245,256)), flame_glow = ((233,256),(233,256),(0,102)), alpha_frac = 0.9, vel = [0,1.7], mass = 1, shield = 8, strength = 2):
        super().__init__(mass, shield, strength)
        self.name = 'meteor'

        if self.mass == 1:
            self.DIM = (meteor1.get_width(), meteor1.get_height())

            self.rotated_sprites = meteor_rotated_sprites1
        elif self.mass == 1.3:
            self.DIM = (meteor2.get_width(), meteor2.get_height())

            self.rotated_sprites = meteor_rotated_sprites2
        elif self.mass == 1.6:
            self.DIM = (meteor3.get_width(), meteor3.get_height())

            self.rotated_sprites = meteor_rotated_sprites3

        self.pos = [random.randrange(0, vw - self.DIM[0]), -self.DIM[1]]
        self.vel = vel
        self.bottom = self.pos[1] + self.DIM[1] / 2

        self.prop = {'pt': (int(self.DIM[0] / 2), int(self.DIM[1] * 0.65)),
                        'acce': (0,0.02)
                        }
        self.props = {'rad_range': range(round(16 * self.mass), round(24 * self.mass)),
                        'vel': ({'min': -0.1, 'max': 0.1},-1),
                        'redux_rate': 0.5 * self.mass,
                        'const_color_range': glow_const,
                        'color_range': flame_glow,
                        'alpha_frac': alpha_frac
                        }
        self.flaming = True
        self.flame = Flame(self.prop, self.props)

        #self.shield = self.shieldMax = 24
        #self.strength = 2

        #self.items = [Choice('life', 1), Choice('auto_strike', 10)]
        self.items = ['life'] * 1# + ['auto_strike'] * 2 + [None] * 7

        self.surf_colors = [(181,114,59), (99,55,28), (39,39,39)]
    
    def combust(self, bg_alpha):
        self.prop['pt'] = (round(self.ROT_DIM[0] / 2), round(self.ROT_DIM[1] * 0.65))
        self.flame.combust(bg_alpha, (self.smoothed_rot_x, self.smoothed_rot_y), self.props['alpha_frac'], self.prop['pt'])
    
    def nav(self):
        Body.nav(self)
        self.bottom = self.pos[1] + self.DIM[1] / 2

    def rot(self):
        Body.rot(self)
        self.smoothed_rot_x = round(self.pos[0]) - int(self.img_rot_w / 2 - 0.5)
        self.smoothed_rot_y = round(self.pos[1]) - round(self.img_rot_h / 2 + 0.5)

        self.ROT_DIM = (self.img_rot_w, self.img_rot_h)




surf = pygame.Surface((vw, vh))
surf = surf.convert_alpha()
surf.set_colorkey((0,0,0,0))
class Comet(Body):
    def __init__(self, vel = [0,2], mass = 1, shield = 8, strength = 1):
        super().__init__(mass, shield, strength)
        self.surf_type = 'draw'
        self.name = 'comet'
        self.rotation = False
        self.flaming = True

        self.w = 32 * self.mass
        self.rad = round(self.w / 2)
        self.color = (0,0,255,105)

        self.pos = [ random.randrange( 0, round(vw - self.w) ), -round(self.w) ]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.w, self.w)
        self.DIM = (self.w, self.w)
        self.vel = vel
        self.bottom = self.rect.top + self.rect.height

        surf.fill((0,0,0,0))
        pygame.draw.circle(surf, (255,255,255,255), (self.rad, self.rad), self.rad)
        self.mask = pygame.mask.from_surface(surf)
        self.outline = []
        for pt in self.mask.outline():
            self.outline.append([pt[0], pt[1]])
        self.outline_pos = []

        self.prop1 = {'pt': (0,16),
                        'ax': 0
                        }
        self.props1 = {'rad_range': range(round(5 * self.mass), round(5 * self.mass + 1)),
                        'vel': ({'min': -3, 'max': 3}, 1.3),
                        'redux_rate': 0.25 * self.mass,
                        'colors': ([155,155,255,155], [255,255,255,155]),
                        }
        self.coma1 = Coma(self.prop1, self.props1)
        self.prop2 = {'pt': (0,14),
                        'ax': 0
                        }
        self.props2 = {'rad_range': range(round(10 * self.mass), round(10 * self.mass + 1)),
                        'vel': ({'min': -2, 'max': 2}, -0.1),
                        'redux_rate': 0.38 * self.mass,
                        'colors': ([155,155,255,125], [255,255,255,125], [255,255,255,125], [255,255,255,125]),
                        }
        self.coma2 = Coma(self.prop2, self.props2)
        self.prop3 = {'pt': (0,6),
                        'ax': 0
                        }
        self.props3 = {'rad_range': range(round(16 * self.mass), round(16 * self.mass + 1)),
                        'vel': ({'min': -1.4, 'max': 1.4}, -2),
                        'redux_rate': 0.8 * self.mass,
                        'colors': ([255,255,255,155],[255,255,255,155]),
                        }
        self.coma3 = Coma(self.prop3, self.props3)
        self.prop4 = {'pt': (0,8),
                        'ax': 0.1
                        }
        self.props4 = {'rad_range': range(round(20 * self.mass), round(20 * self.mass + 1)),
                        'vel': ({'min': -1, 'max': 1}, -8),
                        'redux_rate': 1 * self.mass,
                        'colors': ([255,255,255,205],[255,255,255,205]),
                        }
        self.coma4 = Coma(self.prop4, self.props4)

        self.explode_avg_rad = round(32 * self.mass)
        self.explode_alpha = 255
        self.surf_colors = [(255,255,255), (255,255,255),(0,0,255,105),[155,155,255,155]]

        self.items2 = ['life'] * 1 + ['auto_strike'] * 4 + [None] * 5

    def nav(self):
        #self.pos[1] += self.vel[1]
        self.rect.top += self.vel[1]
        self.bottom = self.rect.top + self.rect.height

    def set_outline(self):
        self.outline_pos = []
        for pt in self.outline:
            self.outline_pos.append( [self.rect.left + pt[0], self.rect.top + pt[1] ] )

    def show(self, bg_obj, bg_alpha):
        self.coma3.outgas(bg_obj, bg_alpha, self.rect.center)
        self.coma2.outgas(bg_obj, bg_alpha, self.rect.center)
        self.coma4.eject(bg_obj, bg_alpha, self.rect.center)
        self.coma1.outgas(bg_obj, bg_alpha, self.rect.center)
        pygame.draw.circle( bg_alpha, self.color, ( int(self.rect.centerx), int(self.rect.centery) ), round(self.w / 2) )
        #pygame.draw.rect(bg_alpha, RED, self.rect, 1)
        #bg.blit(bg_alpha, (0,0))
        #pygame.draw.line(bg_alpha, RED, (self.rect.left, self.rect.top + self.rect.height), (self.rect.left + self.rect.width, self.rect.top + self.rect.height))
        

    def show_life(self, bg_alpha):
        x = self.rect.left + self.DIM[0] + 16
        y = self.rect.top - 8
        pygame.draw.rect(bg_alpha, RED, (x, y, self.shieldMax + 2, 3))
        pygame.draw.rect(bg_alpha, YELLOW, (x + 1, y + 1, self.shield, 1))

    def show_outline(self, bg_obj):
        if self.outline_pos:
            pygame.draw.lines(bg_obj, RED, True, self.outline_pos, 2)