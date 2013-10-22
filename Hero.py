#This is the Hero Class that controls all the charateristics of a hero and loads
#all the models and animation and info of the hero 
import time,random,os,sys                                                             
from math import pi, cos, sin ,sqrt,pow,atan2,atan,hypot,degrees                                                     
from direct.gui.DirectGui import *                                                          
from direct.task.Task  import Task                                                         
from direct.actor.Actor import Actor                                                        
from pandac.PandaModules import *                                                           
from direct.interval.IntervalGlobal import Sequence,Func,Wait                                        
from direct.interval.ProjectileInterval import *                                            
from direct.interval.LerpInterval import LerpPosHprInterval,LerpPosInterval                 
from pandac.PandaModules import CollisionTraverser,CollisionNode,BitMask32
from pandac.PandaModules import CollisionHandlerQueue,CollisionRay,CollisionPlane, CollisionSphere
from pandac.PandaModules import PandaNode,NodePath,Camera,TextNode
from pandac.PandaModules import Vec3,Vec4,BitMask32 
from pandac.PandaModules import Plane, Vec3, Point3
from direct.showbase.DirectObject import DirectObject 
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from pandac.PandaModules import BaseParticleEmitter,BaseParticleRenderer
from pandac.PandaModules import PointParticleFactory,SpriteParticleRenderer
from Global import *

                                     
class Hero(DirectObject):
    def __init__(self,no):
        self.HeroStats(no)
        self.display()
       # self.displaynot()
        self.SetupEvents()
        self.Collision()
        self.Loader()
        self.SkillStatus()
        self.sec=0
        self.min=0
        self.heroPace=None
        self.timesec = OnscreenText(text = '', pos = (1.2,-0.725),fg=(1,1,1,1),mayChange=1,scale=0.05)
        self.timemin = OnscreenText(text = '', pos = (1,-0.725),fg=(1,1,1,1),mayChange=1,scale=0.05)
        self.deathtxt=OnscreenText(text="",pos=(0.5,0.9),scale=0.5)
        taskMgr.add(self.update,"update")
        taskMgr.doMethodLater(1,self.Second,"second")
        taskMgr.add(self.MousePos,"mouse")
    
    def HeroStats(self,no):
        self.char={}
        self.char=hero[no]
        self.name=self.char['name']
        self.model=Actor(MYDIRMODEL+self.char['model']+'.egg')
        self.type=None
        self.heroicon=self.char['icon'][0]
        self.skillicons=(self.char['icon'][1],self.char['icon'][2],self.char['icon'][3],self.char['icon'][4])
        self.StartPos=Point3(25,25,0)
        self.gold=4000
        self.goldrate = 1
        self.items=[-1,-1,-1,-1,-1,-1]  #each stores the no of the item
        self.itemindex=0
        self.itemname="self.itemb"
        self.range=self.char['range']
        self.strdt=self.char['strdt']
        self.agidt=self.char['agidt']
        self.intdt=self.char['intdt']
        self.type=self.char['type']
        self.Delta1=0
        self.Delta2=0
        self.Delta3=0
        self.Delta4=0
        self.Delta5=0
        self.lvl=0
        self.xp=0
        self.Input=None
        self.str=self.char['str']+(self.strdt*self.lvl)
        self.agi=self.char['agi'] + (self.agidt*self.lvl) 
        self.int=self.char['int'] +(self.intdt*self.lvl)
        self.basehp=590+self.str*19
        self.basemp=220+(self.int*13)
        self.maxhp=590 +(self.str*19)
        self.curhp=self.maxhp
        self.maxmp=220 +(self.int*13)
        self.curmp=self.maxmp
        self.armor=self.char['armor'] +(self.agi/7)
        self.atkspeed=1.5/self.agi
        if self.type=='str':
           self.TYPESTR()
        if self.type=='agi':
           self.TYPEAGI()
        if self.type=='int':
           self.TYPEINT() 
           
        self.healrate=0.003 *self.str
        self.mprate=0.02 *self.int
        self.res=0.25
        self.speed=self.char['speed']
        self.skill=0
        self.isDead=False
        self.lon=pi*(self.getX()+10)*(self.getY()+10)
        
    def Loader(self):
        self.model=Actor("models/ralph", {"run": "models/ralph-run"})
      #  self.model=Actor(MYDIRMODEL+self.model+'.egg')
        self.model.setScale(3) 
     #   self.model.setHpr(90,270,0)
        self.model.setTransparency(0.5)
     #   self.model.setScale(0.1)
        self.model.setPos(self.StartPos)
        self.model.reparentTo(render)
     #   self.model.setColor(0, 0, 0, 0)
        self.model.loop("run")
     #   self.Input=Input(self.model)
        Flame(self,self.model)
                         
