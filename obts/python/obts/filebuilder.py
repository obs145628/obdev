import os

import pyutils.config as conf
from pyutils import ucmd
from pyutils import ioutils

DEFAULT_TYPES = {
    'data': ['.data'],
    'app': ['.bin', '.py'],
}

'''
Build files using a 1 to 1 mapping: input file => output file
File types and how to build files is known only using the extension.
Finding input file name is simple: <basename>.ext_out <= <basename>.ext_in
There is a few exceptions:
- when <basename> contains '__', everything starting at '__' is removed in the basename for input file

out_dir: Where all built files are stored.
search_dirs: Where to look for input files. dirs checked in order. out_dir is also checked after.
conf: dict of all config entries to update the way files are built
builders: list of builder objects. Default list provided
types: dict, list of extension for every types. Default provided
'''
class FileBuilder:


    def __init__(self, out_dir, search_dirs, conf, builders=None, types=None):
        if builders is None:
            builders = [GccBuilder(conf), GppBuilder(conf), DataBuilder(conf)]
        if types is None:
            types = DEFAULT_TYPES

        self.out_dir = out_dir
        self.search_dirs = search_dirs
        self.conf = conf
        self.builders = builders
        self.types = types

        self.ext_builders = dict()
        for builder in self.builders:
            ext = builder.out_ext
            if ext not in self.ext_builders:
                self.ext_builders[ext] = []
            self.ext_builders[ext].append(builder)

    '''
    Try to build any file of the specific type
    @param basename has no extension
    @returns the full path of the type if it was build
    @returns None if it couldn't build any file of this type
    '''
    def build_type(self, basename, file_type):
        # get list of possible extensions
        if file_type not in self.types:
            return None
        exts = self.types[file_type]

        # try to build all file extensions, returns first successful one
        for ext in exts:
            res = self.build_file(basename + ext)
            if res is not None:
                return res

        return None
        
    '''
    Try to build file <out_name>/basename
    If file already exists, does nothing
    @returns None if can't build the file
    '''
    def build_file(self, basename):
        out_path = self._search_file(basename)
        if out_path is not None:
            return out_path
        out_path = os.path.join(self.out_dir, basename)
        ext = os.path.splitext(basename)[1]

        if ext in self.ext_builders:
            for builder in self.ext_builders[ext]:
                if self._run_builder(builder, basename, out_path):
                    return out_path
        
        return None


    def _search_file(self, basename):
        for d in self.search_dirs:
            out_path = os.path.join(d, basename)
            if os.path.isfile(out_path):
                return out_path

        out_path = os.path.join(self.out_dir, basename)
        if os.path.isfile(out_path):
            return out_path
            

    def _run_builder(self, builder, basename, out_path):
        for ext in builder.in_exts:
            in_path = self.build_file(self._get_input_filename(basename, ext))
            if in_path is not None:
                builder.build(in_path, ioutils.creat_rec(out_path))
                return True

        return False


    def _get_input_filename(self, out_basename, in_ext):
        out_base, out_ext = os.path.splitext(out_basename)

        limit_idx = out_base.find("__")
        if limit_idx != -1:
            out_base = out_base[:limit_idx]
        
        return out_base + in_ext


class GccBuilder:
    def __init__(self, conf):
        self.conf = conf
        self.out_ext = '.bin'
        self.in_exts = ['.c']

    def build(self, in_path, out_path):
        cc = conf.get('filebuilder-cc')
        cc_flags = conf.get('filebuilder-cc-flags')
        ucmd.run_cmd([cc, in_path, '-o', out_path] + cc_flags, exp0=True)

class GppBuilder:
    def __init__(self, conf):
        self.conf = conf
        self.out_ext = '.bin'
        self.in_exts = ['.cc', '.cpp']

    def build(self, in_path, out_path):
        cxx = conf.get('filebuilder-cxx')
        cxx_flags = conf.get('filebuilder-cxx-flags')
        ucmd.run_cmd([cxx, in_path, '-o', out_path] + cxx_flags, exp0=True)

class DataBuilder:
    def __init__(self, conf):
        self.conf = conf
        self.out_ext = '.data'
        self.in_exts = ['.bin', '.py']
        if 'data_builder_stdin_path' in self.conf:
            self.stdin_path = self.conf['data_builder_stdin_path']

    def build(self, in_path, out_path):
        out = None
        if in_path.endswith('.bin'):
            out = self._build_bin(in_path, out_path)
        elif in_path.endswith('.py'):
            out = self._build_py(in_path, out_path)
        else:
            raise Exception('Internal error: no DataBuilder for {}'.format(in_path))
        
        ioutils.write_file_bin(out_path, out)


    def _build_bin(self, in_path, out_path):
        _, out, _ = ucmd.run_cmd([in_path], stdin_path=self.stdin_path, exp0=True)
        return out

    def _build_py(self, in_path, out_path):
        _, out, _ = ucmd.run_cmd(['python', in_path], stdin_path=self.stdin_path, exp0=True)
        return out
    
