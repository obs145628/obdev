import os

import pyutils.config as conf
from pyutils import ucmd
from .testresult import UTResult

FMT_OUTPUT=('''
Status code: {}
     stdout: <<BEG>>{}<<END>>
     stderr: <<BEG>>{}<<END>>
''').strip()

'''
Test that simply runs a binary file, and expects a return of 0
'''
class UTestSimpleBinary:

    '''
    @param name - ut.name
    @param bin_path - abs path of the binary to be run
    '''
    def __init__(self, ts, name, bin_path):
        self.ts = ts
        self.name = name
        self.bin_path = bin_path

    def get_cmd(self):
        bp = self.bin_path
        ext = os.path.splitext(bp)[1]
        #if ext == '.bin':
        #   return [self.bin_path]
        
        runner = conf.get('run-app-custom-cmd-{}'.format(ext[1:]))
        if not runner:
            raise Exception('Cannot run binary {}: unknown format'.format(bp))

        return [x.format(self.bin_path) for x in runner]

    # Run the test and add the result to ts
    def run(self):
        cmd = self.get_cmd()
        ret, out, err = ucmd.run_cmd(cmd)
        valid = ret == 0
        output = FMT_OUTPUT.format(ret, out.decode('ascii'), err.decode('ascii'))
        expected = 'Status code: 0'
        err_short = ''
        err_long = ''
        if not valid:
            err_short = 'Command with non-0 status code'
            err_long = 'Expected status code of 0, got {}'.format(ret)

        ut = UTResult(
            name=self.name,
            cmd=' '.join(cmd),
            valid=valid,
            status=ret,
            output=output,
            expected=expected,
            err_short=err_short,
            err_long=err_long)

        self.ts.add_test(ut)
            
        
