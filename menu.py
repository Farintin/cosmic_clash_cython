import sys, random
import pygame
from pygame.locals import *
import pygame.gfxdraw
import display, colors, celest, level
from dom import *
import components
import controls as ctrls
import db
dbDoc = db.document


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
    global Option
    Quit = Option = False
    # Buttons
    playBtn = Rect((vw * 0.1, vh * 0.83, vw * 0.7, vh * 0.09), bgColor = (255,255,255,185))
    playBtn.rect.centerx = vc[0]
    playBtn.borderWidth(2)
    playBtn.addChild( Text('PLAY', color = (225,225,225)) )
    playBtn.center_children()

    optionBtn = Rect((playBtn.rect.left, playBtn.rect.top - playBtn.rect.height - 20, playBtn.rect.width, playBtn.rect.height), bgColor = (255,255,255,185))
    optionBtn.borderWidth(2)
    optionBtn.addChild( Text('Option', color = (225,225,225)) )
    optionBtn.center_children()

    quitBtn = Rect((8, 8, vw * 0.1, vw * 0.1), bgColor = (255,255,255,185))
    quitBtn.borderWidth(2)
    quitBtn.addChild( Text('Quit', color = (225,225,225), font_size = 12) )
    quitBtn.center_children()

    settingBtn = Rect((0, 0, quitBtn.rect.width, quitBtn.rect.width), bgColor = (255,255,255,185))
    settingBtn.rect.right = vw - 8
    settingBtn.rect.top = quitBtn.rect.top
    settingBtn.borderWidth(2)
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
    if Option:
        Crafts = Items = Controls = False

        backBtn = Rect((8, 8, vw * 0.1, vw * 0.1), bgColor = (255,255,255,185))
        backBtn.borderWidth(2)
        backBtn.addChild( Text('Back', color = (225,225,225), font_size = 12) )
        backBtn.center_children()

        controlsBtn = Rect((vw * 0.1, vh * 0.83, vw * 0.7, vh * 0.09), bgColor = (255,255,255,185))
        controlsBtn.borderWidth(2)
        controlsBtn.addChild( Text('Controls', color = (225,225,225)) )
        controlsBtn.rect.centerx = vc[0]
        controlsBtn.center_children()

        itemsBtn = Rect((controlsBtn.rect.left, controlsBtn.rect.top - controlsBtn.rect.height - 20, controlsBtn.rect.width, controlsBtn.rect.height), bgColor = (255,255,255,185))
        itemsBtn.borderWidth(2)
        itemsBtn.addChild( Text('Items', color = (225,225,225)) )
        itemsBtn.rect.centerx = vc[0]
        itemsBtn.center_children()

        craftsBtn = Rect((itemsBtn.rect.left, itemsBtn.rect.top - itemsBtn.rect.height - 20, itemsBtn.rect.width, itemsBtn.rect.height), bgColor = (255,255,255,185))
        craftsBtn.borderWidth(2)
        craftsBtn.addChild( Text('Crafts', color = (225,225,225)) )
        craftsBtn.rect.centerx = vc[0]
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
    if Crafts:
        backBtn = Rect((8, 8, vw * 0.1, vw * 0.1), bgColor = (255,255,255,185))
        backBtn.borderWidth(2)
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
    



