# pj.py
import os,utils,g,pygame,random

NR=5; NC=8

class Piece:
    def __init__(self,ind):
        self.ind=ind
        self.img=None; self.rotated=None
        self.mates=[] # list of pieces
        self.group=0
        self.cx0=0; self.cy0=0; self.cx=0; self.cy=0
        self.angle=0 # *-90 -> actual angle clockwise

class Jigsaw:
    def __init__(self):
        # next line layout dependent
        self.rect=pygame.Rect(g.sx(3.9),g.sy(5.2),g.sy(24.2),g.sy(11.5))
        d=.48
        self.frame_rect=pygame.Rect(g.sx(3.9-d),g.sy(5.2-d),g.sy(24.2+2*d),g.sy(11.5+2*d))
        self.total=NC*NR; self.margin=g.sy(.8); self.next_group=0
        self.pieces=[]; self.final=None
        for ind in range(self.total):
            pce=Piece(ind); self.pieces.append(pce)
        self.carry=None; self.dx=0; self.dy=0
        n=0
        for r in range(1,NR+1):
            for c in range(1,NC+1):
                mates=[]
                if r>1: mates.append(self.pieces[n-NC])
                if r<NR: mates.append(self.pieces[n+NC])
                if c>1: mates.append(self.pieces[n-1])
                if c<NC: mates.append(self.pieces[n+1])
                self.pieces[n].mates=mates
                n+=1
        self.ms=-1; self.unrotating=False
        s='1'; self.bcx=g.sx(25.1); self.bcy=g.sy(10.1)
        if g.journal: s=''; self.bcx=g.sx(22); self.bcy=g.sy(7.5)
        self.buttons=utils.load_image('buttons'+s+'.png',True)
        self.right_down=utils.load_image('right_down'+s+'.png',True)
        self.right_displaying=False; self.down=False
        self.rms=0; self.demo=0

    def setup(self,pj_n):
        self.pj_n=pj_n
        random.shuffle(self.pieces)
        self.carry=None; self.next_group=0
        fname=os.path.join('data',str(pj_n),'pieces.txt')
        try:
            f=open(fname, 'r')
        except:
            print 'Peter says unable to load '+fname
            return False
        for i in range(4): ignore=int(f.readline())
        n=0; factor=32.0/1200.0
        for ind in range(self.total):
            n+=1
            pce=self.pce_from_index(ind)
            pce.cx0=g.sx(factor*int(f.readline()))
            pce.cy0=g.sy(factor*int(f.readline()))
            img=utils.load_image(str(n)+'.png',True,str(pj_n))
            if img==None: return False
            if img==None:
                print 'Peter says unable to load data/'+str(pj_n)+'/'+str(n)+'.png'
                return False
            pce.img=img; pce.rotated=None
            pce.group=0
            pce.angle=random.randint(0,3)
            if pce.angle>0:
                pce.rotated=pygame.transform.rotate(pce.img,-pce.angle*90)
        try:
            g.red=int(f.readline())
            g.green=int(f.readline())
            g.blue=int(f.readline())
        except:
            pass
        f.close
        self.layout()
        self.final=None
        self.ms=-1; self.unrotating=False; self.unrotate_time=500
        if g.success>2: self.unrotate_time=50
        if g.success<3:
            self.demo=random.randint(11,14)
            pce=self.pieces[self.demo]
            pygame.mouse.set_pos([pce.cx,pce.cy])
            self.right_displaying=True
            self.rms=pygame.time.get_ticks()+500 # need time for mouse to settle
        return True

    def draw(self):
        if self.complete():
            g.screen.blit(self.final,self.rect)
            g.screen.blit(g.frame,self.frame_rect)
        else:
            grey=100
            pygame.draw.rect(g.screen,(grey,grey,grey),self.rect,2)
            if self.carry!=None:
                self.carry.cx=g.mx+self.dx; self.carry.cy=g.my+self.dy
                if self.carry.group>0: self.align(self.carry)
            for pce in self.pieces:
                img=pce.img
                if pce.angle>0: img=pce.rotated
                utils.centre_blit(g.screen,img,(pce.cx,pce.cy))
            if self.right_displaying:
                img=self.buttons
                if self.down: img=self.right_down
                utils.centre_blit(g.screen,img,(self.bcx,self.bcy))

    def pce_from_index(self,ind):
        for pce in self.pieces:
            if pce.ind==ind: return pce
        
    def solve(self):
        for pce in self.pieces:
            pce.cx=pce.cx0+self.rect[0]+1
            pce.cy=pce.cy0+self.rect[1]+1
            pce.group=1; pce.angle=0

    def top(self,pce):
        self.pieces.remove(pce)
        self.pieces.append(pce)

    def top_gp(self,gp):
        lst=utils.copy_list(self.pieces)
        for pce in lst:
            if pce.group==gp: self.top(pce)

    def which(self):
        l=utils.copy_list(self.pieces)
        for i in range(self.total):
            pce=l.pop()
            img=pce.img
            if pce.angle>0: img=pce.rotated
            if utils.mouse_on_img(img,(pce.cx,pce.cy)):
                if pce.group>0:
                    lst=utils.copy_list(self.pieces)
                    for pce1 in lst:
                        if pce1.group==pce.group: self.top(pce1)
                else:
                    self.top(pce)
                return pce
        return None

    def click(self):
        self.right_displaying=False
        if self.complete(): return False #****
        if self.carry:
            pce=self.carry
            self.carry=None # put down
            if pce.group==0:
                self.check(pce)
            else: # check all members of group
                self.check(pce)
                looking=True
                for i in range(100): # no infinite loop possibility
                    looking=False
                    for pce1 in self.pieces:
                        if pce1.group==pce.group:
                            if self.check(pce1): looking=True
                    if not looking:break
                if looking: print '>>>> avoided loop'
            if pce.group>0: self.top_gp(pce.group)
            self.align(pce)
            return True
        pce=self.which()
        if pce==None: return False
        # pick up
        self.carry=pce; self.dx=pce.cx-g.mx; self.dy=pce.cy-g.my
        return True

    def check(self,pce0):
        tf=False
        for pce in pce0.mates:
            if (pce0.group==pce.group) and pce.group>0: # already in same group
                pass
            elif pce0.angle<>pce.angle: # must be same angle to align
                pass
            else:
                dx0=abs(pce.cx0-pce0.cx0); dy0=abs(pce.cy0-pce0.cy0)
                dx=abs(pce.cx-pce0.cx); dy=abs(pce.cy-pce0.cy)
                if pce.angle in (1,3): dx,dy=dy,dx
                if abs(dx-dx0)<self.margin:
                    if abs(dy-dy0)<self.margin:
                        ok=True
                        # close enough - check if right place
                        angle=pce.angle
                        dind=utils.sign(pce.ind-pce0.ind)
                        dx=utils.sign(pce.cx-pce0.cx)
                        dy=utils.sign(pce.cy-pce0.cy)
                        if abs(pce.ind-pce0.ind)==1: # same row
                            if angle==0:
                                if dx<>dind: ok=False
                            elif angle==1:
                                if dy<>dind: ok=False
                            elif angle==2:
                                if dx<>-dind: ok=False
                            elif angle==3:
                                if dy<>-dind: ok=False
                        else: # same column
                            if angle==0:
                                if dy<>dind: ok=False
                            elif angle==1:
                                if dx<>-dind: ok=False
                            elif angle==2:
                                if dy<>-dind: ok=False
                            elif angle==3:
                                if dx<>dind: ok=False
                        if ok:
                            tf=True
                            if pce.group==0:
                                if pce0.group==0:
                                    self.next_group+=1
                                    pce.group=self.next_group
                                    pce0.group=self.next_group
                                else:
                                    pce.group=pce0.group
                            else:
                                if pce0.group==0:
                                    pce0.group=pce.group
                                else: # two separate groups
                                    for pce1 in self.pieces:
                                        if pce1.group==pce0.group:
                                            pce1.group=pce.group
        return tf

    def align(self,pce0):
        gp0=pce0.group; angle=pce0.angle
        if gp0>0:
            dddx=pce0.cx-pce0.cx0; dddy=pce0.cy-pce0.cy0
            for pce in self.pieces:
                if pce.group==gp0 and (pce<>pce0):
                    ddx=pce.cx0-pce0.cx0; ddy=pce.cy0-pce0.cy0
                    if angle==0: dx=ddx; dy=ddy
                    if angle==1: dx=-ddy; dy=ddx
                    if angle==2: dx=-ddx;dy=-ddy
                    if angle==3: dx=ddy;dy=-ddx
                    pce.angle=angle
                    if pce.angle>0:
                        a=-pce.angle*90
                        pce.rotated=pygame.transform.rotate(pce.img,a)
                    pce.cx=pce0.cx0+dx+dddx
                    pce.cy=pce0.cy0+dy+dddy

    def rotate(self): # response to right click
        if self.carry:
            pce=self.carry
        else:
            pce=self.which()
        if pce<>None:
            pce.angle+=1
            if pce.angle==4: pce.angle=0
            if pce.angle>0:
                pce.rotated=pygame.transform.rotate(pce.img,-pce.angle*90)
            self.align(pce)
            if self.carry:
                img=pce.img
                if pce.angle>0: img=pce.rotated
                if not utils.mouse_on_img(img,(pce.cx,pce.cy)):
                    self.carry=None # no longer on piece

    def complete(self):
        gp=0
        for pce in self.pieces:
            if pce.group==0: return False
            if gp==0:
                gp=pce.group
            else:
                if pce.group<>gp:return False
        if self.final==None:
            self.final=utils.load_image('final.jpg',False,str(self.pj_n))
            g.success+=1
            self.solve() # ensures angle=0
        return True

    def unrotate(self):
        if self.unrotating:
            d=pygame.time.get_ticks()-self.ms
            if self.ms==-1 or d<0 or d>=self.unrotate_time:
                g.redraw=True
                found=False
                for pce in self.pieces:
                    if pce.angle>0:
                        pce.angle+=1
                        if pce.angle==4: pce.angle=0
                        pce.rotated=pygame.transform.rotate(pce.img,-pce.angle*90)
                        found=True; break
                if found: self.ms=pygame.time.get_ticks()
                else: self.unrotating=False
            
    def all_rotated(self):
        for pce in self.pieces:
            if pce.angle>0: return False
        return True

    def right_button_display(self):
        if self.right_displaying:
            d=pygame.time.get_ticks()-self.rms
            if d>=500:
                g.redraw=True
                self.rms=pygame.time.get_ticks()
                self.down=not self.down
                if self.down:
                    self.carry=self.pieces[self.demo]
                    self.rotate(); self.carry=None
                if g.mx>0 and g.my>0:
                    pce=self.pieces[self.demo]
                    if not utils.mouse_on_img(pce.img,(pce.cx,pce.cy)):
                        self.right_displaying=False

# hard coded for 40 piece PJ
    def layout(self):
        ind=0
        y=g.sy(1.5); x0=g.sx(2); dx=g.sy(4); dy=g.sy(2.7)
        for r in range(8):
            x=x0
            for c in range(8):
                if r>1 and r<6 and c>0 and c<7:
                    pass
                else:
                    pce=self.pieces[ind]; pce.cx=x; pce.cy=y
                    ind+=1
                x+=dx
            y+=dy

    def debug(self):
        print '****'
        for p in self.pieces:
            print str(p.ind)+'-'+str(p.group),
        print

                    
                
            
        
        

            
            
        
