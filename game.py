import pygame
from display import view_height as vh
import colors
from celest import Bodies
import explode



class Game:
    def __init__(self, craft, Level, Won, Over):
        self.score = 0
        self.level = Level

        self.craft = craft

        self.bodies = Bodies(Level)
        self.items = []
        self.explosions = []

        self.won = Won
        self.over = Over

    def action(self, bg_obj, bg_alpha):
        renders = []
        if self.bodies.attacks_count < self.level.attacks:
            self.bodies.next()
        elif self.bodies.attacks_count == self.level.attacks and not self.bodies.bodies:
            self.won = True

        for body in self.bodies.bodies:
            if body.exist == False:
                self.bodies.bodies.remove(body)
        for body in self.bodies.bodies:
            if body.rotation:
                body.rot()
            if body.surf_type == 'image':
                renders.append( body.show(bg_obj, bg_alpha) )
            else:
                body.show(bg_obj, bg_alpha)

            body.set_outline()
            
            body.show_life(bg_alpha)
            #body.show_outline(bg_alpha)

            if body.shield <= 12 and body.flaming:
                body.flaming = False
                if body.name == 'meteor':
                    body.vel[1] = 1
                
            
            body.terminate()
            if not body.exist:pass
                #self.over = True
            else:
                for shoot in self.craft.shoots: # Celest and Bullet collision event
                    for bullet in shoot:
                        if not body.exist:
                            break
                        for pt in bullet.outline_pos:
                            if pt in body.outline_pos:
                                body.shield -= bullet.strength
                                body.show_outline(bg_alpha)

                                if body.shield <= 0:
                                    if body.item2: # Put Items
                                        item = body.item2
                                        item.set_pos(body.pos)

                                        self.items.append(item)

                                    if body.rotation:
                                        body.pos = [body.smoothed_rot_x + body.ROT_DIM[0] / 2, body.smoothed_rot_y + body.ROT_DIM[1] / 2]
                                        self.explosions.append( explode.Ripple(body.pos, explode_avg_rad = body.explode_avg_rad, explode_alpha = body.explode_alpha) )
                                        self.explosions.append( explode.Scatter(body.pos, body.surf_colors) )
                                    else:
                                        self.explosions.append( explode.Ripple(body.rect.center, explode_avg_rad = body.explode_avg_rad, explode_alpha = body.explode_alpha) )
                                        self.explosions.append( explode.Scatter(body.rect.center, body.surf_colors) )

                                    body.exist = False
                                    self.score += 1

                                    bullet.exist = False
                                    break

                                bullet.exist = False
                                break
                                
                if body.bottom >= self.craft.rect.top:
                    celest_craft_collision = False # Celest and Craft collision event
                    for x in range(self.craft.rect.left, self.craft.rect.right):
                        for y in range(self.craft.rect.top, self.craft.rect.bottom):
                            if [x,y] in body.outline_pos:
                                celest_craft_collision = True

                                if body.rotation:
                                    body.pos = [body.smoothed_rot_x + body.ROT_DIM[0] / 2, body.smoothed_rot_y + body.ROT_DIM[1] / 2]
                                self.explosions.append(explode.Ripple(body.pos, explode_avg_rad = body.explode_avg_rad, explode_alpha = body.explode_alpha))
                                self.explosions.append( explode.Scatter(body.pos, body.surf_colors) )

                                body.exist = False

                                self.craft.life -= body.strength

                                if self.craft.life <= 0:
                                    self.over = True

                                self.craft.outline_color = colors.RED
                                self.craft.collide = True
                                break

                        if celest_craft_collision:
                            break

                body.nav()


        if self.bodies.attacks_count == 1 and self.bodies.timer == 0:
            print(self.level.bodys_prob)
        
        
        


        # Items obj loops
        for item in self.items:
            if not item.exist:
                self.items.remove(item)
        for item in self.items:
            renders.append( item.show(bg_alpha) )

            item.show_bounds(bg_alpha)

            if item.pos[1] > vh: # Terminate Item out of view bottom
                item.exist = False
            else:
                if item.rect.bottom >= self.craft.rect.top:
                    if pygame.sprite.collide_rect(item, self.craft):
                        if item.name == 'life' and self.craft.life < 3:
                            self.craft.life += 1

                        item.exist = False

                        self.craft.outline_color = colors.BLUE
                        self.craft.collide = True
                        
                item.nav()
                

        # Explosions
        explode.action(self.explosions, bg_alpha)

        bg_obj.blits(renders)
        return self.score, self.bodies.attacks_count, self.won, self.over