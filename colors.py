import random


BLACK = (0,0,0)
WHITE = (255,255,255)

RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (195,195,255)

TRANS_BLACK = (0,0,0,0)
TRANS_WHITE = (255,255,255,0)

def bg_color():
    dark_rgb_focus = random.randrange(0, 3)
    MAX_RGB = 19
    if dark_rgb_focus == 0:
        R = random.randrange(0, MAX_RGB + 1)
        G = 0
        B = 0
    elif dark_rgb_focus == 1:
        R = 0
        G = random.randrange(0, MAX_RGB + 1)
        B = 0
    elif dark_rgb_focus == 2:
        R = 0
        G = 0
        B = random.randrange(0, MAX_RGB + 1)
    DARK = (R, G, B)
    #print('bg_color: ' + str(DARK))
    return DARK