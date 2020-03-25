try:
    from file import *
    from simulation import SU2Simulation
    from case import Case
except:
    from .file import *
    from .simulation import SU2Simulation
    from .case import Case



class SU2Case(Case):
    def __init__(self, cname, work_dir, image_dir, mesh_dir):
       Case.__init__(self, cname, work_dir, image_dir)
       self.mesh_dir = mesh_dir
       self.cmds = ["SU2_CFD", "SU2_SOL"]
    
    def set_logs(self):
       self.logs = [LogFile(self.fname+'.log',self.case_dir, self.log_dir),
                    LogFile(self.fname+'_sol.log',self.case_dir, self.log_dir)]

    def run(self,ncores):
        for i, cmd in enumerate(self.cmds):
           sim = SU2Simulation(self.case_dir, self.image_dir, self.mesh_dir)
           sim.run(cmd, ncores, self.cfgs[i], self.logs[i])

class SU2FOSOCase(SU2Case):
    def __init__(self, cname, work_dir, image_dir, mesh_dir):
       SU2Case.__init__(self, cname, work_dir, image_dir,mesh_dir)
       self.cmds = ["SU2_CFD", "SU2_CFD", "SU2_SOL"]
    
    def set_logs(self):
       self.logs = [LogFile(self.fname+'_fo.log',self.case_dir, self.log_dir),
                    LogFile(self.fname+'_so.log',self.case_dir, self.log_dir),
                    LogFile(self.fname+'_sol.og',self.case_dir, self.log_dir)]

class SU2TriogenTurbineCase(SU2Case):
    def __init__(self, cname, work_dir, image_dir, mesh_dir, rotation_speed, nblades):
       self.rotation_speed = rotation_speed
       self.nblades = nblades
       self.fname = 'turbine'
       SU2Case.__init__(self, cname, work_dir, image_dir, mesh_dir)

    def set_cfgs(self):
       cfg = SU2MultiConfigFile(self.fname+'.cfg', self.case_dir, self.cfg_dir)
       cfg.initialize('turbine.template.cfg')
       cfg.content['RESTART_SOL']="NO"
       cfg.content['SOLUTION_FLOW_FILENAME']='turbine.dat'
       cfg.content['CFL_NUMBER']=1.0
       cfg.set_number_blades(self.nblades)
       cfg.set_rotational_speed(self.rotation_speed)
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

class SU2TriogenTurbineFOSOCase(SU2FOSOCase):
    def __init__(self, cname, work_dir, image_dir, mesh_dir, rotation_speed, nblades):
       self.rotation_speed = rotation_speed
       self.nblades = nblades
       self.fname = 'turbine'
       SU2FOSOCase.__init__(self, cname, work_dir, image_dir, mesh_dir)

    def set_cfgs(self):
       cfg_fo = SU2MultiConfigFile(self.fname+'_fo.cfg', self.case_dir, self.cfg_dir)
       cfg_fo.initialize('turbine.template.cfg')
       cfg_fo.content['RESTART_SOL']="NO"
       cfg_fo.content['EXT_ITER']=1
       cfg_fo.content['SOLUTION_FLOW_FILENAME']='turbine_fo.dat'
       cfg_fo.content['RESTART_FLOW_FILENAME']='turbine_fo.dat'
       cfg_fo.content['CFL_NUMBER']=1.0
       cfg_fo.content['CONV_FILENAME']='history_fo'
       cfg_fo.set_number_blades(self.nblades)
       cfg_fo.set_rotational_speed(self.rotation_speed)
       cfg_fo.set_first_order()
       cfg_so = SU2MultiConfigFile(self.fname+'_so.cfg', self.case_dir, self.cfg_dir)
       cfg_so.initialize('turbine.template.cfg')
       cfg_so.content['RESTART_SOL']="YES"
       cfg_so.content['EXT_ITER']=1
       cfg_so.content['RAMP_OUTLET_PRESSURE']="NO"
       cfg_so.content['RESTART_FLOW_FILENAME']='turbine_so.dat'
       cfg_so.content['SOLUTION_FLOW_FILENAME']='turbine_fo.dat'
       cfg_so.content['CFL_NUMBER']=1.0
       cfg_so.content['CONV_FILENAME']='history_so'
       cfg_so.set_number_blades(self.nblades)
       cfg_so.set_rotational_speed(self.rotation_speed)
       cfg_so.set_second_order()
       self.cfgs = [cfg_fo, cfg_so, cfg_so]

