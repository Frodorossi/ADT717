
class log717():
    payloadUpdates = []
    for i in range(511):
        payloadUpdates.append([False, '000', 'empty'])
    #----------------
    #
    # payloadUpdates format:
    # Word #, updated, Prev payload,  prev payload time
    #      1,   [True,          xxx,       xx:xx:xx:xxx]
    #      2,   [False          xxx,       xx:xx:xx:xxx]
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
        for row in logList:
            iteration+=1
            self.progressUpdate(iteration, logList, 10)
            if len(row) > 1:
                topUpdates = 'Word(s) '
                bottomUpdates = '                            Updated to '
                for i in range(len(row)-4):
                    identifier = self.getInfo(row, i+1)
                    subframe = row[0]
                    payload = row[i+4]
                    if payload != self.payloadUpdates[i][1] and i+2 not in ignoreList[subframe]:
                        time = row[2]
                        time = time[:-1]
                        self.payloadUpdates[i] = [True, payload, time]
                        if i < 99:
                            topUpdates += f'0{i+2}, '
                        else:
                            topUpdates += f'{i+2}, '
                        bottomUpdates += f'{payload}, '
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
    
    def progressUpdate(self, iteration, loglist, divisor):
        if iteration%divisor == 0:
            percent = round((iteration/len(loglist))*100, 2)
            print(f'{percent}%')
    
    def getInfo(self, row, word):
        subframe = row[0]
        identifier = f"{subframe} {word}"
        return identifier