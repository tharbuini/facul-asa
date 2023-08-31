from fastapi import FastAPI
from pydantic import BaseModel
from logging.config import dictConfig
import logging
from src.config import log_config

dictConfig(log_config)

app = FastAPI(debug=True)
logger = logging.getLogger('foo-logger')

class Aluno(BaseModel):
    nome: str
    matricula: str
    curso: str
    

@app.get("/")
async def root():
    logger.debug("Aqui na rota principal")
    mensagem = {"response" : "Arquitetura de software aplicada"}
    return mensagem

@app.get("/parametro/{parametro_id}")
async def mostra_parametro(parametro_id):
    mensagem = f"O valor do paramento - {parametro_id}"
    logger.info("Foi enviado um parametro correto!!!")
    return {"response" : mensagem}

@app.post("/alunos")
async def criar_aluno(aluno: Aluno):
    logger.error('ERROR')
    return aluno