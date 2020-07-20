import pygame
import pygame.gfxdraw
import random
import colors

class Dot:
    def __init__(self, kind, pos, color):
        self.kind  = kind
        self.pos = pos
        self.color = color


class Circle(Dot):
    def __init__(self, kind, pos, color):
        super().__init__(kind, pos, color)
        self.radii = range(1, random.randrange(2,4))
        radii_len = len(self.radii)

        '''self.timer = 0
        self.time = self.tquata = 1 / random.randrange(720, 721)'''
        self.timer = 1 / random.randrange(10, 121)
        self.time = self.timer

        self.static_i = self.color['static_index']
        self.color = self.color['color']
        self.colors = []
        self.dym_color = [self.color[0], self.color[1], self.color[2]]
        self.chromes_step = []

        if self.static_i:
            for index in range(0,3):
                chrome = self.dym_color[index]

                if index == self.static_i:
                    self.chromes_step.append(0)
                else:
                    if chrome == 255:
                        self.chromes_step.append(255 / len(self.radii))
                        self.dym_color[index] = 0
                    else:
                        self.chromes_step.append((255 - self.dym_color[index]) / len(self.radii))
        else:
            for index in range(0,3):
                chrome = self.dym_color[index]
                if chrome == 255:
                    self.chromes_step.append(255 / len(self.radii))
                    self.dym_color[index] = 0
                else:
                    self.chromes_step.append((255 - self.dym_color[index]) / len(self.radii))

        for n in range(1, len(self.radii) + 1):
            r_plus = int(self.chromes_step[0] * n)
            g_plus = int(self.chromes_step[1] * n)
            b_plus = int(self.chromes_step[2] * n)
            self.colors.append([self.dym_color[0] + r_plus, self.dym_color[1] + g_plus, self.dym_color[2] + b_plus])

    def timing(self):
        self.time += self.timer * self.time
        '''self.time += self.time * self.timer
        self.timer += 1'''

        if int(self.time) >= len(self.radii):
            self.time = self.timer
            '''self.time = self.tquata
            self.timer = 0'''
        return int(self.time)

        
def gen(vw, vh):
    stars_min_spacing = 3*9*6*3*9
    stars_max_spacing = stars_min_spacing * 3
    stars_avg_spacing = random.randrange(stars_min_spacing, stars_max_spacing + 1)
    pixel_area = vw * vh
    n_stars = round(pixel_area / stars_avg_spacing)
    positions = []
    x_locations = []
    y_locations = []
    for i in range(n_stars):
        x = random.randrange(0, vw)
        if x in x_locations:
            while x in x_locations:
                x = random.randrange(0, vw)
        x_locations.append(x)

        y = random.randrange(0, vh)
        if y in y_locations:
            while y in y_locations:
                y = random.randrange(0, vh)
        y_locations.append(y)
        positions.append((x,y))

    min_rgb = 100
    star_count = 0
    existing_stars = []
    for x,y in positions:
        if star_count <= round(n_stars * 60/100):
            color = colors.WHITE
            existing_stars.append(Dot('dot', (x, y), color))
        elif star_count >= round(n_stars * 60/100) and star_count <= round(n_stars * 80/100):
            rgb_focus = random.randrange(0, 3)
            if rgb_focus == 0:
                r = 255
                g = random.randrange(min_rgb, 256)
                b = random.randrange(min_rgb, 256)
            elif rgb_focus == 1:
                r = random.randrange(min_rgb, 256)
                g = 255
                b = random.randrange(min_rgb, 256)
            elif rgb_focus == 2:
                r = random.randrange(min_rgb, 256)
                g = random.randrange(min_rgb, 256)
                b = 255
            color = (r,g,b)
            existing_stars.append(Dot('dot', (x, y), color))
        else:
            rgb_focus = random.randrange(0,3)
            if rgb_focus == 2:
                color = {'color': (255,255,125), 'static_index': 2}
            else:
                color = {'color': colors.WHITE, 'static_index': None}
            existing_stars.append(Circle('circle', (x, y), color))

        star_count += 1
    #print('n_stars: %i' %(n_stars), ',stars_avg_spacing: %ipx' %(stars_avg_spacing), ',stars_no._density: %f' %((n_stars / pixel_area) * 10000) + '%')
    return existing_stars



def fix(bg_obj, stars):
    dotObj = pygame.PixelArray(bg_obj)
    for star in stars:
        kind = star.kind
        x = star.pos[0]
        y = star.pos[1]
        color = star.color
        if kind == 'dot':
            dotObj[x][y] = color
        elif kind == 'circle':
            radii = star.radii
            time = star.timing()
            #print(time)
            colors = star.colors

            pygame.gfxdraw.filled_circle(bg_obj, x, y, radii[time], colors[time])
                
    del dotObj