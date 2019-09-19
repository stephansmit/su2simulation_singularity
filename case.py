from file import *
from simulation import SU2Simulation

class Case(object):
    def __init__(self,cname, work_dir, image_dir):
       self.case_dir = os.path.join(work_dir, cname)
       self.log_dir = 'log'
       self.cfg_dir = 'cfg'
       self.image_dir = image_dir
       self.set_cfg()
       self.set_log()


    def create_dir(self):
       os.system('mkdir ' + self.case_dir)
       os.system('mkdir ' + os.path.join(self.case_dir,self.cfg_dir))
       os.system('mkdir ' + os.path.join(self.case_dir, self.log_dir))

    def set_cfg(self):
       pass

    def set_log(self):
       pass 

    def run(self):
       pass


class SU2TriogenStatorCase(Case):
    def __init__(self, cname, work_dir, image_dir, mesh_dir):
       Case.__init__(self, cname, work_dir, image_dir)
       self.mesh_dir = mesh_dir

    def set_cfg(self):
       self.cfg = ConfigFile('stator.cfg', self.case_dir, self.cfg_dir)
       self.cfg.initialize('template.cfg')
       self.cfg.content['RESTART_SOL']="NO"

    def set_log(self):
       self.log = LogFile('stator.log',self.case_dir, self.log_dir)

    def run(self, dry_run=False):
       self.create_dir()
       self.cfg.write()
       if not dry_run:
           sim = SU2Simulation(self.case_dir, self.image_dir, self.mesh_dir)
           sim.run("SU2_CFD", 6, self.cfg, self.log)
