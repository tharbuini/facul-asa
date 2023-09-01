from fastapi import FastAPI, Request
from classes import Request_Aluno
from models import Aluno, session

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
    
    aluno = Aluno(
        nome     = aluno_json.nome,
        email    = aluno_json.endereco,
        cpf      = aluno_json.cpf,
        endereco = aluno_json.endereco
    )
    session.add(aluno)
    session.commit()
    
    return {
        "status" : "SUCESS",
        "data"   : aluno_json
    }
    