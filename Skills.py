from Global import DistancePos
# These are all the skills of the Heroes
def Hex(hero):
    hero.name = loader.loadmodel("/c/hex")
    hero.name.reparentTo(render)
    hero.name.setSpeed(25)
    
    
def lifesteal(hero):
    lifesteal=hero.getDamage*0.10
    hero.heal(lifesteal)

def ChaosBlink(self,hero,target):
    self.hero=hero.getPos()
    self.target=target.getPos()
    self.dist=DistancePos(self,self.hero,self.target)
    self.hero.setPos()

class Skill:
    def __init__(self):
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
    
    def burrowstrike():
        sandking.play(burrow)
        sandking.SetPos(hero.getX()+10,hero.getY()+10,0)
        
    def sandstorm():
        play(sandanimation)
        sandking.setAtlpha(0.5)
        sandking.reparentTo(hidden)
        #Draw a sphere of raduis 100 and any unit in that area recieves damage
   
    
    def causticfinale():
        pass

    def epicenter():
        sandking.set
    
         
class SKKSkill:
    def __init__(self):
        pass

#Morphlings Skill 3 hero.Delta(2,-2,0) changes the str+2 and agi-2 and put it in a domethodlater task of delay 1 sec 