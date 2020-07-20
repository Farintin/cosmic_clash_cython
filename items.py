import pygame
import pygame.gfxdraw
from svg.path import Path, parse_path
import math



class Item:
    def __init__(self, multi):
        self.DIM = (self.img.get_width(), self.img.get_height())
        self.exist = True
        self.magnetized = False

        self.vel = (0,1.5)
        self.scal = 1
        self.acceConst = 400

        self.multi = multi

        self.timing = self.timer = 30 * self.multi
    
    def get_vecs(self, tar_center):
        self.dx = tar_center[0] - self.rect.centerx
        self.dy = tar_center[1] - self.rect.centery
        self.r = math.sqrt(self.dx**2 + self.dy**2)
        if self.dx == 0:
            vec_x = 0
        else:
            vec_x = self.dx / abs(self.dx)
        if self.dy == 0:
            vec_y = 0
        else:
            vec_y = self.dy / abs(self.dy)

        return (vec_x, vec_y)

    def init_attraction(self, tar_center):
        self.tar_center = tar_center
        self.vec = self.get_vecs(self.tar_center)
        self.set_vel()

    def nav(self, craft):
        tar_center = craft.rect.center
        if (not self.magnetized) and craft.magnet:
            self.init_attraction(tar_center)
        self.magnetized = craft.magnet

        if self.magnetized:
            vec = self.get_vecs(tar_center)
            if self.tar_center != tar_center or self.vec != vec:
                self.tar_center = tar_center
                self.vec = vec
                self.set_vel()
            if self.r > 400:
                dv = [self.vel[0] * self.scal / self.acceConst, self.vel[1] * self.scal / self.acceConst]
            else:
                dv = [self.vel[0] / self.r, self.vel[1] / self.r]
            self.pos[0] += dv[0]
            self.pos[1] += dv[1]
        else:
            self.pos[1] += self.vel[1]
        self.rect.top = self.pos[1]
        self.rect.centerx = self.pos[0] + self.rectCenterxLock
        self.bottom = self.pos[1] + self.DIM[1]

    def set_pos(self, pos):
        pos[0] -= int(self.DIM[0] / 10)
        pos[1] -= int(self.DIM[1] / 5)
        self.pos = pos
        self.rect.top = self.pos[1]
        self.rect.centerx = self.pos[0] + self.rectCenterxLock
        self.bottom = self.pos[1] + self.DIM[1]

    def set_vel(self):
        dx = self.dx
        dy = self.dy
        if abs(dy) > abs(dx):
            det = abs(dy)
            if det == 0:
                det = dx = 1
        elif abs(dx) >= abs(dy):
            det = abs(dx)
            if det == 0:
                det = dy = 1
        dx /= det
        dy /= det
        self.vel = [dx * self.acceConst, dy * self.acceConst]

    def show(self, bg_obj):
        pygame.draw.line(bg_obj, (255,0,0), (self.pos[0], self.bottom), (self.pos[0] + self.DIM[0], self.bottom))
        return (self.img, self.pos)

    def show_bounds(self, bg_obj):
        pygame.draw.rect(bg_obj, (255,0,0), self.rect, 1)




class Empty:
    def __init__(self, multi):
        self.name = ''




