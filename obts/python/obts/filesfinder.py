import enum
import os

'''
Find files/dir in a specific folder.
Use filters to only select a subset of all files/dirs
Can be recursive or not
3 types of filter:
- File: to select a file
- Dir: to select a dir
- Rec: to recursively check dir content
'''

class FilterType(enum.Enum):
    File = 1
    Dir = 2
    Rec = 3

class FilesFinder:

    def __init__(self):
        self.filters_file = []
        self.filters_dir = []
        self.filters_rec = []

    '''
    Run the filtering on `dpath`
    Returns a pair of lists (files, dirs)
    Lists are unordered absolute paths
    '''
    def run(self, dpath):
        dpath = os.path.abspath(dpath)
        self.root = dpath

        all_files = []
        all_dirs = []
        
        for root, dirs, files in os.walk(dpath, topdown=True):

            if not self._apply_filters(root, FilterType.Rec):
                files[:] = []
                dirs[:] = []
            
            for name in files:
                f = os.path.join(root, name)
                if self._apply_filters(f, FilterType.File):
                    all_files.append(f)
            for name in dirs:
                f = os.path.join(root, name)
                if self._apply_filters(f, FilterType.Dir):
                    all_dirs.append(f)
            

        return all_files, all_dirs
    

    '''
    Add a filter function that must return True to validate a file/dir
    @param fn - function(abs_path, root_path): bool
    @param ftype - type of filter
    '''
    def filter(self, fn, ftype):
        if ftype == FilterType.File:
            self.filters_file.append(fn)
        elif ftype == FilterType.Dir:
            self.filters_dir.append(fn)
        if ftype == FilterType.Rec:
            self.filters_rec.append(fn)

    # Never select any dirs
    def filter_no_dir(self):
        def fn(*_): return False
        self.filter(fn, FilterType.Dir)

    # Never select any dirs
    def filter_no_file(self):
        def fn(*_): return False
        self.filter(fn, FilterType.File)

    # Disable recursion
    def filter_no_recursion(self):
        def fn(path, root): return path == root
        self.filter(fn, FilterType.Rec)

    # Ignore types recursively
    def ignore_dir(self, dirname):
        def fn(path, _): return os.path.basename(path) != dirname
        self.filter(fn, FilterType.Rec) 

    # Check if the filename (basename) begins with `s`
    def filter_begin_with(self, s, ftype):
        def fn(path, _): return os.path.basename(path).startswith(s)
        self.filter(fn, ftype)
        

    # Check if the filename (basename) ends with `s`
    def filter_end_with(self, s, ftype):
        def fn(path, _): return os.path.basename(path).endswith(s)
        self.filter(fn, ftype)

    # Check if the file extension is in `exts`
    def filter_ext_is_any(self, exts, ftype):
        def fn(path, _): return os.path.splitext(path)[1] in exts
        self.filter(fn, ftype)
        

    def _apply_filters(self, path, ftype):
        filters = None
        if ftype == FilterType.File:
            filters = self.filters_file
        elif ftype == FilterType.Dir:
            filters = self.filters_dir
        if ftype == FilterType.Rec:
            filters = self.filters_rec


        for fn in filters:
            if not fn(path, self.root):
                return False
        return True
