from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import numpy as np
import pandas as pd

df=pd.read_csv("data.csv")
app = FastAPI()

load_dotenv()
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
class dataInput(BaseModel):
    symptoms: List[str]
    anamnesis: List[str]
    familyanamnesis: List[str]


@app.post("/diagnostic")
async def diagnose(input: dataInput, token: str = Header(None)):
    inp = input.symptoms
    symptoms = inp

    X= df[symptoms]
    Y = df[["health-problems"]]

    clf3 = tree.DecisionTreeClassifier() 
    clf3 = clf3.fit(X,Y)
    clf4 = RandomForestClassifier(n_estimators=100)
    clf4 = clf4.fit(X,np.ravel(Y))
    gnb = GaussianNB()
    gnb=gnb.fit(X,np.ravel(Y))
    knn=KNeighborsClassifier(n_neighbors=5,metric='minkowski',p=2)
    knn=knn.fit(X,np.ravel(Y))

    vector = [1 for _ in range(len(symptoms))]

    res = set()

    predict = knn.predict([vector])
    res.add(predict[0])
    for i in range(100):
        predict = clf3.predict([vector])
        res.add(predict[0])
    for i in range(100):
        predict = clf4.predict([vector])
        res.add(predict[0])
    predict = gnb.predict([vector])
    res.add(predict[0])

    return {"results" : sorted(list(res))}