unit = pygame.image.load('img/item/unit.png').convert_alpha()
unit = pygame.transform.scale(unit, (37,37))
class Unit:
    def __init__(self, multi):
        self.name = 'unit'
        self.imgAR = 1
        self.img = unit.copy()

        self.multi = multi

        self.vy = 2.2
        
        self.DIM = (self.img.get_width(), self.img.get_height())
        self.exist = True
        self.magnetized = False

        self.rect = pygame.Rect(0,0, self.DIM[0] / 2.5, self.DIM[1] / 1.2)

        self.collected_color = (255,255,255)

        self.scal = 1.2
        self.acceConst = 500

    def fall(self, craft):
        tar_center = craft.rect.center
        if (not self.magnetized) and craft.magnet:
            self.init_attraction(tar_center)
        self.magnetized = craft.magnet

        if self.magnetized:
            vec = self.get_vecs(tar_center)
            if self.tar_center != tar_center or self.vec != vec:
                self.tar_center = tar_center
                self.vec = vec
                self.set_vel()
            if self.r > 400:
                dv = [self.vx * self.scal / self.acceConst, self.vy * self.scal / self.acceConst]
            else:
                dv = [self.vx / self.r, self.vy / self.r]
            self.left += dv[0]
            self.top += dv[1]
        else:
            self.top += self.vy
        self.rect.top = self.top
        self.rect.centerx = self.left + self.DIM[0] * 0.5
        self.bottom = self.top + self.DIM[1]

    def get_vecs(self, tar_center):
        self.dx = tar_center[0] - self.rect.centerx
        self.dy = tar_center[1] - self.rect.centery
        self.r = math.sqrt(self.dx**2 + self.dy**2)
        if self.dx == 0:
            vec_x = 0
        else:
            vec_x = self.dx / abs(self.dx)
        if self.dy == 0:
            vec_y = 0
        else:
            vec_y = self.dy / abs(self.dy)

        return (vec_x, vec_y)

    def init_attraction(self, tar_center):
        self.tar_center = tar_center
        self.vec = self.get_vecs(self.tar_center)
        self.set_vel()

    def set_pos(self, pos):
        pos[0] -= int(self.DIM[0] / 2)
        pos[1] -= int(self.DIM[1] / 2)
        self.left = pos[0]
        self.top = pos[1]
        self.bottom = self.top + self.DIM[1]

        self.rect.top = self.top
        self.rect.centerx = self.left + self.DIM[0] * 0.53

    def set_vel(self):
        dx = self.dx
        dy = self.dy
        if abs(dy) > abs(dx):
            det = abs(dy)
            if det == 0:
                det = dx = 1
        elif abs(dx) >= abs(dy):
            det = abs(dx)
            if det == 0:
                det = dy = 1
        dx /= det
        dy /= det
        self.vx, self.vy = [dx * self.acceConst, dy * self.acceConst]

    def show(self, bg_obj):
        pygame.draw.line(bg_obj, (255,0,0), (self.left, self.bottom), (self.left + self.DIM[0], self.bottom))
        return (self.img, [self.left, self.top])

    def show_bounds(self, bg_obj):
        pygame.draw.rect(bg_obj, (255,0,0), self.rect, 1)





######################### Items yypes
'''
bubble = pygame.image.load('img/item/bubble.png').convert_alpha()
bubbleAR = bubble.get_width() / bubble.get_height()
bubble = pygame.transform.scale(bubble, (30, round(30 / bubbleAR)))
class Bubble(Item):
    def __init__(self, multi):
        self.name = 'bubble'
        self.imgAR = bubbleAR
        self.img = bubble.copy()

        super().__init__(multi)
        self.rect = pygame.Rect(0,0, self.DIM[0] * 0.8, self.DIM[1] * 0.8)
        self.rectCenterxLock = self.DIM[0] * 0.5

        self.collected_color = (55,155,255)'''


life_gem_orbits_data = []
def make_life_gem_orbs():
    orbit1 = "M 34.725789,26.545096 A 17.525509,6.6771445 30 0 1 16.209682,23.56492 17.525509,6.6771445 30 0 1 4.3707178,9.0195882 17.525509,6.6771445 30 0 1 22.886827,11.999766 17.525509,6.6771445 30 0 1 34.725789,26.545096 Z"
    orbit2 = "M 0.85323813,27.287158 A 9.764492,21.966513 60 0 1 14.994551,7.8476032 9.764492,21.966513 60 0 1 38.900355,5.3206444 9.764492,21.966513 60 0 1 24.759042,24.760199 9.764492,21.966513 60 0 1 0.85323813,27.287158 Z"
    path1 = {'svg': parse_path(orbit1), 'n': 35, 'pos': (0,0), 'rev_dir': 1, 'ptc_color': (250,250,255)}
    path2 = {'svg': parse_path(orbit2), 'n': 50, 'pos': (1,2), 'rev_dir': -1, 'ptc_color': (205,205,255)}
    patterns = [path1, path2]

    for path in patterns:
        pts = [(p.real + path['pos'][0], p.imag + path['pos'][1]) for p in (path['svg'].point(i/path['n']) for i in range(0, path['n']+1))]
        ptsx = [pt[0] for pt in pts]
        ptsy = [pt[1] for pt in pts]
        
        ptsx_min = round(min(ptsx))
        ptsx_max = round(max(ptsx))
        ptsy_min = round(min(ptsy))
        ptsy_max = round(max(ptsy))

        ptsw = ptsx_max - ptsx_min
        ptsh = ptsy_max - ptsy_min

        life_gem_orbits_data.append({'pts': pts,
                                    'minx': ptsx_min,
                                    'maxx': ptsx_max,
                                    'miny': ptsy_min,
                                    'maxy': ptsy_max,
                                    'w': ptsw,
                                    'h': ptsh,
                                    'iter_n': 0,
                                    'rev_dir': path['rev_dir'],
                                    'ptc_color': path['ptc_color']
                                    })
    return life_gem_orbits_data