#-------------------------------------------------------------Display Function---------------------------------------------------#
    def TYPESTR(self):
        self.mindamage=self.char['min']+self.str+self.Delta1
        self.maxdamage=self.char['max']+self.str+self.Delta1
        self.damage=range(int(self.mindamage),int(self.maxdamage)) 
    def TYPEAGI(self):
        self.mindamage=self.char['min']+self.agi+self.Delta1
        self.maxdamage=self.char['max']+self.agi+self.Delta1
        self.damage=range(int(self.mindamage),int(self.maxdamage)) 
    def TYPEINT(self):
        self.mindamage=self.char['min']+self.int+self.Delta1
        self.maxdamage=self.char['max']+self.int+self.Delta1
        self.damage=range(int(self.mindamage),int(self.maxdamage)) 
    def TYPE(self):
        pass
    def display(self):
        x,y,z=self.model.getX(),self.model.getY(),self.model.getZ()
        base.camera.setPos(x,y,z+180)
        base.camera.setP(-30)
        base.camera.lookAt(self.model)
        self.panel=aspect2d.attachNewNode("panel")
        self.panel.setTransparency(1)
        self.SKNode=aspect2d.attachNewNode("skl")
        self.SKNode.setTransparency(0)
        self.HP=DirectLabel(text='',parent = self.panel,text_fg=(0,0.9,0,1),frameColor=(0,0,0,0),pos=(-0.41,0,-0.850),scale=0.04)
        self.MP=DirectLabel(text='',parent = self.panel,text_fg=(0,0,0.8,1),frameColor=(0,0,0,0),pos=(-0.41,0,-0.912),scale=0.04)
        self.LVL=DirectLabel(text ="Level %d"%(self.lvl+1),parent = self.panel,text_fg=(0,0,0,1),frameColor=(0,0,0,0),pos =(-0.5,0,-0.79),scale=Sc)
        Text1(self,"Damage",-0.26,-0.02,-1)
        Text1(self,"Armor",-0.27,0.03,-1)
        Text1(self,"Str",-0.25,0.085,-1)
        Text1(self,"Agi",-0.25,0.13,-1)
        Text1(self,"Int",-0.25,0.17,-1)
        self.DAM=Text2(self,"%d-%d",(self.mindamage-self.Delta1,self.maxdamage-self.Delta1),-0.40,-0.02,-1)
        self.ARM=Text2(self,"%d",(self.armor-self.Delta2),-0.40,0.03,-1)
        self.STR=Text2(self,"%d",(self.str-self.Delta3),-0.40,0.085,-1)
        self.AGI=Text2(self,"%d",(self.agi-self.Delta4),-0.40,0.13,-1)
        self.INT=Text2(self,"%d",(self.int-self.Delta5),-0.40,0.17,-1)
        if self.Delta1!=0:
           self.damdelta=Text3(self,"%d",self.Delta1,-0.4,-0.02,-1)
        if self.Delta2!=0:
           self.armdelta=Text3(self,"%d",self.Delta2,-0.4,0.03,-1)   
        if self.Delta3!=0:
           self.strdelta=Text3(self,"%d",self.Delta3,-0.36,0.085,-1)
        if self.Delta4!=0:
           self.agidelta=Text3(self,"%d",self.Delta4,-0.44,0.13,-1)
        if self.Delta5!=0:
           self.intdelta=Text3(self,"%d",self.Delta5,-0.44,0.17,-1)
        self.hpbar = DirectWaitBar(barColor=(0,0.176470,0,1),parent = self.panel,scale=(0.3,0,0.23), frameColor=(0,0,0,1),pos = (0,0,-0.84))
        self.mpbar=DirectWaitBar(barColor=(0,0,0.6,1),parent = self.panel,scale=(0.3,0,0.23), frameColor=(0,0,0,1),pos = (0,0,-0.90))
        self.lvlbar=DirectWaitBar(barColor=(0,0,0.2,1),parent = self.panel,image='glue/lvlbar.png',image_scale=(1.1,0,0.2),scale=0.35, pos = (0,0,-0.8))
        self.lvlbar.setTransparency(1)
        self.lvlbar.detachNode()
        self.skbtn1=DirectButton(image=self.skillicons[0]+'.png',parent=self.SKNode,pos=(posx-1.3,0,posy-1.2),pad=(-0.1,-0.1),scale=biconscale,command=self.SkillNo,extraArgs=[0])
        self.skbtn2=DirectButton(image=self.skillicons[1]+'.png',parent=self.SKNode,pos=(posx-1.3+0.14,0,posy-1.2),pad=(-0.1,-0.1),scale=biconscale,command=self.SkillNo,extraArgs=[1])
        self.skbtn3=DirectButton(image=self.skillicons[2]+'.png',parent=self.SKNode,pos=(posx-1.3+0.28,0,posy-1.2),pad=(-0.1,-0.1),scale=biconscale,command=self.SkillNo,extraArgs=[2])
        self.skbtn4=DirectButton(image=self.skillicons[3]+'.png',parent=self.SKNode,pos=(posx-1.3+0.42,0,posy-1.2),pad=(-0.1,-0.1),scale=biconscale,command=self.SkillNo,extraArgs=[3])
        self.b2 = DirectButton(text ="dam",parent = self.panel,pos=(-0.5,0,0),enableEdit=1,scale=(0.25,0,0.1),command=self.hurt,extraArgs=[200])
        self.b3 = DirectButton(text ="",image='tome.tga',pos=(0.5,0,0),frameColor=(0,0,0,0),pad=(-0.1,-0.1),enableEdit=1,scale=(0.07,0,0.07),command=self.itemBuy,extraArgs=[0,300])
        self.GOLD=OnscreenText(text='',fg=(1,1,1,1),pos=(1.225,-0.84),scale=0.05)  
       # self.escapeEvent = OnscreenText(text=HELPTEXT, font = font,style=1, fg=(1,1,1,1), pos=(-0.82, -0.725),align=TextNode.ALeft, scale = .045)                         
                                
    def displaynot(self):
        self.panel.detachNode()
        self.SKNode.detachNode()
