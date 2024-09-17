
import tkinter
from tkinter import filedialog

def getLogFile():
    root = tkinter.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    file = open(str(filepath), 'r')
    content = file.read()
    file.close()
    logType = determineLogType(filepath)
    return content, logType
    
def determineLogType(filepath):
    if 'TX' in str(filepath):
        logType = 'TX'
    else:
        logType = '717'
    return logType