class SU2TriogenTurbineFOSOCase_WInletConditions(SU2FOSOCase):
    def __init__(self, cname, work_dir, image_dir, mesh_dir, rotation_speed, nblades, total_temperature, total_pressure):
       self.rotation_speed = rotation_speed
       self.nblades = nblades
       self.total_temperature = total_temperature
       self.total_pressure = total_pressure
       self.fname = 'turbine'
       SU2FOSOCase.__init__(self, cname, work_dir, image_dir, mesh_dir)

    def set_cfgs(self):
       cfg_fo = SU2MultiConfigFile(self.fname+'_fo.cfg', self.case_dir, self.cfg_dir)
       cfg_fo.initialize('turbine.template.cfg')
       cfg_fo.content['RESTART_SOL']="NO"
       cfg_fo.content['EXT_ITER']=1
       cfg_fo.content['SOLUTION_FLOW_FILENAME']='turbine_fo.dat'
       cfg_fo.content['RESTART_FLOW_FILENAME']='turbine_fo.dat'
       cfg_fo.content['CFL_NUMBER']=1.0
       cfg_fo.content['MARKER_GILES']="(inflow, TOTAL_CONDITIONS_PT, "+str(self.total_pressure)+","+str(self.total_temperature)+", 1.0, 0.0, 0.0, 0.9, 0.0, outmix, MIXING_OUT, 0.0, 0.0, 0.0, 0.0, 0.0, 0.95, 0.0, inmix, MIXING_IN, 0.0, 0.0, 0.0, 0.0, 0.0, 0.95,0.0, outflow, STATIC_PRESSURE, 20000, 0.0, 0.0, 0.0, 0.0 , 1.0,0.0)"
       cfg_fo.content['CFL_NUMBER']=1.0
       cfg_fo.content['CONV_FILENAME']='history_fo'
       cfg_fo.set_number_blades(self.nblades)
       cfg_fo.set_rotational_speed(self.rotation_speed)
       cfg_fo.set_first_order()
       cfg_so = SU2MultiConfigFile(self.fname+'_so.cfg', self.case_dir, self.cfg_dir)
       cfg_so.initialize('turbine.template.cfg')
       cfg_so.content['RESTART_SOL']="YES"
       cfg_so.content['EXT_ITER']=1
       cfg_so.content['MARKER_GILES']="(inflow, TOTAL_CONDITIONS_PT, "+str(self.total_pressure)+","+str(self.total_temperature)+", 1.0, 0.0, 0.0, 0.9, 0.0, outmix, MIXING_OUT, 0.0, 0.0, 0.0, 0.0, 0.0, 0.95, 0.0, inmix, MIXING_IN, 0.0, 0.0, 0.0, 0.0, 0.0, 0.95,0.0, outflow, STATIC_PRESSURE, 20000, 0.0, 0.0, 0.0, 0.0 , 1.0,0.0)"
       cfg_so.content['RAMP_OUTLET_PRESSURE']="NO"
       cfg_so.content['RESTART_FLOW_FILENAME']='turbine_so.dat'
       cfg_so.content['SOLUTION_FLOW_FILENAME']='turbine_fo.dat'
       cfg_so.content['CFL_NUMBER']=1.0
       cfg_so.content['CONV_FILENAME']='history_so'
       cfg_so.set_number_blades(self.nblades)
       cfg_so.set_rotational_speed(self.rotation_speed)
       cfg_so.set_second_order()
       self.cfgs = [cfg_fo, cfg_so, cfg_so]