#------------------------------------------------------------Set Functions--------------------------------------------------------#    
    def setDamage(self,amt):
        if delta >1:
         self.damage+=delta
        else:
         self.damage=self.damage+self.damage*delta
    
    def Delta(self,amt1,amt2,amt3,amt4,amt5):          
        if amt1!=0:                                #After changes occur for that period the taks sets the values to zero
           self.Delta1+=amt1
        if amt2!=0:   
           self.Delta2+=amt2
        if amt3!=0:   
           self.Delta3+=amt3
        if amt4!=0:   
           self.Delta4+=amt3
        if amt5!=0:   
           self.Delta5+=amt3
        
    def hurt(self,amt):
         if self.curhp>0:
            if self.curhp<=self.maxhp:           
               self.curhp-=amt*1
    def hurtMag(self,delta):
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
            
    def manaspend(self,amt):
        if self.curmp>amt:
           self.curmp-=amt
                    
    def setSpeed(self,delta):
        if delta > 1:
           self.speed+=delta
        else:
           self.speed=self.speed+self.speed*delta 
    def setArmor(self,delta):            
        self.armor+=delta
    def setPos(self,x,y,z):
        self.model.setPos(x,y,z)
    def setHPColor(self):
        if self.curhp<0.25*self.maxhp:
           self.hpbar['barColor']=(1,0,0,1)
        elif self.curhp<0.5*self.maxhp:
           self.hpbar['barColor']=(1,0.5,0,1)
        elif self.curhp<0.75*self.maxhp:
           self.hpbar['barColor']=(1,1,0,1)
        else:
           self.hpbar['barColor']=(0,0.176470,0,1)
        
