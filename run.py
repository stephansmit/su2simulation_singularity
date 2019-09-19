from su2case import *
import math 
import os 
import sys

cname = sys.argv[1]
image_dir = os.path.join(os.getcwd(), 'images')
work_dir = os.getcwd()

if cname=='stator':
    mesh_dir = os.path.join(os.getcwd(), 'stator_mesh')
    c = SU2TriogenStatorFOSOCase( cname, work_dir, image_dir, mesh_dir)
elif cname=='turbine':
    mesh_dir = os.path.join(os.getcwd(), 'turbine_mesh')
    rotation_speed = 426*math.pi
    nblades = 47
    c = SU2TriogenTurbineFOSOCase( cname, work_dir, image_dir, mesh_dir, rotation_speed, nblades)

c.initialize()
c.run(6)
