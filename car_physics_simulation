
import pygame
import math

class Envir:
    def __init__(self,dimentions):
        self.black=(0,0,0)
        self.white=(250,250,250)
        self.grey=(150,150,150)
        self.green=(0,250,10)
        self.blue=(0,0,250)
        self.red=(250,0,0)

        self.height=dimentions[0]
        self.width=dimentions[1]
        pygame.display.set_caption('car robot simulator')
        self.map=pygame.display.set_mode((self.width,self.height))

        self.font=pygame.font.Font('freesansbold.ttf',20)
        self.text=self.font.render('default',True,self.black,self.white)

        self.textRect=self.text.get_rect()
        self.textRect.center=(dimentions[1]-400, dimentions[0]-100)

        self.text2=self.font.render('default',True,self.black,self.white)
        self.textRect2=self.text2.get_rect()
        self.textRect2.center=(dimentions[1]-400, dimentions[0]-150)

        self.text3=self.font.render('default',True,self.black,self.white)
        self.textRect3=self.text3.get_rect()
        self.textRect3.center=(dimentions[1]-400, dimentions[0]-70)

        self.text4=self.font.render('default',True,self.black,self.white)
        self.textRect4=self.text4.get_rect()
        self.textRect4.center=(dimentions[1]-400, dimentions[0]-50)

        self.trail_set=[]

    def write_info(self,vl,vr,theta):
        txt=f"vl ={vl} vr={vr} Phi={int(math.degrees(theta))}" 
        self.text=self.font.render(txt,True,self.black,self.white)
        self.map.blit(self.text,self.textRect)

        txt2=f'Parameter Tracking:'
        self.text2=self.font.render(txt2,True,self.grey,self.white)
        self.map.blit(self.text2,self.textRect2)

        txt3=f'x={robot.x}'
        self.text3=self.font.render(txt3,True,self.black,self.white)
        self.map.blit(self.text3,self.textRect3)

        txt4=f'y={robot.y}'
        self.text4=self.font.render(txt4,True,self.black,self.white)
        self.map.blit(self.text4,self.textRect4)

    def trail(self,pos):
        for i in range(0,len(self.trail_set)-1):
            pygame.draw.line(self.map,self.grey,(self.trail_set[i][0],self.trail_set[i][1]),
            (self.trail_set[i+1][0],self.trail_set[i+1][1]))
        if self.trail_set.__sizeof__()>40000:
            self.trail_set.pop(0)
        self.trail_set.append(pos)


class Robot:
    def __init__(self,startpos,robotImg,width):
         self.m2p=3779.52
         self.w=width
         self.x=startpos[0]
         self.y=startpos[1]
         self.theta=0
         self.vl=0.01*self.m2p 
         self.vr=0.01*self.m2p
         self.img=pygame.image.load(robotImg)
         self.rotated=self.img
         self.rect=self.rotated.get_rect(center=(self.x,self.y))

    def draw(self,map):
         map.blit(self.rotated,self.rect)

    def move(self,event=None):
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.vl+=0.001*self.m2p
                elif event.key == pygame.K_a:
                    self.vl-=0.001*self.m2p
                elif event.key == pygame.K_e:
                    self.vr+=0.001*self.m2p
                elif event.key == pygame.K_d:
                    self.vr-=0.001*self.m2p

        self.x+=((self.vl+self.vr)/2)*math.cos(self.theta)*dt
        self.y-=((self.vl+self.vr)/2)*math.sin(self.theta)*dt
        self.theta+=(self.vr-self.vl)/self.w*dt

        if self.theta>2*math.pi or self.theta<-2*math.pi:
            self.theta=0

        self.rotated=pygame.transform.rotozoom(self.img, math.degrees(self.theta),1)
        self.rect =self.rotated.get_rect(center=(self.x,self.y))

pygame.init()

start=(200,200)
dims=(800,1200)

run=True
        
environment = Envir(dims)
     
robot=Robot(start,r'C:\Users\Mike Cheuk\source\repos\Revised Simulator\robot.png',0.02116*3779.52)

dt=0
lasttime = pygame.time.get_ticks()

while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run=False
        robot.move(event)

    dt=(pygame.time.get_ticks()-lasttime)/1000
    lasttime = pygame.time.get_ticks()

    environment.map.fill(environment.white)
    environment.write_info(int(robot.vl),int(robot.vr),robot.theta)
    environment.trail((robot.x,robot.y))
    robot.move()
    robot.draw(environment.map)

    pygame.display.update()    
