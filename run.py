from case import *
import math 
import os 

cname = "turbine"
image_dir = os.path.join(os.getcwd(), 'images')
mesh_dir = os.path.join(os.getcwd(), 'turbine_mesh')
#mesh_dir = os.path.join(os.getcwd(), 'stator_mesh')
work_dir = os.getcwd()
rotation_speed = 426*math.pi
nblades = 47
#c = SU2TriogenStatorFOSOCase( cname, work_dir, image_dir, mesh_dir)
#print(c)
c = SU2TriogenTurbineFOSOCase( cname, work_dir, image_dir, mesh_dir, rotation_speed, 47)
#print(c.cfgs)
c.initialize()
c.run(6)
