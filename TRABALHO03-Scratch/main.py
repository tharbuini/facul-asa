from fastapi import FastAPI
from classes import Request_Aluno, Request_Professor, Request_Curso
from model import Aluno, Professor, Curso, CursoAluno, CursoProfessor, session
from publisher import Publisher
import logging

logger = logging.getLogger(__name__)
logging.getLogger("pika").propagate = False
FORMAT = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

app = FastAPI()

config = {
     'host': 'rabbitmq-service',
     'port': 5672, 
     'exchange' : 'alunos'
}

@app.get("/")
async def root():
    return {
        "status": "Rota Principal",
        "data": "TRABALHO 03 - ASA"
    }

## ----------------------- ALUNOS ----------------------- 
@app.get("/alunos")
async def get_all_alunos():
    alunos_query = session.query(Aluno)
    alunos = alunos_query.all()
    return {
        "status": "SUCESS",
        "data": alunos
    }

@app.post("/alunos")
async def criar_aluno(request_aluno: Request_Aluno):
    aluno_json = request_aluno
    aluno = Aluno(
        nome     = aluno_json.nome,
        email    = aluno_json.endereco,
        cpf      = aluno_json.cpf,
        endereco = aluno_json.endereco
    )
    session.add(aluno)
    session.commit()

    return {
        "status": "SUCESS",
        "data": aluno_json
    }

@app.put("/alunos")
async def alterar_aluno(aluno_nome: str, request_aluno: Request_Aluno):
    try:    
        aluno_json = request_aluno
        aluno_query = session.query(Aluno).filter(
            Aluno.nome==aluno_nome
        )
        aluno = aluno_query.first()
        aluno.nome = aluno_json.nome
        aluno.cpf = aluno_json.cpf
        aluno.email = aluno_json.email
        aluno.endereco = aluno_json.endereco

        session.add(aluno)
        session.commit()

        return {
            "status": "SUCESS",
            "data": aluno_json
        }
    
    except Exception as e:
        return {
            "status": "ERROR",
            "data": "ALUNO NÃO ENCONTRADO"
        }

"""
@app.delete("/alunos/")
async def deletar_aluno(nome:str):
    try:    
        aluno_query = session.query(Aluno).filter(
            Aluno.nome==nome
        )

        aluno = aluno_query.first()
        session.delete(aluno)

        return {
            "status": "SUCESS",
            "data": aluno.nome
        }
    
    except Exception as e:
        return {
            "status": "ERROR",
            "data": "ALUNO NÃO ENCONTRADO"
        }
"""

@app.get("/enviar_alunos", status_code=200)
async def get_all_alunos():
    alunos_to_send = []
    logger.info('Coletando as informações dos alunos no banco de dados')
    try:
        alunos_query = session.query(Aluno)
        alunos = alunos_query.all()

        for aluno in alunos:
            item = {
                "id": aluno.id,
                "nome": aluno.nome,
                "email": aluno.email,
                "cpf": aluno.cpf,
                "endereco": aluno.endereco
            }
            aluno_serializer = Request_Aluno(**item)            
            alunos_to_send.append(aluno_serializer)
        
        publisher = Publisher(config)  
        logger.info('Enviando mensagem para o RabbitMQ')       
        publisher.publish('routing_key', aluno_serializer.model_dump_json().encode())
    except Exception as e:
         logger.error(f'Erro na consulta dos alunos -- get_all_alunos() -- {e}')
         print(e)
    return {
        "status": "SUCESS",
        "result": "OK"
    }


## ----------------------- PROFESSOR -----------------------
@app.get("/professores")
async def get_all_professores():
    professores_query = session.query(Professor)
    professores = professores_query.all()

    return {
        "status": "SUCESS",
        "data": professores
    }

# Rota para criar um novo professor
@app.post("/professores")
async def criar_professor(request_professor: Request_Professor):
    professor_json = request_professor
    professor = Professor(
        nome=professor_json.nome,
        email=professor_json.email,
        cpf=professor_json.cpf,
        endereco=professor_json.endereco
    )
    session.add(professor)
    session.commit()

    return {
        "status": "SUCESS",
        "data": professor_json
    }

# Rota para alterar um professor existente
@app.put("/professores")
async def alterar_professor(professor_nome: str, request_professor: Request_Professor):
    try:    
        professor_json = request_professor
        professor_query = session.query(Aluno).filter(
            Professor.nome==professor_nome
        )
        professor = professor_query.first()
        professor.nome = professor_json.nome
        professor.cpf = professor_json.cpf
        professor.email = professor_json.email
        professor.endereco = professor_json.endereco

        session.add(professor)
        session.commit()

        return {
            "status": "SUCESS",
            "data": professor_json
        }
    
    except Exception as e:
        return {
            "status": "ERROR",
            "data": "PROFESSOR NÃO ENCONTRADO"
        }

"""
# Rota para deletar um professor pelo nome
@app.delete("/professores")
def deletar_professor(nome: str):
    try:    
        professor_query = session.query(Professor).filter(
            Professor.nome==nome
        )

        professor = professor_query.first()
        session.delete(professor)

        return {
            "status": "SUCESS",
            "data": professor.nome
        }
    
    except Exception as e:
        return {
            "status": "ERROR",
            "data": "PROFESSOR NÃO ENCONTRADO"
        }
""" 

## ----------------------- CURSO  ----------------------- 
@app.get("/cursos")
async def get_all_cursos():
    cursos_query = session.query(Curso)
    cursos = cursos_query.all()
    return {
        "status": "SUCESS",
        "data": cursos
    }

