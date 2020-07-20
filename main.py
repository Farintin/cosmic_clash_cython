import pygame, sys
from pygame.locals import *
import display, stars, controls, features, dom
from colors import bg_color
import boot, menu
import crafts
from game import Game



### Setup pygame/window ---------------------------------------- #
FPSClock = pygame.time.Clock()
pygame.init()

vw = display.view_width
vh = display.view_height
vc = display.view_center

bg = display.BACKGROUND
bg_alpha = display.bg_alpha

FPS = display.FPS
FPSsec = display.FPSsec

TRUE = -1
FALSE = 0



def main():
    boot.run(bg, vw, vh, vc, display.FPS)
    Level = menu.run(bg, bg_alpha)

    Action = TRUE
    while True: ### main game loop
        action(Level, Action)
        Level = menu.run(bg, bg_alpha, Levels = TRUE)
        Action = TRUE


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
    colored_dark = bg_color()
    bg_stars = stars.gen(vw, vh)

    craft = crafts.Craft1()

    Won = False
    Over = False

    game = Game(craft, Level, Won, Over)


    pauseBtn = dom.Rect((2,7,20,20), bgColor = (255,255,255,155))
    pauseBtn.borderWidth(1)
    pauseRect1 = dom.Rect((0,0,4,10), bgColor = (255,255,255,255))
    pauseRect2 = dom.Rect((0,0,4,10), bgColor = (255,255,255,255))
    pauseBtn.addChildren( ( pauseRect1, pauseRect2 ) )
    pauseBtn.center_children()
    pauseRect1.rect.right = pauseBtn.rect.centerx - 1
    pauseRect2.rect.left = pauseBtn.rect.centerx + 1


    Click = False
    Play = TRUE
    while Action:
        bg.fill(colored_dark)
        stars.fix(bg, bg_stars)
        bg_alpha.fill((0,0,0,0))

        crafts.action(bg, bg_alpha, craft)
        score, count, Won, Over = game.action(bg, bg_alpha)
        features.show_all(bg_alpha, craft, score, Level, count)
        pauseBtn.show(bg_alpha)

        if Click:
            handler1 = dom.Handler( value = [Play] )
            Play, = pauseBtn.onClick([handler1], (mx_up, my_up))[0]

            Click = False
        
        Action, Play = pause(Action, Play)

        if Won or Over:
            Won = won(Level, Won)
            Over = overLoop(Over)
            Action = FALSE


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
                    bg_stars = stars.gen(vw, vh)

                if key == K_LEFT:
                    craft.dx = - int(craft.DIM[0] / 20)

                elif key == K_RIGHT:
                    craft.dx = int(craft.DIM[0] / 20)

                if key == K_UP:
                    if not controls.actions['auto_shoot']:
                        craft.load_bullets()

                if key == K_LCTRL or key == K_RCTRL:
                    controls.keys['ctrl'] = True

                if key == K_s:
                    if controls.keys['ctrl']:
                        if not controls.actions['auto_shoot']:
                            controls.actions['auto_shoot'] = True
                        elif controls.actions['auto_shoot']:
                            controls.actions['auto_shoot'] = False

            if kind == KEYUP:
                key = event.key
                
                if key == K_LEFT or key == K_RIGHT:
                    craft.dx = 0
                
                if key == K_LCTRL or key == K_RCTRL:
                    controls.keys['ctrl'] = False
                    

        pygame.display.update()
        FPSClock.tick(FPS)


def pause(Action, Play):
    modal = dom.Rect((0,0, vw * 0.6, vw * 0.4), bgColor = (255,255,255,55))
    modal.borderWidth(2)
    modal.rect.center = vc

    playBtn = dom.Rect((0,0,55,50), bgColor = (255,255,255,75))
    playBtn.borderWidth(1)
    modal.center_child(playBtn)
    playBtn.rect.top = modal.rect.top + 20
    playIcon = dom.Poly( (0,0, playBtn.rect.width * 0.6, playBtn.rect.height * 0.6), bgColor = (255,255,255,75) )
    playBtn.addChild( playIcon )
    playBtn.center_children()
    playIcon.set_pts( (playIcon.rect.midleft, playIcon.rect.topright, playIcon.rect.bottomright) )

    backBtn = dom.Rect((0,0,75,50), bgColor = (255,255,255,75))
    backBtn.borderWidth(1)
    backBtn.rect.left = modal.rect.left + 30
    backBtn.rect.bottom = modal.rect.bottom - 10
    backBtn.addChild( dom.Text('Back', color = (255,255,255,75)) )
    backBtn.center_children()

    quitBtn = dom.Rect((0,0,75,50), bgColor = (255,255,255,75))
    quitBtn.borderWidth(1)
    quitBtn.rect.right = modal.rect.right - 30
    quitBtn.rect.bottom = modal.rect.bottom - 10
    quitBtn.addChild( dom.Text('Quit', color = (255,255,255,75)) )
    quitBtn.center_children()

    modal.addChildren( ( playBtn, backBtn, quitBtn ) )


    Click = False
    Quit = FALSE
    while not Play:
        modal.show(bg_alpha)
    
        if Click:
            handler1 = dom.Handler( value = [Play] )
            Play, = playBtn.onClick([handler1], (mx_up, my_up))[0]

            handler1 = dom.Handler( value = [Action, Play] )
            Action, Play = backBtn.onClick([handler1], (mx_up, my_up))[0]

            handler1 = dom.Handler( value = [Quit] )
            Quit, = quitBtn.onClick([handler1], (mx_up, my_up))[0]

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


def overLoop(Over):
    timer = 0
    while Over:
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

            if kind == KEYDOWN:
                key = event.key

                if key == K_LEFT:
                    pass

                elif key == K_RIGHT:
                    pass

        ### Blit updating
        pygame.display.update()
        FPSClock.tick(15)

    return Over

def won(Level, Won):
    timer = 0
    while Won:
        features.won(bg_alpha, Level)

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