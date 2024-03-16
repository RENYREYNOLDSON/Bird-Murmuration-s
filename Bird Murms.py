
import pygame,sys,random,math
from pygame.locals import*

pygame.init()

infoObject=pygame.display.Info()
screen=pygame.display.set_mode((1600,900))
pygame.display.set_caption("Boids")
clock=pygame.time.Clock()


skyImage=pygame.image.load("sky.jpg").convert()
skyImage=pygame.image.load("fishBackground.jpg").convert()
waterImage=pygame.image.load("water.png").convert_alpha()

redFish=pygame.image.load("red.png").convert_alpha()
greenFish=pygame.image.load("green.png").convert_alpha()
purpleFish=pygame.image.load("purple.png").convert_alpha()
yellowFish=pygame.image.load("yellow.png").convert_alpha()

font1 = pygame.font.Font('freesansbold.ttf', 15)##font 

#Variables
mousex,mousey=0,0
clicked=False

maxSpeed= 5

minDistance= 200

birdCount= 40

sizex = 10
sizey = 10

redCohesion=600
redAlignment=400
redSeperation=8
redSpeed=5

greenCohesion=600
greenAlignment=400
greenSeperation=8
greenSpeed=5

purpleCohesion=600
purpleAlignment=400
purpleSeperation=8
purpleSpeed=5

yellowCohesion=600
yellowAlignment=400
yellowSeperation=8
yellowSpeed=5



cohesionStrength= 700#Lower Stronger

alignmentStrength= 400#Lower Stronger

seperationStrength= 4#Lower Stronger


class Slider():
    def __init__(self,value,minimum,maximum,colour):
        self.value=value
        self.min=minimum
        self.max=maximum
        self.colour=colour
    def draw(self,x,y,width,height):
        pygame.draw.rect(screen,self.colour,(x,y,width,height),0)#Draws shape of slider
        pygame.draw.rect(screen,(0,0,0),(x,y,width,height),2)

        pygame.draw.circle(screen,(0,0,0),(int(x+width*((self.value-self.min)/(self.max-self.min))),int(y+height/2)),int(height/2))#Draws ball in correct location on the slider

        ##Setting a hold to the value of the variable
        if collide(mousex,mousey,x,y,width,height):
            if clicked==True:
                self.value=self.min+(mousex-x)*(self.max-self.min)/width
            infoText=font1.render(str("%.1f"%self.value),True,(0,0,0))
            screen.blit(infoText,(x+width+5,y))
        return self.value



class Bird:
    def __init__(self,colour):
        self.x=random.randint(100,1500)
        self.y=random.randint(200,800)
        self.xvel=random.randint(-10,10)
        self.yvel=random.randint(-10,10)
        self.image=colour

        number=random.randint(0,20)
        self.colour=(number,number,number)

    def move(self):
        self.x+=self.xvel
        self.y+=self.yvel

    def draw(self):
        #pygame.draw.rect(screen,self.colour,(self.x,self.y,sizex,sizey),0)

        
        angle=math.atan2(self.xvel,self.yvel)

        newImg=pygame.transform.rotate(self.image,math.degrees(angle)+90)
        screen.blit(newImg,(self.x,self.y))


class BirdRed(Bird):
    def boids(self):
        local=[]
        closest=None
        totalx=0
        totaly=0
        totalxvel=0
        totalyvel=0
        close=0
        for bird in redArray:#Get birds in their range
            dist=math.sqrt((bird.x-self.x)**2+(bird.y-self.y)**2)
            if dist<minDistance:#100 is current range
                totalx+=bird.x
                totaly+=bird.y
                totalxvel+=bird.xvel
                totalyvel+=bird.yvel
                close+=1
                if dist<20 and (self.x!=bird.x and self.y!=bird.y):
                    closest=bird


        avgX=totalx/close
        avgY=totaly/close
        avgxvel=totalxvel/close
        avgyvel=totalyvel/close
        #Moving toward with a strength factor
        self.xvel-=(self.x-avgX)/redCohesion
        self.yvel-=(self.y-avgY)/redCohesion
        self.xvel+=avgxvel/redAlignment
        self.yvel+=avgyvel/redAlignment
        if closest!=None:
            self.xvel+=(self.x-closest.x)/redSeperation
            self.yvel+=(self.y-closest.y)/redSeperation


                          #Move away from birds  SEPERATION

                          #Head to direction     ALIGNMENT

                          #Move from edge of window
        if self.x<100:
            self.xvel+=10*(5/self.x)

        elif self.x>1400:
            self.xvel+=10*(5/(1400-self.x))

        if self.y<220:
            self.yvel+=10*(5/self.y)

        elif self.y>800:
            self.yvel+=10*(5/(800-self.y))

        if self.xvel>redSpeed:
            self.xvel=redSpeed
        elif self.xvel<-redSpeed:
            self.xvel=-redSpeed

        if self.yvel>redSpeed:
            self.yvel=redSpeed
        elif self.yvel<-redSpeed:
            self.yvel=-redSpeed


