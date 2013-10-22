#This is the class that create's the creeps for each team and sets their starting position
#and their intervals.
#
#Unit.py
#
#
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.gui.DirectGui import * 
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.interval.LerpInterval import LerpPosInterval
from pandac.PandaModules import Point3
from Global import *

class Unit1:
    def __init__(self):
        self.x,self.y,self.z = 0,0,0
        self.lon=pi*(self.x+10)*(self.x+10)
        self.range=100
        self.mindamage=24
        self.maxdamage=27
        self.damage=range(self.mindamage,self.maxdamage)
        self.armor=3
        self.armortype=None
        self.res=0
        self.speed=290
        self.atkspeed=1.7
        self.maxhp=590
        self.curhp=590
        self.maxmp=290
        self.curmp=290
        self.model=loader.loadModel('panda.egg')
        self.model.reparentTo(render)
        self.model.setPos(15,15,15)
        self.model.setTag("Unit",'1')
        self.display()
        self.panel.detachNode()
        self.isdead=False
        if self.curhp == 0:
            self.isdead=True
       # taskMgr.add(self.TimeTask, "TimeTask") 
        taskMgr.add(self.update,"up")
    def display(self):
        self.panel=aspect2d.attachNewNode("panel")
        self.panel.setTransparency(1)
        self.HP=DirectLabel(text='',parent = self.panel,text_fg=(0,0.8,0,1),frameColor=(0,0,0,0),pos=(-0.3,0,-0.6),scale=Sc)
        self.MP=DirectLabel(text='',parent = self.panel,text_fg=(0,0,0.8,1),frameColor=(0,0,0,0),pos=(-0.3,0,-0.65),scale=Sc)
        Text1(self,"Damage",-0.26,-0.02,-1)
        self.DAM=Text2(self,"%d-%d",(self.mindamage,self.maxdamage),-0.26,0.03,-1)
        Text1(self,"Armor",-0.27,0.12,-1)
        self.ARM=Text2(self,"%d",self.armor,-0.26,0.17,-1)
        self.hpbar = DirectWaitBar(barColor=(0,0.6,0,1),parent = self.panel,scale=0.2, frameColor=(0,0,0,1),pos = (0,0,-0.6))
        self.mpbar=DirectWaitBar(barColor=(0,0,0.6,1),parent = self.panel,scale=0.2, frameColor=(0,0,0,1),pos = (0,0,-0.64))
        self.HP=DirectLabel(text='',parent = self.panel,text_fg=(0,0.8,0,1),frameColor=(0,0,0,0),pos=(-0.3,0,-0.6),scale=Sc)
        self.MP=DirectLabel(text='',parent = self.panel,text_fg=(0,0,0.8,1),frameColor=(0,0,0,0),pos=(-0.3,0,-0.65),scale=Sc)
        
    def displaynot(self):
        self.panel.detachNode()
    def setDamage(self,amt):
        if delta >1:
           self.damage+=delta
        else:
           self.damage=self.damage+self.damage*delta
         
        
    def hurt(self,amt):
         if self.curhp>0:
            if self.curhp<=self.maxhp:           
               self.curhp-=delta*0.50
    def hurtspell(self,delta):
          if self.curhp>0:
            if self.curhp<=self.maxhp:           
               self.curhp-=delta*self.res          
    def heal(self,delta):
        if self.curhp!=self.maxhp:
           if self.curhp < self.maxhp:                    
              self.curhp+=delta
        
    def replenish(self,delta):
        if self.curmp!=self.maxmp:
           if self.curmp < self.maxmp:
              if self.curmp>0:                    
                 self.curmp+=delta
              else:Error("No Mana") 
    def manacost(self,amt):
        if self.curmp>amt:
           self.curmp-=amt
        else:
            Error("No Mana")
                                
    def setSpeed(self,delta):
        if delta > 1:
           self.speed+=delta
        else:
           self.speed=self.speed+self.speed*delta 
    def setArmor(self,delta):            
        self.armor+=delta
    def setPos(self,x,y,z):
        self.model.setPos(x,y,z) 
    def getDamage(self):
        return self.damage
    def getPos(self):
        return self.model.getPos() 
    def getX(self):
        return self.model.getX()
    def getY(self):
        return self.model.getY()
    def getZ(self):
        return self.model.getZ()
    def getModel(self):
        return self.model
   
    def update(self,task):
        self.maxhp=590
        self.maxmp=290     
        self.hpbar['range']=int(self.maxhp)
        self.hpbar['value']=int(self.curhp)
        self.mpbar['range']=int(self.maxmp)
        self.mpbar['value']=int(self.curmp)
        self.HP['text']="HP"+str(int(self.curhp))+"/"+str(int(self.maxhp))
        self.MP['text']="MP"+str(int(self.curmp))+"/"+str(int(self.maxmp))
        self.DAM['text']=str(int(self.mindamage))+'-'+str(int(self.maxdamage))
        self.ARM['text']=str(int(self.armor))
        if self.curhp<=0:
           self.isDead=True
           self.model.detachNode()
           self.panel.detachNode()
        return task.cont
    
    def destroy(self):
        self.panel.detachNode()
        self.model.remove()
    def TimeTask(self,task):
        if self.timedt == int(task.time):
           self.startInterval()
           self.timedt+=30
        return task.cont
    def startInterval(self):
        self.trent = Actor("models/panda-model",{"walk": "models/panda-walk4"})
        self.trent.setPos(25,25,0)
        self.trent.setScale(0.01)
        self.trent.reparentTo(render)
        self.trent.loop("walk")
        Int1=self.trent.posInterval(5,Point3(-20,0,0),startPos=Point3(20, 0, 0))
       # Int2=self.trent.posInterval(5,Point3(self.trent.getX(),self.trent.getY()+20,0),startPos=Point3(self.trent.getX(), self.trent.getY(), 0))
       # Int3=self.trent.hprInterval(3,Point3(90,0,0),startHpr=Point3(0,0,0))
       # Int4=self.trent.posInterval(13,Point3(-20,0,0),startPos=Point3(20,0,0))      
        self.trentPace = Sequence(Int1,name="trentPace")
        self.trentPace.start()
        
      #  posInterval1 = Actor.posInterval(1,Actor2.getPos(),startPos=Actor.getPos())
      #  posInterval2 = Actor.posInterval(1,Actor.getPos(),startPos=Actor2.getPos()) 
      #  Actor1.accept("mouse1",self.handleClick)    
            
            
                                     
    def stopInterval(self):
        self.trentPace.stop()
        self.lastStopX,self.lastStopY = self.x,self.y    
        
    