# Rota para criar um novo curso
@app.post("/cursos")
async def criar_curso(request_curso: Request_Curso):
    curso_json = request_curso
    curso = Curso(
        descricao = curso_json.descricao
    )
    session.add(curso)
    session.commit()

    return {
        "status": "SUCESS",
        "data": curso_json
    }

# Rota para alterar um curso existente
@app.put("/cursos")
async def alterar_curso(curso_descricao: str, request_curso: Request_Curso):
    try:    
        curso_json = request_curso
        curso_query = session.query(Curso).filter(
            Curso.descricao==curso_descricao
        )
        curso = curso_query.first()
        curso.descricao = curso_json.descricao

        session.add(curso)
        session.commit()

        return {
            "status": "SUCESS",
            "data": curso_json
        }
    
    except Exception as e:
        return {
            "status": "ERROR",
            "data": "CURSO NÃO ENCONTRADO"
        }
    
"""
# Rota para deletar um curso pelo nome
@app.delete("/cursos")
def deletar_curso(descricao: str):
    try:    
        curso_query = session.query(Curso).filter(
            Curso.descricao==descricao
        )

        curso = curso_query.first()
        session.delete(curso)

        return {
            "status": "SUCESS",
            "data": curso.descricao
        }
    
    except Exception as e:
        return {
            "status": "ERROR",
            "data": "CURSO NÃO ENCONTRADO"
        }
"""

## ----------------------- CURSO - ALUNO ----------------------- 
@app.get("/curso_alunos")
async def get_all_alunos_curso():
    alunos_curso_query = session.query(CursoAluno)
    alunos_curso = alunos_curso_query.all()
    return {
        "status": "SUCESS",
        "data": alunos_curso
    }

# Rota para adicionar um aluno ao curso
@app.post("/curso_alunos")
async def adicionar_aluno_curso(aluno_nome: str, curso_descricao:  str):
    try:
        aluno_query = session.query(Aluno).filter(
            Aluno.nome==aluno_nome
        )

        curso_query = session.query(Curso).filter(
            Curso.descricao==curso_descricao
        )

        aluno_json = aluno_query.first()
        curso_json = curso_query.first()
        
        curso_aluno = CursoAluno(
            aluno = aluno_json,
            curso = curso_json
        )

        session.add(curso_aluno)
        session.commit()

        return {
            "status": "SUCESS",
            "data": curso_aluno
        }
    
    except Exception as e:
        print(e)
        return {
            "status": "ERROR",
            "data": "ALUNO/CURSO NÃO ENCONTRADO"
        }

"""
# Rota para deletar um aluno de um curso pelo nome
@app.delete("/curso_alunos")
def deletar_aluno_curso(aluno_nome: str, curso_descricao: str):
    try:   
        aluno_query = session.query(Aluno).filter(
            Aluno.nome==aluno_nome
        )

        curso_query = session.query(Curso).filter(
            Curso.descricao==curso_descricao
        )

        aluno_json = aluno_query.first()
        curso_json = curso_query.first()
        
        curso_aluno = CursoAluno(
            aluno = aluno_json,
            curso = curso_json
        )

        curso_aluno_query = session.query(CursoAluno).filter(
            CursoAluno.aluno == curso_aluno.aluno and CursoAluno.curso == curso_aluno.curso
        )

        curso_aluno_remove = curso_aluno_query.first()
        session.delete(curso_aluno_remove)

        return {
            "status": "SUCESS",
            "data": curso_aluno_remove
        }

    except Exception as e:
        print(e)
        return {
            "status": "ERROR",
            "data": "ALUNO/CURSO NÃO ENCONTRADO"
        }
"""

## ----------------------- CURSO - PROFESSOR ----------------------- 
@app.get("/curso_professor")
async def get_all_professor_cursos():
    professor_curso_query = session.query(CursoProfessor)
    professor_curso = professor_curso_query.all()
    return {
        "status": "SUCESS",
        "data": professor_curso
    }

# Rota para adicionar um aluno ao curso
@app.post("/curso_professor")
async def adicionar_professor_curso(professor_nome: str, curso_descricao:  str):
    try:
        professor_query = session.query(Professor).filter(
            Professor.nome==professor_nome
        )

        curso_query = session.query(Curso).filter(
            Curso.descricao==curso_descricao
        )

        professor_json = professor_query.first()
        curso_json = curso_query.first()
        
        curso_professor = CursoProfessor(
            professor = professor_json,
            curso = curso_json
        )

        session.add(curso_professor)
        session.commit()

        return {
            "status": "SUCESS",
            "data": curso_professor
        }
    
    except Exception as e:
        print(e)
        return {
            "status": "ERROR",
            "data": "PROFESSOR/CURSO NÃO ENCONTRADO"
        }

"""
# Rota para deletar um professor de um curso pelo nome
@app.delete("/curso_professor")
def deletar_professor_curso(professor_nome: str, curso_descricao: str):
    try:   
        professor_query = session.query(Professor).filter(
            Professor.nome==professor_nome
        )

        curso_query = session.query(Curso).filter(
            Curso.descricao==curso_descricao
        )

        professor_json = professor_query.first()
        curso_json = curso_query.first()
        
        curso_professor = CursoProfessor(
            professor = professor_json,
            curso = curso_json
        )

        curso_professor_query = session.query(CursoProfessor).filter(
            CursoProfessor.professor == curso_professor.professor and CursoProfessor.curso == curso_professor.curso
        )

        curso_professor_remove = curso_professor_query.first()
        session.delete(curso_professor_remove)

        return {
            "status": "SUCESS",
            "data": curso_professor_remove
        }

    except Exception as e:
        print(e)
        return {
            "status": "ERROR",
            "data": "PROFESSOR/CURSO NÃO ENCONTRADO"
        }
"""