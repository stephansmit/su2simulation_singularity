from file import *
from simulation import SU2Simulation

class Case(object):
    def __init__(self,cname, work_dir, image_dir):
       self.case_dir = os.path.join(work_dir, cname)
       self.log_dir = 'log'
       self.cfg_dir = 'cfg'
       self.image_dir = image_dir
       self.set_cfgs()
       self.set_logs()


    def create_dir(self):
       os.system('mkdir ' + self.case_dir)
       os.system('mkdir ' + os.path.join(self.case_dir,self.cfg_dir))
       os.system('mkdir ' + os.path.join(self.case_dir, self.log_dir))

    def set_cfgs(self):
       pass
    
    def set_logs(self):
       self.logs = [LogFile(self.fname+'.log',self.case_dir, self.log_dir),
                    LogFile(self.fname+'_sol.log',self.case_dir, self.log_dir)]

    def initialize(self):
        self.create_dir()
        for cfg in self.cfgs:
            cfg.write()

    def run(self):
       pass


class SU2FOSOCase(Case):
    def __init__(self, cname, work_dir, image_dir, mesh_dir):
       SU2Case.__init__(self, cname, work_dir, image_dir)
       self.cmds = ["SU2_CFD", "SU2_CFD", "SU2_SOL"]


class SU2Case(Case):
    def __init__(self, cname, work_dir, image_dir, mesh_dir):
       Case.__init__(self, cname, work_dir, image_dir)
       self.mesh_dir = mesh_dir
       self.cmds = ["SU2_CFD", "SU2_SOL"]

    def run(self, dry_run=False):
        for i, cmd in enumerate(self.cmds):
           sim = SU2Simulation(self.case_dir, self.image_dir, self.mesh_dir)
           sim.run(cmd, 6, self.cfgs[i], self.logs[i])

    def set_logs(self):
       self.logs = [LogFile(self.fname+'_fo.log',self.case_dir, self.log_dir),
                    LogFile(self.fname+'_so.log',self.case_dir, self.log_dir),
                    LogFile(self.fname+'_sol.og',self.case_dir, self.log_dir)]

class SU2TriogenTurbineFOSOCase(SU2Case):
    def __init__(self, cname, work_dir, image_dir, mesh_dir, rotation_speed):
       self.rotation_speed = rotation_speed
       self.fname = 'turbine'
       SU2Case.__init__(self, cname, work_dir, image_dir, mesh_dir)
       self.cmds = ["SU2_CFD", "SU2_CFD", "SU2_SOL"]

    def set_cfgs(self):
       cfg_fo = SU2MultiConfigFile(self.fname+'_fo.cfg', self.case_dir, self.cfg_dir, self.rotation_speed)
       cfg_fo.initialize('turbine.template.cfg')
       cfg_fo.content['RESTART_SOL']="NO"
       cfg_fo.content['MUSCL_FLOW']="NO"
       cfg_fo.content['MUSCL_TURB']="NO"
       cfg_fo.content['EXT_ITER']=1
       cfg_fo.content['SOLUTION_FLOW_FILENAME']='turbine_fo.dat'
       cfg_fo.content['RESTART_FLOW_FILENAME']='turbine_fo.dat'
       cfg_fo.content['CFL_NUMBER']=1.0
       cfg_so = SU2MultiConfigFile(self.fname+'_so.cfg', self.case_dir, self.cfg_dir, self.rotation_speed)
       cfg_so.initialize('turbine.template.cfg')
       cfg_so.content['RESTART_SOL']="YES"
       cfg_so.content['MUSCL_FLOW']="YES"
       cfg_so.content['MUSCL_TURB']="YES"
       cfg_so.content['EXT_ITER']=1
       cfg_so.content['RESTART_FLOW_FILENAME']='turbine_so.dat'
       cfg_so.content['SOLUTION_FLOW_FILENAME']='turbine_fo.dat'
       cfg_so.content['CFL_NUMBER']=1.0
       self.cfgs = [cfg_fo, cfg_so, cfg_so]


class SU2TriogenTurbineCase(SU2Case):
    def __init__(self, cname, work_dir, image_dir, mesh_dir, rotation_speed):
       self.rotation_speed = rotation_speed
       self.fname = 'turbine'
       SU2Case.__init__(self, cname, work_dir, image_dir, mesh_dir)

    def set_cfgs(self):
       cfg = SU2MultiConfigFile(self.fname+'.cfg', self.case_dir, self.cfg_dir, self.rotation_speed)
       cfg.initialize('turbine.template.cfg')
       cfg.content['RESTART_SOL']="NO"
       cfg.content['SOLUTION_FLOW_FILENAME']='turbine.dat'
       cfg.content['CFL_NUMBER']=1.0
       self.cfgs = [cfg, cfg]


class SU2TriogenStatorCase(SU2Case):
    def __init__(self, cname, work_dir, image_dir, mesh_dir):
       self.fname = 'stator'
       SU2Case.__init__(self, cname, work_dir, image_dir, mesh_dir)

    def set_cfgs(self):
       cfg = ConfigFile(self.fname+'.cfg', self.case_dir, self.cfg_dir)
       cfg.initialize('stator.template.cfg')
       cfg.content['RESTART_SOL']="NO"
       cfg.content['SOLUTION_FLOW_FILENAME']='stator.dat'
       self.cfgs = [cfg, cfg]

class SU2TriogenStatorFOSOCase(SU2Case):
    def __init__(self, cname, work_dir, image_dir, mesh_dir):
       self.fname = 'stator'
       SU2Case.__init__(self, cname, work_dir, image_dir, mesh_dir)
       self.cmds = ["SU2_CFD", "SU2_CFD", "SU2_SOL"]


    def set_cfgs(self):
       cfg_fo = ConfigFile(self.fname+'_fo.cfg', self.case_dir, self.cfg_dir)
       cfg_fo.initialize('stator.template.cfg')
       cfg_fo.content['RESTART_SOL']="NO"
       cfg_fo.content['MUSCL_FLOW']="NO"
       cfg_fo.content['MUSCL_TURB']="NO"
       cfg_fo.content['EXT_ITER']=1
       cfg_fo.content['SOLUTION_FLOW_FILENAME']='stator_fo.dat'
       cfg_fo.content['RESTART_FLOW_FILENAME']='stator_fo.dat'
       cfg_fo.content['CFL_NUMBER']=1.0
       cfg_so = ConfigFile(self.fname+'_so.cfg', self.case_dir, self.cfg_dir)
       cfg_so.initialize('stator.template.cfg')
       cfg_so.content['RESTART_SOL']="YES"
       cfg_so.content['MUSCL_FLOW']="YES"
       cfg_so.content['MUSCL_TURB']="YES"
       cfg_so.content['EXT_ITER']=1
       cfg_so.content['RESTART_FLOW_FILENAME']='stator_so.dat'
       cfg_so.content['SOLUTION_FLOW_FILENAME']='stator_fo.dat'
       cfg_so.content['CFL_NUMBER']=1.0
       self.cfgs = [cfg_fo, cfg_so, cfg_so]

