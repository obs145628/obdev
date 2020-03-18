import os
import sys

from pyutils import ioutils
from pyutils import ucmd
from .filebuilder import FileBuilder
from .testresult import UTResult

FMT_OUTPUT=('''
Status code: {}
     stdout: <<BEG>>{}<<END>>
     stderr: <<BEG>>{}<<END>>
''').strip()

'''
Test for a whole dir
'''
class UTestDir:

    '''
    @ param 
    @param name - ut.name
    @param bin_path - abs path of the binary to be run
    '''
    def __init__(self, ts, dir_path, out_dir, search_dirs):
        self.ts = ts
        self.dir_path = dir_path
        self.out_dir = out_dir
        self.search_dirs = search_dirs
        self.conf = dict()

    # Run the test and add the result to ts
    def run(self):
        in_files = [x[:-6] for x in os.listdir(self.dir_path) if x.endswith(".input")]
        if len(in_files) == 0:
            self.run_one(None)
        else:
            for f in in_files:
                self.run_one(f)

    def run_one(self, input_name):
        dir_path = self.dir_path
        input_path = None if input_name is None else os.path.join(dir_path, input_name + '.input')
        self.conf['data_builder_stdin_path'] = input_path
        name = os.path.basename(dir_path)[6:]
        out_dir = os.path.join(self.out_dir, 'tmp', name)
        builder = FileBuilder(out_dir, [dir_path] + self.search_dirs, conf=self.conf)
        test_basename = 'test_{}'.format(name)
        ref_basename = 'ref_{}'.format(name) if input_name is None else 'ref_{}__in_{}'.format(name, input_name)
        name = name if input_name is None else '{}_in:{}'.format(name, input_name)

        test_bin = builder.build_type(test_basename, 'app')
        if test_bin is None:
            self._ts_err("Failed to setup UnitTest: couldn't build binary for {}".format(name))
            
        ref_out = builder.build_type(ref_basename, 'data')
        if ref_out is None:
            print(ref_basename)
            self._ts_err("Failed to setup UnitTest: couldn't build ref output for {}".format(name))
        test_ret, test_out, test_err = ucmd.run_cmd([test_bin], stdin_path=input_path)
        test_out_ca = test_out.decode('ascii', 'ignore')
        test_err_ca = test_err.decode('ascii', 'ignore')
        ref_out = ioutils.read_file_bin(ref_out)
        ref_out_ca = ref_out.decode('ascii', 'ignore')
        valid_out = test_out == ref_out
        valid = test_ret == 0 and valid_out

        output = FMT_OUTPUT.format(test_ret, test_out_ca, test_err_ca)
        expected = 'stdout:\n{}'.format(ref_out_ca)
        err_short = ''
        err_long = ''
        if not valid:
            if test_ret != 0:
                err_short = 'Expected status code 0, got {}'.format(ret)
                err_long += err_short + '\n'
            if not valid_out:
                err_short = 'Invalid stdout, differs from ref file.'
                err_long += 'Invalid stdout, differs from ref file:\n' + (
                    ' Ref: {} bytes\nTest: {} bytes'.format(len(ref_out), len(test_out)))

        ut = UTResult(
            name=name,
            cmd=(test_bin if input_path is None else '{} < {}'.format(test_bin, input_path)),
            valid=valid,
            status=test_ret,
            output=output,
            expected=expected,
            err_short=err_short,
            err_long=err_long)
        
        self.ts.add_test(ut)
        


    def _ts_err(self, msg):
        sys.stderr.write(msg + '\n')
        sys.exit(2)
