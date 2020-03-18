'''
Usage
python control-cli.py <task> ...

# project

@TODO implement project task

python control-cli.py project add <path>
Add a new project to the list, given its relative path

python control-cli.py project rm <path>
Remove a project from the list, given its relative path

python control-cli.py project list
Display all projects

The name of the project is given by the directory name
@TODO Use repo name instead of directory name as project name

There is no need to have other settings other than the path.
All settings are in the config files.

# run-ts

@TODO Implement run-ts rask

python control-cli.py run-ts <proj-name> ...
Same as running python tsauto.py run <project-path> ...
'''


'''
General config file
All config options more general to the whole obdev project
Other options, more specific are detailled in their related parts
File is obdev.config.js, at the root of the project
'''


import os
import sys


DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/obcontrol"))


def main(args):
    print('Hello from obcontrol !')
    return 0
