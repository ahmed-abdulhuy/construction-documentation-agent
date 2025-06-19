import numpy as np
import pandas as pd


class RecordPrompt:
    def __init__(self, recordsCSVFile=''):
        self.recordsCSVFile = recordsCSVFile

        
    def readCSVFile(self, filePath):
        return pd.read_csv(filePath)
    

    def convertRecordsToDict(self, records):
        promptList = []
        for row in records.iterrows():
            prompt = row.to_dict()
            promptList.append(prompt)

        return np.array(promptList)

