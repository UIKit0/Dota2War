import os,sys
from math import sqrt,pow
from direct.task import Task
from direct.gui.DirectGui import OnscreenText,OnscreenImage,DirectButton,DirectLabel
import direct.directbase.DirectStart 
from pandac.PandaModules import *
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup

wx=base.win.getXSize()
wy=base.win.getYSize()
MYDIR=os.path.abspath(sys.path[0])
MYDIR=Filename.fromOsSpecific(MYDIR).getFullpath()
MYDIRMODEL=MYDIR+'/Models/'
MYDIRICONS=MYDIR+'/Icons/'
MYDIRIMG=MYDIR+'/Glues/'
MYDIRPART=MYDIR+'/Particles/'
font = loader.loadFont("cmss12")
base.accept("o",base.oobe)
base.setBackgroundColor(0,0,0)
base.disableMouse()
base.enableParticles()
#------------To Do List------------
#1.Create a Unit class for inheritance that sets the display of unit details to make it easier
#2.Create a attack class that sets the attack of unit class
#3.Create a Player class that belongs to a team and same team cant fire at themselves
#4.Create The Network Part of World CLass
#5.Add a LAN Screen With detection
#------------------------------- For Resolution of 1440*900 Wide Screen-----------------------------
if wx>=0 and wy>=0:
   X=1.0
   Y=0.79
   Sx=0.068
   Sy=0.070
   Sc=0.045
   Tx=0.70
   Ty=0.95
   Tsx=0.65
   Tsy=0.055
   posx=1.1
   posy=0.53
   Scale=0.075
   SKtxt=0.05
   IconSx=0.06
   IconSy=0.06
   biconscale=(IconSy,0,IconSy)
   bscale=(0.16,0,0.11) # (0.30,0,0.09) 
   biscale=(1.15,0,0.71) #(1.6,0,0.65)
   btscale=(0.8,0.3)
   btcolor=(1,1,1,1)
   btpos=(0.05,-0.15)
bpos=(posx,0,posy)

HELPTEXT = """
Damage
Armor
Str
Agi
Int
"""
#-------------------------------------Game Constants----------------------------------------------------
SPEED = 5.5
SCROLLSPEED=50
MAPLIMIT=100
bimages=(MYDIRIMG+"btnof.png",MYDIRIMG+"btnon.png",MYDIRIMG+"btnon.png",None)
Team1=[]
Team2=[]
Displayed=False
SERVER=False
#-------------------------------------Game Images--------------------------------------------------
models=('CentaurKhan','Dryad','AshenBush0','ad.x','Magnus')
icons=('kunkaa','beastmaster','centaurkhan','earthshaker','arthas','panda','rogue','tiny','taurenchief',None,None,None,
        None,'bristleback','techies','dragonknight','magnus','huskar','sandking','tide',None,None,None,None,None,
        'axe','nessaj','doombringer',None,'abbadon','lycan','balanar','pitlord','pudge','skeletonking','bara',None,
        'antimage','sniper','yunero','syllabear','luna','motred','siren',None,'mirana','riki','troll',None,
        'gondar','drow','void','meepo','razor','medusa','templar','ursa','silk','murloc',None,None,
        'blood','clinkz','brood','anubarak','weaver','motred','nevermore','terrorblade',None,'venomancer','viper',None,
        'jaina',None,'puck',None,None,'zeus','furion','silencer','slayer',None,'windrunner',None,
        None,'techies','invoker','necrolic','ogremagi',None,'rhasta','tinker','torment','jakiro',None,None,
        None,'darkseer','deathprophet','lion',None,'lich',None,None,None,'akasha','warlock',None
        )


# This is the Data File That contains All the details of the hero including
#HERO NAME
#HERO CLASS
#HERO MODEL
#HERO IMAGES
#HERO TYPE
#STR,AGI,INT
#START HP
#START MANA
#MinDAMAGE
#MaxDAMAGE
#SPEED
#Attackspeed
hero=({'name':'kunnka','type':'str','icon':('kunkaa','lightning','tornado','criticalstrike','death'),'model':'CentaurKhan','range':10,'speed':30,'armor':1,'str':20,'agi':14,'int':11,'strdt':2.7,'agidt':1.2,'intdt':1.5,'min':45,'max':57},
      {'name':'rexxar','type':'str','icon':('beastmaster','ColdArrows','Blue','Cleave','ChaosGrunt'),'model':'Dryad','range':10,'speed':30,'armor':4,'str':22,'agi':19,'int':16,'strdt':2.2,'agidt':1.9,'intdt':1.6,'min':32,'max':43},                          
      )     
      
