
import os

class ParamList():
    def __init__(self):
        params = getParams()
        self.logTXRowSplit = '\n'
        self.logTXColumnSplit = params[0]
        self.log717RowSplit = '\n'
        self.log717ColumnSplit = params[1]
        self.log717StartBuffer = params[2]

def getParamFile():
    paramDirectory = os.path.dirname(os.path.realpath(__file__))
    paramPath = paramDirectory + '\\Params.txt'
    file = open(paramPath, 'r')
    paramContent = file.read()
    file.close()
    return paramContent

def getParams():
    paramContent = getParamFile()
    paramRows = paramContent.split('\n')
    params = []
    for i in range(len(paramRows)):
        try:
            payload = paramRows[i].rsplit(':', 1)[1]
            params.append(payload[1:-1])
        except:
            pass
    return params