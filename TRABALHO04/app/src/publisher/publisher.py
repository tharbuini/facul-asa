from fastapi import FastAPI
from pydantic import BaseModel
import pika
import json
from models import session, Item, Caminhao, Cliente, Pedido

# API ========================================================
class Request_Item(BaseModel):
    id: int
    nome: str
    descricao: str
    peso: float

class Request_Caminhao(BaseModel):
    id: int
    modelo: str
    capacidade_carga: float
    localizacao: str
    status: str
    motorista: str

class Request_Cliente(BaseModel):
    id: int
    nome: str
    telefone: str
    cpf: str
    cep: str
    numero: str
    complemento: str

class Request_Pedido(BaseModel):
    id: int
    quantidade: int
    status: str  # Status do pedido
    cliente_id: int
    item_id: int
    caminhao_id: int

description = """
**Adminer:** [adminer.io](http://192.168.58.2:30000)

**Dashboard:** [kubernetes.dashboard.io](http://127.0.0.1:43187/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/)
"""

tags_metadata = [
    {"name":"Get"},
    {"name":"Post"},
    {"name":"Put"},
    {"name":"Delete"},
    {"name":"Itens"},
    {"name":"Caminhões"},
    {"name":"Clientes"},
    {"name":"Pedidos"}
]

app = FastAPI(
    title="TransportadoraAPI",
    version="2.0",
    description=description,
    openapi_tags=tags_metadata
)

# ========================================================================================

# PUBLISHER
async def publish_message(tipo: str, tabela: str, message: str):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('10.99.236.228'))
        channel = connection.channel()
        channel.queue_declare(queue='transportadora_queue')

        # Inclui o tipo na mensagem
        message_data = {
            "tipo": tipo,
            "tabela": tabela,
            "dados": message
        }

        channel.basic_publish(exchange='', routing_key='transportadora_queue', body=json.dumps(message_data))
        connection.close()
    except Exception as e:
        print(f"Erro ao publicar mensagem: {e}")

# ========================================================================================

@app.get("/", tags=["Default"])
async def api_is_running():
    return {"status": "API IS RUNNING"}

# Item CRUD
@app.post("/items/", tags=["Itens", "Post"])
async def create_item_api(request_item: Request_Item):
    try:
        # Publica a mensagem no RabbitMQ
        await publish_message("post", "itens", request_item.model_dump_json())
        return {
            "status": "SUCESS",
            "data": request_item
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "log":  f"Erro ao publicar mensagem: {e}"
        }

@app.get("/items/{item_id}", tags=["Itens", "Get"])
async def read_itens_api(item_id: int):
    return {
        "status": "SUCESS",
        "data": session.query(Item).filter(Item.id == item_id).first()
    }

@app.get("/items/", tags=["Itens", "Get"])
async def read_itens_api():
    return {
        "status": "SUCESS",
        "data": session.query(Item).all()
    }

@app.put("/items/", tags=["Itens", "Put"])
async def update_item_api(request_item: Request_Item):
    try:
        # Publica a mensagem no RabbitMQ
        await publish_message("put", "itens", request_item.model_dump_json())
        return {
            "status": "SUCESS",
            "data": request_item
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "log":  f"Erro ao publicar mensagem: {e}"
        }

@app.delete("/items/{item_id}", tags=["Itens", "Delete"])
async def delete_item_api(item_id: int):
    item = session.query(Item).filter(Item.id == item_id).first()
    session.delete(item)
    session.commit()
    return {
        "status": "SUCESS",
        "data": item
    }

# ========================================================================================
# Caminhao CRUD
@app.post("/caminhoes/", tags=["Caminhões",  "Post"])
async def create_caminhao_api(request_caminhao: Request_Caminhao):
    try:
        # Publica a mensagem no RabbitMQ
        await publish_message("post", "caminhoes", request_caminhao.model_dump_json())
        return {
            "status": "SUCESS",
            "data": request_caminhao
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "log":  f"Erro ao publicar mensagem: {e}"
        }

@app.get("/caminhoes/{caminhao_id}", tags=["Caminhões", "Get"])
async def read_caminhoes_api(caminhao_id: int):
    return {
        "status": "SUCESS",
        "data": session.query(Caminhao).filter(Caminhao.id == caminhao_id).first()
    }

@app.get("/caminhoes/", tags=["Caminhões", "Get"])
async def read_caminhoes_api():
    return {
        "status": "SUCESS",
        "data": session.query(Caminhao).all()
    }