gem = pygame.image.load('img/item/gem.png').convert_alpha()
gemAR = gem.get_width() / gem.get_height()
class Life(Item):
    def __init__(self, multi):
        self.name = 'life'
        self.imgAR = gemAR
        self.img = gem.copy()
        
        self.orbits_data = life_gem_orbits_data
        super().__init__(multi)
        self.rect = pygame.Rect(0,0, self.DIM[0] * 0.3, self.DIM[1] * 0.8)
        self.rectCenterxLock = self.DIM[0] * 0.5

        self.collected_color = (175,175,255)

    def intra_animate(self, bg_obj):
        for orbit in self.orbits_data:
            if orbit['rev_dir'] == 1:
                self.index = orbit['iter_n']
            elif orbit['rev_dir'] == -1:
                self.index = len(orbit['pts']) -1 - orbit['iter_n']

            self.pt = orbit['pts'][self.index] 
            self.x = round(self.pt[0])
            self.y = round(self.pt[1])
        
            pygame.gfxdraw.filled_circle(bg_obj, round(self.pos[0] + self.x), round(self.pos[1] + self.y), 1, orbit['ptc_color'])

            orbit['iter_n'] += 1
            if orbit['rev_dir'] == 1:
                if orbit['iter_n'] > len(orbit['pts']) - 1:
                    orbit['iter_n'] = 0
            elif orbit['rev_dir'] == -1:
                orbit['iter_n'] += 1
                if orbit['iter_n'] >= len(orbit['pts']):
                    orbit['iter_n'] = 0

    def show(self, bg_obj):
        self.intra_animate(bg_obj)
        return Item.show(self, bg_obj)


magnet = pygame.image.load('img/item/magnet.png').convert_alpha()
magnetAR = magnet.get_width() / magnet.get_height()
magnet = pygame.transform.scale(magnet, (30, round(30 / magnetAR)))
class Magnet(Item):
    def __init__(self, multi):
        self.name = 'magnet'
        self.imgAR = magnetAR
        self.img = magnet.copy()

        super().__init__(multi)
        self.rect = pygame.Rect(0,0, self.DIM[0] * 0.8, self.DIM[1] * 0.9)
        self.rectCenterxLock = self.DIM[0] * 0.5

        self.collected_color = (255,55,55)


puff = pygame.image.load('img/item/puff.png').convert_alpha()
puff = pygame.transform.scale(puff, (37, 37))
class Puff(Item):
    def __init__(self, multi):
        self.name = 'puff'
        self.imgAR = 1
        self.img = puff.copy()

        super().__init__(multi)
        self.rect = pygame.Rect(0,0, self.DIM[0] * 0.8, self.DIM[1] * 0.9)
        self.rectCenterxLock = self.DIM[0] * 0.55

        self.collected_color = (255,195,55)

        if self.multi == 1:
            self.half_w = 3
        elif self.multi == 2:
            self.half_w = 4
        elif self.multi == 4:
            self.half_w = 5
        self.h = self.half_w * 2 * 2


rapid = pygame.image.load('img/item/rapid.png').convert_alpha()
rapidAR1 = rapid.get_width() / rapid.get_height()
rapidAR2 = 25 / (20 / rapidAR1)
rapid = pygame.transform.scale(rapid, (25, round(25 / rapidAR2)))
class Rapid(Item):
    def __init__(self, multi):
        self.name = 'rapid'
        self.imgAR = rapidAR2
        self.img = rapid.copy()
        
        super().__init__(multi)
        self.rect = pygame.Rect(0,0, self.DIM[0] * 0.5, self.DIM[1] * 0.8)
        self.rectCenterxLock = self.DIM[0] * 0.5

        self.collected_color = (255,235,55)


shield = pygame.image.load('img/item/shield.png').convert_alpha()
shieldAR = shield.get_width() / shield.get_height()
shield = pygame.transform.scale(shield, (32, round(32 / shieldAR)))
class Shield(Item):
    def __init__(self, multi):
        self.name = 'shield'
        self.imgAR = shieldAR
        self.img = shield.copy()
        
        super().__init__(multi)
        self.rect = pygame.Rect(0,0, self.DIM[0] * 0.8, self.DIM[1] * 0.9)
        self.rectCenterxLock = self.DIM[0] * 0.55

        self.collected_color = (0,255,205)