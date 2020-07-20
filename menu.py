import sys, random
import pygame
from pygame.locals import *
import pygame.gfxdraw
import display, colors, celest, level
from dom import *


FPSClock = pygame.time.Clock()

vw = display.view_width
vh = display.view_height
vc = display.view_center
        

bgImg = pygame.image.load('img/menu_bg.png')
bgImg_rect = bgImg.get_rect()

bgImgAspectDim = (bgImg_rect.width, bgImg_rect.height)
bgImg = pygame.transform.scale( bgImg, (round((bgImgAspectDim[0] / bgImgAspectDim[1]) * vh), vh) )
bgImg_rect = bgImg.get_rect()

bgImg_rect.midtop = (vc[0], 0)

TRUE = -1
FALSE = 0


def run(bg, bg_alpha, Home = TRUE, Levels = FALSE):
    global Option
    Quit = Option = FALSE
    # Buttons
    playBtn = Rect((vw * 0.1, vh * 0.83, vw * 0.7, vh * 0.09), bgColor = (255,255,255,55))
    playBtn.rect.centerx = vc[0]
    playBtn.borderWidth(1)
    playBtn.addChild( Text('PLAY', color = (225,225,225)) )
    playBtn.center_children()

    optionBtn = Rect((playBtn.rect.left, playBtn.rect.top - playBtn.rect.height - 20, playBtn.rect.width, playBtn.rect.height), bgColor = (255,255,255,55),)
    optionBtn.borderWidth(1)
    optionBtn.addChild( Text('Option', color = (225,225,225)) )
    optionBtn.center_children()

    quitBtn = Rect((vw * 0.02, vw * 0.02, vw * 0.1, vw * 0.1), bgColor = (255,255,255,155))
    quitBtn.borderWidth(1)
    quitBtn.addChild( Text('Quit', color = (225,225,225), font_size = 12) )
    quitBtn.center_children()

    settingBtn = Rect((0, 0, quitBtn.rect.width, quitBtn.rect.width), bgColor = (255,255,255,155))
    settingBtn.rect.right = vw - vw * 0.02
    settingBtn.rect.top = quitBtn.rect.top
    settingBtn.borderWidth(1)
    settingBtn.addChild( Text('Set', color = (225,225,225), font_size = 12) )
    settingBtn.center_children()

    btns = (playBtn, optionBtn, quitBtn, settingBtn)

    MouseMotion = False
    Click = False
    while Home:
        mx, my = pygame.mouse.get_pos()

        bg.blit(bgImg, bgImg_rect.topleft)

        bg_alpha.fill((0,0,0,0))
        

        if MouseMotion:
            for btn in btns:
                handler1 = Handler( func = bgColor, value = {'bgColor': (255,255,255,255)} )
                handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
                handler3 = Handler( func = color, value = {'color': (15,15,15,255)}, elem = btn.getChildBy('name', 'text') )
                btn.onHover([handler1, handler2, handler3], (mx, my))
        playBtn.show(bg_alpha)
        optionBtn.show(bg_alpha)
        quitBtn.show(bg_alpha)
        settingBtn.show(bg_alpha)

        if Click:
            handler1 = Handler( value = [Quit] )
            Quit, = quitBtn.onClick([handler1], (mx_up, my_up))[0]

            handler1 = Handler( value = [Option] )
            Option, = optionBtn.onClick([handler1], (mx_up, my_up))[0]

            handler1 = Handler( value = [Levels] )
            Levels, = playBtn.onClick([handler1], (mx_up, my_up))[0]

            Click = False

        egress(Quit)
        option(bg, bg_alpha)
        Home, Levels = levels(bg, bg_alpha, Home, Levels)


        bg.blit(bg_alpha, (0,0))



        for event in pygame.event.get(): # Event loop block
            kind = event.type

            if kind == QUIT:
                pygame.quit()
                sys.exit()
            
            if kind == MOUSEMOTION:
                MouseMotion = True
            else:
                MouseMotion = False

            if kind == MOUSEBUTTONUP:
                mx_up, my_up = event.pos
                Click = True


        pygame.display.update()
        FPSClock.tick(15)

    return level.selected


