#!/usr/bin/python
# PJ.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,utils,pygame,gtk,sys,jigsaw,buttons

class PJ:
    
    def __init__(self):
        self.success=0
        self.journal=True # set to False if we come in via main()
        self.jigsaw_n=0

    def display(self,wait=False):
        if g.state==1:
            self.menu_display()
            utils.display_number(g.success,(g.sx(.2),g.sy(.15)),g.font2)
        else:
            if self.pj.complete():
                g.screen.blit(g.bgd,(g.sx(0),0))
                utils.display_number(g.success,(g.sx(.5),g.sy(.5)),g.font1)
            else:
#                g.screen.fill((g.red,g.green,g.blue))
                g.screen.fill(utils.CYAN)
            self.pj.draw()
            buttons.draw()
            if self.bu2.active:
                if self.pj.all_rotated():
                    self.bu2.off()
                else:
                    utils.centre_blit(g.screen,g.smiley1,(g.smiley1_x,g.smiley_y))
                    utils.centre_blit(g.screen,g.smiley2,(g.smiley2_x,g.smiley_y))

    def menu_display(self):
        g.screen.fill(utils.BLACK)
        d=g.sy(.22); w=g.sy(7.73); h=g.sy(3.68); y0=g.sy(1)
        y=y0; ind=0
        for r in range(5):
            x=d
            for c in range(4):
                g.screen.blit(g.menu[ind],(x,y))
                ind+=1           
                x+=w+d
            y+=h+d
                                 
    def menu_click(self):
        d=g.sy(.22); w=g.sy(7.73); h=g.sy(3.68); y0=g.sy(1)
        y=y0; n=0
        for r in range(5):
            x=d
            for c in range(4):
                n+=1
                if utils.mouse_in(x,y,x+w,y+h):
                    self.jigsaw_n=n; g.state=2
                    g.screen.fill(utils.CYAN)
                    utils.centre_blit(g.screen,g.wait,(g.sx(16),g.sy(11)))
                    pygame.display.flip()
                    return
                x+=w+d
            y+=h+d
        
    def do_button(self,button):
        if button=='menu':
            g.state=1
        elif button=='unrotate':
            self.pj.unrotating=True

    def setup(self):
        self.bu1.on(); self.bu2.on(); self.bu3.off()
        return self.pj.setup(self.jigsaw_n)

    def run(self):
        g.init()
        g.journal=self.journal
        if not self.journal:
            utils.load(); self.success=g.success
        else:
            g.success=self.success
        x=g.sx(8); y=g.sy(8.8)
        self.bu1=buttons.Button("menu",(x,y))
        x=g.sx(16); y=g.smiley_y
        self.bu2=buttons.Button("unrotate",(x,y))
        x=g.sx(16); y=g.sy(19)
        self.bu3=buttons.Button("menu",(x,y)); self.bu3.off()
        self.pj=jigsaw.Jigsaw()
        going=True
        while going:
            ms=pygame.time.get_ticks()
            g.mx,g.my=pygame.mouse.get_pos()
            # Pump GTK messages.
            while gtk.events_pending():
                gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.redraw=True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==2: # centre button
                        g.version_display=not g.version_display; break
                    elif event.button==3: # right button
                        self.pj.rotate(); break
                    elif event.button==1: # left button
                        if g.state==3:
                            bu=buttons.check() 
                            if bu!='': self.do_button(bu); break
                    if g.state==1:
                        self.menu_click()
                        if g.state==2:
                            if not self.setup(): going=False; break
                            g.state=3
                    elif g.state==3:
                        if self.pj.click():
                            self.bu1.off(); self.bu2.off()
                            if self.pj.complete(): self.bu3.on()
            if not going: break
            if g.state==3:
                self.pj.right_button_display()
                self.pj.unrotate()
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                if self.pj.carry:
                    g.screen.blit(g.negative,(g.mx,g.my))
                else:
                    g.screen.blit(g.pointer,(g.mx,g.my))
                pygame.display.flip()
                g.redraw=False
            self.success=g.success
            g.clock.tick(40)
            d=pygame.time.get_ticks()-ms; g.frame_rate=int(1000/d)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((800,600))
    game=PJ()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
