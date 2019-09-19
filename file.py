import os
class File(object):
    def __init__(self, fname, workdir, filedir):
        self.filedir = filedir 
        self.workdir = workdir 
        self.fname = os.path.join(filedir, fname)
        self.content = {}

    def write(self):
        pass

class ConfigFile(File):
    def __init__(self, fname, workdir, cfgdir):
        File.__init__(self, fname, workdir, cfgdir)

    def initialize(self, template):
        with open(template, 'r') as f:
            for line in f:
                if line[0].isupper():
                    self.content[line.split('=')[0]]=line.split('=')[1].strip()
    def _write_zones(self):
        pass

    def write(self):
        self._write_zones()
        with open(os.path.join(self.workdir, self.fname), 'w') as f: 
            for key, value in self.content.items():
                f.write("=".join([key, str(value)])+'\n')

class SU2MultiConfigFile(ConfigFile):
    def __init__(self, fname, workdir, cfgdir, rotation_speed):
        ConfigFile.__init__(self, fname, workdir, cfgdir)
        zone1= ConfigFile("zone_1.cfg", workdir, cfgdir)
        zone1.content['GRID_MOVEMENT']='NONE'
        zone2 = ConfigFile("zone_2.cfg", self.workdir, cfgdir)
        zone2.content['GRID_MOVEMENT']='ROTATING_FRAME'
        zone2.content['MACH_MOTION']=0.35
        zone2.content['MOTION_ORIGIN']='0.0 0.0 0.0'
        zone2.content['ROTATION_RATE'] ='0.0 0.0 '+str(rotation_speed)
        self.zones = [zone1, zone2]
   
    def _write_zones(self):
        for z in self.zones:
           with open(os.path.join(self.workdir, z.fname), 'w') as f: 
                for key, value in self.content.items():
                    f.write("=".join([key, str(value)])+'\n')


class LogFile(File):
    def __init__(self, fname, workdir, logdir):
        File.__init__(self, fname, workdir, logdir)
        self.fname = os.path.join(workdir, logdir, fname)

