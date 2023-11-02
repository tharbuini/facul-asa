from fastapi import FastAPI
from classes import Request_Aluno
from models import Aluno, session
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
        "status": "SUCESS",
        "data": "NO DATAS"
    }

@app.get("/alunos")
async def get_all_alunos():
    alunos_query = session.query(Aluno)
    alunos = alunos_query.all()
    return {
        "status": "SUCESS",
        "data": alunos
    }

@app.put("/alunos")
async def alterar_aluno(request_aluno: Request_Aluno):
    try:    
        aluno_json = request_aluno
        aluno_query = session.query(Aluno).filter(
            Aluno.id==aluno_json.id
        )
        aluno = aluno_query.first()
        print(aluno.nome)
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
                "status": "SUCESS",
                "data": "ALUNO NÃO ENCONTRADO"
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
        "status": "SUCESS",
        "data": aluno_json
    }

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
     
    