import os
import tkinter
from tkinter import filedialog

def getLogFile():
    root = tkinter.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    file = open(str(filepath), 'r')
    content = file.read()
    file.close()
    return content

content = getLogFile()

rowSplit = content.split('\n')
newData = []
for i in range(len(rowSplit)):
    newRow = f'12/09/2024 | {rowSplit[i]}'
    newData.append(newRow)

out = ''
for i in range(len(newData)):
    out += newData[i]+'\n'

def write(payload):
    path = os.path.dirname(os.path.realpath(__file__))
    fpath = path + '\\TX-202409121402.001.log'
    file = open(fpath, 'w')
    file.write(payload)
    file.close()

write(out)
'''
fpath2 = path + '\\TX-202409121402.001.log'
file = open(path, 'w')
file.write(out)
file.close()'''