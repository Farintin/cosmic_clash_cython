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


def run(bg, bg_alpha, Home = True, Levels = False):
    global Option, quitBtn, quitTxt, playBtn
    Quit = Option = False

    ### Dom
    body = Rect((0,0, vw, vh))
    body.id = 'body'
    body.setBound('padding', 8)
    # Buttons
    quitBtn = Rect((vw * 0.02, vw * 0.02, vw * 0.1, vw * 0.1), bg_color = (255,255,255,155))
    quitBtn.state['border_width'] = 2
    quitBtn.hovering['bg_color'] = [255,255,255,255]
    quitBtn.hovering['border_width'] = 0
    quitTxt = Text('Quit', color = (225,225,225), font_size = 12)
    quitTxt.hovering['bg_color'] = quitBtn.hovering['bg_color']
    quitTxt.hovering['color'] = [15,15,15,255]
    quitBtn.addChild(quitTxt)
    quitBtn.centerChildren()

    setBtn = Rect((0, 0, quitBtn.state['rect'].width, quitBtn.state['rect'].height), bg_color = quitBtn.state['bg_color'])
    setBtn.state['alignX'] = 'right'
    setBtn.state['border_width'] = quitBtn.state['border_width']
    setBtn.hovering['border_width'] = quitBtn.hovering['border_width']
    setBtn.hovering['bg_color'] = quitBtn.hovering['bg_color']
    setTxt = Text('Set', color = quitTxt.state['color'], font_size = 12)
    setTxt.hovering['color'] = quitTxt.hovering['color']
    setTxt.hovering['bg_color'] = quitTxt.hovering['bg_color']
    setBtn.addChild(setTxt)
    setBtn.centerChildren()

    playBtn = Rect((0,0, vw * 0.75, vh * 0.09), bg_color = (255,255,255,135))
    playBtn.setDisplay('block')
    playBtn.state['alignX'] = 'center'
    playBtn.setBound('margin', (vh - 8*2 - quitBtn.state['rect'].height * 2 - playBtn.state['rect'].height * 2 - 8, 0, 8, 0))
    playBtn.state['border_width'] = 2
    playBtn.hovering['border_width'] = 0
    playBtn.hovering['bg_color'] = quitBtn.hovering['bg_color']
    playTxt = Text('PLAY', color = (225,225,225))
    playTxt.hovering['color'] = quitTxt.hovering['color']
    playTxt.hovering['bg_color'] = quitTxt.hovering['bg_color']
    playBtn.addChild(playTxt)
    playBtn.centerChildren()

    optBtn = Rect((playBtn.state['rect'].left, playBtn.state['rect'].top - playBtn.state['rect'].height - 20, playBtn.state['rect'].width, playBtn.state['rect'].height), bg_color = playBtn.state['bg_color'])
    optBtn.setDisplay('block')
    optBtn.state['alignX'] = 'center'
    optBtn.state['border_width'] = playBtn.state['border_width']
    optBtn.hovering['bg_color'] = playBtn.hovering['bg_color']
    optBtn.hovering['border_width'] = playBtn.hovering['border_width']
    optTxt = Text('Option', color = playTxt.state['color'])
    optTxt.hovering['color'] = playTxt.hovering['color']
    optTxt.hovering['bg_color'] = playTxt.hovering['bg_color']
    optBtn.addChild(optTxt)
    optBtn.centerChildren()

    btns = [quitBtn, setBtn, playBtn, optBtn]
    body.addChildren(btns)
    body.update()
    body.render()

    MouseMotion = False
    Click = False
    while Home:
        mx, my = pygame.mouse.get_pos()
        bg.blit(bgImg, bgImg_rect)
        bg_alpha.fill((0,0,0,0))

        if MouseMotion:
            for btn in btns:
                handler1 = Handler( func = bgColor )
                handler2 = Handler( func = borderWidth )
                handler3 = Handler( func = color, elem = btn.getChildBy('name', 'text') )
                handler4 = Handler( func = bgColor, elem = btn.getChildBy('name', 'text') )
                btn.onHover([handler1, handler2, handler3, handler4], (mx, my))
        body.show(bg_alpha)
        if Click:
            handler1 = Handler( value = [Quit] )
            Quit, = quitBtn.onClick([handler1], (mx_up, my_up))[0]
            handler1 = Handler( value = [Option] )
            Option, = optBtn.onClick([handler1], (mx_up, my_up))[0]
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
    if Option:
        Crafts = Items = Controls = False
        ### Dom
        body = Rect((0,0, vw, vh))
        body.id = 'body'
        body.setBound('padding', 8)
        # Buttons
        backBtn = Rect((vw * 0.02, vw * 0.02, vw * 0.1, vw * 0.1), bg_color = (255,255,255,155))
        backBtn.state['border_width'] = 2
        backBtn.hovering['bg_color'] = [255,255,255,255]
        backBtn.hovering['border_width'] = 0
        backTxt = Text('Back', color = (225,225,225), font_size = 12)
        backTxt.hovering['bg_color'] = backBtn.hovering['bg_color']
        backTxt.hovering['color'] = [15,15,15,255]
        backBtn.addChild(backTxt)
        backBtn.centerChildren()

        itemsBtn = Rect((0, 0, vw * 0.8, vh * 0.09), bg_color = quitBtn.state['bg_color'])
        itemsBtn.setDisplay('block')
        itemsBtn.state['alignX'] = 'center'
        itemsBtn.state['border_width'] = 2
        itemsBtn.setBound('margin', (vh - 8*2 - quitBtn.state['rect'].height * 2 - playBtn.state['rect'].height * 3 - 4*4, 0, 4, 0))
        itemsBtn.hovering['bg_color'] = quitBtn.hovering['bg_color']
        itemsBtn.hovering['border_width'] = quitBtn.hovering['border_width']
        itemsTxt = Text('Items', color = (225,225,225))
        itemsTxt.hovering['color'] = quitTxt.hovering['color']
        itemsTxt.hovering['bg_color'] = quitTxt.hovering['bg_color']
        itemsBtn.addChild(itemsTxt)
        itemsBtn.centerChildren()

        craftsBtn = Rect((itemsBtn.state['rect'].left, itemsBtn.state['rect'].top - itemsBtn.state['rect'].height - 20, itemsBtn.state['rect'].width, itemsBtn.state['rect'].height), bg_color = itemsBtn.state['bg_color'])
        craftsBtn.setDisplay('block')
        craftsBtn.state['alignX'] = 'center'
        craftsBtn.state['border_width'] = itemsBtn.state['border_width']
        craftsBtn.setBound('margin', [4,0,4,0])
        craftsBtn.hovering['bg_color'] = itemsBtn.hovering['bg_color']
        craftsBtn.hovering['border_width'] = itemsBtn.hovering['border_width']
        craftsTxt = Text('Crafts', color = itemsTxt.state['color'])
        craftsTxt.hovering['color'] = itemsTxt.hovering['color']
        craftsTxt.hovering['bg_color'] = itemsTxt.hovering['bg_color']
        craftsBtn.addChild(craftsTxt)
        craftsBtn.centerChildren()

        ctrlsBtn = Rect((craftsBtn.state['rect'].left, craftsBtn.state['rect'].top - craftsBtn.state['rect'].height - 20, craftsBtn.state['rect'].width, craftsBtn.state['rect'].height), bg_color = craftsBtn.state['bg_color'])
        ctrlsBtn.setDisplay('block')
        ctrlsBtn.state['alignX'] = 'center'
        ctrlsBtn.setBound('margin', [4,0,4,0])
        ctrlsBtn.state['border_width'] = 2
        ctrlsBtn.hovering['border_width'] = 0
        ctrlsBtn.hovering['bg_color'] = craftsBtn.hovering['bg_color']
        ctrlsTxt = Text('Controls', color = (225,225,225))
        ctrlsTxt.hovering['color'] = craftsTxt.hovering['color']
        ctrlsTxt.hovering['bg_color'] = craftsTxt.hovering['bg_color']
        ctrlsBtn.addChild(ctrlsTxt)
        ctrlsBtn.centerChildren()

        btns = [backBtn, itemsBtn, craftsBtn, ctrlsBtn]
        body.addChildren(btns)
        body.update()
        body.render()

        MouseMotion = False
        Click = False
    while Option:
        mx, my = pygame.mouse.get_pos()

        bg.blit(bgImg, bgImg_rect.topleft)

        bg_alpha.fill((0,0,0,0))
        
        if MouseMotion:
            for btn in btns:
                handler1 = Handler( func = bgColor )
                handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
                handler3 = Handler( func = color, value = {'color': (15,15,15,255)}, elem = btn.getChildBy('name', 'text') )
                handler4 = Handler( func = bgColor, elem = btn.getChildBy('name', 'text') )
                btn.onHover([handler1, handler2, handler3, handler4], (mx, my))
        body.show(bg_alpha)

        if Click:
            handler1 = Handler( value = [Crafts] )
            Crafts, = craftsBtn.onClick([handler1], (mx_up, my_up))[0]

            handler1 = Handler( value = [Items] )
            Items, = itemsBtn.onClick([handler1], (mx_up, my_up))[0]

            handler1 = Handler( value = [Controls] )
            Controls, = ctrlsBtn.onClick([handler1], (mx_up, my_up))[0]

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