class Unit:
    def __init__(self):
        self.x,self.y,self.z = 0,0,0
        self.lon=pi*(self.x+10)*(self.x+10)
        self.range=100
        self.mindamage=24
        self.maxdamage=27
        self.damage=range(self.mindamage,self.maxdamage)
        self.armor=3
        self.armortype=None
        self.res=0
        self.speed=290
        self.atkspeed=1.7
        self.maxhp=590
        self.curhp=590
        self.mana=0
        self.trent=Actor("models/panda-model",{"walk": "models/panda-walk4"})
        self.trent.setPos(25,25,0)
        self.trent.setScale(0.01)
        self.timedt=5
        self.newtime=0
        self.lastStopX=0
        self.lastStopY=0
        self.isdead= False
        if self.curhp == 0:
            self.isdead=True
        taskMgr.add(self.TimeTask, "TimeTask")      #Loops The Units to respawn after 30 seconds           
        
    #Sets Increase oR Dercrease in Damage        
    def setDamage(self,delta):
        if delta >1:
           self.damage+=delta
        else:
           self.damage*=delta
    
    # If Current hp is lower than Maximum Hp ang Greater than Zero otherwis no Inflict
    def inflict(self,amount):
         if self.curhp>0:
            if self.curhp<=self.maxhp:           
               self.curhp+=amount
    
    # If Current hp is lower than Maximum Hp otherwis no Heal 
    def heal(self,amount):
         if self.curhp < self.maxhp:                    
            self.curhp+=amount
    
    # Increases or Decreases the Speed for the Unit
    def setSpeed(self,amount):
        if amount >1:
           self.speed+=amount
        else:
           self.speed=self.speed+self.speed*amount 
        
    # Increases of Decreases Armor
    def setArmor(self,delta):            
        self.armor+=delta

    def getX(self):
        return self.trent.x

    def getY(self):
        return self.trent.y
    
    def getZ(self):
        return self.trent.z
   
    # Define a procedure to move the Unit.
 
    def TimeTask(self,task):
        if self.timedt == int(task.time):
           self.startInterval()
           self.timedt+=30
           
        return task.cont
             
    
   # Create the four lerp intervals needed for the trent to
   # walk back and forth.    
   # Create and play the sequence that coordinates the intervals.      
   # Have to change the Int1,Int2 params to self.x,self.y
    def startInterval(self):
        self.trent = Actor("models/panda-model",{"walk": "models/panda-walk4"})
        self.trent.setPos(25,25,0)
        self.trent.setScale(0.01)
        self.trent.reparentTo(render)
        self.trent.loop("walk")
        Int1=self.trent.posInterval(5,Point3(-20,0,0),startPos=Point3(20, 0, 0))
       # Int2=self.trent.posInterval(5,Point3(self.trent.getX(),self.trent.getY()+20,0),startPos=Point3(self.trent.getX(), self.trent.getY(), 0))
       # Int3=self.trent.hprInterval(3,Point3(90,0,0),startHpr=Point3(0,0,0))
       # Int4=self.trent.posInterval(13,Point3(-20,0,0),startPos=Point3(20,0,0))      
        self.trentPace = Sequence(Int1,name="trentPace")
        self.trentPace.start()
        
      #  posInterval1 = Actor.posInterval(1,Actor2.getPos(),startPos=Actor.getPos())
      #  posInterval2 = Actor.posInterval(1,Actor.getPos(),startPos=Actor2.getPos()) 
      #  Actor1.accept("mouse1",self.handleClick)    
            
            
                                     
    def stopInterval(self):
        self.trentPace.stop()
        self.lastStopX,self.lastStopY = self.x,self.y

    
            
            
            
                                   
        
       