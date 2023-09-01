from fastapi import FastAPI, Request
from classes.py import Request_Aluno

app = FastAPI()

@app.get("/")
async def root():
    return {
        "status": "SUCESS",
        "data": "NO DATA"
    }

@app.post("/alunos")
async def criar_aluno(request_aluno: Request_Aluno):
    aluno_json = request_aluno
    print(aluno_json.nome)
    
    return {
        "status" : "SUCESS",
        "data"   : aluno_json
    }
    