#-------------------------------------------------------------Setup Keys And EVENTS--------------------------------------------------#
    def SetupEvents(self):
        self.dt=0
        self.keyMap = {"left":0, "right":0, "forward":0}
        self.isMoving = False
        self.Change=False
        self.Animate=False
        self.pos3d=None
        self.target=Point3()
        self.dist=0
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)
        self.Text = OnscreenText(text="Set PanRate",pos=(-1.25,-0.15),scale=0.1)
        self.slider = DirectSlider(range=(20,100), value=50, pageSize=2, pos=(-1.25,0,-0.2),scale= (0.2,0.2,0.2), command=self.setScrollSpeed)
        self.dumm=loader.loadModel("models/panda.egg")
        self.dumm.reparentTo(render)
        self.dumm.setTag("Unit",'1')
        self.dumm.setPos(0,0,0)
        self.mini=0
        self.x1,self.y1=self.model.getX(),self.model.getY()
        self.x2,self.y2=self.dumm.getX(),self.dumm.getY()
        self.fired=False
        self.atk=Attack(self.model,self.dumm,1.4)
        self.accept("arrow_left", self.setKey1, ["left",1,True])
        self.accept("arrow_right", self.setKey1, ["right",1,True])
        self.accept("arrow_up", self.setKey1, ["forward",1,True])
        self.accept("arrow_left-up", self.setKey1, ["left",0,False])
        self.accept("arrow_right-up", self.setKey1, ["right",0,False])
        self.accept("arrow_up-up", self.setKey1, ["forward",0,False])
        self.accept("mouse1",self.ObjectClick)
        self.accept("mouse3",self.MoveHero)
        
    def MoveHero(self):
        self.startR=self.model.getHpr()
        self.target=self.mpos3d
        x2,y2,z2=self.target.getX(),self.target.getY(),self.target.getZ()
        h1,p1,r1=self.model.getH(),self.model.getP(),self.model.getR()
        self.dist=sqrt(pow(self.x1-x2,2)+pow(self.y1-y2,2))
        self.sptime=self.dist/(self.speed)
        self.hall=270-degrees(y2/x2)
       # self.model.setPos(self.model,self.spd,0,self.spd)
        self.Inter=LerpPosHprInterval(self.model,self.sptime,pos=self.target ,startPos=self.model.getPos(),startHpr=self.startR,hpr=self.startR)#(h1,p1,self.hall))
        #Inter2=Func(self.model.lookAt(self.target),Wait(0.3))
        self.heroPace = Sequence(self.Inter,name="heroPace")
        self.heroPace.start()
        
    def Collision(self):
        self.mpos3d=0
        self.plane = Plane(Vec3(0, 0, 1), Point3(0, 0, 0)) 
        base.cTrav = CollisionTraverser()
        self.collHandler = CollisionHandlerQueue()
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        base.cTrav.addCollider(self.pickerNP, self.collHandler)
    
    def ObjectClick(self): 
        if base.mouseWatcherNode.hasMouse():    
           mpos = base.mouseWatcherNode.getMouse()   
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())    
        base.cTrav.traverse(render)   # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.   
        if self.collHandler.getNumEntries() > 0:      # This is so we get the closest object.      
            self.collHandler.sortEntries()      
            self.pickedObj = self.collHandler.getEntry(0).getIntoNodePath()      
            self.pickedObj = self.pickedObj.findNetTag('Unit')
            if not self.pickedObj.isEmpty():
                self.Attack(self.pickedObj.getPos())
                #Handles the object       
                
    def setKey1(self, key, value,value2):
        self.keyMap[key] = value
        self.Change=value2
    
    def checkKeys(self):
        if (self.keyMap["left"]!=0):
            self.model.setH(self.model.getH() + self.dt*300)
        if (self.keyMap["right"]!=0):
            self.model.setH(self.model.getH() - self.dt*300)
        if (self.keyMap["forward"]!=0):
            self.model.setX(self.model, +(self.dt*25*SPEED))  
        
    def checkAnim(self):
        if self.Change:                    #(self.keyMap["forward"]!=0) or (self.keyMap["left"]!=0) or (self.keyMap["right"]!=0):
            if self.isMoving is False:
                self.model.loop("run")
                self.isMoving = True
        else:
            if self.isMoving:
                self.model.stop()
                self.model.pose("walk",5)
                self.isMoving = False
                
        if self.Animate:
            pass
    def Attack(self,pos):
        self.atk.setWeil(self.model)
        self.atk.setTarg(self.dumm)
        self.atk.setDist(self.mini)
        if self.mini<=60:
           self.Animate=self.atk.ATT()
        else:
           messenger.send('mouse3')
           if self.mini<=60:
              self.atk.ATT()
    
    def setScrollSpeed(self):
        SCROLLSPEED=self.slider['value']
    def UnSetupEvents(self):
        self.ignore("arrow_left")
        self.ignore("arrow_right")
        self.ignore("arrow_up")
        self.ignore("arrow_left-up")
        self.ignore("arrow_right-up")
        self.ignore("arrow_up-up")
        self.ignore("enter")
        self.ignore("mouse1")
        self.ignore("mouse3")
        taskMgr.remove("update")
        taskMgr.remove("second")
        taskMgr.remove("mouse")
#--------------------------------------------------------------Return Functions------------------------------------------------------#         
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
    def getlvl(self):
        return self.lvl
    def getModel(self):
        return self.model
    def gainxp(self,unit):
        self.xp+=unit
    
    def gainGold(self,gain):
        self.gold+=gain
    def sendTime(self,min,sec):
        self.min=min
        self.sec=sec