class BirdYellow(Bird):
    def boids(self):
        local=[]
        closest=None
        totalx=0
        totaly=0
        totalxvel=0
        totalyvel=0
        close=0
        for bird in yellowArray:#Get birds in their range
            dist=math.sqrt((bird.x-self.x)**2+(bird.y-self.y)**2)
            if dist<minDistance:#100 is current range
                totalx+=bird.x
                totaly+=bird.y
                totalxvel+=bird.xvel
                totalyvel+=bird.yvel
                close+=1
                if dist<20 and (self.x!=bird.x and self.y!=bird.y):
                    closest=bird



        avgX=totalx/close
        avgY=totaly/close
        avgxvel=totalxvel/close
        avgyvel=totalyvel/close
        #Moving toward with a strength factor
        self.xvel-=(self.x-avgX)/yellowCohesion
        self.yvel-=(self.y-avgY)/yellowCohesion
        self.xvel+=avgxvel/yellowAlignment
        self.yvel+=avgyvel/yellowAlignment
        if closest!=None:
            self.xvel+=(self.x-closest.x)/yellowSeperation
            self.yvel+=(self.y-closest.y)/yellowSeperation

                          #Move away from birds  SEPERATION

                          #Head to direction     ALIGNMENT

                          #Move from edge of window
        if self.x<100:
            self.xvel+=10*(5/self.x)

        elif self.x>1400:
            self.xvel+=10*(5/(1400-self.x))

        if self.y<220:
            self.yvel+=10*(5/self.y)

        elif self.y>800:
            self.yvel+=10*(5/(800-self.y))

        if self.xvel>yellowSpeed:
            self.xvel=yellowSpeed
        elif self.xvel<-yellowSpeed:
            self.xvel=-yellowSpeed

        if self.yvel>yellowSpeed:
            self.yvel=yellowSpeed
        elif self.yvel<-yellowSpeed:
            self.yvel=-yellowSpeed


class BirdGreen(Bird):
    def boids(self):
        local=[]
        closest=None
        totalx=0
        totaly=0
        totalxvel=0
        totalyvel=0
        close=0
        for bird in greenArray:#Get birds in their range
            dist=math.sqrt((bird.x-self.x)**2+(bird.y-self.y)**2)
            if dist<minDistance:#100 is current range
                totalx+=bird.x
                totaly+=bird.y
                totalxvel+=bird.xvel
                totalyvel+=bird.yvel
                close+=1
                if dist<20 and (self.x!=bird.x and self.y!=bird.y):
                    closest=bird



        avgX=totalx/close
        avgY=totaly/close
        avgxvel=totalxvel/close
        avgyvel=totalyvel/close
        #Moving toward with a strength factor
        self.xvel-=(self.x-avgX)/greenCohesion
        self.yvel-=(self.y-avgY)/greenCohesion
        self.xvel+=avgxvel/greenAlignment
        self.yvel+=avgyvel/greenAlignment
        if closest!=None:
            self.xvel+=(self.x-closest.x)/greenSeperation
            self.yvel+=(self.y-closest.y)/greenSeperation

                          #Move away from birds  SEPERATION

                          #Head to direction     ALIGNMENT

                          #Move from edge of window
        if self.x<100:
            self.xvel+=10*(5/self.x)

        elif self.x>1400:
            self.xvel+=10*(5/(1400-self.x))

        if self.y<220:
            self.yvel+=10*(5/self.y)

        elif self.y>800:
            self.yvel+=10*(5/(800-self.y))

        if self.xvel>greenSpeed:
            self.xvel=greenSpeed
        elif self.xvel<-greenSpeed:
            self.xvel=-greenSpeed

        if self.yvel>greenSpeed:
            self.yvel=greenSpeed
        elif self.yvel<-greenSpeed:
            self.yvel=-greenSpeed


