import json
import os

VERSION = "0.0.1"
DEBUG = False


# @TODO Fill DEFAULT_CONF
DEFAULT_CONF = {

    # obts settings
    'filebuilder-cc': 'clang',
    'filebuilder-cxx': 'clang++',
    'filebuilder-cc-flags': ['-Wall', '-Wextra', '-Werror', '-std=c99'],
    'filebuilder-cxx-flags': ['-Wall', '-Wextra', '-Werror', '-std=c++17'],
    'bin-extensions': ['.bin'],
}


_conf = [DEFAULT_CONF]

'''
Config based on Stack.
Push / pop config files.
When looking for config, starting at top, going lower
At the bottom is default config
'''

def push_file(path):
    if not os.path.isfile(path):
        return False
    with open(path, 'r') as f:
        conf =json.load(f)
    _conf.append(conf)
    return True


def pop_file():
    if len(_conf) == 1: #index 0 is DEFAULT_CONF
        raise Exception("Empty config stack")
    _conf.pop()


def get(key):
    for conf in _conf[::-1]:
        if key in conf:
            return conf[key]
    return None

    
