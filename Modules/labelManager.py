
import os
import json

class LabelList():
    def __init__(self):
        self.labelDictionary = getLabels()

def getLabels():
    labelDirectory = os.path.dirname(os.path.realpath(__file__))
    labelPath = f"{labelDirectory}\\Labels.json"
    with open(labelPath, 'r') as f:
        labels = json.load(f)
    return labels