def items(bg, bg_alpha):
    global Items
    if Items:
        ### Dom
        body = Rect((0,0, vw, vh))
        body.id = 'body'
        body.setBound('padding', 8)
        # Buttons
        backBtn = Rect((vw * 0.02, vw * 0.02, vw * 0.1, vw * 0.1), bg_color = (255,255,255,155))
        backBtn.state['border_width'] = 2
        backBtn.hovering['bg_color'] = [255,255,255,255]
        backBtn.hovering['border_width'] = 0
        backTxt = Text('Back', color = (225,225,225), font_size = 12)
        backTxt.hovering['bg_color'] = backBtn.hovering['bg_color']
        backTxt.hovering['color'] = [15,15,15,255]
        backBtn.addChild(backTxt)
        backBtn.centerChildren()

        header = Text('ITEMS', color = (225,225,225), font_size = 24)
        header.state['alignX'] = 'center'
        header.state['alignY'] = 'center'

        btns = [backBtn]
        body.addChildren(btns + [header])
        body.update()
        body.render()

        MouseMotion = False
        Click = False
    while Items:
        mx, my = pygame.mouse.get_pos()
        bg.blit(bgImg, bgImg_rect.topleft)
        bg_alpha.fill((0,0,0,0))





        if MouseMotion:
            for btn in btns:
                handler1 = Handler( func = bgColor, value = {'bg_color': (255,255,255,255)} )
                handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
                handler3 = Handler( func = color, value = {'color': (15,15,15,255)}, elem = backBtn.getChildBy('name', 'text') )
                handler4 = Handler( func = bgColor, elem = btn.getChildBy('name', 'text') )
                btn.onHover([handler1, handler2, handler3, handler4], (mx, my))

        body.show(bg_alpha)

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


