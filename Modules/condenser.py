
class data():
    def __init__(self):
        self.lastTimestamp = []
        self.lastUpdateTime = []
        self.lastUpdateData = []
        self.condensedData = []

class dataTX(data):
    def __init__(self):
        data.__init__(self)
        self.idCodes = []

class data717(data):
    def __init__(self):
        data.__init__(self)
        
def condense(log, logType):
    if logType == 'TX':
        pass
    else:
        pass
    
    