puffy = pygame.image.load('img/item/puff.png').convert_alpha()
rapid = pygame.image.load('img/item/rapid.png').convert_alpha()
rapidAR = rapid.get_width() / rapid.get_height()
magnet = pygame.image.load('img/item/magnet.png').convert_alpha()
magnetAR = magnet.get_width() / magnet.get_height()
shield = pygame.image.load('img/item/shield-sm.png').convert_alpha()
shieldAR = shield.get_width() / shield.get_height()
bubble = pygame.image.load('img/item/bubble-sm.png').convert_alpha()
bubbleAR = bubble.get_width() / bubble.get_height()
lifeGem = pygame.image.load('img/item/gem.png').convert_alpha()
lifeGemAR = lifeGem.get_width() / lifeGem.get_height()
unit = pygame.image.load('img/item/unit.png').convert_alpha()
def items(bg, bg_alpha):
    global Items
    if Items:
        backBtn = Rect((8, 8, vw * 0.1, vw * 0.1), bgColor = (255,255,255,205))
        backBtn.borderWidth(2)
        backBtn.addChild( Text('Back', color = (225,225,225), font_size = 12) )
        backBtn.center_children()

        unitsTxt = Text('Units: '+str(dbDoc["units"]), color = (255,255,255), font_size = 20)
        unitsTxt.rect.midright = (vw - 8, backBtn.rect.centery)

        Frame = Rect((8, backBtn.rect.bottom + 8, vw - 16, 0), bgColor = (255,255,255,0))
        Frame2 = Rect((8, backBtn.rect.bottom + 8, vw - 16, vh - backBtn.rect.bottom - 8 - 80), bgColor = (255,255,255,185))
        Frame2.borderWidth(1)
        opaque1 = Rect((0,0, vw, Frame.rect.top), bgColor = (0,0,0,0))

        puffyInv = components.itemInv12(Frame, {'img': puffy,'w': 60,'h': 60}, 'Puffy', 'Enlarge\'s bullet\nsize and power in\nmultiples.', itemDoc = dbDoc["item"]['items']['puffy'], periodsDoc = dbDoc["item"]["periods"])
        puffyInv.addTo(Frame)
        rapidInv = components.itemInv12(Frame, {'img': rapid,'w': 40,'h': round(40/rapidAR)}, 'Rapid', 'Increases and\ngives Constant\nstrike rate in\nmultiples.', dbDoc["item"]['items']['rapid'], dbDoc["item"]["periods"])
        rapidInv.addTo(Frame)
        magnetInv = components.itemInv2(Frame, {'img': magnet,'w': 50,'h': round(50/magnetAR)}, 'Magnet', 'Enables attraction\nof items.', dbDoc["item"]['items']['magnet'], dbDoc["item"]["periods"])
        magnetInv.addTo(Frame)
        bubbleInv = components.itemInv2(Frame, {'img': bubble,'w': 60,'h': round(60/bubbleAR)}, 'Bubble', 'Periodic force-field\nbubble protection\naround craft.', dbDoc["item"]['items']['bubble'], dbDoc["item"]["periods"])
        bubbleInv.addTo(Frame)
        shieldInv = components.itemInv3(Frame, {'img': shield,'w': 50,'h': round(50/shieldAR)}, 'Shield', 'Extra Protection\ncount.', dbDoc["item"]['items']['shield'])
        shieldInv.addTo(Frame)
        lifeGemInv = components.itemInv3(Frame, {'img': lifeGem,'w': 60,'h': round(60/lifeGemAR)}, 'Life Gem', 'Gives a contination\nchances.', dbDoc["item"]['items']['life'])
        lifeGemInv.addTo(Frame)
        unitInv = components.itemInv1(Frame, {'img': unit,'w': 65,'h': 65}, 'Unit', 'Increase multiple of\nunit gain per a\ntake.', dbDoc["item"]['items']['unit'])
        unitInv.addTo(Frame)

        invsComp = [puffyInv, rapidInv, magnetInv, bubbleInv, shieldInv, lifeGemInv, unitInv]

        Frame.rect.height = len(Frame.children) * (100+8)+8
        opaque2 = Rect((0, vh - 80, vw, 80), bgColor = (0,0,0,0))

        upBtn = Rect((vw - 50 - 8, vh - 44-8,50,20), bgColor = (255,255,255,205))
        upBtn.borderWidth(2)
        upIcon = Poly( (0,0, upBtn.rect.width * 0.7, upBtn.rect.height * 0.55), bgColor = (255,255,255,255) )
        upBtn.addChild( upIcon )
        upBtn.center_children()
        upIcon.set_pts( (upIcon.rect.midtop, upIcon.rect.bottomright, upIcon.rect.bottomleft) )
        downBtn = Rect((upBtn.rect.left, upBtn.rect.bottom + 2,50,20), bgColor = (255,255,255,205))
        downBtn.borderWidth(2)
        downIcon = Poly( (0,0, downBtn.rect.width * 0.7, downBtn.rect.height * 0.55), bgColor = (255,255,255,255) )
        downBtn.addChild( downIcon )
        downBtn.center_children()
        downIcon.set_pts( (downIcon.rect.topleft, downIcon.rect.topright, downIcon.rect.midbottom) )

        allPurchaseBtns = []
        for comp in invsComp:
            if comp.upgradable:
                allPurchaseBtns.append(comp.upgradeBtn)
            if comp.extendable:
                allPurchaseBtns.append(comp.extendBtn)
            if comp.buyable:
                allPurchaseBtns.append(comp.buyBtn)

        MouseMotion = False
        MouseHeld = False
        Click = False
        Scroll_dy = 0
    while Items:
        mx, my = pygame.mouse.get_pos()
        bg.blit(bgImg, bgImg_rect.topleft)
        bg_alpha.fill((0,0,0,0))

        if Scroll_dy:
            if (Scroll_dy > 0 and Frame.rect.top >= backBtn.rect.bottom + 8) or (Scroll_dy < 0 and Frame.rect.top >= backBtn.rect.bottom + 8 and Frame.rect.bottom <= vh - 80-8):
                Scroll_dy = 0
                Frame.rect.top = backBtn.rect.bottom + 8
            elif Scroll_dy < 0 and Frame.rect.bottom <= vh - 80-8:
                Scroll_dy = 0
                Frame.rect.bottom = vh - 80-8
            Frame.rect.top += Scroll_dy 
            Frame.vacate()

        if MouseMotion:
            handler1 = Handler( func = bgColor, value = {'bgColor': (255,255,255,255)} )
            handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
            handler3 = Handler( func = color, value = {'color': (15,15,15,255)}, elem = backBtn.getChildBy('name', 'text') )
            backBtn.onHover([handler1, handler2, handler3], (mx, my))
            handler1 = Handler( func = bgColor, value = {'bgColor': (255,255,255,255)} )
            handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
            handler3 = Handler( func = bgColor, value = {'bgColor': (0,0,0,255)}, elem = upIcon )
            upBtn.onHover([handler1, handler2, handler3], (mx, my))
            handler1 = Handler( func = bgColor, value = {'bgColor': (255,255,255,255)} )
            handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
            handler3 = Handler( func = bgColor, value = {'bgColor': (0,0,0,255)}, elem = downIcon )
            downBtn.onHover([handler1, handler2, handler3], (mx, my))

            handler1 = Handler( func = bgColor, value = {'bgColor': (255,25,255,255)} )
            handler2 = Handler( func = borderWidth, value = {'border_width': 0} )
            for btn in allPurchaseBtns:
                btn.onHover([handler1, handler2], (mx, my))
            
        Frame.show(bg_alpha)
        Frame2.show(bg_alpha)
        opaque1.show(bg_alpha)
        opaque2.show(bg_alpha)
        backBtn.show(bg_alpha)
        unitsTxt.show(bg_alpha)
        upBtn.show(bg_alpha)
        downBtn.show(bg_alpha)
        
        if Click:
            handler1 = Handler( value = [Items] )
            Items, = backBtn.onClick([handler1], (mx_up, my_up))[0]
            upBtn.onClick(pos = (mx_up, my_up))
            downBtn.onClick(pos = (mx_up, my_up))

            for comp in invsComp:
                item_name = comp.item_name
                price = 0
                if comp.upgradable:
                    comp.upgradeBtn.onClick(pos = (mx_up, my_up))
                    if comp.upgradeBtn.click:
                        aPurchaseBtnClicked = True
                        price = comp.upgradePrice
                        purchasable = comp.upgradePurchasable
                        if purchasable and dbDoc["units"] >= price and price != 0:
                            comp.multiState += 1
                    else:
                        aPurchaseBtnClicked = False

                if comp.extendable and not aPurchaseBtnClicked:
                    comp.extendBtn.onClick(pos = (mx_up, my_up))
                    if comp.extendBtn.click:
                        aPurchaseBtnClicked = True
                        price = comp.extendPrice
                        purchasable = comp.extendPurchasable
                        if purchasable and dbDoc["units"] >= price and price != 0:
                            comp.periodState += 1
                    else:
                        aPurchaseBtnClicked = False

                if comp.buyable and not aPurchaseBtnClicked:
                    comp.buyBtn.onClick(pos = (mx_up, my_up))
                    if comp.buyBtn.click:
                        aPurchaseBtnClicked = True
                        price = comp.price
                        if dbDoc["units"] >= price:
                            comp.bought += 1
                    else:
                        aPurchaseBtnClicked = False

                if aPurchaseBtnClicked:
                    dbDoc["units"] -= price
                    comp.updateDb(dbDoc)
                    comp.render()
                    comp.reAddTo(Frame)
                    unitsTxt = Text('Units: '+str(dbDoc["units"]), color = (255,255,255), font_size = 20)
                    unitsTxt.rect.midright = (vw - 8, backBtn.rect.centery)

            allPurchaseBtns = []
            for comp in invsComp:
                if comp.upgradable:
                    allPurchaseBtns.append(comp.upgradeBtn)
                if comp.extendable:
                    allPurchaseBtns.append(comp.extendBtn)
                if comp.buyable:
                    allPurchaseBtns.append(comp.buyBtn)

            Click = False

        if MouseHeld:
            if upBtn.click:
                Scroll_dy = 8
            elif downBtn.click:
                Scroll_dy = -8
        else:
            if Scroll_dy and not ctrls.keys['up'] and not ctrls.keys['down']:
                Scroll_dy = 0
                upBtn.click = False
                downBtn.click = False

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

            if kind == MOUSEBUTTONDOWN:
                mx_up, my_up = event.pos
                Click = True
                MouseHeld = True
            elif kind == MOUSEBUTTONUP:
                mx_up, my_up = event.pos
                MouseHeld = False
            
            if kind == KEYDOWN:
                key = event.key
                if key == K_UP:
                    Scroll_dy = 8
                    ctrls.keys['up'] = True
                if key == K_DOWN:
                    Scroll_dy = -8
                    ctrls.keys['down'] = True
            
            if kind == KEYUP:
                key = event.key
                if (key == K_UP or key == K_DOWN):
                    Scroll_dy = 0
                    ctrls.keys['up'] = False
                    ctrls.keys['down'] = False

        pygame.display.update()
        FPSClock.tick(15)