def crafts(bg, bg_alpha):
    global Crafts
    if Crafts:
        ### Dom
        body = Rect((0,0, vw, vh))
        body.id = 'body'
        body.setBound('padding', 8)
        # Buttons
        backBtn = Rect((vw * 0.02, vw * 0.02, vw * 0.1, vw * 0.1), bg_color = (255,255,255,155))
        backBtn.state['border_width'] = 2
        backBtn.hovering['bg_color'] = [255,255,255,255]
        backBtn.hovering['border_width'] = 0
        backTxt = Text('Back', color = (225,225,225), font_size = 12)
        backTxt.hovering['bg_color'] = backBtn.hovering['bg_color']
        backTxt.hovering['color'] = [15,15,15,255]
        backBtn.addChild(backTxt)
        backBtn.centerChildren()

        header = Text('CRAFTS', color = (225,225,225), font_size = 24)
        header.state['alignX'] = 'center'
        header.state['alignY'] = 'center'

        btns = [backBtn]
        body.addChildren(btns + [header])
        body.update()
        body.render()
        
        MouseMotion = False
        Click = False
    while Crafts:
        mx, my = pygame.mouse.get_pos()

        bg.blit(bgImg, bgImg_rect.topleft)

        bg_alpha.fill((0,0,0,0))
        

        if MouseMotion:
            for btn in btns:
                handler1 = Handler( func = bgColor, value = {'bg_color': (255,255,255,255)} )
                handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
                handler3 = Handler( func = color, value = {'color': (15,15,15,255)}, elem = backBtn.getChildBy('name', 'text') )
                handler4 = Handler( func = bgColor, elem = btn.getChildBy('name', 'text') )
                btn.onHover([handler1, handler2, handler3, handler4], (mx, my))

        body.show(bg_alpha)


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


