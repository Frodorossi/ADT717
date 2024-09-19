from datetime import datetime

class logTX():
    payloadUpdates = []
    #----------------
    #
    # payloadUpdates format:
    # Index, Pos 0,      Pos 1,        Pos 2,             Pos 3
    #   0,  [identifier, prev payload, prev payload time, prev instance time]
    #   1,  [identifier, prev payload, prev payload time, prev instance time]
    #
    #----------------
    def __init__(self, log, rowSplitTX, columnSplitTX):
        logTXlist = self.TXlogToList(log, rowSplitTX, columnSplitTX)
        condensedList = self.condense(logTXlist)
        self.output = self.reformat(condensedList, columnSplitTX)
    
    def TXlogToList(self, log, rowSplitTX, columnSplitTX):
        rowSplit = log.split(rowSplitTX)
        columnSplit = []
        for i in range(len(rowSplit)):
            temp = rowSplit[i].split(columnSplitTX)
            columnSplit.append(temp)
        del columnSplit[-1]
        return columnSplit
    
    def condense(self, logList):
        condensedList = []
        iteration = 0
        identifiers = []
        
        for row in logList:
            iteration +=1
            self.progressUpdate(iteration, logList, 1000)
            
            if len(row) > 4:
                time, identifier, payload, identifiers = self.getInfo(row, identifiers)
                
                for i in range(len(self.payloadUpdates)):
                    
                    if identifier == self.payloadUpdates[i][0]:
                        
                        dint = self.checkForDataLoss(time, i)
                        
                        if payload != self.payloadUpdates[i][1]:
                            self.payloadUpdates[i][1] = payload
                            condensedList.append(row)
            else:
                condensedList.append(row)
        return condensedList
    
    def progressUpdate(self, iteration, logList, divisor):
         if iteration%divisor == 0:
                percent = round((iteration/len(logList))*100, 2)
                print(f'{percent}%')
                    
    def getInfo(self, row, identifiers):
        time = row[0]
        label = row[1]
        source = row[2]
        payload = row[3]
        sdi = row[6]
        try:
            ssm = row[7]
        except:
            ssm = '00'
        identifier = f'{label} {source} {sdi} {ssm}'
        if not identifier in identifiers:
            identifiers.append(identifier)
            self.payloadUpdates.append([identifier, 0, 'empty', 'empty'])
        return time, identifier, payload, identifiers
    
    def reformat(self, list, column):
        formattedList = []
        for row in list:
            tempRow = ''
            for i in range(len(row)):
                tempRow += row[i] + column
            extraChars = len(column)
            tempRow = tempRow[:-extraChars]
            formattedList.append(tempRow)
        return formattedList
    
    def checkForDataLoss(self, time, i):
        previousTime = self.payloadUpdates[i][3]
        if self.payloadUpdates[i][3] == 'empty':
            self.payloadUpdates[i][3] == time
            previousTime = time
        t1 = datetime.strptime(previousTime, '%H:%M:%S:%f')
        t2 = datetime.strptime(time, '%H:%M:%S:%f')
        delta = t2 - t1
        dint = delta.total_seconds()
        self.payloadUpdates[i][3] = time
        return dint