class SU2TriogenTurbinePPCase(SU2Case):
    def __init__(self, cname, work_dir, image_dir, mesh_dir):
       self.fname = 'turbine'
       SU2Case.__init__(self, cname, work_dir, image_dir, mesh_dir)

    def set_cfgs(self):
       cfg_pp = SU2ConfigFile(self.fname + "_sol.cfg", self.case_dir, self.cfg_dir)
       cfg_pp.initialize(os.path.join(self.case_dir, 'cfg', 'turbine_so.cfg'))
       cfg_pp.content['EXT_ITER']=1
       cfg_pp.content['SOLUTION_FLOW_FILENAME']='turbine_so.dat'
       cfg_pp.content['RESTART_SOL']='YES'
       cfg_pp.content.pop('DV_PARAM', None)
       cfg_pp.content.pop('DV_VALUE', None)
       self.cfgs = [cfg_pp, cfg_pp]

    def set_logs(self):
       self.logs = [LogFile(self.fname+'_pp.log',self.case_dir, self.log_dir),
                    LogFile(self.fname+'_sol.log',self.case_dir, self.log_dir)]

class SU2TriogenStatorFOSOCase(SU2FOSOCase):
    def __init__(self, cname, work_dir, image_dir, mesh_dir):
       self.fname = 'stator'
       SU2FOSOCase.__init__(self, cname, work_dir, image_dir, mesh_dir)

    def set_cfgs(self):
       cfg_fo = SU2ConfigFile(self.fname+'_fo.cfg', self.case_dir, self.cfg_dir)
       cfg_fo.initialize('stator.template.cfg')
       cfg_fo.content['RESTART_SOL']="NO"
       cfg_fo.content['EXT_ITER']=1
       cfg_fo.content['SOLUTION_FLOW_FILENAME']='stator_fo.dat'
       cfg_fo.content['RESTART_FLOW_FILENAME']='stator_fo.dat'
       cfg_fo.content['CFL_NUMBER']=1.0
       cfg_fo.content['CONV_FILENAME']='history_fo'
       cfg_fo.set_first_order()
       cfg_so = SU2ConfigFile(self.fname+'_so.cfg', self.case_dir, self.cfg_dir)
       cfg_so.initialize('stator.template.cfg')
       cfg_so.content['RESTART_SOL']="YES"
       cfg_so.content['EXT_ITER']=1
       cfg_so.content['RAMP_OUTLET_PRESSURE']="NO"
       cfg_so.content['RESTART_FLOW_FILENAME']='stator_so.dat'
       cfg_so.content['SOLUTION_FLOW_FILENAME']='stator_fo.dat'
       cfg_so.content['CFL_NUMBER']=1.0
       cfg_so.content['CONV_FILENAME']='history_so'
       cfg_so.set_second_order()
       self.cfgs = [cfg_fo, cfg_so, cfg_so]

