# g.py - globals
import pygame,utils,random

app='PJ'; ver='1.0'
ver='1.1'
# Jigsaw.check() ensures close pieces are in right place as well
# includes complete() & final pic
# journal read/write - g.success = # of successes
ver='2.0'
# unrotate button presentation - smilies on jigsaw pieces
# non XO mouse pic
# fancy effect on solution
# menu
ver='2.1'
# g.py - fixed double def of offset
# 20 jigsaws
# bgd always cyan
ver='2.2'
# no infinite loop possibility in check()
# added wait smiley
# made sure game.success tracked g.success
# added g.success display @ complete
# negative cursor on pick up
ver='2.3'
# added g.success display @ menu
ver='3.0'
# redraw implemented
ver='3.1'
# save.dat -> pj.dat
ver='3.2'
# dropped the disappearing cursor @ top

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,pointer,font1,font2,clock
    global factor,offset,imgf,message,version_display,frame_rate
    redraw=True
    version_display=False; frame_rate=0
    screen = pygame.display.get_surface()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    pygame.mouse.set_visible(False)
    pygame.display.set_caption(app)
    clock=pygame.time.Clock()
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    if pygame.font:
        t=int(60*imgf); font1=pygame.font.Font(None,t)
        t=int(40*imgf); font2=pygame.font.Font(None,t)
    pointer=utils.load_image('pointer.png',True)
    message=''
    (mx,my)=pygame.mouse.get_pos() # used by utils.mouse_on_img()
    
    # this activity only
    global red,green,blue,success,smiley1,smiley2,smiley1_x,smiley2_x,smiley_y
    global bgd,frame,state,menu,wait,negative
    red=0; green=0; blue=100; success=0
    smiley1=utils.load_image('smiley1.png',True)
    smiley2=utils.load_image('smiley2.png',True)
    offset1=4; smiley1_x=sx(16-offset1); smiley2_x=sx(16+offset1)
    smiley_y=sy(13.5)
    bgd=utils.load_image('bgd.jpg',False)
    frame=utils.load_image('frame.png',True)
    wait=utils.load_image('wait.png',True)
    negative=utils.load_image('negative.png',True)
    state=1 #1=menu, 2=require setup of jigsaw_n, 3=jigsaw
    menu=[]
    for ind in range(20):
        n=ind+1
        img=utils.load_image('menu.jpg',False,str(n))
        menu.append(img)

def sx(f): # scale x function
    return int(f*factor+offset+.5)

def sy(f): # scale y function
    return int(f*factor+.5)



