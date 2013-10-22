import direct.directbase.DirectStart
from direct.task import Task
from pandac.PandaModules import *
from direct.gui.DirectGui import DirectSlider
from direct.gui.DirectGui import OnscreenText
from math import pi, sin, cos
# set the ambient light
class Lights:
    def __init__(self, parent=None):
        self.txt = aspect2d.attachNewNode("txt")
        # 12 minute = 720 seconds = 1 day in the game
        self.daySeconds = 10
        self.days = 0
        self.hour = self.daySeconds / 24.0
        ang=20
        day_second=0
        # set the sunlight
        self.sun = DirectionalLight('sun')
        self.sun.setColor(VBase4(1,1,1,1))
        self.sun_node = render.attachNewNode(self.sun)
        self.sun_node.setHpr(0, -10, 0)
        render.setLight(self.sun_node)
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.12, 0.12, 0.12, 1))
        alnp = render.attachNewNode(alight)
        render.setLight(alnp)
        taskMgr.add(self.meteo, "meteo")
        self.Text= OnscreenText(text="Set Brightness",parent =self.txt,pos=(-1.25,-0.35),scale=0.1)
        self.slider = DirectSlider(range=(0,360), value=60,parent =self.txt, pos =(-1.25,0,-0.4),pageSize=2,scale =(0.3,0.3,0.3), command=self.setLight)
    
    def setLight(self):
         self.sun_node.setP (-self.slider['value']) 
    
    # method that manages the sun movement
    def meteo(self, task):
        day_second = task.time
        SunTime=day_second*18              # The Multiplier Changes the speed of the sun
        angrad=day_second*(pi/180)
       # self.sun_node.setPos(20*sin(angrad),-20*cos(angrad),0)
       # self.sun_node.setHpr(SunTime, -10, 0) #This Produces the Sun light within the grass set p = SunTime for whole Map
     
        # if the day is finished
        if day_second > self.daySeconds:
            self.days += 1
        
        # if is day
        if day_second < self.daySeconds*0.6:
            day_hour = day_second / self.hour
           # self.sun_node.setHpr(day_second*15, -10, 0)
        
        return task.cont

    def destroy(self):
        taskMgr.remove("meteo")
        self.txt.detachNode()
        self.sun_node.detachNode()
        self.alnp.detachNode()
        