class BirdPurple(Bird):
    def boids(self):
        local=[]
        closest=None
        totalx=0
        totaly=0
        totalxvel=0
        totalyvel=0
        close=0
        for bird in purpleArray:#Get birds in their range
            dist=math.sqrt((bird.x-self.x)**2+(bird.y-self.y)**2)
            if dist<minDistance:#100 is current range
                totalx+=bird.x
                totaly+=bird.y
                totalxvel+=bird.xvel
                totalyvel+=bird.yvel
                close+=1
                if dist<20 and (self.x!=bird.x and self.y!=bird.y):
                    closest=bird



        avgX=totalx/close
        avgY=totaly/close
        avgxvel=totalxvel/close
        avgyvel=totalyvel/close
        #Moving toward with a strength factor
        self.xvel-=(self.x-avgX)/purpleCohesion
        self.yvel-=(self.y-avgY)/purpleCohesion
        self.xvel+=avgxvel/purpleAlignment
        self.yvel+=avgyvel/purpleAlignment
        if closest!=None:
            self.xvel+=(self.x-closest.x)/purpleSeperation
            self.yvel+=(self.y-closest.y)/purpleSeperation

                          #Move away from birds  SEPERATION

                          #Head to direction     ALIGNMENT

                          #Move from edge of window
        if self.x<100:
            self.xvel+=10*(5/self.x)

        elif self.x>1400:
            self.xvel+=10*(5/(1400-self.x))

        if self.y<220:
            self.yvel+=10*(5/self.y)

        elif self.y>800:
            self.yvel+=10*(5/(800-self.y))

        if self.xvel>purpleSpeed:
            self.xvel=purpleSpeed
        elif self.xvel<-purpleSpeed:
            self.xvel=-purpleSpeed

        if self.yvel>purpleSpeed:
            self.yvel=purpleSpeed
        elif self.yvel<-purpleSpeed:
            self.yvel=-purpleSpeed

            

def collide(checkx,checky,x,y,w,h):
    if checkx>x and checkx<x+w and checky>y and checky<y+h:
        return True
    else:
        return False
            

def process():
    if collide(mousex,mousey,100,0,50,40):
        for i in redArray:
            i.draw()
            i.move()
            i.boids()

    elif collide(mousex,mousey,250,0,50,40):
        for i in greenArray:
            i.draw()
            i.move()
            i.boids()

    elif collide(mousex,mousey,400,0,50,40):
        for i in purpleArray:
            i.draw()
            i.move()
            i.boids()

    elif collide(mousex,mousey,550,0,50,40):
        for i in yellowArray:
            i.draw()
            i.move()
            i.boids()
    
    else:
        for i in redArray:
            i.draw()
            i.move()
            i.boids()

        for i in greenArray:
            i.draw()
            i.move()
            i.boids()

        for i in purpleArray:
            i.draw()
            i.move()
            i.boids()

        for i in yellowArray:
            i.draw()
            i.move()
            i.boids()



