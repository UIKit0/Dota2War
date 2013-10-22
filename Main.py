#This is the menu class that creates the scene
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
from HeroMenu import HeroMenu
from ExitMenu import ExitMenu
from World import World
                    
class MainMenu:
    def __init__(self):
        self.World=None
        self.Info=None
        self.Credits=None
        self.Exit=None
        self.back=None
        self.images=('Menu.jpg','line.jpg','w2.png','w1.png','chain.png')
        self.FirstScreen()
        self.LoadLights()
    
    def FirstScreen(self):
        self.Menu=aspect2d.attachNewNode("MainMenu")
        self.Menu.setTransparency(1)
        self.menuButton("Start",0,1)
        self.menuButton("RPG",-0.21,2)
        self.menuButton("Hero Info",-0.42,3)
        self.menuButton("Credits",-0.62,4)
        self.menuButton("Exit",-0.83,5)
        self.menuImage(1,1.56,0,0.0459,1)
        self.menuImage(1,-1.55,0,0.0459,1)            
        self.menuImage(2,1.32,-0.9,0.2,0.15)
        self.menuImage(3,-1.32,-0.9,0.2,0.15)
        self.bg =loader.loadModel(MYDIRMODEL+'environment')
        self.bg.reparentTo(render)
        self.bg.setScale(0.25, 0.25, 0.25)        
        self.bg.setPos(-8, 50, -3)
        taskMgr.add(self.spinCameraTask,"spin")
        
        if self.back !=None:
           self.back.destroy()
        
    def LoadLights(self):
        self.sun = DirectionalLight('sun')
        self.sun.setColor(VBase4(1,1,1,1))
        self.sun_node = render.attachNewNode(self.sun)
        self.sun_node.setHpr(0, -10, 0)
        render.setLight(self.sun_node)
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.12, 0.12, 0.12, 1))
        self.alnp = render.attachNewNode(alight)
        render.setLight(self.alnp)
    
    def DestroyLight(self):
        self.sun_node.detachNode()
        self.alnp.detachNode()
        
            
    def FirstScreenDestroy(self):
     #   self.DestroyLight()
        self.bg.remove()
        self.Menu.detachNode()
        taskMgr.remove('spin') 
    
    def NextScreen(self,index):
        self.FirstScreenDestroy()
        self.back = DirectButton(text ="Back",text_fg=(0,0.2,0,1),text_pos=(0.05,-0.15),text_scale=0.70,image=(MYDIRIMG+"btnof.png",MYDIRIMG+"btnon.png",MYDIRIMG+"btnon.png",None),frameColor=(0,0,0,0),pos=(1.2,0,-0.90),image_scale=(1.0,0,0.7),scale=(0.15,0,0.10),command=self.Back,extraArgs=[index])
        self.back.setTransparency(1)
        if index==1:
           self.World=World()
           self.back.setPos(-1.0,0,-0.93)
           self.back['text']="Quit"
        if index==2:
            pass   
        if index==3:
           self.Info=HeroMenu()
        if index==4:
           self.names=DirectLabel(text="Author: pyros2097",pos=(0,0,0),scale=0.06,text_fg=(1,1,1,1),frameColor=(0,0,0,0))
        if index==5:
           self.Exit=sys.exit(0)
           self.Exit
           
    def Back(self,index):
        if index ==1:
           self.World.destroy()
        if index ==2:
           pass
        if index ==3:
           self.Info.__del__()
        if index ==4:
           self.names.destroy() 
        self.FirstScreen() 
     
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0                             #angle degrees increases like the task
        angleRadians = angleDegrees * (pi / 180.0)                 #angle radians is fixed to the interval (-1,1) because of function
        base.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)        
        base.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    def menuButton(self,text,y,arg):
        DirectButton(text =text,text_fg=btcolor,text_font=font,parent=self.Menu,text_pos=btpos,text_scale=btscale,image=bimages,frameColor=(0,0,0,0),pos=(bpos[0],bpos[1],bpos[2]+y),image_scale=biscale,scale=bscale,command=self.NextScreen,extraArgs=[arg]) 

    def menuImage(self,arg,x,y,sx,sy):
        OnscreenImage(image=MYDIRIMG+self.images[arg],parent=self.Menu,pos=(x,0,y),scale=(sx,0,sy))

    def menuText(self,text,y):
        OnscreenText(text=text,fg =(1,1,1,1),font=font,parent=self.Menu,pos=(posx,posy+y),scale=Scale)

if __name__ == '__main__':         
    #ExitMenu() 
    MainMenu()
    run()







