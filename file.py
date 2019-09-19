import os
class File(object):
    def __init__(self, fname, workdir, filedir):
        self.filedir = filedir 
        self.workdir = workdir 
        self.fname = os.path.join(filedir, fname)

    def write(self):
        pass

class ConfigFile(File):
    def __init__(self, fname, workdir, cfgdir):
        File.__init__(self, fname, workdir, cfgdir)

    def initialize(self, template):
        self.content = {}
        with open(template, 'r') as f:
            for line in f:
                if line[0].isupper():
                    self.content[line.split('=')[0]]=line.split('=')[1].strip()

    def write(self):
        with open(os.path.join(self.workdir, self.fname), 'w') as f: 
            for key, value in self.content.items():
                f.write("=".join([key, value])+'\n')

class LogFile(File):
    def __init__(self, fname, workdir, logdir):
        File.__init__(self, fname, workdir, logdir)
        self.fname = os.path.join(workdir, logdir, fname)

