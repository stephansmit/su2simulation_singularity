try:
    from file import *
    from simulation import SU2Simulation
except:
    from .file import *
    from .simulation import SU2Simulation
class Case(object):
    def __init__(self,cname, work_dir, image_dir):
        self.case_dir = os.path.join(work_dir, cname)
        self.log_dir = 'log'
        self.cfg_dir = 'cfg'
        self.image_dir = image_dir
        self.set_cfgs()
        self.set_logs()

    def create_dir(self):
        os.system('mkdir -p ' + self.case_dir)
        os.system('mkdir -p ' + os.path.join(self.case_dir, self.cfg_dir))
        os.system('mkdir -p ' + os.path.join(self.case_dir, self.log_dir))

    def initialize(self):
        self.create_dir()
        for cfg in self.cfgs:
            cfg.write()

    def set_cfgs(self):
        raise NotImplementedError

    def set_logs(self):
        raise NotImplementedError

    def run(self, ncores):
        raise NotImplementedError

    def run_return(self, ncores):
        raise NotImplementedError

