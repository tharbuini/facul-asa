from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from logging.config import dictConfig
import logging
from src.config import log_config

dictConfig(log_config)

app = FastAPI(debug=True)
logger = logging.getLogger('foo-logger')

# Lista para armazenar os alunos simulados
alunos_db = []

class Aluno(BaseModel):
    nome: str
    matricula: str
    curso: str

# Rota principal
@app.get("/")
async def root():
    logger.debug("Aqui na rota principal")
    mensagem = {"response" : "Trabalho 01 - ASA"}
    return mensagem

# Rota para obter a lista de alunos (GET) no alunos_db
@app.get("/alunos/")
def get_alunos():
    return {"alunos": alunos_db}

# Rota para criar um novo aluno (POST) e adicionar no alunos_db
@app.post("/alunos/")
def create_aluno(aluno: Aluno):
    logger.error('ERROR')
    alunos_db.append(aluno)
    return {"message": "Aluno cadastrado com sucesso", "aluno": aluno}

# Rota para atualizar um aluno existente (PUT)
@app.put("/alunos/")
def update_aluno(aluno_matricula, aluno: Aluno):
    logger.error('ERROR')
    for aluno_ in alunos_db:
        if aluno_.matricula == aluno_matricula:
            alunos_db.remove(aluno_)
            alunos_db.append(aluno)
            return {"message": "Aluno atualizado com sucesso", "aluno": aluno}
            

# Rota para excluir um aluno (DELETE)
@app.delete("/alunos/")
def delete_aluno(aluno_matricula: str):
    logger.error('ERROR')
    for aluno in alunos_db:
        if aluno.matricula == aluno_matricula:
            alunos_db.remove(aluno)
            return {"message": "Aluno removido com sucesso", "aluno": aluno_matricula}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
