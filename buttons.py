# buttons.py
import g,utils,pygame

class Button:
    _instances=[]
    
    def __init__(self,name,(x1,y1),centre=True): # eg ('plus',(30,40))
        self._instances.append(self)
        up=utils.load_image(name+"_up.png",True)
        down=utils.load_image(name+"_down.png",True)
        w=up.get_width();h=up.get_height();x=x1;y=y1
        if centre: x=x-w/2; y=y-h/2
        self.rect=pygame.Rect(x,y,w,h)
        self.name=name; self.x=x; self.y=y; self.active=True
        self.up=up; self.down=down

    def mouse_on(self):
        (mx,my)=pygame.mouse.get_pos()
        return self.rect.collidepoint(mx,my)

    def draw_up(self):
        g.screen.blit(self.up,(self.x,self.y))

    def draw_down(self):
        g.screen.blit(self.down,(self.x,self.y))

    def on(self):
        self.active=True

    def off(self):
        self.active=False

def draw():
    for b in Button._instances:
        if b.active: b.draw_up()

def check():
    for b in Button._instances:
        if b.active:
            if b.mouse_on():
                b.draw_down()
                pygame.display.flip()
                pygame.time.wait(300)
                return b.name #****
    return '' # no button pressed

def active(name):
    for b in Button._instances:
        if b.name==name: return b.active #****
    return False # not found

# eg1 buttons.on('plus')
# eg2 buttons.on(['plus','times'])
def on(name):
    if type(name)==type('a'):
        list1=[]; list1.append(name)
    else:
        list1=name
    for b in Button._instances:
        if b.name in list1: b.active=True

# eg1 buttons.off('plus')
# eg2 buttons.off(['plus','times'])
def off(name):
    if type(name)==type('a'):
        list1=[]; list1.append(name)
    else:
        list1=name
    for b in Button._instances:
        if b.name in list1: b.active=False

