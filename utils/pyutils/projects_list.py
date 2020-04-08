import os
import sys

HOME_DIR = os.getenv("HOME")
PROJECT_DIRS = ["lun", "rep"]
ORG_DIR = os.path.join(HOME_DIR, 'organizer')

class Project:

    def __init__(self, name):
        self.name = name
        self.main_file = os.path.join(ORG_DIR, '{}.txt'.format(name))
        self.ready = False
        self.repos = []

    def prepare(self):
        if self.ready:
            return

        with open(self.main_file, 'r') as f:
            for l in f.readlines():
                l = l.strip()
                if len(l) == 0: continue

                if l.startswith('@repo'):
                    self.repos = [x.strip() for x in l.split()[1:]]


        self.ready = True

    '''
    Print all file content to stdout
    '''
    def dump_file_content(self):
        with open(self.main_file, 'rb') as f:
            sys.stdout.buffer.write(f.read())

    def put_field(self, key, val):
        field_beg = '<<@OBDEV ### {} ####'.format(key)
        field_end = '>>@OBDEV ### {} ####'.format(key)
        if len(val) == 0 or val[-1] != '\n':
            val += '\n'

        new_lines = []
        skip = False
        with open(self.main_file, 'r') as f:
            for l in f.readlines():
                l = l.strip()
                if l == field_beg:
                    skip = True
                elif l ==field_end:
                    skip = False
                elif not skip:
                    new_lines.append(l)

        with open(self.main_file, 'w') as f:
            for l in new_lines:
                f.write(l + '\n')
            f.write(field_beg + '\n')
            f.write(val)
            f.write(field_end + '\n')
        

def resolve_dirname(path):
    if len(path) == 0:
        return 0
    letter = path[0]
    proj = None
    for p in PROJECT_DIRS:
        if p[0].upper() == letter:
            proj = p
    if proj is None:
        return path

    dirname = os.path.join(HOME_DIR, proj, path[1:])
    if os.path.isdir(dirname):
        return dirname
    return path


_projs = []
def get_projects():
    if len(_projs) == 0:
        projs = [x for x in os.listdir(ORG_DIR) if not x.startswith('_') and x.endswith('.txt')]
        for p in projs:
            _projs.append(Project(os.path.splitext(p)[0]))
    return list(_projs)

def get_project(name):
    projs = get_projects()
    for p in projs:
        if p.name == name:
            p.prepare()
            return p
    raise Exception('Project {} not found'.format(name))
