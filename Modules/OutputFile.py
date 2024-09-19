
import os

def write(payload):
    path = os.path.dirname(os.path.realpath(__file__))
    fpath = path + '\\outTest.txt'
    file = open(fpath, 'w')
    file.write(payload)
    file.close()