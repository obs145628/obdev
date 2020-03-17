from .testsuite import UnitTest
import os

def split_all_path(p):

    res = []
    while True:
        p, last = os.path.split(p)
        if last != '':
            res.append(last)
        else:
            if p != '':
                res.append(p)
            break
    return res[::-1]

class FilesTestFinder:

    def __init__(self):
        self.filters = []
        self.dirs = []

    def add_filter(self, f):
        self.filters += [f]

    def add_filter_endswith(self, s):
        self.filters += [lambda x : x.endswith(s)]
        
    def list_recur(self, d):
        res = []
        
        for root, dirs, files in os.walk(d):
            for name in files:
                f = os.path.join(root, name)
                if self.is_valid_file(f):
                    res += [self.get_unit(f, d)]
            
        return res
            

    def list_notrecur(self, d):
        res = []
        for name in os.listdir(d):
            f = os.path.join(d, name)
            if os.path.isfile(f) and self.is_valid_file(f):
                res += [self.get_unit(f, d)]
        return res

    def add_dir(self, d, recursive=False):
        self.dirs += [(d, recursive)]

    

    def find(self):
        res = []
        for d, recursive in self.dirs:
            files = self.list_recur(d) if recursive else self.list_notrecur(d)
            res += files

        res.sort(key = lambda x: x.name)

        return res


    def get_unit(self, f, base_dir):
        f = os.path.abspath(f)
        base_dir = os.path.abspath(base_dir)

        rel_path = os.path.relpath(f, base_dir)
        name = '.'.join(split_all_path(rel_path))

        return UnitTest(name, f)

    def is_valid_file(self, f):
        for ftr in self.filters:
            if not ftr(f):
                return False
        return True