#----------------------------------------------------------------ITEM FUNCTIONS--------------------------------------------------------#        
    def itemBuy(self,arg,cost):
           if self.gold>=0:
              if self.itemindex<=5:
                 del self.items[self.itemindex]  
                 self.items.insert(self.itemindex,arg)
                 self.gainGold(-cost)
                 if self.items[self.itemindex]!=-1:
                    if self.itemindex==0:
                       self.itm0= aspect2d.attachNewNode("item0")
                       DirectButton(text ="",parent=self.itm0,image='tome.tga',pos=(0+0.12*self.itemindex,0,-0.90),pad=(-0.1,-0.1),scale=(0.05,0,0.05),extraArgs=[arg,cost],command=self.itemSold)#,commandButtons=DGG.RMB)
                    if self.itemindex==1:
                       self.itm1= aspect2d.attachNewNode("item1")
                       DirectButton(text ="",parent=self.itm1,image='tome.tga',pos=(0+0.12*self.itemindex,0,-0.90),pad=(-0.1,-0.1),scale=(0.05,0,0.05),extraArgs=[arg,cost],command=self.itemSold)#,commandButtons=DGG.RMB)   
                    if self.itemindex==2:
                       self.itm2= aspect2d.attachNewNode("item2")
                       DirectButton(text ="",parent=self.itm2,image='tome.tga',pos=(0+0.12*self.itemindex,0,-0.90),pad=(-0.1,-0.1),scale=(0.05,0,0.05),extraArgs=[arg,cost],command=self.itemSold)#,commandButtons=DGG.RMB)
                    if self.itemindex==3:
                       self.itm3= aspect2d.attachNewNode("item3")
                       DirectButton(text ="",parent=self.itm3,image='tome.tga',pos=(0+0.12*self.itemindex,0,-0.90),pad=(-0.1,-0.1),scale=(0.05,0,0.05),extraArgs=[arg,cost],command=self.itemSold)#,commandButtons=DGG.RMB)
                    if self.itemindex==4:
                       self.itm4= aspect2d.attachNewNode("item4")
                       DirectButton(text ="",parent=self.itm4,image='tome.tga',pos=(0+0.12*self.itemindex,0,-0.90),pad=(-0.1,-0.1),scale=(0.05,0,0.05),extraArgs=[arg,cost],command=self.itemSold)#,commandButtons=DGG.RMB)
                    if self.itemindex==5:
                       self.itm5= aspect2d.attachNewNode("item5")
                       DirectButton(text ="",parent=self.itm5,image='tome.tga',pos=(0+0.12*self.itemindex,0,-0.90),pad=(-0.1,-0.1),scale=(0.05,0,0.05),extraArgs=[arg,cost],command=self.itemSold)#,commandButtons=DGG.RMB)                        
                    self.itemindex+=1
                    
              else:
                  Error("No Empty Slots")
                 
           else:
               Error("No Gold")
               
    def itemSold(self,itemtosell,cost):
        self.ind=self.items.index(itemtosell)
        del self.items[self.ind]  
        self.items.insert(self.ind,-1)
        self.gainGold(cost/2)
        if self.ind==0:
           self.itm0.detachNode()
        if self.ind==1:
           self.itm1.detachNode()
        if self.ind==2:
           self.itm2.detachNode()
        if self.ind==3:
           self.itm3.detachNode()
        if self.ind==4:
           self.itm4.detachNode() 
        if self.ind==5:
           self.itm5.detachNode()        
        self.itemindex-=1     
        
        
        
        
        
        
    def lvlup(self):
        self.lvl+=1
        self.str=self.char['str'] +(self.strdt*self.lvl)
        self.str=self.char['str'] +(self.agidt*self.lvl)
        self.int=self.char['int'] +(self.intdt*self.lvl)
        self.hpgain=(self.strdt+self.Delta1)*19
        self.mpgain=(self.intdt+self.Delta3)*13
        self.maxhp=590+self.str*19
        self.maxmp=290+self.int*13      #some error here
        self.heal(self.hpgain)
        self.replenish(self.mpgain)
        self.xp =0
#---------------------------------------------------------SKILL FUNCTIONS-------------------------------------#    
    def SkillStatus(self):
        self.sp1=0
        self.sp2=0
        self.sp3=0
        self.sp4=0
        self.sp1dam=0
        self.sp2dam=0
        self.sp3dam=0
        self.sp4dam=0
        if self.sp1==1:
           self.range=400
           self.sp1dam=130
           self.raduis=100
           self.sp2dam=30
           self.sp3dam=90
           self.pulses=6
           
    def SkillNo(self,arg):
        if arg==0:
           if self.curmp>=100:
              self.accept("mouse1",Blink,extraArgs=[self])
              self.skbtn1['image']='cancel.png'
        #      self.skbtn1['command']=self.setOpen()
           else:
              Error("NO MANA") 
        elif arg==1:
             StatUp(self)
        elif arg==2:
             StatDn(self)
        else: 
             Ulti(self)
    
    def setOpen(self):
        self.open=False
        self.ignore("mouse1")
        self.skbtn1['image']=self.skillicons[0]+'.png'
        self.accept("mouse1",self.ObjectClick)
    
    
    
    
    
    