def controls(bg, bg_alpha):
    global Controls
    if Controls:
        ### Dom
        body = Rect((0,0, vw, vh))
        body.id = 'body'
        body.setBound('padding', 8)
        # Buttons
        backBtn = Rect((vw * 0.02, vw * 0.02, vw * 0.1, vw * 0.1), bg_color = (255,255,255,155))
        backBtn.state['border_width'] = 2
        backBtn.hovering['bg_color'] = [255,255,255,255]
        backBtn.hovering['border_width'] = 0
        backTxt = Text('Back', color = (225,225,225), font_size = 12)
        backTxt.hovering['bg_color'] = backBtn.hovering['bg_color']
        backTxt.hovering['color'] = [15,15,15,255]
        backBtn.addChild(backTxt)
        backBtn.centerChildren()

        header = Text('CONTROLS', color = (225,225,225), font_size = 24)
        header.state['alignX'] = 'center'
        header.state['alignY'] = 'center'

        btns = [backBtn]
        body.addChildren(btns + [header])
        body.update()
        body.render()
        

        MouseMotion = False
        Click = False
    while Controls:
        mx, my = pygame.mouse.get_pos()

        bg.blit(bgImg, bgImg_rect.topleft)

        bg_alpha.fill((0,0,0,0))
        if MouseMotion:
            for btn in btns:
                handler1 = Handler( func = bgColor, value = {'bg_color': (255,255,255,255)} )
                handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
                handler3 = Handler( func = color, value = {'color': (15,15,15,255)}, elem = backBtn.getChildBy('name', 'text') )
                handler4 = Handler( func = bgColor, elem = btn.getChildBy('name', 'text') )
                btn.onHover([handler1, handler2, handler3, handler4], (mx, my))

        body.show(bg_alpha)
        
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
    if Levels:
        ### Dom
        body = Rect((0,0, vw, vh))
        body.id = 'body'
        body.setBound('padding', 8)
        # Buttons
        backBtn = Rect((vw * 0.02, vw * 0.02, vw * 0.1, vw * 0.1), bg_color = (255,255,255,155))
        backBtn.state['border_width'] = 2
        backBtn.hovering['bg_color'] = [255,255,255,255]
        backBtn.hovering['border_width'] = 0
        backTxt = Text('Back', color = (225,225,225), font_size = 12)
        backTxt.hovering['bg_color'] = backBtn.hovering['bg_color']
        backTxt.hovering['color'] = [15,15,15,255]
        backBtn.addChild(backTxt)
        backBtn.centerChildren()

        scrollFrame = Rect((vw - 8, 0, 8, vh), bg_color = (105,105,105,155))
        scrollFrame.state['display'] = 'auto'
        scrollFrame.state['border_width'] = 0
        scrollBar = Rect((0,0, scrollFrame.state['rect'].width,72), bg_color = (255,255,255,255))
        scrollBar.state['display'] = 'auto'
        scrollBar.state['border_width'] = 0
        scrollBar.state['rect'].bottomleft = scrollFrame.state['rect'].bottomleft
        scrollFrame.addChild( scrollBar )


        stages, gridFrame, grid_h = level.set_grids()
        gridFrame.state['rect'].top = -grid_h + vh
        gridFrame.id = 
        i = 0
        for obj in gridFrame.children:
            obj.state['rect'].centery = gridFrame.state['rect'].top + obj.offSet[1]
            obj.state['rect'].centerx = gridFrame.state['rect'].left + obj.offSet[0]
            obj.state['display'] = 'auto'
            obj.centerChildren(True)

            stages[i].update()
            if stages[i].unlocked:
                obj.setBgColor((255,45,255,225))
                obj.state['bg'] = True

                obj.getChildBy('name', 'circle').setBgColor((255,255,255,255))
                child_text = obj.getChildBy('name', 'text')
                child_text.state['color'] = child_text.setColor((255,255,255))
                
            if stages[i].current:
                obj.setBgColor((255,255,0,230))
                obj.state['bg'] = True

                obj.getChildBy('name', 'circle').setBgColor((255,255,255,255))
                child_text = obj.getChildBy('name', 'text')
                child_text.state['color'] = child_text.setColor((255,255,255))

                current_lvl_dom = obj
                current_lvl = stages[i]
            i += 1

        gridFrame.update()
        gridFrame.render()
        body.addChildren([backBtn, scrollFrame])
        body.update()
        body.render()
        

        MouseMotion = False
        Click = False
        Scroll_dy = 0
        MouseHeld = False
        MouseHeld_counter = 0
        ScrollBarFocus = False
        scrollRule = [vh - scrollBar.rect.height / 2, 0 + scrollBar.rect.height / 2]
        scrollRule.append( scrollRule[0] - scrollRule[1] )
        scrollBarPercent = 0
        loop_counter = 0
    while Levels:
        mx, my = pygame.mouse.get_pos()
        bg.blit(bgImg, bgImg_rect.topleft)

        if Scroll_dy:
            if Scroll_dy > 0 and gridFrame.state['rect'].top >= 0:
                Scroll_dy = 0
                gridFrame.state['rect'].top = 0
            elif Scroll_dy < 0 and gridFrame.state['rect'].bottom <= vh:
                Scroll_dy = 0
                gridFrame.state['rect'].bottom = vh

            gridFrame.state['rect'].top += Scroll_dy 
            for obj in gridFrame.children:
                obj.state['rect'].centery = gridFrame.state['rect'].top + obj.offSet[1]

            scrollBar.state['rect'].centery = -(((gridFrame.state['rect'].top + (grid_h - vh)) / (grid_h - vh)) * scrollRule[2]) + scrollRule[0]

        if loop_counter == 0:
            ScrollBarFocus = True
            
        if ScrollBarFocus:
            if loop_counter == 0:
                Tposy = vh - round(vh * 0.15)

                gridFrame.state['rect'].top = -(grid_h - vh)
                gridFrame.state['rect'].top += Tposy - current_lvl_dom.state['rect'].centery
                for obj in gridFrame.children:
                    obj.state['rect'].centery = gridFrame.state['rect'].top + obj.offSet[1]

                scrollBar.state['rect'].centery = -(((gridFrame.state['rect'].top + (grid_h - vh)) / (grid_h - vh)) * scrollRule[2]) + scrollRule[0]
                ScrollBarFocus = False
            else:
                scrollBar.state['rect'].centery = my
                if scrollBar.state['rect'].top <= 0:
                    scrollBar.state['rect'].top = 0
                elif scrollBar.state['rect'].bottom >= vh:
                    scrollBar.state['rect'].bottom = vh
                
                scrollBarPercent = ( abs(scrollBar.state['rect'].centery - scrollRule[0]) / scrollRule[2] ) * 100
                ScrollBar_dy = round( (grid_h - vh) * (scrollBarPercent / 100) )

                gridFrame.state['rect'].top =  -((grid_h - vh) - ScrollBar_dy)
                for obj in gridFrame.children:
                    obj.state['rect'].centery = gridFrame.state['rect'].top + obj.offSet[1]
        else:
            ScrollBar_dy = 0
        

        if MouseMotion:
            handler1 = Handler( func = bgColor, value = {'bg_color': (255,255,255,255)} )
            handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
            handler3 = Handler( func = color, value = {'color': (15,15,15,255)}, elem = backBtn.getChildBy('name', 'text') )
            handler4 = Handler( func = bgColor, elem = backBtn.getChildBy('name', 'text') )
            backBtn.onHover([handler1, handler2, handler3, handler4], (mx, my))

            i = 0
            for lvl in gridFrame.children:
                handler1 = Handler( func = bgState, value = {'bg': True} )
                if stages[i].unlocked:
                    handler2 = Handler( func = bgColor, value = {'bg_color': (45,255,45,225)} )
                else:
                    handler2 = Handler( func = bgColor, value = {'bg_color': (255,0,0,255)} )
                handler3 = Handler( func = bgColor, value = {'bg_color': (255,255,255,255)}, elem = lvl.getChildBy('name', 'circle') )
                handler4 = Handler( func = color, value = {'color': (255,255,255)}, elem = lvl.getChildBy('name', 'text') )

                lvl.onHover([handler1, handler2, handler3, handler4], (mx, my))
                i += 1

        '''gridFrame.show(bg_alpha)
        level.show_grids(bg_alpha, gridFrame)
        backBtn.show(bg_alpha)
        scrollFrame.show(bg_alpha)'''
        gridFrame.show(bg_alpha)
        level.show_grids(bg_alpha, gridFrame)
        body.show(bg_alpha)


        if MouseHeld:
            if MouseHeld_counter == 0:
                handler1 = Handler( value = [ScrollBarFocus] )
                ScrollBarFocus, = scrollBar.onClick([handler1], (mx_up, my_up))[0]
                
            MouseHeld_counter += 1
        else:
            MouseHeld_counter = 0
            ScrollBarFocus = False

        if Click:
            handler1 = Handler( value = [Levels] )
            Levels, = backBtn.onClick([handler1], (mx_up, my_up))[0]
            
            i = 0
            for lvl in gridFrame.children:
                handler1 = Handler( func = moveBack_moveOn, value = [Home, Levels] )
                Home, Levels = lvl.onClick([handler1], (mx_up, my_up))[0]

                if lvl.clicked:
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