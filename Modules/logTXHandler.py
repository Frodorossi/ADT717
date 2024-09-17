
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
            if iteration%1000 == 0:
                percent = round((iteration/len(logList))*100, 2)
                print(f'{percent}%')
            if len(row) > 4:
                time, identifier, payload = self.getInfo(row)
            
                if not identifier in identifiers:
                    identifiers.append(identifier)
                    self.payloadUpdates.append([identifier, 0, 'empty', 'empty'])
                
                for i in range(len(self.payloadUpdates)):
                    
                    if identifier == self.payloadUpdates[i][0]:
                        
                        if self.payloadUpdates[i][2] == 'empty':
                            self.payloadUpdates[i][2] = time
                        if self.payloadUpdates[i][3] == 'empty':
                            self.payloadUpdates[i][3] == time
                        
                        if payload != self.payloadUpdates[i][1]:
                            self.payloadUpdates[i][1] = payload
                            condensedList.append(row)
            else:
                condensedList.append(row)
        return condensedList
                    
    def getInfo(self, row):
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
        return time, identifier, payload
    
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