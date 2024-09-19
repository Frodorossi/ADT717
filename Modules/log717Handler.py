from datetime import datetime

class log717():
    payloadUpdates = []
    #----------------
    #
    # payloadUpdates format:
    # Identifier , Prev payload
    # SF:1 (word),        'xxx']
    # SF:2 (word),        'xxx']
    # 511 Words not incuding a sync word as it is not important here
    #
    #----------------
    
    def __init__(self, log, rowSplit717, columnSplit717, ignoreList):
        log717list = self.log717ToList(log, rowSplit717, columnSplit717)
        condensedList = self.condense(log717list, ignoreList)
        self.output = condensedList
    
    def log717ToList(self, log, rowSplit717, columnSplit717):
        rowSplit = log.split(rowSplit717)
        columnSplit = []
        for i in range(len(rowSplit)):
            temp = rowSplit[i].split(columnSplit717)
            del temp[-1]
            columnSplit.append(temp)
        return columnSplit
    
    def condense(self, logList, ignoreList):
        condensedList = []
        iteration = 0
        identifiers = []
        syncList, checkWord = self.getAllSyncWords(logList)
        prevTime = 'Empty'
        for row in logList:
            iteration+=1
            self.progressUpdate(iteration, logList, 10)
            topUpdates = 'Word(s) '
            bottomUpdates = '                            Updated to '
            if len(row) > 1:
                checkWord, condensedList, prevTime = self.checkForErrors(checkWord, condensedList, row, syncList, prevTime)
                for i in range(len(row)-4):
                    topUpdates, bottomUpdates, identifiers = self.filterLine(row, i, identifiers, ignoreList, topUpdates, bottomUpdates)
                condensedList = self.addUpdates(topUpdates, bottomUpdates, row, condensedList)
        return condensedList
    
    def progressUpdate(self, iteration, loglist, divisor):
        if iteration%divisor == 0:
            percent = round((iteration/len(loglist))*100, 2)
            print(f'{percent}%')
    
    def getInfo(self, row, i):
        subframe = row[0]
        word = i+1
        payload = row[i+4]
        identifier = f"{subframe} {word}"
        return identifier, subframe, payload
    
    def getTime(self, row):
        time = row[2]
        time = time[:-1]
        return time
    
    def getAllSyncWords(self, logList):
        syncWords = []
        i = 0
        while len(syncWords) < 4:
            if len(logList[i]) > 1:
                word = logList[i][3]
                if not word in syncWords:
                    syncWords.append(word)
                else:
                    syncWords = []
            i += 1
        print(syncWords)
        checkWord = syncWords[0]
        return syncWords, checkWord
    
    def getCurrentSyncWord(self, row):
        word = row[3]
        return word
    
    def getNextSyncWord(self, syncList, currentWord):
        index = syncList.index(currentWord)
        try:
            nextWord = syncList[index+1]
        except:
            nextWord = syncList[0]
        return nextWord
    
    def checkForDataLoss(self, time, previousTime):
        if previousTime == 'Empty':
            previousTime = time
        t1 = datetime.strptime(previousTime, '%H:%M:%S.%f')
        t2 = datetime.strptime(time, '%H:%M:%S.%f')
        delta = t2 - t1
        dint = delta.total_seconds()
        previousTime = time
        return dint, previousTime
    
    def checkForErrors(self, checkWord, condensedList, row, syncList, prevTime):
        syncWord = self.getCurrentSyncWord(row)
        if syncWord != checkWord:
            dataLossMessage = f"{row[0]} {row[1]} {row[2]} OUT OF ORDER SUBFRAME TRANSMITTED"
            condensedList.append(dataLossMessage)
        checkWord = self.getNextSyncWord(syncList, syncWord)
        time = self.getTime(row)
        dint, prevTime = self.checkForDataLoss(time, prevTime)
        if dint > 1.5:
            dataLossMessage = f"{row[0]} {row[1]} {row[2]} DATA LOSS DETECTED: GREATER THAN 1.5 SECONDS SINCE LAST SUBFRAME"
            condensedList.append(dataLossMessage)
        return checkWord, condensedList, prevTime
    
    def addUpdates(self, topUpdates, bottomUpdates, row, condensedList):
        if topUpdates != 'Word(s) ':
            topUpdates = topUpdates[:-2]
            bottomUpdates = bottomUpdates[:-2]
            subframe = row[0]
            date = row[1]
            timestamp = row[2]
            newRow = f'{subframe} {date} {timestamp} {topUpdates}'
            condensedList.append(newRow)
            condensedList.append(bottomUpdates)
        return condensedList
    
    def filterLine(self, row, i, identifiers, ignoreList, topUpdates, bottomUpdates):
        identifier, subframe, payload = self.getInfo(row, i)
        if not identifier in identifiers:
            identifiers.append(identifier)
            self.payloadUpdates.append([identifier, '000'])
        for j in range(len(self.payloadUpdates)):
            if identifier == self.payloadUpdates[j][0] and i+2 not in ignoreList[subframe] and payload != self.payloadUpdates[j][1]:
                self.payloadUpdates[j][1] = payload
                if i < 99:
                    topUpdates += f'0{i+2}, '
                else:
                    topUpdates += f'{i+2}, '
                bottomUpdates += f'{payload}, '
        return topUpdates, bottomUpdates, identifiers