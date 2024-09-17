
from Modules import paramHandler, log717Handler, logTXHandler, InputFile, OutputFile, labelManager

params = paramHandler.ParamList()
labels = labelManager.LabelList()
log = []

content, logType = InputFile.getLogFile()
if logType == 'TX':
    TXlog = logTXHandler.logTX(content, params.logTXRowSplit, params.logTXColumnSplit)
    log = TXlog.output
elif logType == '717':
    log717 = log717Handler.log717(content, params.log717RowSplit, params.log717ColumnSplit, labels.labelDictionary)
    log = log717.output
else:
    print('something went wrong with the input file')

out = ''
for i in range(len(log)):
    out += log[i]+'\n'

OutputFile.write(out)
    
