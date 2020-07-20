import pygame
from display import view_height as vh
import colors
from celestCy import Bodies
from explodeCy import action as explode_action
#from multiprocessing import Process



cdef list shoot, pt
cdef int x, y
cdef object body, bullet, unit, item
cdef bint fail


cdef class Game:
    cdef public int score, units
    cdef public object level, craft, bodies
    cdef list items, explosions, renders
    cdef bint won, over

    def __init__(self, object craft, object Level, bint Won, bint Over):
        self.score = 0
        self.level = Level

        self.craft = craft

        self.bodies = Bodies(Level)
        self.items = []
        self.explosions = []

        self.won = Won
        self.over = Over

    '''def bodyProcess(self, object bg_obj, object bg_alpha):
        self.renders = []
        for body in self.bodies.bodies:
            if body.rotation:
                body.rot()
            if body.surf_type == 'image':
                self.renders.append( body.show(bg_obj, bg_alpha) )
            else:
                body.show(bg_obj, bg_alpha)

            body.set_outline()
            
            body.show_shield(bg_alpha)
            #body.show_outline(bg_alpha)

            if body.shield < body.shieldMax / 2 and body.flaming:
                if body.name == 'meteor':
                    body.flaming = False
                    body.vel[1] = 1
                
            fail = False
            if body.name == 'comet':
                if body.rect.top > vh:
                    #fail = True
                    body.exist = False
            elif body.smoothed_rot_y > vh:
                #fail = True
                body.exist = False
            self.over = fail
            if fail:
                break
            else:
                for shoot in self.craft.shoots: # Celest and Bullet collision event
                    for bullet in shoot:
                        if not body.exist:
                            break
                        for pt in bullet.outline_pos:
                            if pt in body.outline_pos:
                                body.shield -= bullet.power
                                body.show_outline(bg_alpha)

                                if body.shield <= 0:
                                    # Put Items
                                    unit = body.units
                                    unit.set_pos(body.pos)
                                    self.items.append(unit)
                                    if body.item.name != 'none':
                                        item = body.item
                                        item.set_pos(body.pos)
                                        self.items.append(item)
                                    ###333333333333333333333333333333333

                                    if body.rotation:
                                        body.pos = [body.smoothed_rot_x + body.ROT_DIM[0] / 2, body.smoothed_rot_y + body.ROT_DIM[1] / 2]
                                        self.explosions.append( explodeCy.Ripple(body.pos, explode_avg_rad = body.explode_avg_rad, explode_alpha = body.explode_alpha) )
                                        self.explosions.append( explodeCy.Scatter(body.pos, body.surf_colors) )
                                    else:
                                        self.explosions.append( explodeCy.Ripple(body.rect.center, explode_avg_rad = body.explode_avg_rad, explode_alpha = body.explode_alpha) )
                                        self.explosions.append( explodeCy.Scatter(body.rect.center, body.surf_colors) )

                                    body.exist = False
                                    self.score += 1

                                    bullet.exist = False
                                    break

                                bullet.exist = False
                                break
                                
                if body.bottom >= self.craft.rect.top:
                    for pt in body.outline_pos:
                        if pt[0] in range(self.craft.rect.left, self.craft.rect.right) and pt[1] in range(self.craft.rect.top, self.craft.rect.bottom):
                            if body.rotation:
                                body.pos = [body.smoothed_rot_x + body.ROT_DIM[0] / 2, body.smoothed_rot_y + body.ROT_DIM[1] / 2]
                            self.explosions.append(explodeCy.Ripple(body.pos, explode_avg_rad = body.explode_avg_rad, explode_alpha = body.explode_alpha))
                            self.explosions.append( explodeCy.Scatter(body.pos, body.surf_colors) )

                            body.exist = False

                            self.craft.shield -= body.power

                            if self.craft.shield <= 1:
                                self.over = True

                            self.craft.outline_color = colors.RED
                            self.craft.collide = True
                            break
                body.nav()


        for item in self.items:
            self.renders.append( item.show(bg_alpha) )

            #item.show_bounds(bg_alpha)

            if item.pos[1] > vh: # Terminate Item out of view bottom
                item.exist = False
            else:
                if item.rect.bottom >= self.craft.rect.top:
                    if pygame.sprite.collide_rect(item, self.craft):
                        if item.name == 'shield' and self.craft.shield < 3:
                            self.craft.shield += item.multi

                        item.exist = False

                        self.craft.outline_color = colors.BLUE
                        self.craft.collide = True
                item.nav()'''

    cdef tuple action
    def action(self, object bg_obj, object bg_alpha):
        self.craft.action(bg_obj, bg_alpha)

        if self.bodies.attacks_count < self.level.attacks:
            self.bodies.next()

        if self.bodies.attacks_count == self.level.attacks and not self.bodies.bodies and not self.items:
            self.won = True

        for body in self.bodies.bodies:
            if not body.exist:
                self.bodies.bodies.remove(body)

        for item in self.items:
            if not item.exist:
                self.items.remove(item)

        '''bodiesAction = Process(target=self.bodyProcess(bg_obj, bg_alpha))
        bodiesAction.start()
        bodiesAction.join()'''
        self.renders = []
        for body in self.bodies.bodies:
            if body.rotation:
                body.rot()
            if body.surf_type == 'image':
                self.renders.append( body.show(bg_obj, bg_alpha) )
            else:
                body.show(bg_obj, bg_alpha)

            body.set_outline()
            
            body.show_shield(bg_alpha)
            #body.show_outline(bg_alpha)

            if body.shield < body.shieldMax / 2 and body.flaming:
                if body.name == 'meteor':
                    body.flaming = False
                    body.vel[1] = 1
                
            '''body.terminate()
            if not body.exist:continue
                #self.over = True'''
            fail = False
            if body.name == 'comet':
                if body.rect.top > vh:
                    #fail = True
                    body.exist = False
            elif body.smoothed_rot_y > vh:
                #fail = True
                body.exist = False
            self.over = fail
            if fail:
                break
            else:
                ### Celest and Craft collision event
                self.craft.body_collision(body, self.explosions)

                for shoot in self.craft.shoots: # Celest and Bullet collision event
                    for bullet in shoot:
                        for pt in bullet.outline_pos:
                            if pt in body.outline_pos:
                                body.shield -= bullet.power
                                body.show_outline(bg_alpha)

                                if body.shield <= 0:
                                    # Put Items
                                    if body.rotation:
                                        pos = body.pos
                                    else:
                                        pos = [body.rect.centerx, body.rect.centery]

                                    unit = body.units
                                    unit.set_pos(pos)
                                    self.items.append(unit)
                                    item = body.item(1)
                                    if item.name:
                                        item.set_pos(pos)
                                        self.items.append(item)
                                    ###333333333333333333333333333333333
                                    #print(self.items)

                                    ### Set Explosion
                                    if body.rotation:
                                        explode_pos = [body.smoothed_rot_x + body.ROT_DIM[0] / 2, body.smoothed_rot_y + body.ROT_DIM[1] / 2]
                                    else:
                                        explode_pos = body.rect.center
                                    ripple = body.ripple
                                    ripple.set_pos(explode_pos)
                                    scatter = body.scatter
                                    scatter.set_pos(explode_pos)
                                    scatter.gen()
                                    self.explosions.append(ripple)
                                    self.explosions.append(scatter)

                                    body.exist = False
                                    self.score += 1

                                bullet.exist = False
                                break
                body.nav()

        if self.craft.shield < 1:
            self.over = True
        



        ### Items obj loops
        for item in self.items:
            self.renders.append( item.show(bg_alpha) )
            item.show_bounds(bg_alpha)

            if item.name == 'unit':
                if item.top > vh: # Terminate Item out of view bottom
                    item.exist = False
            else:
                if item.pos[1] > vh: # Terminate Item out of view bottom
                    item.exist = False

            if not item.exist:
                continue
            else:
                self.craft.item_collision(item)
                if item.name == 'unit':
                    item.fall(self.craft)
                else:
                    item.nav(self.craft)


        if self.bodies.attacks_count == 1 and self.bodies.timer == 0:
            print(self.level.bodys_prob)
                

        # Explosions
        explode_action(self.explosions, bg_alpha)

        bg_obj.blits(self.renders)
        return self.score, self.bodies.attacks_count, self.won, self.over