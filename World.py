from direct.task import Task
from direct.actor.Actor import Actor 
from direct.gui.DirectGui import DirectEntry,OnscreenText,OnscreenImage,DirectLabel
from direct.showbase import DirectObject
from pandac.PandaModules import *
from Hero import Hero
from Unit import Unit1
from Camera import Camera
from Lights import Lights
import direct.directbase.DirectStart 
from minimap import minimap
#from Menu import *
from Global import *
import time,random
from pandac.PandaModules import CollisionTraverser,CollisionNode,BitMask32
from pandac.PandaModules import CollisionHandlerQueue,CollisionRay,CollisionPlane, CollisionSphere
from pandac.PandaModules import PandaNode,NodePath,Camera,TextNode
from pandac.PandaModules import Vec3,Vec4,BitMask32 
from pandac.PandaModules import Plane, Vec3, Point3
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from pandac.PandaModules import BaseParticleEmitter,BaseParticleRenderer
from pandac.PandaModules import PointParticleFactory,SpriteParticleRenderer


#-----------------------------------------------------------World CLass---------------------------------------------------#
#This Class acts as the server and sends and gets all the info from other games hero classes
class World(DirectObject.DirectObject): 
    def __init__(self):
      self.creeps=None
      self.open=False
      self.sec=0
      self.min=0
      self.pindex=1            #This is the Pause Index
      self.index=-1            #This is the hero Index
      self.rindex=False        #This is the Repick Index
      self.hpicked=[]          #This List Stores All The Heroes Picked and Removes Them
      for i in range (0,110):
          self.hpicked.append(-1)    #Gotta change and check this
      self.hindex=0                        #When a hero is picked this index saves it and stores it in the list
      self.RND=render.attachNewNode("rend")
      self.LightHandler=None
      self.Players()
      self.LoadTerrain()            #Load the Map
      self.SetupCamera()           
      self.SetupLight()
      self.SetupEvents()
      self.SetupTimer()
      self.chooseHero()
      self.SetupMap()
      self.SetupCreeps()
      self.SetupCollision()
      self.displayed=False
      self.keyMap = {"cam-left":0, "cam-right":0,"cam-up":0,"cam-down":0,"zoom-in":0,"zoom-out":0}
      self.chatindex=0
      self.chat=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      self.text=["text1","text2","text3","text4","text5""text6""text7""text8""text9","text10","text11"]
      self.task=None
    
    def Players(self):
        self.hero1=None
        self.hero2=None
        self.hero3=None
        self.hero4=None
        self.hero5=None
        self.hero6=None
        self.hero7=None
        self.hero8=None
        self.hero9=None
        self.hero10=None
        self.player1=None
        self.player2=None
        self.player3=None
        self.player4=None
        self.player5=None
        self.player6=None
        self.player7=None
        self.player8=None
        self.player9=None
        self.player10=None
        


    def LoadTerrain(self):
        self.terrain = loader.loadModel('models/environment')
        self.terrain.setTag("Map",'1')
        self.terrain.reparentTo(self.RND)
        self.itmpan1=OnscreenImage(image=MYDIRIMG+'/3.png',scale=(0.3,0,0.09),pos=(0.61,0,-0.915))
        self.itmpan2=OnscreenImage(image=MYDIRIMG+'/3.png',scale=(0.3,0,0.09),pos=(0.61,0,-0.740))
        self.t2=OnscreenImage(image=MYDIRIMG+'/t2.png',scale=(0.25,0,0.06),pos=(1.160,0,-0.71))
        self.t1=OnscreenImage(image=MYDIRIMG+'/t1.png',scale=(0.25,0,0.06),pos=(1.160,0,-0.83))
        self.end=OnscreenImage(image=MYDIRIMG+'/end.png',scale=(0.1,0,0.2),pos=(1.510,0,-0.80))
        self.back=OnscreenImage(image=MYDIRIMG+'/back.png',scale=(0.57,0,0.2),pos=(-0.26,0,-0.80))
       
    def SetupCollision(self):
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
            self.pickedObj1 = self.pickedObj.findNetTag('Unit')
            self.pickedObj2 = self.pickedObj.findNetTag('MyHero')
            self.pickedObj3 = self.pickedObj.findNetTag('Map')
            self.pickedObj4 = self.pickedObj.findNetTag('MyHero')
            if self.pickedObj1==self.creeps.getModel():
               if self.displayed is False:
                  self.displayed=True 
                  self.creeps.display()
            else:
                if self.displayed is True:
                   self.displayed=False 
                   self.creeps.displaynot()
            if self.hero!=None:
               if self.pickedObj2==self.hero1.getModel():
                  if self.displayed is False:
                     self.displayed=True 
                     self.hero1.display()
               else:
                   if self.displayed is True:
                      self.displayed=False 
                      self.hero1.displaynot()
                          
                  
            
    def SetupCamera(self):
        base.camera.setPos(0,0,180)
        base.camera.setP(-30)
        base.camera.lookAt(0,0,0)
   
    def SetupTimer(self):
        self.btn=aspect2d.attachNewNode("btn")
        self.btn.setTransparency(1)
        self.timesec = OnscreenText(text = '', pos = (1.3,-0.71),fg=(1,1,1,1),mayChange=1,scale=0.05)
        self.timemin = OnscreenText(text = '', pos = (1.1,-0.71),fg=(1,1,1,1),mayChange=1,scale=0.05)
        self.pausebtn=DirectButton(text ="Pause (%d)"%(self.pindex),parent=self.btn,text_fg=(0,0.2,0,1),text_pos=(0.05,-0.15),text_scale=(0.48,0.53),image=(MYDIRIMG+"btnof.png",MYDIRIMG+"btnon.png",MYDIRIMG+"btnon.png",None),frameColor=(0,0,0,0),pos=(-1.0,0,-0.81),image_scale=(1.0,0,0.7),scale=(0.15,0,0.10),command=self.Pause)
        self.infobtn=DirectButton(text ="Info",parent=self.btn,text_fg=(0,0.2,0,1),text_pos=(0.05,-0.15),text_scale=0.6,image=(MYDIRIMG+"btnof.png",MYDIRIMG+"btnon.png",MYDIRIMG+"btnon.png",None),frameColor=(0,0,0,0),pos=(-1.0,0,-0.68),image_scale=(1.0,0,0.7),scale=(0.15,0,0.10),command=self.Pause)
        taskMgr.doMethodLater(1, self.Timer, 'tickTask')
              
    def SetupMap(self):
        self.minimap= minimap(None)
    
    def SetupLight(self):
        self.LightHandler=Lights(None)    
        
    def SetupEvents(self):
        self.DEntry = DirectEntry(text = "" ,pos=(-0.6,0.0,-0.7),image=MYDIRIMG+'/tooltips9.png',frameColor=(0,0,0,1),width=27,image_pos=(13.5,0,0.2),image_scale=(15,0,0.6),scale=.05,initialText="",numLines = 1,focus=1,command=self.Parser)
        self.DEntry.setTransparency(1)
        self.DEntry.detachNode()
        taskMgr.add(self.MoveCamera,"CameraControl")
        self.accept("enter",self.MsgBox)
        self.accept("wheel_up",self.setKey, ["zoom-in",1])
        self.accept("wheel_down",self.setKey, ["zoom-out",1])
    #   self.accept("wheel_up-up",self.setKey, ["zoom-in",0])
     #    self.accept("wheel_down-up",self.setKey, ["zoom-out",0])
        self.accept("a", self.setKey, ["cam-left",1])
        self.accept("d", self.setKey, ["cam-right",1])
        self.accept("w", self.setKey, ["cam-up",1])
        self.accept("s", self.setKey, ["cam-down",1])
        self.accept("+", self.setKey, ["zoom-in",1])
        self.accept("-", self.setKey, ["zoom-out",1])
        self.accept("a-up", self.setKey, ["cam-left",0])
        self.accept("d-up", self.setKey, ["cam-right",0])
        self.accept("w-up", self.setKey, ["cam-up",0])
        self.accept("s-up", self.setKey, ["cam-down",0])
        self.accept("+-up", self.setKey, ["zoom-in",0])
        self.accept("--up", self.setKey, ["zoom-out",0])
        self.accept("mouse1",self.ObjectClick)
    
    def UnSetupEvents(self):
        self.ignore("a")
        self.ignore("s")
        self.ignore("w")
        self.ignore("s")
        self.ignore("+")
        self.ignore("-")
        self.ignore("enter")
        self.ignore("wheel_up")
        self.ignore("wheel_down")
        taskMgr.remove("CameraControl")

        
    def setKey(self, key, value,):
        self.keyMap[key] = value 
    
    def MoveCamera(self,task):
        mpos = base.mouseWatcherNode.getMouse()
        elapsed = globalClock.getDt()
        self.dt=elapsed
        self.mx=mpos.getX()
        self.my=mpos.getY()
        if (self.keyMap["cam-left"]!=0):
            base.camera.setX(base.camera, -(self.dt*20))
        if (self.keyMap["cam-right"]!=0):
            base.camera.setX(base.camera, +(self.dt*20))
        if (self.keyMap["zoom-in"]!=0):
            base.camera.setY(base.camera, -(self.dt*20))
        if (self.keyMap["zoom-out"]!=0):
            base.camera.setY(base.camera, +(self.dt*20))    
        if (self.keyMap["cam-down"]!=0):
            base.camera.setZ(base.camera, -(self.dt*20))
        if (self.keyMap["cam-up"]!=0):
            base.camera.setZ(base.camera, +(self.dt*20)) 
        if self.mx>0.95:
           if base.camera.getX()<MAPLIMIT:
              base.camera.setX(base.camera, +(self.dt*SCROLLSPEED))
        if self.mx<-0.95:
           if base.camera.getX()>-MAPLIMIT: 
              base.camera.setX(base.camera, -(self.dt*SCROLLSPEED))      
        if self.my>0.95:
           if base.camera.getY()<MAPLIMIT:  
              base.camera.setZ(base.camera, +(self.dt*SCROLLSPEED)) 
        if self.my<-0.95:
           if base.camera.getY()>-MAPLIMIT:  
              base.camera.setZ(base.camera, -(self.dt*SCROLLSPEED))
        return task.cont
    
    
    
    def chooseHero(self):
        if self.hero1==None:
           self.BTNnode = aspect2d.attachNewNode("buttons")
           for i in range (0,3):
               for j in range (0,4):
                   self.index+=1 
                   if icons[self.index]==None:
                      continue
                   if self.hpicked[self.index]==self.index:
                      continue
                   self.worldHeroButton(-1.8+j*0.1,-i*0.1,self.index)

    def worldHeroButton(self,x,y,arg):
        DirectButton(text="",parent=self.BTNnode,text_font=font,image=MYDIRICONS+icons[arg]+'.tga',frameColor=(0,0,0,0),pad=(-0.1,-0.1),image_scale=(IconSx+0.2,0,IconSy+0.2),pos=(posx-0.5+x,0,posy+y),scale=(0.20,0,0.20),command=self.SetupHero,extraArgs=[arg])
        
    def SetupCreeps(self):
        self.creeps=Unit1()
        
    def SetupHero(self,no):
        self.hpicked.insert(self.hindex,no)
        self.hindex+=1
        self.BTNnode.detachNode()
        self.hero1=Hero(no)
        self.hero1.getModel().setTag("Hero1",'1')

    def Timer(self,task):
        self.task=task
        self.sec+=1
        if self.hero1!=None:
           self.hero1.sendTime(self.min,self.sec) 
        if self.sec>=60:
           self.sec=0
           self.min+=1
           self.timemin.setText(str(self.min))
        self.timesec.setText(str(self.sec))
        return task.again
         
    def MsgBox(self):
        if self.open ==False: 
           self.DEntry.reparentTo(aspect2d)
           self.open=True                  
        else:
           self.DEntry.detachNode()
           self.open=False
    
    
    
    def Parser(self,text):
        Text=text
        # Within 120 seconds on the game
        if self.hero1==None: 
            self.BTNnode.detachNode() 
            if Text == '-random':
               self.hero1=Hero(random.randint(0,96))
            elif Text=='-random int':
               self.hero1=Hero(random.randint(66,96))
            elif Text=='-random str':
               self.hero1=Hero(random.randint(0,36))
            elif Text=='-random agi':
               self.hero1==Hero(random.randint(36,66))
        if Text=='-repick':
            if self.rindex==False:
               if self.hero1!=None:
                  self.hero1.destroy()
                  self.hero1=None
                  self.index=-1
                  self.chooseHero()
                  self.rindex=True
            else:
                 Error("Cannot Repick")      
        elif Text=='-':
             pass          
        else: 
            pass
      #      self.Chat(Text,self.task)
       #     taskMgr.add(self.Chat,"nn",extraArgs=[Text]) 
        #this sends text to allies
        

    def ChatTimer(self,task,chat,i):
        chat.destroy()
        self.chat.insert(i,0)
        self.chatindex-=1        
        return task.done    
    
    def Chat(self,text,task):
        for i in range (1,15):
            if self.chat[i]==0:
               self.text[i]=OnscreenText(text=text,pos=(-1.3,-0.4),fg=(0,0,0,1),scale=0.07)
               self.chat.insert(self.chatindex,1)
               taskMgr.doMethodLater(5,self.ChatTimer,"chat",[task,self.text[i],i])
               self.chatindex+=1
               break
            else:
               self.text[i].setY(-(0.1*i)+0.4)
        return task.done 
         
    def Pause(self):
        if self.pindex!=0:
           self.pindex-=1
           time.sleep(2)
           self.pausebtn['text']="Pause (%d)"%(self.pindex)
        else:
           Error("Pause Limits Used")     
        
    def destroy(self):
        if self.hero1!=None:
           self.hero1.destroy()
        self.minimap.destroy()
        self.btn.detachNode()
        self.BTNnode.detachNode()
        taskMgr.remove('timer')
        self.terrain.detachNode() 
        del self.LightHandler
        del self.creeps
        self.UnSetupEvents()
        

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

class Player:
    def __init__(self,name):
        self.playername=name
        self.no=None

class Player2:
    def __init__(self,no,name):
        self.playerno=no
        self.playername=name
        self.playercolor=color[no]
        
    def selectHero(self):
        #do hero select here
        pass
    
    def playerscore(self):
        #get score here
        pass
    
    def playersend(self):
        #sends player data to server World
        pass
    
    def playerget(self):
        #gets the server data on the minimap and world changes
        pass
    
    def playerstats(self):
        #stores all the player hero's gold,kills,deaths,items for futher use by server
        pass
        