from data_processing import *

class Diagnostic:
    def __init__(self, healthProblemDict, symptomDict, anamnesisDict, familyanamnesisDict):
        self.healthProblemDict = healthProblemDict
        self.symptomDict = symptomDict
        self.anamnesisDict = anamnesisDict
        self.familyanamnesisDict = familyanamnesisDict
    
    def diagnose(self, symptoms, anamnesis, familyanamnesis):
        self.preData = dict()
        for symptom in symptoms:
            for healthProblem in self.symptomDict[symptom]:
                try:
                    self.preData[healthProblem["health-problems"]] = self.preData[healthProblem["health-problems"]] + int(healthProblem["characteristic-level"])
                except Exception:
                    self.preData[healthProblem["health-problems"]] = int(healthProblem["characteristic-level"])
        
        for healthProblem in anamnesis:
            for anamnesisItem in self.familyanamnesisDict[healthProblem]:
                try:
                    self.preData[anamnesisItem["id"]] = self.preData[anamnesisItem["id"]] + int(anamnesisItem["characteristic-level"])
                except Exception:
                    pass
        
        for healthProblem in familyanamnesis:
            for anamnesisItem in self.anamnesisDict[healthProblem]:
                try:
                    self.preData[anamnesisItem["id"]] = self.preData[anamnesisItem["id"]] + int(anamnesisItem["characteristic-level"])
                except Exception:
                    pass

        self.sortedData = {k: v for k, v in sorted(self.preData.items(), key=lambda item: item[1], reverse = True)}
        # print(self.sortedData)
        maxValues = []
        for key, val in self.sortedData.items():
            if val not in maxValues: maxValues.append(val)
            if len(maxValues) == 3: break
        
        self.finalData = []
        for key, val in self.sortedData.items():
            if val in maxValues:
                self.finalData.append(key)

        return self.finalData


if __name__ == '__main__':
    read = ReadData("private_key.json")
    read.getData()
    symptoms = ["eye02", "urinary01", "lung01", "digest01"]
    anamnesis = ["digest01", "ent01"]
    familyanamnesis = ["digest01"]
    diagnostic = Diagnostic(read.healthProblemDict, read.symptomDict, read.anamnesisDict, read.familyanamnesisDict)
    # print( read.anamnesisDict)
    print(diagnostic.diagnose(symptoms, anamnesis, familyanamnesis))