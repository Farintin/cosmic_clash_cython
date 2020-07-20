import pygame
import display
import random
from math import *



cdef float FPSsec = display.FPSsec

cdef class Flame:
    cdef tuple pt, acce, vel, c1, c2, c3, color_set, color
    cdef list sizes, particles, pos, ptc
    cdef float velx1, velx2, vely, redux_rate, velx, size, timer

    def __init__(self, dict prop, dict props):
        self.pt = prop['pt']
        self.acce = prop['acce']

        self.sizes = list(props['rad_range'])
        self.vel = props['vel']
        self.velx1 = self.vel[0]['min']
        self.velx2 = self.vel[0]['max']
        self.vely = self.vel[1]
        self.redux_rate = props['redux_rate']

        self.particles = []
        self.timer = 0

        c1 = (random.randrange(props['const_color_range'][0][0], props['const_color_range'][0][1]), random.randrange(props['const_color_range'][1][0], props['const_color_range'][1][1]), random.randrange(props['const_color_range'][2][0], props['const_color_range'][2][1]), props['alpha_frac'] * 255)
        c2 = (random.randrange(props['color_range'][0][0], props['color_range'][0][1]), random.randrange(props['color_range'][1][0], props['color_range'][1][1]), random.randrange(props['color_range'][2][0], props['color_range'][2][1]), props['alpha_frac'] * 255)
        c3 = (random.randrange(props['color_range'][0][0], props['color_range'][0][1]), random.randrange(props['color_range'][1][0], props['color_range'][1][1]), random.randrange(props['color_range'][2][0], props['color_range'][2][1]), props['alpha_frac'] * 255)
        self.color_set = (c1, c2, c3)

    cdef bint combust
    def combust(self, object bg_alpha, list lock_pos, tuple pt = ()):
        if pt:
            self.pt = pt

        self.pos = [lock_pos[0] + self.pt[0], lock_pos[1] + self.pt[1]]
        self.velx = (random.randint(0, round(2 * self.velx2 * 10)) / 10) + self.velx1
        self.size = random.choice(self.sizes)
        
        if self.timer >= 3 * FPSsec:
            self.particles.append([ self.pos, [self.velx, self.vely], self.size])
            self.timer = 0
        else:
            self.timer += FPSsec

        for ptc in self.particles:
            ptc[0][0] += ptc[1][0]
            ptc[0][1] += ptc[1][1]
            ptc[2] -= self.redux_rate
            ptc[1][1] += self.acce[1]
            
            color = random.choice(self.color_set)

            pygame.draw.circle(bg_alpha, color, [int(ptc[0][0]), int(ptc[0][1])], int(ptc[2]))
            if ptc[2] <= 0:
                self.particles.remove(ptc)


class Coma:
    def __init__(self, dict prop, dict props):
        self.pt = prop['pt']
        self.ax = prop['ax']

        self.sizes = list(props['rad_range'])
        self.redux_rate = props['redux_rate']

        self.vel = props['vel']
        self.velx1 = self.vel[0]['min']
        self.velx2 = self.vel[0]['max']
        self.vely = self.vel[1]

        self.colors = props['colors']

        self.particles = []

    def outgas(self, bg_obj, bg_alpha, tuple lock_pos):
        self.pos = [lock_pos[0] + self.pt[0], lock_pos[1] + self.pt[1]]

        color = random.choice(self.colors)

        self.velx = (random.randint(0, 2 * self.velx2 * 10) / 10) + self.velx1
        self.size = random.choice(self.sizes)

        self.particles.append([ self.pos, [self.velx, self.vely], self.size, color])
    
        for ptc in self.particles:
            ptc[0][0] += ptc[1][0]
            ptc[0][1] += ptc[1][1]

            ptc[2] -= self.redux_rate
            
            pygame.draw.circle(bg_alpha, ptc[3], [int(ptc[0][0]), int(ptc[0][1])], int(ptc[2]))
            if ptc[2] <= 0:
                self.particles.remove(ptc)

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

            if ptc[2] > 0:
                ptc[2] -= self.redux_rate
            else:
                ptc[2] = 0

            x = ptc[0][0]
            y = ptc[0][1]
            if x < lock_pos[0]:
                ptc[1][0] += self.ax
            elif x > lock_pos[0]:
                ptc[1][0] -= self.ax
            else:
                ptc[1][0] = 0
            
            if ptc[2] <= 0 or ptc[0][0] == lock_pos[0]:
                self.particles.remove(ptc)
                continue
            else:
                pygame.draw.circle(bg_alpha, ptc[3], [int(ptc[0][0]), int(ptc[0][1])], int(ptc[2]))

        bg_obj.blit(bg_alpha, (0,0))




class Ripple:
    def __init__(self, props):
        self.active = True

        self.out_speed = props['out_speed']
        self.acce = props['acce']

        self.stable_counter = 0

        self.avg_r = props['avg_r']
        self.r = 2
        self.w = 0
        if self.avg_r > 19:
            self.final_w = 2
        else:
            self.final_w = 1
        self.color = props['color']
        self.color_decrement = props['color_decrement']

    def expand(self, bg_alpha):
        if self.active:
            pygame.draw.circle(bg_alpha, self.color, self.pos, round(self.r), round(self.w))

            self.r += self.out_speed
            if self.r >= self.avg_r:
                if self.w <= self.final_w:
                    self.w = self.final_w
                else:
                    self.w -= 2
                    for i in range(0, len(self.color)):
                        self.color[i] -= self.color_decrement[i]
                        if self.color[i] < 0:
                            self.color[i] = 0
            else:
                self.w += self.out_speed

            self.out_speed += self.acce

            if self.r >= self.avg_r * 3:
                self.r = self.avg_r * 3
                self.stable_counter += FPSsec

                if self.stable_counter >= 0.5:
                    self.active = False

    def set_pos(self, pos):
        self.pos = (round(pos[0]), round(pos[1]))


#M = 600
p = 30
#acce = 0.005
class Scatter:
    def __init__(self, props):
        self.active = True

        self.colors = props['colors']
        self.M = props['M']
        self.acce = props['acce']

        self.particles= []
        self.masses = []
        self.mass = 0

        self.period = 0


    def expand(self, bg_alpha):
        if self.active:
            for ptc in self.particles:
                ptc[0][0] += round(ptc[1][0])
                ptc[0][1] += round(ptc[1][1])
                
                if ptc[1][0] > 0:
                    ptc[1][0] += self.acce
                elif ptc[1][0] < 0:
                    ptc[1][0] -= self.acce
                if ptc[1][1] > 0:
                    ptc[1][1] += self.acce
                elif ptc[1][1] < 0:
                    ptc[1][1] -= self.acce

                if ptc[3][3] < 0:
                    ptc[3][3] = 0

                pygame.draw.circle(bg_alpha, ptc[3], (round(ptc[0][0]), round(ptc[0][1])), ptc[2])

                if ptc[3][3] > 0:
                    ptc[3][3] -= 0.5
                    ptc[3][3] = round(ptc[3][3])

            self.period += FPSsec
    
            if self.period >= 0.5:
                self.active = False
    
    def gen(self):
        while self.mass < self.M:
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

            self.particles.append( [[self.x, self.y], vel, round(sqrt(mass / pi)) + 1, color] )

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]





def action(explosions, bg_alpha):
    for explode in explosions:
        if not explode.active:
            explosions.remove(explode)

    for explode in explosions:
        explode.expand(bg_alpha)