class SU2TriogenTurbine3D_FOCase(SU2Case):
    def __init__(self, cname, work_dir, image_dir, mesh_dir, sol_dir,rotation_speed, nblades, total_temperature, total_pressure):
       self.sol_dir = sol_dir
       self.rotation_speed = rotation_speed
       self.nblades = nblades
       self.total_temperature = total_temperature
       self.total_pressure = total_pressure
       self.fname = 'turbine'
       SU2Case.__init__(self, cname, work_dir, image_dir, mesh_dir)
       self.cmds = ["SU2_CFD", "SU2_CFD"]

    def set_cfgs(self):
        cfg_1iter = SU2MultiConfigFile(self.fname+'_1iter.cfg', self.case_dir, self.cfg_dir)
        cfg_1iter.initialize('turbine.template.cfg')
        cfg_1iter.content['RESTART_SOL']="NO"
        cfg_1iter.content['OUTER_ITER']=2
        cfg_1iter.content['SOLUTION_FILENAME']='turbine_fo.dat'
        cfg_1iter.content['WRT_SOL_FREQ']=1
        cfg_1iter.content['OUTPUT_WRT_FREQ']=1
        cfg_1iter.content['RESTART_FILENAME']='turbine_fo.dat'
        cfg_1iter.content['RAMP_ROTATING_FRAME']="YES"
        cfg_1iter.set_speed_ramp_coeff(39,10000)
        cfg_1iter.content['VOLUME_FILENAME']='flow_fo'
        cfg_1iter.content['RELAXATION_FACTOR_TURB']=0.75
        cfg_1iter.content['RELAXATION_FACTOR_FLOW']=0.75
        cfg_1iter.content['MARKER_GILES']="(inflow, TOTAL_CONDITIONS_PT, "+str(self.total_pressure)+","+str(self.total_temperature)+", 1.0, 0.0, 0.0, 0.9, 0.0, outmix, MIXING_OUT, 0.0, 0.0, 0.0, 0.0, 0.0, 0.95, 0.0, inmix, MIXING_IN, 0.0, 0.0, 0.0, 0.0, 0.0, 0.95,0.0, outflow, STATIC_PRESSURE, 20000, 0.0, 0.0, 0.0, 0.0 , 1.0,0.0)"
        cfg_1iter.content['CFL_NUMBER']=1.0
        cfg_1iter.content['CONV_FILENAME']='history_fo'
        cfg_1iter.set_number_blades(self.nblades)
        cfg_1iter.set_rotational_speed(self.rotation_speed)
        cfg_1iter.set_first_order()

        cfg_fo = SU2MultiConfigFile(self.fname+'_fo.cfg', self.case_dir, self.cfg_dir)
        cfg_fo.initialize('turbine.template.cfg')
        cfg_fo.content['OUTER_ITER']=100000
        cfg_fo.content['WRT_SOL_FREQ']=100
        cfg_fo.content['OUTPUT_WRT_FREQ']=100
        cfg_fo.content['RESTART_SOL']="YES"
        cfg_fo.content['RAMP_ROTATING_FRAME']="YES"
        cfg_fo.set_speed_ramp_coeff(39,10000)
        cfg_fo.content['SOLUTION_FILENAME']='turbine_fo.dat'
        cfg_fo.content['RESTART_FILENAME']='turbine_fo.dat'
        cfg_fo.content['VOLUME_FILENAME']='flow_fo'
        cfg_fo.content['RELAXATION_FACTOR_TURB']=0.75
        cfg_fo.content['RELAXATION_FACTOR_FLOW']=0.75
        cfg_fo.content['MARKER_GILES']="(inflow, TOTAL_CONDITIONS_PT, "+str(self.total_pressure)+","+str(self.total_temperature)+", 1.0, 0.0, 0.0, 0.9, 0.0, outmix, MIXING_OUT, 0.0, 0.0, 0.0, 0.0, 0.0, 0.95, 0.0, inmix, MIXING_IN, 0.0, 0.0, 0.0, 0.0, 0.0, 0.95,0.0, outflow, STATIC_PRESSURE, 20000, 0.0, 0.0, 0.0, 0.0 , 1.0,0.0)"
        cfg_fo.content['CFL_NUMBER']=1.0
        cfg_fo.content['CONV_FILENAME']='history_fo'
        cfg_fo.set_number_blades(self.nblades)
        cfg_fo.set_rotational_speed(self.rotation_speed)
        cfg_fo.set_first_order()

        self.cfgs = [cfg_1iter, cfg_fo]
    
    def run(self,ncores):
       sim = SU2Simulation(self.case_dir, self.image_dir, self.mesh_dir)
       sim.image_url = 'shub://stephansmit/su2_containers:fork_blackbird_v7.0.2'
       sim.run(self.cmds[0], ncores, self.cfgs[0], self.logs[0])
       print("Copying the converged stator")
       os.system('cp '+ os.path.join(self.sol_dir, 'stator_fo_0.dat')+" "+ os.path.join(self.case_dir,"turbine_fo_0.dat") )
       sim.run(self.cmds[1], ncores, self.cfgs[1], self.logs[1])
    
    def set_logs(self):
       self.logs = [LogFile(self.fname+'_1iter.log',self.case_dir, self.log_dir),
                    LogFile(self.fname+'_fo.log',self.case_dir, self.log_dir)]

