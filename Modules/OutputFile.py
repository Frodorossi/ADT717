
import os
'''
samplePayload = 'Here is a test of what\nI want to write\nBut now its even longer\n\n\nWith some space'

path = os.path.dirname(os.path.realpath(__file__))
fpath = path + '\\outTest.txt'
file = open(fpath, 'w')
file.write(samplePayload)
file.close()
'''

def write(payload):
    path = os.path.dirname(os.path.realpath(__file__))
    fpath = path + '\\outTest.txt'
    file = open(fpath, 'w')
    file.write(payload)
    file.close()