def DistancePos(self,pos1,target):
    return sqrt(pow(pos1.getX()-target.getX(),2)+pow(pos1.getY()-target.getY(),2))

#----------------------------------------------Error Function----------------------------------  
ErrorText = OnscreenText(pos=(0,-0.5))
def timer(task):
    ErrorText.destroy()
    global ErrorText
    ErrorText=OnscreenText(pos=(0,-0.5))
    taskMgr.remove("tim")
    return task.done
def Error(text):
    ErrorText.setText(text)
    taskMgr.doMethodLater(3,timer,"tim")

#-------------------------------------------Debugging Functions-------------------------
debug1=OnscreenText(pos=(0,-0.5))
debug2=OnscreenText(pos=(-0.1,-0.5))
def Debug1(self,text):
    debug1.setText(text)
def Debug2(self,text):
    debug2.setText(text)
    

def Blink(self):
    self.open=True
    self.accept("escape",self.setOpen)
    if self.open==True:
    #       self.heroPace.stop()
       self.model.setPos(self.mpos3d)
       self.manaspend(100)
       self.setOpen()  

def StatUp(self):
    self.Delta(2,2,2,0,0)
def StatDn(self):
    self.Delta(-2,-2,-2,0,0)
def Ulti(self):
    pass
 
 #------------------------------These are Functions for Particles----------------------------------------#
def Steam(self,model):
    p1 = ParticleEffect()
    p1.cleanup()
    p1 = ParticleEffect()
    p1.loadConfig(Filename(MYDIRPART+'steam.ptf'))        
    p1.start(model)
    p1.setPos(3.000, 0.000, 2.250)

def Flame(self,model):
    p1 = ParticleEffect()
    p1.cleanup()
    p1 = ParticleEffect()
    p1.loadConfig(Filename('ee.ptf'))#'fireish.ptf'))        
    p1.start(model)
    p1.setPos(3.000, 0.000, 2.250)
    setupLights(self,model)

def Water(self,model):
    p1 = ParticleEffect()
    p1.cleanup()
    p1 = ParticleEffect()
    p1.loadConfig(Filename(MYDIRPART+'fountain.ptf'))        
    p1.start(model)
    p1.setPos(3.000, 0.000, 2.250)
    
def Dust(self,model):
    p1 = ParticleEffect()
    p1.cleanup()
    p1 = ParticleEffect()
    p1.loadConfig(Filename(MYDIRPART+'dust.ptf'))        
    p1.start(model)
    p1.setPos(3.000, 0.000, 2.250)

def Smoke(self,model):
    p1 = ParticleEffect()
    p1.cleanup()
    p1 = ParticleEffect()
    p1.loadConfig(Filename(MYDIRPART+'smoke.ptf'))        
    p1.start(model)
    p1.setPos(3.000, 0.000, 2.250)

def SmokeRing(self,model):
    p1 = ParticleEffect()
    p1.cleanup()
    p1 = ParticleEffect()
    p1.loadConfig(Filename(MYDIRPART+'smokering.ptf'))        
    p1.start(model)
    p1.setPos(0, 0.000, 0)

def setupLights(self,model):
        lAttrib = LightAttrib.makeAllOff()
        ambientLight = AmbientLight( "ambientLight" )
        ambientLight.setColor( VBase4(1,1,1,1) )
        lAttrib = lAttrib.addLight( ambientLight )
        directionalLight = DirectionalLight( "directionalLight" )
        directionalLight.setDirection( Vec3( 0, 8, -2.5 ) )
        directionalLight.setColor( Vec4( 0.9, 0.8, 0.9, 1 ) )
        lAttrib = lAttrib.addLight( directionalLight )
        self.model.attachNewNode( directionalLight.upcastToPandaNode() ) 
        self.model.attachNewNode( ambientLight.upcastToPandaNode() ) 
        self.model.node().setAttrib( lAttrib )

    


    
    