#----------------------------------------TASK FUNCTIONS------------------------------------------------------#
    def Delay(self,task):
        self.Delta(-2,-2,-2)
        return task.done    
    def Second(self,task):
        self.gainGold(self.goldrate)
        self.heal(self.healrate)
        self.replenish(self.mprate)
        return task.again
        
    def update(self,task):
        self.timemin.setText(str(self.min))
        self.timesec.setText(str(self.sec))
        self.str=self.char['str'] +(self.strdt*self.lvl)+self.Delta3        
        self.agi=self.char['agi'] + (self.agidt*self.lvl)+self.Delta4
        self.int=self.char['int']+(self.intdt*self.lvl)+self.Delta5
        self.hpgain=(self.strdt+self.Delta1)*19
        self.mpgain=(self.intdt+self.Delta3)*13
        self.maxhp=590+self.str*19
        self.maxmp=290+self.int*13      #some error here
      #  self.heal(self.hpgain)
     #   self.replenish(self.mpgain)
        self.armor=self.char['armor'] +(self.agi/7)+self.Delta2
        self.atkspeed=1.5/self.agi
        if self.type=='str':
           self.TYPESTR()
        if self.type=='agi':
           self.TYPEAGI()
        if self.type=='int':
           self.TYPEINT() 
        self.healrate=0.03 *self.str
        self.mprate=0.02 *self.int
        self.GOLD.setText(str(self.gold))
        self.hpbar['range']=int(self.maxhp)
        self.hpbar['value']=int(self.curhp)
        self.mpbar['range']=int(self.maxmp)
        self.mpbar['value']=int(self.curmp)
        self.lvlbar['range']=int(10*self.lvl)
        self.lvlbar['value']=int(self.xp)
        self.HP['text']="HP"+str(int(self.curhp))+"/"+str(int(self.maxhp))
        self.MP['text']="MP"+str(int(self.curmp))+"/"+str(int(self.maxmp))
        self.DAM['text']=str(int(self.mindamage))+'-'+str(int(self.maxdamage))
        self.ARM['text']=str(int(self.armor))
        self.STR['text']=str(int(self.str))
        self.AGI['text']=str(int(self.agi))
        self.INT['text']=str(int(self.int))
        self.LVL['text']="LEVEL "+str(int(self.lvl))
        
        if self.xp>=20*20:
           self.lvlup()   
        if self.curhp<=0:
           taskMgr.add(self.Death,"death")
        self.x1,self.y1=self.model.getX(),self.model.getY()
        self.x2,self.y2=self.dumm.getX(),self.dumm.getY()
        self.mini=sqrt(pow(self.x1-self.x2,2)+pow(self.y1-self.y2,2))
        Debug2(self,str(self.mini))
        elapsed = globalClock.getDt()
        self.dt=elapsed
        self.setHPColor()
        self.checkAnim()
        self.checkKeys()
       #     base.camera.lookAt(self.model)         
       # self.floater.setPos(self.model.getPos())
       # base.camera.lookAt(self.floater)      
        return task.cont
    
    def Death(self,task):
        self.isDead=True
        Debug2(self,str(task.time))
        if self.isDead==True:
           self.model.reparentTo(hidden)
           self.panel.detachNode()
           self.deathtime=(self.lvl+1)*3
           self.isDead=False
        if int(task.time)==self.deathtime:
            self.model.setPos(self.StartPos)
            self.model.reparentTo(render)
            self.curhp=self.maxhp
            self.model.loop("walk")
            self.display()
            taskMgr.remove("death")
          #  self.deathtxt.destroy()
        return task.cont
    
    def MousePos(self, task): #This Took me 1.5 Months to Learn
        if base.mouseWatcherNode.hasMouse(): 
           mpos = base.mouseWatcherNode.getMouse() 
           self.mpos3d = Point3() 
           nearPoint = Point3() 
           farPoint = Point3()                                   
           base.camLens.extrude(mpos, nearPoint, farPoint)
        if self.plane.intersectsLine(self.mpos3d, render.getRelativePoint(camera, nearPoint),render.getRelativePoint(camera, farPoint)):
           pass    
        return task.again  
    
    def destroy(self):
        self.panel.detachNode()
        self.t1.destroy()
        self.t2.destroy()
        self.model.remove()
        self.timesec.destroy()
        self.timemin.destroy()
        self.UnsetupEvents()


#----------------------------------------ATTACK CLASS--------------------------------------------------------#  
 
class Attack:
    def __init__(self,hero,target,atkspeed):
        self.vel=120
        self.missile = loader.loadModel("/c/miss")
        self.missile.setScale(0.09,0.09,0.09)
        self.missile.reparentTo(render)
        self.missile.setPos(25,25,0)
        self.weilder=0
        self.target=0
        self.dist=0
        self.fired=False
        self.atkspeed=atkspeed
        self.Animate=False
        
    def ATT(self):
        if self.fired==False:
           self.fired=True
           self.AnimON()
           self.time=self.dist/self.vel
           self.trajectory = ProjectileInterval(self.missile,startPos =self.weilder,endPos =self.target, duration =self.time) 
           self.trajectory.start()
           taskMgr.doMethodLater(self.atkspeed,self.setFired,"Fire")
           
    def setFired(self,task):
        self.fired=False
        self.AnimOFF()
        taskMgr.remove("Fire")
        return task.done          
    def setWeil(self,arg):
        self.weilder=arg.getPos()
    def setTarg(self,arg):
        self.target=arg.getPos()
    def setDist(self,arg):
        self.dist=arg
    def setAtkSpeed(self):
        self.atkspeed=atkspeed
    def AnimON(self):
        return True
    def AnimOFF(self):
        return False
        
            
        
        
