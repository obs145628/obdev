import subprocess
import os

from . import config

def run_cmd(cmd, stdin_path=None, exp0 = False):

    if config.DEBUG:
        if stdin_path is None:
            print("Run command '{}'".format(' '.join(cmd)))
        else:
            print("Run command '{}' < {}".format(' '.join(cmd), stdin_path))

    if stdin_path is not None:
        stdin = open(stdin_path, 'rb')
    else:
        stdin = None
    
    p = subprocess.Popen(cmd,
                         stdin=stdin,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()
    out, err = p.communicate()
    ret = p.returncode

    if exp0 and ret != 0:
        print('Failed to run command: {} (exit status {})'.format(' '.join(cmd), ret))
        print('OUTPUT: <<{}>>'.format(out.decode('ascii')))
        print('ERROR: <<{}>>'.format(err.decode('ascii')))
        raise Exception('Command failed')
    
    return ret, out, err

def run_system(cmd):
    res = os.system(cmd)
    return os.WEXITSTATUS(res)
