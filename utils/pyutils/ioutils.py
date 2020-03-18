import json
import os

from . import config

def creat_rec(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path

def read_file_bin(path):
    with open(path, 'rb') as f:
        data = f.read()
    if config.DEBUG:
        print('Read bin file {} ({} bytes)'.format(path, len(data)))
    return data

def write_file_bin(path, data):
    if config.DEBUG:
        print('Write bin file {} ({} bytes)'.format(path, len(data)))
    with open(path, 'wb') as f:
        f.write(data)

def read_file_json(path):
    with open(path, 'r') as f:
        return json.load(f)
