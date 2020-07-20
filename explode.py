import pygame
import display
import random
from math import *




class Flame:
    def __init__(self, prop, props):
        self.pt = prop['pt']
        self.acce = prop['acce']

        self.sizes = props['rad_range']
        self.vel = props['vel']
        self.velx1 = self.vel[0]['min']
        self.velx2 = self.vel[0]['max']
        self.vely = self.vel[1]
        self.redux_rate = props['redux_rate']
        self.const_color_range = props['const_color_range']
        self.color_range = props['color_range']

        self.particles = []

    def combust(self, bg_alpha, lock_pos, alpha = 1, pt = ()):
        if pt:
            self.pt = pt

        self.pos = [lock_pos[0] + self.pt[0], lock_pos[1] + self.pt[1]]
        self.velx = (random.randint(0, 2 * self.velx2 * 10) / 10) + self.velx1
        self.size = random.choice(self.sizes)

        self.particles.append([ self.pos, [self.velx, self.vely], self.size])
        #particles.append([[mx, my], [random.randint(0, 10) / 10 - 0.5, 2], random.randint(4, 6)])

        
        for ptc in self.particles:
            ptc[0][0] += ptc[1][0]
            ptc[0][1] += ptc[1][1]
            ptc[2] -= self.redux_rate
            ptc[1][1] += self.acce[1]
                
            self.dye_conc = random.randrange(0,3)
            if self.dye_conc == 0:
                self.dyeR = random.randrange(self.const_color_range[0][0], self.const_color_range[0][1])
                self.dyeG = random.randrange(self.const_color_range[1][0], self.const_color_range[1][1])
                self.dyeB = random.randrange(self.const_color_range[2][0], self.const_color_range[2][1])
            elif self.dye_conc == 1:
                self.dyeR = random.randrange(self.color_range[0][0], self.color_range[0][1])#(233,256)
                self.dyeG = random.randrange(self.color_range[1][0], self.color_range[1][1])#(233,256)
                self.dyeB = random.randrange(self.color_range[2][0], self.color_range[2][1])#(0,102)
            elif self.dye_conc == 2:
                self.dyeR = random.randrange(self.color_range[0][0], self.color_range[0][1])#(233,256)
                self.dyeG = random.randrange(self.color_range[1][0], self.color_range[1][1])#(233,256)
                self.dyeB = random.randrange(self.color_range[2][0], self.color_range[2][1])#(0,102)

            pygame.draw.circle(bg_alpha, (self.dyeR, self.dyeG, self.dyeB, alpha * 255), [int(ptc[0][0]), int(ptc[0][1])], int(ptc[2]))
            if ptc[2] <= 0:
                #ptc[3] = False
                self.particles.remove(ptc)



class Coma:
    def __init__(self, prop, props):
        self.pt = prop['pt']
        self.ax = prop['ax']

        self.sizes = props['rad_range']
        self.redux_rate = props['redux_rate']

        self.vel = props['vel']
        self.velx1 = self.vel[0]['min']
        self.velx2 = self.vel[0]['max']
        self.vely = self.vel[1]

        self.colors = props['colors']

        self.particles = []

    def outgas(self, bg_obj, bg_alpha, lock_pos):
        self.pos = [lock_pos[0] + self.pt[0], lock_pos[1] + self.pt[1]]

        color = random.choice(self.colors)

        self.velx = (random.randint(0, 2 * self.velx2 * 10) / 10) + self.velx1
        self.size = random.choice(self.sizes)

        self.particles.append([ self.pos, [self.velx, self.vely], self.size, color])
        #self.particles.append([[pos[0], pos[1]], [random.randint(0, 60) / 10 - 3, 0.5], 4, va, color])
    
        for ptc in self.particles:
            ptc[0][0] += ptc[1][0]
            ptc[0][1] += ptc[1][1]

            ptc[2] -= self.redux_rate
            
            pygame.draw.circle(bg_alpha, ptc[3], [int(ptc[0][0]), int(ptc[0][1])], int(ptc[2]))
            if ptc[2] <= 0:
                self.particles.remove(ptc)
            '''elif ptc[0][0] == vc[0]:
                self.particles.remove(ptc)'''

        bg_obj.blit(bg_alpha, (0,0))

    def eject(self, bg_obj, bg_alpha, lock_pos):
        self.pos = [lock_pos[0] + self.pt[0], lock_pos[1] + self.pt[1]]

        color = random.choice(self.colors)

        self.velx = (random.randint(0, 2 * self.velx2 * 10) / 10) + self.velx1
        self.size = random.choice(self.sizes)

        self.particles.append([ self.pos, [self.velx, self.vely], self.size, color])
    
        for ptc in self.particles:
            ptc[0][0] += ptc[1][0]
            ptc[0][1] += ptc[1][1]

            ptc[2] -= self.redux_rate

            x = ptc[0][0]
            y = ptc[0][1]
            if x < lock_pos[0]:
                ptc[1][0] += self.ax
            elif x > lock_pos[0]:
                ptc[1][0] -= self.ax
            else:
                ptc[1][0] = 0
            
            pygame.draw.circle(bg_alpha, ptc[3], [int(ptc[0][0]), int(ptc[0][1])], int(ptc[2]))
            if ptc[2] <= 0:
                self.particles.remove(ptc)
            elif ptc[0][0] == lock_pos[0]:
                self.particles.remove(ptc)

        bg_obj.blit(bg_alpha, (0,0))