#--------------------------------------------------------ITEM CLASS-------------------------------------#        
class Item:
    def __init__(self):
        self.ItemList=[0,0,0,0,0,0]
        
    def put(self,item):
        if self.ItemList[0]==0:
           self.ItemList.insert(0,self.item)
        elif self.ItemList[1]==0:
             self.ItemList.insert(1,self.item)
        elif self.ItemList[2]==0:
             self.ItemList.insert(2,self.item)
        elif self.ItemList[3]==0:
             self.ItemList.insert(3,self.item)
        elif self.ItemList[4]==0:
             self.ItemList.insert(4,self.item)
        elif self.ItemList[5]==0:
             self.ItemList.insert(5,self.item) 
    def remove(self,item):
        pass
            
        
#--------------------------------------------------------INPUT CLASS------------------------------------------------------------------#        
class Input(DirectObject):
    def __init__(self,model):
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)
        self.Text = OnscreenText(text="Set PanRate",pos=(-1.25,-0.15),scale=0.1)
        self.slider = DirectSlider(range=(20,100), value=50, pageSize=2, pos=(-1.25,0,-0.2),scale= (0.2,0.2,0.2), command=self.setScrollSpeed)
    
        

       
        
        
                
    def Attack(self,pos):
        self.atk.setWeil(self.model)
        self.atk.setTarg(self.dumm)
        self.atk.setDist(self.mini)
        if self.mini<=60:
           self.Animate=self.atk.ATT()
        else:
           messenger.send('mouse3')
           if self.mini<=60:
              self.atk.ATT()
    
    def setScrollSpeed(self):
        SCROLLSPEED=self.slider['value']
        
    
    def MousePos(self, task): #This Took me 1.5 Months to Learn
        if base.mouseWatcherNode.hasMouse(): 
           mpos = base.mouseWatcherNode.getMouse() 
           self.pos3d = Point3() 
           self.nearPoint = Point3() 
           self.farPoint = Point3()                                   
           base.camLens.extrude(mpos, self.nearPoint, self.farPoint) 
        if self.plane.intersectsLine(self.pos3d, 
           render.getRelativePoint(camera, self.nearPoint), 
           render.getRelativePoint(camera, self.farPoint)):
             pass
        return task.again 
    
    
    def MoveHero(self):
        self.startR=self.model.getHpr()
        self.target=self.pos3d
        x2,y2,z2=self.target.getX(),self.target.getY(),self.target.getZ()
        h1,p1,r1=self.model.getH(),self.model.getP(),self.model.getR()
        self.dist=sqrt(pow(self.x1-x2,2)+pow(self.y1-y2,2))
        self.sptime=self.dist/(30)
        self.hall=270-degrees(y2/x2)
       # self.model.setPos(self.model,self.spd,0,self.spd)
        Inter=LerpPosHprInterval(self.model,self.sptime,pos=self.target ,startPos=self.model.getPos(),startHpr=self.startR,hpr=self.startR)#(h1,p1,self.hall))
        #Inter2=Func(self.model.lookAt(self.target),Wait(0.3))
        self.heroPace = Sequence(Inter,name="heroPace")
        self.heroPace.start()
    
    
        
    def Move(self,task):
        self.x1,self.y1=self.model.getX(),self.model.getY()
        self.x2,self.y2=self.dumm.getX(),self.dumm.getY()
        self.mini=sqrt(pow(self.x1-self.x2,2)+pow(self.y1-self.y2,2))
        Debug2(self,str(self.mini))
        elapsed = globalClock.getDt()
        self.dt=elapsed
        self.setAnim()
        if (self.keyMap["left"]!=0):
            self.model.setH(self.model.getH() + self.dt*300)
        if (self.keyMap["right"]!=0):
            self.model.setH(self.model.getH() - self.dt*300)
        if (self.keyMap["forward"]!=0):
            self.model.setX(self.model, +(self.dt*25*SPEED))  
       #     base.camera.lookAt(self.model)         
        self.floater.setPos(self.model.getPos())
       # base.camera.lookAt(self.floater)      
        return task.cont
    
    def Setup(self):
        self.accept("arrow_left", self.setKey1, ["left",1,True])
        self.accept("arrow_right", self.setKey1, ["right",1,True])
        self.accept("arrow_up", self.setKey1, ["forward",1,True])
        self.accept("arrow_left-up", self.setKey1, ["left",0,False])
        self.accept("arrow_right-up", self.setKey1, ["right",0,False])
        self.accept("arrow_up-up", self.setKey1, ["forward",0,False])
        self.accept("mouse1",self.ObjectClick)
        self.accept("mouse3",self.MoveHero)
     
    def setKey1(self, key, value,value2):
        self.keyMap[key] = value
        self.Change=value2
    
    def setAnim(self):
        if self.Change:                    #(self.keyMap["forward"]!=0) or (self.keyMap["left"]!=0) or (self.keyMap["right"]!=0):
            if self.isMoving is False:
                self.model.loop("run")
                self.isMoving = True
        else:
            if self.isMoving:
                self.model.stop()
                self.model.pose("walk",5)
                self.isMoving = False
                
        if self.Animate:
            pass
            #set the attack anim here
                    
                
    def Coll(self):
        base.cTrav = CollisionTraverser()
        self.collHandler = CollisionHandlerQueue()
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        base.cTrav.addCollider(self.pickerNP, self.collHandler)
    
    def ObjectClick(self):   
        mpos = base.mouseWatcherNode.getMouse()   
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())    
        base.cTrav.traverse(render)   # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.   
        if self.collHandler.getNumEntries() > 0:      # This is so we get the closest object.      
            self.collHandler.sortEntries()      
            self.pickedObj = self.collHandler.getEntry(0).getIntoNodePath()      
            self.pickedObj = self.pickedObj.findNetTag('Unit')
            if not self.pickedObj.isEmpty():
                self.Attack(self.pickedObj.getPos())
                #self.pickedObj.reparentTo(hidden)   #Handles the object       


