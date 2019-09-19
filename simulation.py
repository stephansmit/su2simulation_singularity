import os
import subprocess
from spython.main import Client as client
from file import *

class Simulation(object):
    def __init__(self, case_dir, image_dir):
        self.case_dir = case_dir
        self.image_dir= image_dir

    def _pull_image(self):
        client.pull(image=self.image_url,name=self.image_name, pull_folder=self.image_dir)
        return

    def run(self):
        raise NotImplementedError

class SU2Simulation(Simulation):
    def __init__(self, case_dir, image_dir, mesh_dir):
        Simulation.__init__(self,case_dir, image_dir)
        self.mesh_dir=mesh_dir
        self.image_name='su2_container.sif'
        self.image_url = 'shub://stephansmit/su2_containers:fork_dev'
        self.restart_dir = 'restart_files'
    
    def rerun_with_lower_cfl(self, cmd, cores, cfg, log):
        cfg.content['CFL_NUMBER']=0.5*cfg.content['CFL_NUMBER']
        self.run(cmd, cores, cfg, log)

    def run(self, cmd, cores, cfg, log):
        self._pull_image()
        client.load(os.path.join(self.image_dir,self.image_name))
        totalcmd = ['mpirun', '-np', str(cores), '/SU2/bin/'+cmd, cfg.fname]
        output = client.execute(totalcmd, 
                                bind=','.join([self.case_dir+":/data", self.mesh_dir+":/mesh"]), 
                                options=['--pwd','/data', '--cleanenv'], stream=True)
        with open(log.fname, 'w', buffering=100) as lfile:
            for line in output:
                lfile.write(line)