def option(bg, bg_alpha):
    global Option, Crafts, Items, Controls
    Crafts = Items = Controls = FALSE

    backBtn = Rect((vw * 0.02, vw * 0.02, vw * 0.1, vw * 0.1), bgColor = (255,255,255,155))
    backBtn.borderWidth(1)
    backBtn.addChild( Text('Back', color = (225,225,225), font_size = 12) )
    backBtn.center_children()

    controlsBtn = Rect((vw * 0.1, vh * 0.83, vw * 0.8, vh * 0.09), bgColor = (255,255,255,55))
    controlsBtn.borderWidth(1)
    controlsBtn.addChild( Text('Controls', color = (225,225,225)) )
    controlsBtn.center_children()

    itemsBtn = Rect((controlsBtn.rect.left, controlsBtn.rect.top - controlsBtn.rect.height - 20, controlsBtn.rect.width, controlsBtn.rect.height), bgColor = (255,255,255,55))
    itemsBtn.borderWidth(1)
    itemsBtn.addChild( Text('Items', color = (225,225,225)) )
    itemsBtn.center_children()

    craftsBtn = Rect((itemsBtn.rect.left, itemsBtn.rect.top - itemsBtn.rect.height - 20, itemsBtn.rect.width, itemsBtn.rect.height), bgColor = (255,255,255,55))
    craftsBtn.borderWidth(1)
    craftsBtn.addChild( Text('Crafts', color = (225,225,225)) )
    craftsBtn.center_children()

    btns = (controlsBtn, itemsBtn, craftsBtn, backBtn)

    MouseMotion = False
    Click = False
    while Option:
        mx, my = pygame.mouse.get_pos()

        bg.blit(bgImg, bgImg_rect.topleft)

        bg_alpha.fill((0,0,0,0))
        
        if MouseMotion:
            for btn in btns:
                handler1 = Handler( func = bgColor, value = {'bgColor': (255,255,255,255)} )#, (255,255,255,255))
                handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
                handler3 = Handler( func = color, value = {'color': (15,15,15,255)}, elem = btn.getChildBy('name', 'text') )
                btn.onHover([handler1, handler2, handler3], (mx, my))
        craftsBtn.show(bg_alpha)
        itemsBtn.show(bg_alpha)
        controlsBtn.show(bg_alpha)
        backBtn.show(bg_alpha)

        if Click:
            handler1 = Handler( value = [Crafts] )
            Crafts, = craftsBtn.onClick([handler1], (mx_up, my_up))[0]

            handler1 = Handler( value = [Items] )
            Items, = itemsBtn.onClick([handler1], (mx_up, my_up))[0]

            handler1 = Handler( value = [Controls] )
            Controls, = controlsBtn.onClick([handler1], (mx_up, my_up))[0]

            handler1 = Handler( value = [Option] )
            Option, = backBtn.onClick([handler1], (mx_up, my_up))[0]

            Click = False

        crafts(bg, bg_alpha)
        items(bg, bg_alpha)
        controls(bg, bg_alpha)

        bg.blit(bg_alpha, (0,0))

        for event in pygame.event.get(): # Event loop block
            kind = event.type

            if kind == QUIT:
                pygame.quit()
                sys.exit()

            if kind == MOUSEMOTION:
                MouseMotion = True
            else:
                MouseMotion = False

            if kind == MOUSEBUTTONUP:
                mx_up, my_up = event.pos
                Click = True


        pygame.display.update()
        FPSClock.tick(15)