class Ripple:
    def __init__(self, pos, **kwargs):
        self.active = True
        self.pos = (round(pos[0]), round(pos[1]))
        self.avg_r = kwargs['explode_avg_rad']
        self.alpha_max = kwargs['explode_alpha']
        self.Fsec_i = 0
        self.out_speed = 1.5
        self.acce = 0.05

    def expand(self, bg_alpha):
        if self.active:
            if self.Fsec_i == 0:
                self.r = self.w = 0
                self.alpha = self.alpha_max

            pygame.draw.circle(bg_alpha, (255,255,255, self.alpha), self.pos, round(self.r), round(self.w))

            self.r += self.out_speed
            if self.r >= self.avg_r:
                if self.w <= 2:
                    self.w = 2
                    self.alpha = 55
                else:
                    self.w -= self.out_speed
                    self.alpha -= ( 255 * (self.out_speed) ) / self.avg_r
            else:
                self.w += self.out_speed

            self.out_speed += self.acce

            if self.alpha < 0:
                self.alpha = 0

            if self.r >= self.avg_r * 3 and self.Fsec_i > 0:
                self.alpha = self.alpha_max
                self.active = False
                self.Fsec_i = -1
                self.out_speed = 1.5

            self.Fsec_i += 1

M = 600
p = 30
acce = 0.005
class Scatter:
    def __init__(self, pos, colors):
        self.active = True
        self.x = pos[0]
        self.y = pos[1]

        self.particles= []
        self.masses = []
        self.mass = 0

        self.alpha = 255
        self.period = 0

        self.colors = colors

        while self.mass < M:
            range_choice = random.randint(1,2)
            if range_choice == 1:
                m = random.randint(9,21)
            elif range_choice == 2:
                m = random.randint(34,42)
            self.masses.append(m)
            self.mass += m

        self.mass_n = len(self.masses)
        self.i = 0
        for mass in self.masses:
            angle = (360 / self.mass_n) * self.i
            self.i += 1
            d = p / mass

            vel = [round( cos(radians(angle)) * d * 1 ), round( sin(radians(angle)) * d * 1 )]

            color = random.choice(self.colors)

            self.particles.append( [ [self.x, self.y], vel, round(sqrt(mass / pi)), color] )

    def expand(self, bg_alpha):
        if self.active:
            for ptc in self.particles:
                ptc[0][0] += round(ptc[1][0])
                ptc[0][1] += round(ptc[1][1])
                
                if ptc[1][0] > 0:
                    ptc[1][0] += acce
                elif ptc[1][0] < 0:
                    ptc[1][0] -= acce
                if ptc[1][1] > 0:
                    ptc[1][1] += acce
                elif ptc[1][1] < 0:
                    ptc[1][1] -= acce

                pygame.draw.circle(bg_alpha, (ptc[3][0], ptc[3][1], ptc[3][2], self.alpha), ( round(ptc[0][0]), round(ptc[0][1])), ptc[2])
            
            self.alpha -= 2
            self.period += display.FPSsec
    
            if self.period >= 0.5:
                self.active = False





def action(explosions, bg_alpha):
    for explode in explosions:
        if not explode.active:
            explosions.remove(explode)

    for explode in explosions:
        explode.expand(bg_alpha)