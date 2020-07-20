import sys, random
import pygame
from pygame.locals import *
import items
from celestCy import sprites_init




FPSClock = pygame.time.Clock()

def slide1(bg, vw, vh, vc):
    logo = pygame.image.load('img/ibrand_studios.png')
    logo_rect = logo.get_rect()
    logoAspectDim = (logo_rect.width, logo_rect.height)

    logo = pygame.transform.scale( logo, (150, round( 150/(logoAspectDim[0] / logoAspectDim[1]) ) ))
    logo_rect = logo.get_rect()
    logo_rect.center = vc

    FPS = 2
    slide1period = 3
    slide1FPSperiod = slide1period * FPS

    FPSsec_i = 0

    slide1 = True
    while slide1:
        bg.fill((0,0,0))
        bg.blit(logo, logo_rect.topleft)

        #bg.blit(bootSurf, (0,0))

        if FPSsec_i >= slide1FPSperiod:
            slide1 = False
            #FPSsec_i = 0
        else:
            FPSsec_i += 1


        for event in pygame.event.get(): # Event loop block
                e_type = event.type
                if e_type == QUIT:
                    pygame.quit()
                    sys.exit()


        pygame.display.update()
        FPSClock.tick(FPS)

def slide2(bg, vw, vh, vc, FPS):
    bgImg = pygame.image.load('img/bg_and_title.png')
    bgImg_rect = bgImg.get_rect()
    bgImgAspectDim = (bgImg_rect.width, bgImg_rect.height)
    bgImg = pygame.transform.scale( bgImg, (vw, round( vw/(bgImgAspectDim[0] / bgImgAspectDim[1]) ) ))

    loadingBarFrame = pygame.Rect(0,0, vc[0], 2)
    loadingBarFrame.center = (vc[0], round(vh * 0.8))

    loadingBar = pygame.Rect((0,0,0,2))
    loadingBar.topleft = loadingBarFrame.topleft

    slide2period = 7
    slide2FPSperiod = slide2period * FPS

    heavyLoadPoint1 = random.randint(1, int(slide2FPSperiod * 0.5))
    heavyLoadPoint2 = random.randint(int(slide2FPSperiod * 0.5) + 1, slide2FPSperiod)

    FPSsec_i = 0

    slide2 = True
    while slide2:
        bg.blit(bgImg, (0,0))

        pygame.draw.rect(bg, (55,55,55), loadingBarFrame)
        pygame.draw.rect(bg, (255,255,255), loadingBar)

        if loadingBar.width >= loadingBarFrame.width:
            slide2 = False
        else:
            FPSsec_i += 1
            loadingBar.width = round((FPSsec_i / slide2FPSperiod) * loadingBarFrame.width)

        #bg.blit(bootSurf, (0,0))


        ### Load heavy hardware processing codes
        if FPSsec_i == heavyLoadPoint1:#round(0.3 * slide2FPSperiod):
            items.life_gem_orbits_data = items.make_life_gem_orbs()
            #life = items.Life()
            #del life
        elif FPSsec_i == heavyLoadPoint2:
            sprites_init.load_rotated_sprites()
            sprites_init.load_comet_outline()

        ###333333333333333333333333333333333333333333333


        for event in pygame.event.get(): # Event loop block
                e_type = event.type
                if e_type == QUIT:
                    pygame.quit()
                    sys.exit()


        pygame.display.update()
        FPSClock.tick(FPS)


def run(bg, vw, vh, vc, FPS):
    slide1(bg, vw, vh, vc)
    slide2(bg, vw, vh, vc, FPS)