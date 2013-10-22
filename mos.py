from direct.showbase.ShowBase import Plane, ShowBase, Vec3, Point3, CardMaker 


class YourClass(ShowBase): 
  def __init__(self): 
    ShowBase.__init__(self) 
    self.disableMouse()
    self.pos3d=None
    self.nearPoint=None
    self.farPoint=None 
    self.camera.setPos(0, 60, 25) 
    self.camera.lookAt(0, 0, 0) 
    z = 0 
    self.plane = Plane(Vec3(0, 0, 1), Point3(0, 0, z)) 
    self.model = loader.loadModel("ralph") 
    self.model.reparentTo(render) 
    self.accept("mouse1",self.set)
    taskMgr.add(self.__getMousePos, "_YourClass__getMousePos") 
  
  def __getMousePos(self, task): 
    if base.mouseWatcherNode.hasMouse(): 
      mpos = base.mouseWatcherNode.getMouse() 
      self.pos3d = Point3() 
      self.nearPoint = Point3() 
      self.farPoint = Point3() 
      base.camLens.extrude(mpos, self.nearPoint, self.farPoint) 
      if self.plane.intersectsLine(self.pos3d, 
          render.getRelativePoint(camera, self.nearPoint), 
          render.getRelativePoint(camera, self.farPoint)): 
        print "Mouse ray intersects ground plane at ", self.pos3d 
       # self.model.setPos(render, pos3d) 
    return task.again 
  def set(self):
      self.model.setPos(render, self.pos3d) 
YourClass();base.taskMgr.run()