import display, colors
import pygame
import db
import dom


vw = display.view_width
vh = display.view_height
vc = display.view_center
FPSsec = display.FPSsec


pauseBtn = dom.Rect((2,7,20,20), bgColor = (255,255,255,155))
pauseBtn.borderWidth(1)
pauseRect1 = dom.Rect((0,0,4,10), bgColor = (255,255,255,255))
pauseRect2 = dom.Rect((0,0,4,10), bgColor = (255,255,255,255))
pauseBtn.addChildren( ( pauseRect1, pauseRect2 ) )
pauseBtn.center_children()
pauseRect1.rect.right = pauseBtn.rect.centerx - 1
pauseRect2.rect.left = pauseBtn.rect.centerx + 1


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




def craft_items(bg_alpha, craft):
    craft.items_state()

    timer_frame = pygame.Rect(20,36,16,15)
    timer_frame_default_width = timer_frame.width
    for item in craft.items:
        item_timer_frame = timer_frame
        item_timer_frame.width += 16 * item.multi

        bg_alpha.blit( item.img, (2, round( item_timer_frame.centery - item.img.get_width() / 2 )) )

        pygame.draw.rect(bg_alpha, (255,255,255), item_timer_frame, 1)

        item_bar_rect = (item_timer_frame.left + 1, item_timer_frame.top + 1, round( (item.timing / item.timer) * (item_timer_frame.width - 2)), item_timer_frame.height - 2)
        pygame.draw.rect(bg_alpha, item.collected_color, item_bar_rect)

        item.timing -= FPSsec
        if item.timing <= 0:
            item.timing = 0

        timer_frame.top += timer_frame.height + 8
        timer_frame.width = timer_frame_default_width



shield = pygame.image.load('img/item/shield.png').convert_alpha()
shieldAR = shield.get_width() / shield.get_height()
shield = pygame.transform.scale(shield, (20, round(20 / shieldAR)))
shield_bar_w = 6
shield_bar_g = 5
shield_bar_h = 15
def craft_shield(bg_alpha, craft):
    if craft.shield <= 1:
        craft.shield_color = colors.RED
    else:
        craft.shield_color = colors.WHITE
    for n in range(0, craft.shield):
        x = (shield_bar_w * n + shield_bar_g * (n + 1)) + (shield.get_width() / 2) + 35
        y = 10
        w = shield_bar_w
        h = shield_bar_h
        pygame.draw.rect(bg_alpha, craft.shield_color, (x, y, w, h))
    bg_alpha.blit(shield, (25,5))

def Wave(bg_alpha, Level, count):
    textSurfaceObj = display.fontObj.render('Wave%i: %i /%i' %(Level.n, count, Level.attacks), True, colors.WHITE)

    textRectObj = textSurfaceObj.get_rect()
    textRectObj.left = round(vw - textRectObj.width - 5)
    textRectObj.top = round(textRectObj.height / 0.5)
    bg_alpha.blit(textSurfaceObj, textRectObj)

def score(bg_alpha, score):
    textSurfaceObj = display.fontObj.render('Score: %i' %(score), True, colors.WHITE)

    textRectObj = textSurfaceObj.get_rect()
    textRectObj.left = round(vw - textRectObj.width - 5)
    textRectObj.top = round(textRectObj.height / 1.8)
    bg_alpha.blit(textSurfaceObj, textRectObj)


def show_all(bg_alpha, craft, Score, Level, count):
    pauseBtn.show(bg_alpha)
    craft_shield(bg_alpha, craft)

    score(bg_alpha, Score)
    Wave(bg_alpha, Level, count)

    craft_items(bg_alpha, craft)



dbDoc = db.document
def gameOver(bg_alpha):
    fontObj = pygame.font.Font('freesansbold.ttf', 48)
    textSurfaceObj = fontObj.render('Game Over', True, colors.RED)

    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = vc

    bg_alpha.blit(textSurfaceObj, textRectObj)

def won(bg_alpha):
    fontObj = pygame.font.Font('freesansbold.ttf', 64)
    textSurfaceObj = fontObj.render('Level Up', True, colors.BLUE)

    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = vc

    bg_alpha.blit(textSurfaceObj, textRectObj)


def setCurrentLevel(next_lvl_n):
    if next_lvl_n - 1 >= dbDoc['levels']['current']:
        dbDoc['levels']['current'] = next_lvl_n
        db.save(dbDoc)

def updateCraftsUnit(units):
    dbDoc['units'] += units
    db.save(dbDoc)

def updateLevelScore(lvl_n, score):
    dbDoc['levels']['scores'][str(lvl_n)] = score
    db.save(dbDoc)
