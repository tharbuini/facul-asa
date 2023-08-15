from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Aluno(BaseModel):
    nome : str
    matricula : str
    curso : str

@app.get("/")
async def root():
    mensagem = {"response" : "Ei Real Madrid"}
    return mensagem

@app.get("/parameter/{parameterID}")
async def mostraParametro(parameterID):
    mensagem = f"O valor do parametro: {parameterID}"
    return {"response" : mensagem }

@app.post("/alunos")
async def criarAluno(aluno : Aluno):
    return aluno

# pip install fastapi
# pip install uvicorn
# uvicorn main:app --reload