@app.put("/caminhoes/", tags=["Caminhões", "Put"])
async def update_caminhao_api(request_caminhao: Request_Caminhao):
    try:
        # Publica a mensagem no RabbitMQ
        await publish_message("put", "caminhoes", request_caminhao.model_dump_json())
        return {
            "status": "SUCESS",
            "data": request_caminhao
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "log":  f"Erro ao publicar mensagem: {e}"
        }

@app.delete("/caminhoes/{caminhao_id}", tags=["Caminhões", "Delete"])
async def delete_caminhao_api(caminhao_id: int):
    caminhao = session.query(Caminhao).filter(Caminhao.id == caminhao_id).first()
    session.delete(caminhao)
    session.commit()
    return {
        "status": "SUCESS",
        "data": caminhao
    }

# # ========================================================================================
# Cliente CRUD
@app.post("/clientes/", tags=["Clientes",  "Post"])
async def create_cliente_api(request_cliente: Request_Cliente):
    try:
        # Publica a mensagem no RabbitMQ
        await publish_message("post", "clientes", request_cliente.model_dump_json())
        return {
            "status": "SUCESS",
            "data": request_cliente
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "log":  f"Erro ao publicar mensagem: {e}"
        }

@app.get("/clientes/{cliente_id}", tags=["Clientes", "Get"])
async def read_clientes_api(cliente_id: int):
    return {
        "status": "SUCESS",
        "data": session.query(Cliente).filter(Cliente.id == cliente_id).first()
    }

@app.get("/clientes/", tags=["Clientes", "Get"])
async def read_clientes_api():
    return {
        "status": "SUCESS",
        "data": session.query(Cliente).all()
    }

@app.put("/clientes/", tags=["Clientes", "Put"])
async def update_cliente_api(request_cliente: Request_Cliente):
    try:
        # Publica a mensagem no RabbitMQ
        await publish_message("put", "clientes", request_cliente.model_dump_json())
        return {
            "status": "SUCESS",
            "data": request_cliente
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "log":  f"Erro ao publicar mensagem: {e}"
        }

@app.delete("/clientes/{cliente_id}", tags=["Clientes", "Delete"])
async def delete_cliente_api(cliente_id: int):
    cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
    session.delete(cliente)
    session.commit()
    return {
        "status": "SUCESS",
        "data": cliente
    }

# # ========================================================================================
# Pedido CRUD
@app.post("/pedidos/", tags=["Pedidos",  "Post"])
async def create_pedido_api(request_pedido: Request_Pedido):
    try:
        # Publica a mensagem no RabbitMQ
        await publish_message("post", "pedidos", request_pedido.model_dump_json())
        return {
            "status": "SUCESS",
            "data": request_pedido
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "log":  f"Erro ao publicar mensagem: {e}"
        }

@app.get("/pedidos/{pedido_id}", tags=["Pedidos", "Get"])
async def read_pedidos_api(pedido_id: int):
    return {
        "status": "SUCESS",
        "data": session.query(Pedido).filter(Pedido.id == pedido_id).first()
    }

@app.get("/pedidos/", tags=["Pedidos", "Get"])
async def read_pedidos_api():
    return {
        "status": "SUCESS",
        "data": session.query(Pedido).all()
    }

@app.put("/pedidos/", tags=["Pedidos", "Put"])
async def update_pedido_api(request_pedido: Request_Pedido):
    try:
        # Publica a mensagem no RabbitMQ
        await publish_message("put", "pedidos", request_pedido.model_dump_json())
        return {
            "status": "SUCESS",
            "data": request_pedido
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "log":  f"Erro ao publicar mensagem: {e}"
        }

    try:
        pedido = session.query(Pedido).filter(Pedido.id == request_pedido.id).first()
        original_pedido = Pedido(
            id          = pedido.id,
            quantidade  = pedido.quantidade,
            status      = pedido.status,
            cliente_id  = pedido.cliente_id,
            item_id     = pedido.item_id,
            caminhao_id = pedido.caminhao_id
        )
        pedido.quantidade   = request_pedido.quantidade,
        pedido.status       = request_pedido.status,
        pedido.cliente_id   = request_pedido.cliente_id,
        pedido.item_id      = request_pedido.item_id,
        pedido.caminhao_id  = request_pedido.caminhao_id

        session.commit()
        session.refresh(pedido)
        return {
            "status": "SUCESS",
            "original": original_pedido,
            "data": pedido
        }
    except Exception as e:
        return{
            "status": "NOT SUCESS",
            "data": "PEDIDO NÃO ENCONTRADO",
            "error": e
        }

@app.delete("/pedidos/{pedido_id}", tags=["Pedidos", "Delete"])
async def delete_pedido_api(pedido_id: int):
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
    session.delete(pedido)
    session.commit()
    return {
        "status": "SUCESS",
        "data": pedido
    }

