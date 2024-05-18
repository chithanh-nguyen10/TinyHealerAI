from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List
from data_processing import *
from diagnostic import *
from dotenv import load_dotenv
import os

read = ReadData("private_key.json")
read.getData()
diagnostic = Diagnostic(read.healthProblemDict, read.symptomDict, read.anamnesisDict)

app = FastAPI()

load_dotenv()
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
class dataInput(BaseModel):
    symptoms: List[str]
    anamnesis: List[str]

@app.get("/update")
async def update():
    read.getData()
    diagnostic = Diagnostic(read.healthProblemDict, read.symptomDict, read.anamnesisDict)
    print(read.healthProblemDict)
    return {"message": "succeed"}


@app.post("/diagnostic")
async def diagnose(input: dataInput, token: str = Header(None)):
    if token != SECRET_TOKEN:
        return {"error": "Invalid token"}

    results = diagnostic.diagnose(input.symptoms, input.anamnesis)
    return {"health_problems": results}