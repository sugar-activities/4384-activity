# utils.py
import g,pygame,os,random,copy

#constants
RED,BLUE,GREEN,BLACK,WHITE=(255,0,0),(0,0,255),(0,255,0),(0,0,0),(255,255,255)
CYAN,ORANGE,CREAM=(0,255,255),(255,165,0),(255,255,192)

def exit():
    save()
    pygame.display.quit()
    pygame.quit()
    sys.exit()

def save():
    dir=''
    dir=os.environ.get('SUGAR_ACTIVITY_ROOT')
    if dir==None: dir=''
    fname=os.path.join(dir,'data','pj.dat')
    f=open(fname, 'w')
    f.write(str(g.success)+'\n')
    f.close
    
def load():
    dir=''
    dir=os.environ.get('SUGAR_ACTIVITY_ROOT')
    if dir==None: dir=''
    fname=os.path.join(dir,'data','pj.dat')
    try:
        f=open(fname, 'r')
    except:
        return None #****
    try:
        g.success=int(f.readline())
    except:
        pass
    f.close
    
def version_display():
    g.message=g.app+' V '+g.ver
    g.message+='  '+str(g.screen.get_width())+' x '+str(g.screen.get_height())+' '+str(g.h)
    g.message+='  '+str(g.frame_rate)+'fps'
    message(g.screen,g.font1,g.message)
    
# loads an image (eg pic.png) from the data subdirectory
# converts it for optimum display
# resizes it using the image scaling factor, g.imgf
#   so it is the right size for the current screen resolution
#   all images are designed for 1200x900
def load_image(file1,alpha=False,subdir=''): # eg subdir='glow'
    data='data'
    if subdir!='': data=os.path.join('data',subdir)
    fname=os.path.join(data,file1)
    try:
        img=pygame.image.load(fname)
    except:
        print "Peter says: Can't find "+fname; return None
    if alpha:
        img=img.convert_alpha()
    else:
        img=img.convert()
    if abs(g.imgf-1.0)>.1: # only scale if factor <> 1
        w=img.get_width(); h=img.get_height()
        try: # allow for less than 24 bit images
            img=pygame.transform.smoothscale(img,(int(g.imgf*w),int(g.imgf*h)))
        except:
            img=pygame.transform.scale(img,(int(g.imgf*w),int(g.imgf*h)))
    return img
        
# eg new_list=copy_list(old_list)
def copy_list(l):
    new_list=[];new_list.extend(l)
    return new_list

def centre_blit(screen,img,(cx,cy),angle=0): # rotation is clockwise
    img1=img
    if angle!=0: img1=pygame.transform.rotate(img,-angle)
    rect=img1.get_rect()
    screen.blit(img1,(cx-rect.width/2,cy-rect.height/2))
    
# m is the message
# d is the # of pixels in the border around the text
# (cx,cy) = co-ords centre - (0,0) means use screen centre
def message(screen,font,m,(cx,cy)=(0,0),d=20):
    if m!='':
        if pygame.font:
            text=font.render(m,True,(255,255,255))
            shadow=font.render(m,True,(0,0,0))
            rect=text.get_rect();
            if cx==0: cx=screen.get_width()/2
            if cy==0: cy=screen.get_height()/2
            rect.centerx=cx;rect.centery=cy
            bgd=pygame.Surface((rect.width+2*d,rect.height+2*d))
            bgd.fill((0,255,255))
            bgd.set_alpha(128)
            screen.blit(bgd,(rect.left-d,rect.top-d))
            screen.blit(shadow,(rect.x+2,rect.y+2,rect.width,rect.height))
            screen.blit(text,rect)

def mouse_on_img(img,(cx,cy)):
    mx=g.mx; my=g.my
    w2=img.get_width()/2; dx=cx-w2; x=mx-dx
    h2=img.get_height()/2; dy=cy-h2; y=my-dy
    if mx<(cx-w2): return False
    if mx>(cx+w2): return False
    if my<(cy-h2): return False
    if my>(cy+h2): return False
    try: # in case out of range
        col=img.get_at((int(x),int(y)))
    except:
        return False
    if col[3]<10: return False
    return True
            
def mouse_in(x1,y1,x2,y2):
    (mx,my)=pygame.mouse.get_pos()
    if x1>mx: return False
    if x2<mx: return False
    if y1>my: return False
    if y2<my: return False
    return True

def display_number(n,(x,y),font,colour=CREAM,bgd=None):
    if pygame.font:
        if bgd==None:
            text=font.render(str(n),True,colour)
        else:
            text=font.render(str(n),True,colour,bgd)
        g.screen.blit(text,(x,y))

def text_blit1(screen,s,font,(x,y),(r,g,b)):
    text=font.render(s,True,(r,g,b))
    rect=text.get_rect(); rect.x=x; rect.y=y
    screen.blit(text,rect)

def sign(n):
    if n<0: return -1
    return 1