def controls(bg, bg_alpha):
    global Controls
    if Controls:
        backBtn = Rect((8, 8, vw * 0.1, vw * 0.1), bgColor = (255,255,255,185))
        backBtn.borderWidth(2)
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
    if Levels:
        backBtn = Rect((8, 8, vw * 0.1, vw * 0.1), bgColor = (255,255,255,185))
        backBtn.borderWidth(2)
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
        ScrollBarFocus = False
        scrollRule = [vh - scrollBar.rect.height / 2, 0 + scrollBar.rect.height / 2]
        scrollRule.append( scrollRule[0] - scrollRule[1] )
        scrollBarPercent = 0
        init = True
    while Levels:
        mx, my = pygame.mouse.get_pos()

        bg.blit(bgImg, bgImg_rect.topleft)

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


        if init:
            Tposy = vh - round(vh * 0.15)

            gridFrame.rect.top = -(grid_h - vh)
            gridFrame.rect.top += Tposy - current_lvl_dom.rect.centery
            for obj in gridFrame.children:
                obj.rect.centery = gridFrame.rect.top + obj.offSet[1]
                obj.center_children()

            scrollBar.rect.centery = -(((gridFrame.rect.top + (grid_h - vh)) / (grid_h - vh)) * scrollRule[2]) + scrollRule[0]
            init = False
        if ScrollBarFocus:
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
            ScrollBarFocus = False

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

                if lvl.click:
                    #print('Clicked')
                    level.selected = stages[i]
                    #lvl.clicked = False
                    break
                i += 1
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