def crafts(bg, bg_alpha):
    global Crafts

    backBtn = Rect((vw * 0.02, vw * 0.02, vw * 0.1, vw * 0.1), bgColor = (255,255,255,155))
    backBtn.borderWidth(1)
    backBtn.addChild( Text('Back', color = (225,225,225), font_size = 12) )
    backBtn.center_children()

    header = Text('Crafts', color = (225,225,225))
    header.rect.center = vc
    
    
    MouseMotion = False
    Click = False
    while Crafts:
        mx, my = pygame.mouse.get_pos()

        bg.blit(bgImg, bgImg_rect.topleft)

        bg_alpha.fill((0,0,0,0))
        

        if MouseMotion:
            handler1 = Handler( func = bgColor, value = {'bgColor': (255,255,255,255)} )
            handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
            handler3 = Handler( func = color, value = {'color': (15,15,15,255)}, elem = backBtn.getChildBy('name', 'text') )
            backBtn.onHover([handler1, handler2, handler3], (mx, my))
        backBtn.show(bg_alpha)
        header.show(bg_alpha)


        if Click:
            handler1 = Handler( value = [Crafts] )
            Crafts, = backBtn.onClick([handler1], (mx_up, my_up))[0]

            Click = False

        bg.blit(bg_alpha, (0,0))

        for event in pygame.event.get(): # Event loop block
            kind = event.type

            if kind == QUIT:
                pygame.quit()
                sys.exit()

            if kind == MOUSEMOTION:
                MouseMotion = True
            else:
                MouseMotion = False

            if kind == MOUSEBUTTONUP:
                mx_up, my_up = event.pos
                Click = True


        pygame.display.update()
        FPSClock.tick(15)
    

def items(bg, bg_alpha):
    global Items

    backBtn = Rect((vw * 0.02, vw * 0.02, vw * 0.1, vw * 0.1), bgColor = (255,255,255,155))
    backBtn.borderWidth(1)
    backBtn.addChild( Text('Back', color = (225,225,225), font_size = 12) )
    backBtn.center_children()

    header = Text('Items', color = (225,225,225))
    header.rect.center = vc

    MouseMotion = False
    Click = False
    while Items:
        mx, my = pygame.mouse.get_pos()

        bg.blit(bgImg, bgImg_rect.topleft)

        bg_alpha.fill((0,0,0,0))

        if MouseMotion:
            handler1 = Handler( func = bgColor, value = {'bgColor': (255,255,255,255)} )
            handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
            handler3 = Handler( func = color, value = {'color': (15,15,15,255)}, elem = backBtn.getChildBy('name', 'text') )
            backBtn.onHover([handler1, handler2, handler3], (mx, my))
        backBtn.show(bg_alpha)
        header.show(bg_alpha)
        
        if Click:
            handler1 = Handler( value = [Items] )
            Items, = backBtn.onClick([handler1], (mx_up, my_up))[0]

            Click = False

        bg.blit(bg_alpha, (0,0))

        for event in pygame.event.get(): # Event loop block
            kind = event.type

            if kind == QUIT:
                pygame.quit()
                sys.exit()

            if kind == MOUSEMOTION:
                MouseMotion = True
            else:
                MouseMotion = False

            if kind == MOUSEBUTTONUP:
                mx_up, my_up = event.pos
                Click = True


        pygame.display.update()
        FPSClock.tick(15)


def controls(bg, bg_alpha):
    global Controls

    backBtn = Rect((vw * 0.02, vw * 0.02, vw * 0.1, vw * 0.1), bgColor = (255,255,255,155))
    backBtn.borderWidth(1)
    backBtn.addChild( Text('Back', color = (225,225,225), font_size = 12) )
    backBtn.center_children()

    header = Text('Controls', color = (225,225,225))
    header.rect.center = vc

    MouseMotion = False
    Click = False
    while Controls:
        mx, my = pygame.mouse.get_pos()

        bg.blit(bgImg, bgImg_rect.topleft)

        bg_alpha.fill((0,0,0,0))
        if MouseMotion:
            handler1 = Handler( func = bgColor, value = {'bgColor': (255,255,255,255)} )
            handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
            handler3 = Handler( func = color, value = {'color': (15,15,15,255)}, elem = backBtn.getChildBy('name', 'text') )
            backBtn.onHover([handler1, handler2, handler3], (mx, my))
        backBtn.show(bg_alpha)
        header.show(bg_alpha)
        
        if Click:
            handler1 = Handler( value = [Controls] )
            Controls, = backBtn.onClick([handler1], (mx_up, my_up))[0]

            Click = False

        bg.blit(bg_alpha, (0,0))

        for event in pygame.event.get(): # Event loop block
            kind = event.type

            if kind == QUIT:
                pygame.quit()
                sys.exit()
            
            if kind == MOUSEMOTION:
                MouseMotion = True
            else:
                MouseMotion = False

            if kind == MOUSEBUTTONUP:
                mx_up, my_up = event.pos
                Click = True


        pygame.display.update()
        FPSClock.tick(15)


