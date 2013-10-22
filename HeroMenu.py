import os
import sys
import random
from direct.gui.DirectGui import * 
import direct.directbase.DirectStart 
from direct.actor.Actor import Actor
from direct.task import Task
from math import pi, sin, cos
from pandac.PandaModules import *
from direct.showbase import DirectObject
from Global import *

class HeroMenu:
    def __init__(self):
        self.icons=('ColdArrows','Blue','Cleave','ChaosGrunt','Centaur')
        self.nexticon=0
        self.previcon=0
        self.index=0
        self.txt1=OnscreenText(text='',scale=0.09,fg=(1,1,1,1)) # must remove this
        self.txt2=OnscreenText(text='',scale=0.09,fg=(1,1,1,1),pos=(0.1,0,0)) # must remove this
        self.tavern=OnscreenText(text='',scale=0.09,fg=(1,1,1,1))
        self.HInode = aspect2d.attachNewNode("skills")
        self.BTNnode = aspect2d.attachNewNode("buttons")
        self.HInode.setTransparency(1) 
        self.BTNnode.setTransparency(1) 
        self.next=DirectButton(text ="Next",text_fg=(0,0.2,0,1),parent=self.HInode,text_pos=(0.05,-0.15),text_scale=0.70,image=(MYDIRIMG+"btnof.png",MYDIRIMG+"btnon.png",MYDIRIMG+"btnon.png",None),frameColor=(0,0,0,0),pos=(1.2,0,0.90),image_scale=(1.0,0,0.7),scale=(0.15,0,0.10),command=self.CreateButtons,extraArgs=[1]) 
        self.prev=DirectButton(text ="Previous",text_fg=(0,0.2,0,1),parent=self.HInode,text_pos=(0.05,-0.15),text_scale=0.70,image=(MYDIRIMG+"btnof.png",MYDIRIMG+"btnon.png",MYDIRIMG+"btnon.png",None),frameColor=(0,0,0,0),pos=(-1.2,0,0.90),image_scale=(1.0,0,0.7),scale=(0.15,0,0.10),command=self.CreateButtons,extraArgs=[-1])
        self.Create()
        #self.CreateButtons(0)
        
        
    def Create(self):
        self.Hero1=Actor(MYDIRMODEL+"/ralph", {"run": MYDIRMODEL+"/ralph-run"}) #MYDIRMODEL+"gar.x"
        self.Hero1.setScale(0.5)      
        self.Hero1.setPos(0,0,3.5)
        self.Hero1.setH(12)
        self.Hero1.setTransparency(1)
       # self.Hero1.setColor(0,1,1,1)
        self.Hero1.reparentTo(render)
        self.Hero1.loop("run")
     
    def CreateButtons(self,arg):
        if self.index<=105:
           if self.next==None:
              self.next=DirectButton(text ="Next",text_fg=(0,0.2,0,1),parent=self.HInode,text_pos=(0.05,-0.15),text_scale=0.70,image=(MYDIRIMG+"btnof.png",MYDIRIMG+"btnon.png",MYDIRIMG+"btnon.png",None),frameColor=(0,0,0,0),pos=(1.2,0,0.90),image_scale=(1.0,0,0.7),scale=(0.15,0,0.10),command=self.CreateButtons,extraArgs=[1]) 
           self.BTNnode.detachNode()
           self.BTNnode = aspect2d.attachNewNode("buttons")
           self.nexticon+=arg
        if self.nexticon>7:
           self.next.destroy()
           self.next=None
           
        if self.nexticon==0:
           self.index=-1
           self.prev.destroy()
           self.prev=None
        else:
           self.index=12*self.nexticon
           if self.prev==None:
              self.prev=DirectButton(text ="Previous",text_fg=(0,0.2,0,1),parent=self.HInode,text_pos=(0.05,-0.15),text_scale=0.70,image=(MYDIRIMG+"btnof.png",MYDIRIMG+"btnon.png",MYDIRIMG+"btnon.png",None),frameColor=(0,0,0,0),pos=(-1.2,0,0.90),image_scale=(1.0,0,0.7),scale=(0.15,0,0.10),command=self.CreateButtons,extraArgs=[-1])
        for i in range (0,3):
             for j in range (0,4):
                 if self.index>=105:
                    break 
                 self.index+=1 
                 if icons[self.index]==None:
                    continue
                 self.heroButton(-1.8+j*0.1,-i*0.1,self.index)
        self.txt1.setText(str(self.index))      # must remove this
        self.txt2.setText(str(self.nexticon))     # must remove this                                # Took me 1hr 30mins to figure next and prev buttons 31/7/2010
       
         
    def setHero(self,arg):
        self.Hero1.remove()
        self.Hero1=loader.loadModel(MYDIRMODEL+models[arg])
        self.Hero1.setHpr(12,280,90)
        self.Hero1.setScale(0.03)       
        self.Hero1.setPos(0,0,3.5)
        self.Hero1.reparentTo(render)
        for i in range (0,4):
            self.heroSkill(-2.6+i*0.85,-0.8,i)
            self.heroText("Skill %d"%(i+1),-2.4+i*0.85,-0.8)
            for j in range (0,4):
                self.heroText("Level %d:"%(j+1),-2.375+i*0.85,-0.8-(j+1)*0.07)

    def heroButton(self,x,y,arg):
        DirectButton(text="",text_font=font,parent=self.BTNnode,image=MYDIRICONS+icons[arg]+'.tga',frameColor=(0,0,0,0),pad=(-0.1,-0.1),image_scale=(IconSx+0.2,0,IconSy+0.2),pos=(posx-0.5+x,0,posy+y),scale=(0.20,0,0.20),command=self.setHero,extraArgs=[arg])

    def heroSkill(self,x,y,arg):
        OnscreenImage(image=self.icons[arg]+'.tga',parent=self.HInode,pos=(posx+x,0,posy+y),scale=biconscale)

    def heroText(self,text,x,y):
        DirectLabel(text=text,text_fg =(1,1,1,1),text_font=font,frameColor=(0,0,0,0),parent=self.HInode,pos=(posx+x,0,posy+y),scale=SKtxt)

    def Img1(self,loc,x,y,m,n):
        OnscreenImage(image =os.path.join('Glues',loc+'.jpg'), parent =self.panel,pos = ((X+x)*m,0,(Y+y)*n), scale = (Sx,0,Sy))
    
    def Img2(self,loc,x,y,m,n):
        OnscreenImage(image =os.path.join('Glues',loc+'.jpg'),parent =self.panel,pos = ((Tx+x)*m,0,(Ty+y)*n), scale = (Tsx,0,Tsy))
    
    def Img3(self,loc,x,y,m,n,s1,s2):
        OnscreenImage(image =os.path.join('Glues',loc+'.jpg'),parent =self.panel, pos = ((X+x)*m,0,(Y+y)*n), scale = (0+s1,0,0+s2))    #comma makes slash and plus joins
        
    def Text1(self,text,x,y,n):
        OnscreenText(text =text ,fg =(1,1,0,1),font=font,parent=self.panel,pos =((X+x)*n,(Y+y)*n),scale = Sc)
    def Text2(self,text,var,x,y,n):
        return DirectLabel(text =text %(var) ,text_font=font,text_fg =(1,1,1,1),frameColor=(0,0,0,0),parent=self.panel,pos =((X+x)*n,0,(Y+y)*n),scale = Sc)
    def Text3(self,text,var,x,y,n):
        return DirectLabel(text =text %(var) ,text_font=font,text_fg =(0,0.2,0,1),frameColor=(0,0,0,0),parent=self.panel,pos =((X+x)*n,0,(Y+y)*n),scale = Sc)
    def HeroSkillBTN(self,x,y,arg):
        DirectButton(image=self.skillicons[arg]+'.tga',parent=self.SKNode,pos=(posx+x,0,posy+y),pad=(-0.1,-0.1),scale=biconscale,command=self.SkillNo,extraArgs=[arg])

        
    def __del__(self):
        self.Hero1.reparentTo(hidden) 
        self.HInode.detachNode()
        self.BTNnode.detachNode()