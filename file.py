import os
import math
class File(object):
    def __init__(self, fname, workdir, filedir):
        self.filedir = filedir 
        self.workdir = workdir 
        self.fname = os.path.join(filedir, fname)
        self.content = {}

class ConfigFile(File):
    def __init__(self, fname, workdir, cfgdir):
        File.__init__(self, fname, workdir, cfgdir)

    def initialize(self, template):
        with open(template, 'r') as f:
            for line in f:
                if line[0].isupper():
                    self.content[line.split('=')[0]]=line.split('=')[1].strip()

    def _write_file(self):
        with open(os.path.join(self.workdir, self.fname), 'w') as f: 
            for key, value in self.content.items():
                f.write("=".join([key, str(value)])+'\n')

    def write(self):
        self._write_file()

class SU2ConfigFile(ConfigFile):
    def __init__(self, fname, workdir, cfgdir):
        ConfigFile.__init__(self, fname, workdir, cfgdir)

    def set_second_order(self):
        self.content['MUSCL_TURB']="YES"
        self.content['MUSCL_FLOW']="YES"

    def set_first_order(self):
        self.content['MUSCL_TURB']="NO"
        self.content['MUSCL_FLOW']="NO"

    def set_speed_ramp_coeff(self, iter, max_iter):
        self.content['RAMP_ROTATING_FRAME_COEFF']="(0.0,"+str(iter)+","+str(max_iter)+")"

class SU2MultiConfigFile(SU2ConfigFile):
    def __init__(self, fname, workdir, cfgdir):
        SU2ConfigFile.__init__(self, fname, workdir, cfgdir)
        self.zone1= ConfigFile("zone_1.cfg", workdir, cfgdir)
        self.zone1.content['GRID_MOVEMENT']='ROTATING_FRAME'
        self.zone1.content['MACH_MOTION']=0.35
        self.zone1.content['MOTION_ORIGIN']='0.0 0.0 0.0'
        self.zone1.content['ROTATION_RATE'] ='0.0 0.0 0.0'
        self.zone2 = ConfigFile("zone_2.cfg", self.workdir, cfgdir)
        self.zone2.content['GRID_MOVEMENT']='ROTATING_FRAME'
        self.zone2.content['MACH_MOTION']=0.35
        self.zone2.content['MOTION_ORIGIN']='0.0 0.0 0.0'
        self.zone2.content['ROTATION_RATE'] ='0.0 0.0 '+str(426*math.pi*2)

    def set_rotational_speed(self, rotation_speed):
        self.zone2.content['ROTATION_RATE'] ='0.0 0.0 '+str(rotation_speed)

    def set_number_blades(self, nblades):
        self.content['MARKER_PERIODIC']= '(per_1, per_2, 0.0, 0.0, 0.0, 0.0, 0.0, -20, 0.0, 0.0, 0.0, ' + \
                                         'per_5, per_6, 0.0, 0.0, 0.0, 0.0, 0.0,'+str(360./float(nblades))+', 0.0, 0.0, 0.0)'
   
    def write(self):
        self._write_file()
        self.zone1._write_file()
        self.zone2._write_file()
    
class LogFile(File):
    def __init__(self, fname, workdir, logdir):
        File.__init__(self, fname, workdir, logdir)
        self.fname = os.path.join(workdir, logdir, fname)