def gui():
    global redArray,greenArray,purpleArray,yellowArray

    global redCohesion,redAlignment,redSeperation,redSpeed
    global greenCohesion,greenAlignment,greenSeperation,greenSpeed
    global purpleCohesion,purpleAlignment,purpleSeperation,purpleSpeed
    global yellowCohesion,yellowAlignment,yellowSeperation,yellowSpeed
    
    pygame.draw.rect(screen,(200,0,0),(10,16,50,20),0)
    text=font1.render("Reset",True,(255,255,255))
    screen.blit(text,(12,18))
    if clicked==True:
        if collide(mousex,mousey,10,16,50,20):
            redArray=[]
            for i in range(birdCount):
                redArray.append(BirdRed(redFish))

            greenArray=[]
            for i in range(birdCount):
                greenArray.append(BirdGreen(greenFish))

            purpleArray=[]
            for i in range(birdCount):
                purpleArray.append(BirdPurple(purpleFish))

            yellowArray=[]
            for i in range(birdCount):
                yellowArray.append(BirdYellow(yellowFish))
            


    screen.blit(redFish,(100,0))

    screen.blit(greenFish,(250,0))

    screen.blit(purpleFish,(400,0))

    screen.blit(yellowFish,(550,0))

    text=font1.render("Cohesion",True,(0,0,0))#######red
    screen.blit(text,(90,40))
    redC=Slider(redCohesion,100,1000,(255,0,0))
    redCohesion=redC.draw(75,55,100,10)

    text=font1.render("Alignment",True,(0,0,0))
    screen.blit(text,(90,70))
    redA=Slider(redAlignment,0,1000,(255,0,0))
    redAlignment=redA.draw(75,85,100,10)

    text=font1.render("Seperation",True,(0,0,0))
    screen.blit(text,(90,100))
    redS=Slider(redSeperation,3,10,(255,0,0))
    redSeperation=redS.draw(75,115,100,10)

    text=font1.render("Max Speed",True,(0,0,0))
    screen.blit(text,(90,130))
    redS=Slider(redSpeed,1,10,(255,0,0))
    redSpeed=redS.draw(75,145,100,10)




    text=font1.render("Cohesion",True,(0,0,0))########green
    screen.blit(text,(240,40))
    greenC=Slider(greenCohesion,100,1000,(0,255,0))
    greenCohesion=greenC.draw(225,55,100,10)

    text=font1.render("Alignment",True,(0,0,0))
    screen.blit(text,(240,70))
    greenA=Slider(greenAlignment,0,1000,(0,255,0))
    greenAlignment=greenA.draw(225,85,100,10)

    text=font1.render("Seperation",True,(0,0,0))
    screen.blit(text,(240,100))
    greenS=Slider(greenSeperation,3,10,(0,255,0))
    greenSeperation=greenS.draw(225,115,100,10)

    text=font1.render("Max Speed",True,(0,0,0))
    screen.blit(text,(240,130))
    greenS=Slider(greenSpeed,1,10,(0,255,0))
    greenSpeed=greenS.draw(225,145,100,10)




    text=font1.render("Cohesion",True,(0,0,0))#######purple
    screen.blit(text,(390,40))
    purpleC=Slider(purpleCohesion,100,1000,(255,0,255))
    purpleCohesion=purpleC.draw(375,55,100,10)

    text=font1.render("Alignment",True,(0,0,0))
    screen.blit(text,(390,70))
    purpleA=Slider(purpleAlignment,0,1000,(255,0,255))
    purpleAlignment=purpleA.draw(375,85,100,10)

    text=font1.render("Seperation",True,(0,0,0))
    screen.blit(text,(390,100))
    purpleS=Slider(purpleSeperation,3,10,(255,0,255))
    purpleSeperation=purpleS.draw(375,115,100,10)

    text=font1.render("Max Speed",True,(0,0,0))
    screen.blit(text,(390,130))
    purpleS=Slider(purpleSpeed,1,10,(255,0,255))
    purpleSpeed=purpleS.draw(375,145,100,10)




    text=font1.render("Cohesion",True,(0,0,0))#####yellow
    screen.blit(text,(540,40))
    yellowC=Slider(yellowCohesion,100,1000,(255,255,0))
    yellowCohesion=yellowC.draw(525,55,100,10)

    text=font1.render("Alignment",True,(0,0,0))
    screen.blit(text,(540,70))
    yellowA=Slider(yellowAlignment,0,1000,(255,255,0))
    yellowAlignment=yellowA.draw(525,85,100,10)

    text=font1.render("Seperation",True,(0,0,0))
    screen.blit(text,(540,100))
    yellowS=Slider(yellowSeperation,3,10,(255,255,0))
    yellowSeperation=yellowS.draw(525,115,100,10)

    text=font1.render("Max Speed",True,(0,0,0))
    screen.blit(text,(540,130))
    yellowS=Slider(yellowSpeed,1,10,(255,255,0))
    yellowSpeed=yellowS.draw(525,145,100,10)
            


redArray=[]
for i in range(birdCount):
    redArray.append(BirdRed(redFish))

greenArray=[]
for i in range(birdCount):
    greenArray.append(BirdGreen(greenFish))

purpleArray=[]
for i in range(birdCount):
    purpleArray.append(BirdPurple(purpleFish))

yellowArray=[]
for i in range(birdCount):
    yellowArray.append(BirdYellow(yellowFish))

    

while True:
    screen.fill((255,255,255))
    screen.blit(skyImage,(0,0))
    
    process()
    #screen.blit(waterImage,(0,0)) # water for the water, too laggy due to opacity
    gui()

    clicked=False
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

        elif event.type==pygame.MOUSEMOTION:
            mousex,mousey=event.pos
        elif event.type==pygame.MOUSEBUTTONUP:
            clicked=True
    pygame.display.update()
    clock.tick(60)




#Currently just shows shoals of fish, need to add evolution


#Make each species evolve to see how they change


#Make them die due to 

##Found several glitches such as seperation not working and made it more efficient
##Lower a stat is the stronger it is, except speed. It is the reciprocal
#Ultra fast fish swarns can now be made
#Different stats could be used with ai to make them move from a predator
#May need form of communication

#Show how to make full shoals etc










    

    
    
