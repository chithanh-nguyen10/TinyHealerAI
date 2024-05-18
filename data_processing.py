import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import gspread
from google.oauth2.service_account import Credentials

def delete_collection(coll_ref, batch_size=20):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        doc.reference.delete()
        deleted += 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

class ReadData:
    def __init__(self, private_key):
        
        self.data = None
        cred = credentials.Certificate(private_key)
        firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def getData(self):
        if self.data is not None: raise Exception("You already get data")

        collection_ref = self.db.collection("health-problems")
        docs = collection_ref.stream()
        self.healthProblemDict = dict()
        for doc in docs:
            t = doc.to_dict()
            self.healthProblemDict[t['id']] = {'name': t['name'], 'description': t['description']}


        collection_ref = self.db.collection("symptom")
        docs = collection_ref.stream()
        self.symptomDict = dict()
        for doc in docs:
            t = doc.to_dict()
            try:
                self.symptomDict[t['id']].append({'name': t['name'], 'health-problems': t['health-problems'], 'characteristic-level' : t['characteristic-level']})
            except Exception:
                self.symptomDict[t['id']] = [{'name': t['name'], 'health-problems': t['health-problems'], 'characteristic-level' : t['characteristic-level']}]
        

        collection_ref = self.db.collection("anamnesis")
        docs = collection_ref.stream()
        self.anamnesisDict = dict()
        for doc in docs:
            t = doc.to_dict()
            try:
                self.anamnesisDict[t['health-problem-B']].append(t['health-problem-A'])
            except Exception:
                self.anamnesisDict[t['health-problem-B']] = [t['health-problem-A']]


if __name__ == '__main__':
    read = ReadData("private_key.json")
    read.getData()
    print(read.healthProblemDict)
    print()
    print(read.symptomDict)
    print()
    print(read.anamnesisDict)