def levels(bg, bg_alpha, Home, Levels):
    backBtn = Rect((vw * 0.02, vw * 0.02, vw * 0.1, vw * 0.1), bgColor = (255,255,255,155))
    backBtn.borderWidth(1)
    backBtn.addChild( Text('Back', color = (225,225,225), font_size = 12) )
    backBtn.center_children()

    scrollFrame = Rect((vw - 8, 0, 8, vh), bgColor = (105,105,105,155))
    scrollBar = Rect((0,0, scrollFrame.rect.width,72), bgColor = (255,255,255,255))
    scrollBar.rect.bottomleft = scrollFrame.rect.bottomleft
    scrollFrame.addChild( scrollBar )

    
    stages, gridFrame, grid_h = level.set_grids()
    gridFrame.rect.top = -grid_h + vh
    i = 0
    for obj in gridFrame.children:
        obj.rect.centery = gridFrame.rect.top + obj.offSet[1]
        obj.center_children()

        stages[i].update()
        if stages[i].unlocked:
            '''obj.bg_color((255,45,255,225))
            obj.getChildBy('name', 'circle').bg_color((255,45,255,225))
            child_text = obj.getChildBy('name', 'text')
            child_text.default['color'] = child_text.setColor((255,255,255))'''
            obj.default['border_width'] = obj.border_width = 0
            obj.bg_color((255,45,255,225))
            obj.default['bg'] = obj.bg = True

            obj.getChildBy('name', 'circle').bg_color((255,255,255,255))
            child_text = obj.getChildBy('name', 'text')
            child_text.default['color'] = child_text.setColor((255,255,255))
            
        if stages[i].current:
            obj.default['border_width'] = obj.border_width = 0
            obj.bg_color((255,255,0,230))
            obj.default['bg'] = obj.bg = True

            obj.getChildBy('name', 'circle').bg_color((255,255,255,255))
            child_text = obj.getChildBy('name', 'text')
            child_text.default['color'] = child_text.setColor((255,255,255))

            current_lvl_dom = obj
            current_lvl = stages[i]
        i += 1

    MouseMotion = False
    Click = False
    Scroll_dy = 0
    MouseHeld = False
    MouseHeld_counter = 0
    ScrollBarFocus = FALSE
    scrollRule = [vh - scrollBar.rect.height / 2, 0 + scrollBar.rect.height / 2]
    scrollRule.append( scrollRule[0] - scrollRule[1] )
    scrollBarPercent = 0
    loop_counter = 0
    while Levels:
        mx, my = pygame.mouse.get_pos()
        bg.blit(bgImg, bgImg_rect.topleft)
        #bg_alpha.fill((0,0,0,155))

        if Scroll_dy:
            if Scroll_dy > 0 and gridFrame.rect.top >= 0:
                Scroll_dy = 0
                gridFrame.rect.top = 0
            elif Scroll_dy < 0 and gridFrame.rect.bottom <= vh:
                Scroll_dy = 0
                gridFrame.rect.bottom = vh

            gridFrame.rect.top += Scroll_dy 
            for obj in gridFrame.children:
                obj.rect.centery = gridFrame.rect.top + obj.offSet[1]
                obj.center_children()

            scrollBar.rect.centery = -(((gridFrame.rect.top + (grid_h - vh)) / (grid_h - vh)) * scrollRule[2]) + scrollRule[0]

        if loop_counter == 0:
            ScrollBarFocus = TRUE
            #Tpos = vh - round(vh * 0.15)
            
        if ScrollBarFocus:
            if loop_counter == 0:
                Tposy = vh - round(vh * 0.15)

                gridFrame.rect.top = -(grid_h - vh)
                gridFrame.rect.top += Tposy - current_lvl_dom.rect.centery
                for obj in gridFrame.children:
                    obj.rect.centery = gridFrame.rect.top + obj.offSet[1]
                    obj.center_children()

                scrollBar.rect.centery = -(((gridFrame.rect.top + (grid_h - vh)) / (grid_h - vh)) * scrollRule[2]) + scrollRule[0]
                ScrollBarFocus = FALSE
            else:
                scrollBar.rect.centery = my
                if scrollBar.rect.top <= 0:
                    scrollBar.rect.top = 0
                elif scrollBar.rect.bottom >= vh:
                    scrollBar.rect.bottom = vh
                
                scrollBarPercent = ( abs(scrollBar.rect.centery - scrollRule[0]) / scrollRule[2] ) * 100
                ScrollBar_dy = round( (grid_h - vh) * (scrollBarPercent / 100) )

                gridFrame.rect.top =  -((grid_h - vh) - ScrollBar_dy)
                for obj in gridFrame.children:
                    obj.rect.centery = gridFrame.rect.top + obj.offSet[1]
                    obj.center_children()
        else:
            ScrollBar_dy = 0
        

        if MouseMotion:
            handler1 = Handler( func = bgColor, value = {'bgColor': (255,255,255,255)} )
            handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
            handler3 = Handler( func = color, value = {'color': (15,15,15,255)}, elem = backBtn.getChildBy('name', 'text') )
            backBtn.onHover([handler1, handler2, handler3], (mx, my))

            i = 0
            for lvl in gridFrame.children:
                handler1 = Handler( func = bg_state, value = {'bg': True} )
                if stages[i].unlocked:
                    handler2 = Handler( func = bgColor, value = {'bgColor': (45,255,45,225)} )
                else:
                    handler2 = Handler( func = bgColor, value = {'bgColor': (255,0,0,255)} )
                handler3 = Handler( func = bgColor, value = {'bgColor': (255,255,255,255)}, elem = lvl.getChildBy('name', 'circle') )
                handler4 = Handler( func = color, value = {'color': (255,255,255)}, elem = lvl.getChildBy('name', 'text') )

                lvl.onHover([handler1, handler2, handler3, handler4], (mx, my))
                i += 1


        gridFrame.show(bg_alpha)
        level.show_grids(bg_alpha, gridFrame)
        backBtn.show(bg_alpha)
        scrollFrame.show(bg_alpha)


        if MouseHeld:
            if MouseHeld_counter == 0:
                handler1 = Handler( value = [ScrollBarFocus] )
                ScrollBarFocus, = scrollBar.onClick([handler1], (mx_up, my_up))[0]
                
            MouseHeld_counter += 1
        else:
            MouseHeld_counter = 0
            ScrollBarFocus = FALSE

        if Click:
            handler1 = Handler( value = [Levels] )
            Levels, = backBtn.onClick([handler1], (mx_up, my_up))[0]
            
            i = 0
            for lvl in gridFrame.children:
                '''if stages[i].unlocked:
                    handler1 = Handler( func = moveBack_moveOn, value = [Home, Levels] )
                    Home, Levels = lvl.onClick([handler1], (mx_up, my_up))[0]

                    if lvl.clicked:
                        #print('Clicked')
                        level.selected = stages[i]
                        lvl.clicked = False
                        break'''
                handler1 = Handler( func = moveBack_moveOn, value = [Home, Levels] )
                Home, Levels = lvl.onClick([handler1], (mx_up, my_up))[0]

                if lvl.clicked:
                    #print('Clicked')
                    level.selected = stages[i]
                    lvl.clicked = False
                    break
                i += 1
            Click = False


        bg.blit(bg_alpha, (0,0))

        if loop_counter < 2:
            loop_counter += 1


        for event in pygame.event.get(): # Event loop block
            kind = event.type

            if kind == QUIT:
                pygame.quit()
                sys.exit()

            if kind == MOUSEMOTION:
                MouseMotion = True
            else:
                MouseMotion = False

            if kind == MOUSEBUTTONDOWN:
                mx_up, my_up = event.pos
                MouseHeld = True

            if kind == MOUSEBUTTONUP:
                mx_up, my_up = event.pos
                Click = True
                MouseHeld = False

            if kind == KEYDOWN:
                key = event.key
                if key == K_UP:
                    Scroll_dy = vh * 0.05
                if key == K_DOWN:
                    Scroll_dy = -vh * 0.05
            
            if kind == KEYUP:
                key = event.key
                if key == K_UP or key == K_DOWN:
                    Scroll_dy = 0


        pygame.display.update()
        FPSClock.tick(15)
    
    return Home, Levels