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

class ExitMenu(DirectObject.DirectObject):
    def __init__(self):
        self.accept("escape",self.Create)
        self.open=False

    def Create(self):
        if self.open==False:       
           self.loser=('Lost!','Ya,Quit','Yes!Run to Your Mommy')
           self.panel=OnscreenImage(image='1.png',scale=(0.5,0,0.2))
           self.panel.setTransparency(1)
           self.ext=OnscreenImage(image=MYDIRICONS+'/holy.png',scale=0.05)
           self.ext.setTransparency(1)
           self.comment=OnscreenText(text='',fg=(0,0,0,1),pos=(0,0.2),scale=0.065)
           self.comment.setText(self.loser[random.randint(0,2)])
           self.extb1=DirectButton(text="Yes",pos=(-0.2,0,0),command=sys.exit,text_fg=(0,0.2,0,1),text_pos=(0.05,-0.15),text_scale=0.70,image=(MYDIRIMG+"btnof.png",MYDIRIMG+"btnon.png",MYDIRIMG+"btnon.png",None),frameColor=(0,0,0,0),image_scale=(1.0,0,0.7),scale=(0.15,0,0.10))
           self.extb2=DirectButton(text="No",pos=(0.2,0,0),command=self.__del__,text_fg=(0,0.2,0,1),text_pos=(0.05,-0.15),text_scale=0.70,image=(MYDIRIMG+"btnof.png",MYDIRIMG+"btnon.png",MYDIRIMG+"btnon.png",None),frameColor=(0,0,0,0),image_scale=(1.0,0,0.7),scale=(0.15,0,0.10))
           self.extb1.setTransparency(1)
           self.extb2.setTransparency(1)
           self.open=True

    def __del__(self):
        self.open=False
        self.panel.destroy()
        self.ext.destroy()
        self.comment.destroy()
        self.extb1.destroy()
        self.extb2.destroy()