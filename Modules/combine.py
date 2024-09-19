
from datetime import datetime

class CombineLogs():
    
    def __init__(self, logTX, log717):
        self.combinedList = self.combine(logTX, log717)
    
    def combine(self, logTX, log717):
        firstTimestamp = self.getFirstTime(logTX, log717)
    
    def getFirstTime(self, logTX, log717):
        timeTX, time717 = self.getTimes(logTX, log717, 0, 0)
        delta = timeTX - time717
        dint = delta.total_seconds()
        if dint <= 0:
            firstTimestamp = time717
        else:
            firstTimestamp = timeTX
        return firstTimestamp
    
    def getTimes(self, logTX, log717, rowTX, row717):
        time1 = logTX[rowTX][0]
        time2 = log717[row717][0]
        timeTX = datetime.strptime(time1, '%H:%M:%S:%f')
        time717 = datetime.strptime(time2, '%H:%M:%S.%f')
        return timeTX, time717