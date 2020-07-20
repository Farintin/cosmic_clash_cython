import pygame, sys
import pygame.gfxdraw
import display


vw = display.view_width
vh = display.view_height


class Text:
    def __init__(self, text, color = (255,255,255,255), font_size = 16, font_type = 'freesansbold.ttf'):
        self.obj_type = 'surf'
        self.name = 'text'
        self.text = text
        self.color = color
        self.font = pygame.font.Font(font_type, font_size)
        self.render = self.font.render(self.text, True, self.color)
        self.rect = self.render.get_rect()

        self.default = {'color': self.color, 'font_size': font_size, 'center': self.rect.center}
    
    def setColor(self, color = (255,255,255,255)):
        if color != (255,255,255,255):
            self.color = color
        self.render = self.font.render(self.text, True, self.color)
        self.rect = self.render.get_rect()

        self.rect.center = self.default['center']

        return self.color

    def show(self, bg_alpha):
        bg_alpha.blit(self.render, self.rect)



class Container:
    def __init__(self, color):
        self.obj_type = 'draw'
        self.children = []

        self.bgColor = color
        self.border_width = 0
        self.visible = True

        self.focusCounter = 0

        self.default = {'bgColor': self.bgColor, 'border_width': self.border_width}

        self.click = False
        self.clicked = False
    
    def addChild(self, obj):
        self.children.append(obj)
    
    def addChildren(self, objs):
        for obj in objs:
            self.children.append(obj)

    def borderWidth(self, w = None):
        if w != None:
            self.default['border_width'] = self.border_width = w
        if not self.visible:
            self.bgColor = (255,255,255,0)

        return self.border_width

    def bg_color(self, color = None):
        if color:
            self.default['bgColor'] = self.bgColor = color
        return self.bgColor

    def center_child(self, child):
        child.default['center'] = child.rect.center = self.rect.center

    def center_children(self):
        for child in self.children:
            child.default['center'] = child.rect.center = self.rect.center
    
    def getChildBy(self, attr, value):
        for child in self.children:
            if attr == 'name' and child.name == value:
                return child

    def nav(self, dx, dy):
        self.rect.left += dx
        self.rect.top += dy
        for child in self.children:
            child.rect.left += dx
            child.rect.top += dy

    def onHover(self, handlers, pos):
        if self.name == 'rect':
            if (pos[0] in range(self.rect.left, self.rect.left + self.rect.width)) and (pos[1] in range(self.rect.top, self.rect.top + self.rect.height)):
                hover = True
            else:
                hover = False
        elif self.name == 'circle':
            if pygame.sprite.collide_circle(CursorTarget(pos), self):
                hover = True
            else:
                hover = False

        if hover:
            self.focusCounter += 1
            if self.focusCounter == 1:
                for handler in handlers:
                    handler.run(self)
        else:
            if self.focusCounter != 0:
                for handler in handlers:
                    handler.reset(self)
                self.focusCounter = 0

    def onClick(self, handlers, pos):
        bools = []
        if self.name == 'rect':
            if (pos[0] in range(self.rect.left, self.rect.left + self.rect.width)) and (pos[1] in range(self.rect.top, self.rect.top + self.rect.height)):
                self.click = True
                self.clicked = True
            else:
                self.click = False
        elif self.name == 'circle':
            if pygame.sprite.collide_circle(CursorTarget(pos), self):
                self.click = True
                self.clicked = True
            else:
                self.click = False
        
        if self.click:
            for handler in handlers:
                bools.append(handler.switch(self))
            #print(self.getChildBy('name', 'text').text, bools)
        else:
            for handler in handlers:
                bools.append(handler.passOn(self))
        return bools

    def show(self, bg_alpha):
        if self.name == 'rect':
            pygame.draw.rect(bg_alpha, self.bgColor, self.rect, self.border_width)
        elif self.name == 'circle':
            if self.bg:
                pygame.gfxdraw.filled_circle(bg_alpha, self.rect.centerx, self.rect.centery, self.radius, self.bgColor)
            else:
                pygame.gfxdraw.circle(bg_alpha, self.rect.centerx, self.rect.centery, self.radius, self.bgColor)

        for child in self.children:
            child.show(bg_alpha)


class Rect(Container):
    def __init__(self, rect, bgColor):
        super().__init__(bgColor)
        self.name = 'rect'
        self.rect = pygame.Rect(rect)

class Poly(Rect):
    def __init__(self, rect, bgColor):
        super().__init__(rect, bgColor)
        self.name = 'poly'

    def set_pts(self, pts):
        self.pts = pts

    def show(self, bg_alpha):
        pygame.draw.polygon(bg_alpha, self.bgColor, self.pts)




surf = pygame.Surface((vw, vh))
surf = surf.convert_alpha()
surf.set_colorkey((0,0,0,0))
class Circle(Container):
    def __init__(self, bgColor, rad, center):
        super().__init__(bgColor)
        self.name = 'circle'

        self.surf = surf
        self.radius = rad
        self.rect = pygame.draw.circle(self.surf, (255,255,255), (self.radius, self.radius), self.radius)
        self.center = self.rect.center = center

        self.bg = False

        self.default['radius'] = self.radius
        self.default['bg'] = self.bg


class Handler:
    def __init__(self, func = None, value = False, elem = None):
        self.elem = elem
        self.func = func
        self.value = value

    def run(self, elem):
        if not self.elem:
            self.elem = elem
        return self.func(self.elem, self.value)

    def reset(self, elem):
        if not self.elem:
            self.elem = elem
        self.func(self.elem, self.elem.default)
    
    def passOn(self, elem):
        if not self.elem:
            self.elem = elem
        return passOn(self.elem, self.value)
    
    def switch(self, elem):
        if not self.elem:
            self.elem = elem
        if self.func:
            return self.func(self.elem, self.value)
        else:
            return switch(self.elem, self.value)



class CursorTarget:
    def __init__(self, pos):
        self.surf = surf
        self.radius = 1
        self.rect = pygame.draw.circle(self.surf, (255,255,255), pos, self.radius)





###### Events
def bg_state(elem, data):#boolean):
    elem.bg = data['bg']

def bgColor(elem, data):
    elem.bgColor = data['bgColor']

def borderWidth(elem, data):
    elem.border_width = data['border_width']

def color(elem, data):
    color = data['color']
    if elem.name == 'text':
        elem.setColor(color)
    else:
        elem.color = color

def egress(Quit):
    if Quit:
        pygame.quit()
        sys.exit()

def moveBack_moveOn(elem, Whiles):
    bools = []
    for While in Whiles:
        bools.append(0)
    return bools

def switch(elem, Whiles):
    bools = []
    for While in Whiles:
        bools.append((While + 1) * -1)
    return bools

def passOn(elem, Whiles):
    bools = []
    for While in Whiles:
        bools.append(While)
    return bools