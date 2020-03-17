import os
import sys

class ControlApp:

    def __init__(self, data_dir):
        self.data_dir = data_dir


    def run(self):
        print('Hello from ControlApp: {}'.format(self.data_dir))
        return 0
