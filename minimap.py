from direct.gui.OnscreenImage import OnscreenImage 
from direct.gui.DirectGui import * 
from direct.showbase.DirectObject import DirectObject 
from pandac.PandaModules import * 
import os

class minimap:   #a strategic minimap to display on screen 

   image = None   #the PNMImage 
   onscreen = None      #the OnscreenImage to show mini-map on 
   texture = None   # the texture image is saved to 
   map = None      #the map as represented by a multi-dimensional array of many '1' and '2'. 


   def __init__(self, map = None): 
    
      if map == None:      #if no map given, default image size 
         self.image = PNMImage(256,256) 
         self.image.fill(0,0,0) 
      else:   #if map given, image is size of map 
         self.image = PNMImage(len(map[0]), len(map)) 
         self.image.fill(0,0,0) 
          
   #   self.image.write("minimap.png")      #saves the mini-map to hard drive (I just wanted to, not sure if necessary or not.) 
       
      self.map = map 
      self.texture = Texture() 
      self.texture.load(os.path.join('Glues','minimap.tga')) 
      self.onscreen = OnscreenImage(image=self.texture,pos=(-1.4,0,-0.81),scale=(0.2,0,0.19)) 
       
       

   def createmap(self, map):   #updates the map 
      self.image.clear() 
      del self.image 
      self.image = PNMImage(len(map[0]),len(map))      #if map size has changed, 
       
      for i in range(0, len(map)): 
         for me in range(0, len(map[0])): 
             
             
            if map[i][me] == 2: 
               self.image.setXel( me , len(map)-1 - i , 0,1,0) 
            if map[i][me] == 1: 
               self.image.setXel( me , len(map)-1 - i , 0,0,1)             
       


   def __update__(self, map):      #a update function to be called every frame or every couple. 
      pass 
      self.createmap(map)   #update map 
      self.texture.load(self.image)   #save map image to texture 
      self.onscreen.setImage(self.texture)   #set onscreenimage to that texture 


   def destroy(self):
       self.onscreen.destroy()