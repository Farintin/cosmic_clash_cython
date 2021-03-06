import pygame, sys
from pygame.locals import *
import display, starsCy, controls, features, dom
from colors import bg_color
import boot, menu
import craftsCy
from gameCy import Game
import db


### Setup pygame/window ---------------------------------------- #
FPSClock = display.FPSClock
FPS = display.FPS
FPSsec = display.FPSsec

vw = display.view_width
vh = display.view_height
vc = display.view_center

bg = display.BACKGROUND
bg_alpha = display.bg_alpha




def main():
    boot.run(bg, vw, vh, vc, display.FPS)
    Level = menu.run(bg, bg_alpha)

    Action = True
    while True: ### main game loop
        game = action(Level, Action)
        features.updateCraftsUnit(game.craft.units)### Update units

        Level = menu.run(bg, bg_alpha, Levels = True)
        Action = True

        ### Event loop block
        for event in pygame.event.get():
            kind = event.type

            if kind == QUIT:
                pygame.quit()
                sys.exit()

            if kind == KEYDOWN:
                key = event.key
                    
        ### Blit updating
        pygame.display.update()
        FPSClock.tick(FPS)


def action(Level, Action):
    if Action:
        colored_dark = bg_color()
        bg_stars = starsCy.gen(vw, vh)

        craft = craftsCy.Craft1()

        Won = False
        Over = False

        game = Game(craft, Level, Won, Over)

        Click = False
        Play = True
    while Action:
        bg.fill(colored_dark)
        starsCy.fix(bg, bg_stars)
        bg_alpha.fill((0,0,0,0))

        score, count, Won, Over = game.action(bg, bg_alpha)
        features.show_all(bg_alpha, craft, score, Level, count)

        Action, Play = pause(Action, Play)
        if Click:
            handler1 = dom.Handler( value = [Play] )
            init_play = Play
            Play, = features.pauseBtn.onClick([handler1], (mx_up, my_up))[0]
            if init_play and not Play:
                for child in features.pauseBtn.children:
                    if child.name == 'rect':
                        child.visible = False
                    else:
                        child.visible = True

            Click = False
        

        if Won or Over:
            Action = False
            Won = won(Level, Won, game)
            Over, Action = overLoop(Over, Action, game)


        bg.blit(bg_alpha, (0,0))


        ### Event loop block
        for event in pygame.event.get():
            kind = event.type

            if kind == QUIT:
                pygame.quit()
                sys.exit()

            if kind == MOUSEBUTTONUP:
                mx_up, my_up = event.pos
                Click = True

            if kind == KEYDOWN:
                key = event.key

                if key == K_ESCAPE:
                    colored_dark = bg_color()
                    bg_stars = starsCy.gen(vw, vh)

                if key == K_LEFT:
                    craft.dx = - int(craft.DIM[0] / 20)
                elif key == K_RIGHT:
                    craft.dx = int(craft.DIM[0] / 20)

                if key == K_UP:
                    craft.shooting = True
                    if not craft.rapid_strike:
                        craft.load_bullets()

                '''if key == K_LCTRL or key == K_RCTRL:
                    controls.keys['ctrl'] = True

                if key == K_s:
                    if controls.keys['ctrl']:
                        if not craft.rapid_strike:
                            craft.rapid_strike = True
                        else:
                            craft.rapid_strike = False'''

            if kind == KEYUP:
                key = event.key
                
                if key == K_LEFT or key == K_RIGHT:
                    craft.dx = 0
                
                '''if key == K_LCTRL or key == K_RCTRL:
                    controls.keys['ctrl'] = False'''

                if key == K_UP:
                    craft.shooting = False
                    

        pygame.display.update()
        FPSClock.tick(FPS)
    return game


def pause(Action, Play):
    if not Play:
        Click = False
        Quit = False
    while not Play:
        features.modal.show(bg_alpha)
    
        if Click:
            handler1 = dom.Handler( value = [Play] )
            init_play = Play
            Play, = features.playBtn.onClick([handler1], (mx_up, my_up))[0]
            if not Play:
                Play, = features.pauseBtn.onClick([handler1], (mx_up, my_up))[0]

            handler1 = dom.Handler( value = [Action, Play] )
            Action, Play = features.backBtn.onClick([handler1], (mx_up, my_up))[0]
            
            if not init_play and Play:
                for child in features.pauseBtn.children:
                    if child.name == 'poly':
                        child.visible = False
                    else:
                        child.visible = True

            handler1 = dom.Handler( value = [Quit] )
            Quit, = features.quitBtn.onClick([handler1], (mx_up, my_up))[0]

            Click = False

        dom.egress(Quit)
            
        bg.blit(bg_alpha, (0,0))

        
        for event in pygame.event.get(): ### Event loop block
            kind = event.type

            if kind == QUIT:
                pygame.quit()
                sys.exit()

            if kind == MOUSEBUTTONUP:
                mx_up, my_up = event.pos
                Click = True

            if kind == KEYDOWN:
                key = event.key

                if key == K_LEFT:
                    pass

                elif key == K_RIGHT:
                    pass

        ### Blit updating
        pygame.display.update()
        FPSClock.tick(15)
    
    return Action, Play


def overLoop(Over, Action, game):
    if Over:
        timer = 0
        continueModal = True
        Click = False
    while Over:
        if db.document["item"]["items"]["life"]["bought"] and continueModal:
            features.continueModal.show(bg_alpha)
            if Click:
                handler1 = dom.Handler( value = [Action, Over] )
                Action, Over = features.continueModalComp.yesBtn.onClick([handler1], (mx_up, my_up))[0]
                handler1 = dom.Handler( value = [Over] )
                features.continueModalComp.noBtn.onClick([handler1], (mx_up, my_up))[0]

                if features.continueModalComp.yesBtn.click and not Over and Action:
                    db.document["item"]["items"]["life"]["bought"] = db.document["item"]["items"]["life"]["bought"] - 1
                    features.continueModalComp.render(features.continueModal)
                    game.craft.shield = game.craft.defaults['shield']
                    game.over = False
                    continueModal = False
                elif features.continueModalComp.noBtn.click:
                    continueModal = False

                Click = False
        else:
            features.gameOver(bg_alpha)
            timer += 1/15
            if timer >= 3:
                Over = False

        bg.blit(bg_alpha, (0,0))

        
        for event in pygame.event.get(): ### Event loop block
            kind = event.type

            if kind == QUIT:
                pygame.quit()
                sys.exit()

            if kind == MOUSEBUTTONUP:
                mx_up, my_up = event.pos
                Click = True

            if kind == KEYDOWN:
                key = event.key

                if key == K_LEFT:
                    pass

                elif key == K_RIGHT:
                    pass

        ### Blit updating
        pygame.display.update()
        FPSClock.tick(15)

    return Over, Action

def won(Level, Won, game):
    if Won:
        timer = 0
    while Won:
        features.won(bg_alpha)
        if timer == 0:### Update data
            features.setCurrentLevel(Level.n + 1)
            features.updateLevelScore(Level.n, game.score)

        timer += 1/15
        if timer >= 3:
            Won = False

        bg.blit(bg_alpha, (0,0))

        
        for event in pygame.event.get(): ### Event loop block
            kind = event.type

            if kind == QUIT:
                pygame.quit()
                sys.exit()

            if kind == KEYDOWN:
                key = event.key

                if key == K_LEFT:
                    pass

                elif key == K_RIGHT:
                    pass

        ### Blit updating
        pygame.display.update()
        FPSClock.tick(15)
    
    return Won





if __name__ == '__main__':
    main()