class Input1(DirectObject):
    def __init__(self,model):
        # We will detect the height of the terrain by creating a collision
        # ray and casting it downward toward the terrain.  One ray will
        # start above ralph's head, and the other will start above the camera.
        # A ray may hit the terrain, or it may hit a rock or a tree.  If it
        # hits the terrain, we can detect the height.  If it hits anything
        # else, we rule that the move is illegal.

        self.cTrav = CollisionTraverser()

        self.ralphGroundRay = CollisionRay()
        self.ralphGroundRay.setOrigin(0,0,1000)
        self.ralphGroundRay.setDirection(0,0,-1)
        self.ralphGroundCol = CollisionNode('ralphRay')
        self.ralphGroundCol.addSolid(self.ralphGroundRay)
        self.ralphGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.ralphGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.ralphGroundColNp = self.ralph.attachNewNode(self.ralphGroundCol)
        self.ralphGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.ralphGroundColNp, self.ralphGroundHandler)

        self.camGroundRay = CollisionRay()
        self.camGroundRay.setOrigin(0,0,1000)
        self.camGroundRay.setDirection(0,0,-1)
        self.camGroundCol = CollisionNode('camRay')
        self.camGroundCol.addSolid(self.camGroundRay)
        self.camGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.camGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.camGroundColNp = base.camera.attachNewNode(self.camGroundCol)
        self.camGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.camGroundColNp, self.camGroundHandler)

        # Uncomment this line to see the collision rays
        self.ralphGroundColNp.show()
        self.camGroundColNp.show()
       
        #Uncomment this line to show a visual representation of the 
        #collisions occuring
        self.cTrav.showCollisions(render)
       

    
    #Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value
    

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):

        # Get the time elapsed since last frame. We need this
        # for framerate-independent movement.
        elapsed = globalClock.getDt()       #Has a Change in time from 0.04 to 0.09 constantly changes
        # If the camera-left key is pressed, move camera left.
        # If the camera-right key is pressed, move camera right.

        base.camera.lookAt(self.model.getX(),self.model.getY(),0)
        # save ralph's initial position so that we can restore it,
        # in case he falls off the map or runs into something.

        startpos = self.model.getPos()

        # If a move-key is pressed, move ralph in the specified direction.
                
        # If the camera is too far from ralph, move it closer.
        # If the camera is too close to ralph, move it farther.

        camvec = self.model.getPos() - base.camera.getPos()
        camvec.setZ(5)
        camdist = camvec.length()
        camvec.normalize()
        if (camdist > 30.0):
            base.camera.setPos(base.camera.getPos() + camvec*(camdist-30))
            camdist = 30.0
        if (camdist < 15.0):
            base.camera.setPos(base.camera.getPos() - camvec*(15-camdist))
            camdist = 15.0
            
        # The camera should look in ralph's direction,
        # but it should also try to stay horizontal, so look at
        # a floater which hovers above ralph's head.
        # Keep the camera at one foot above the terrain,
        # or two feet above ralph, whichever is greater.
        self.floater.setPos(self.model.getPos())
        base.camera.lookAt(self.floater)        
        # Now check for collisions.

        self.cTrav.traverse(render)

        # Adjust ralph's Z coordinate.  If ralph's ray hit terrain,
        # update his Z. If it hit anything else, or didn't hit anything, put
        # him back where he was last frame.

        entries = []
        for i in range(self.ralphGroundHandler.getNumEntries()):
            entry = self.ralphGroundHandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            self.ralph.setZ(entries[0].getSurfacePoint(render).getZ())
        else:
            self.ralph.setPos(startpos)

        
        
        entries = []
        for i in range(self.camGroundHandler.getNumEntries()):
            entry = self.camGroundHandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            base.camera.setZ(entries[0].getSurfacePoint(render).getZ()+1.0)
        if (base.camera.getZ() < self.ralph.getZ() + 2.0):
            base.camera.setZ(self.ralph.getZ() + 2.0)
            
        
        return Task.cont



