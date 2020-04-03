'''
Usage:

obts: <task> ...

# Run

Run the test suite of a project
@TODO Implement run mode inplace
@TODO Implement run mode ext
@TODO Implement run mode container

obts: run <project-path> [--mode <tsmode>] [--out <output-dir>]

--mode <tsmode>:
- inplace: Run the test suite in the current project dir
- extern: Copy only source files to /tmp, then rebuild whole project and run ts there
- container: Create archive of source file and copy to QEMU guest machine by ssh.
  Compile and run ts in guest, then copy results back to host
  This is the only way to run tests on other archs
- default: Use first of the 3 above that is available
Default value is default

-o/--out <output-dir>:
Where are saved the TS results file and tmp files
Default is './obts'
'''

'''
General config file

ts-mode (<string>, default="inplace|extern|container")
List of modes supported by the test suite.
Leave empty if the project doesn't have a TS.
'''

import argparse
import sys

from .tsauto import TSAuto



def task_run(args):
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument('--mode',
                    dest='mode',
                    default='default',                  
                    action='store',
                    nargs='?',
                    type=str)
    ap.add_argument('-o', '--out',
                    dest='out',
                    default='./obts',
                    action='store',
                    nargs='?',
                    type=str)
    args = ap.parse_args(args)

    root = args.root
    out = args.out

    mode = args.mode
    if mode == 'default':
        mode = 'inplace'
    if mode != 'inplace':
        sys.stderr.write('obts: Only inplace mode supported for now\n')
        return 1
    
    ts = TSAuto(root=root, output_dir=out)
    return ts.run()
    

def main(args):
    if len(args) < 1:
        sys.stderr.write('obts: Missing task argument\n')
        return 1

    task = args[0]
    if task == 'run':
        return task_run(args[1:])
    else:
        sys.stderr.write('obts: Unknown task {}\n'.format(task))
        return 1
    
    


