import pika
import json
import asyncio
from models import Session, Item, Caminhao, Cliente, Pedido

def callback(ch, method, properties, body):
    # Deserialize a mensagem
    message_data = json.loads(body)

    # Verifica o tipo e processa os dados correspondentes
    tipo = message_data.get("tipo")
    tabela = message_data.get("tabela")
    dados = message_data.get("dados")

    print(f"\nRabbitMQ\n{tipo=}\n{tabela=}\n{dados=}")

    if tabela == "itens":
        retorno = processa_itens(tipo, dados)
    elif tabela == "caminhoes":
        retorno = processa_caminhoes(tipo, dados)
    elif tabela == "clientes":
        retorno = processa_clientes(tipo, dados)
    elif tabela == "pedidos":
        retorno =  processa_pedidos(tipo, dados)

    print(f"{retorno=}")

def processa_itens(tipo, dados):
    item = Item(**json.loads(dados))
    if tipo == "post":
        return inserir_no_banco(item)
    elif tipo == "put":
        session = Session()
        try:
            BDitem = session.query(Item).filter(Item.id == item.id).first()
            original_item = Item(
                id          = BDitem.id,
                nome        = BDitem.nome,
                descricao   = BDitem.descricao,
                peso        = BDitem.peso
            )

            BDitem.nome       = item.nome
            BDitem.descricao  = item.descricao
            BDitem.peso       = item.peso

            session.commit()
            session.refresh(BDitem)

            return {
                "status": "SUCESS",
                "original": original_item,
                "data": item
            }
        except Exception as e:
            print(f"Erro ao atualizar o banco: {str(e)}")
            session.rollback()
        finally:
            session.close()

def processa_caminhoes(tipo, dados):
    caminhao = Caminhao(**json.loads(dados))
    if tipo == "post":
        return inserir_no_banco(caminhao)
    elif tipo == "put":
        session = Session()
        try:
            BDcaminhao = session.query(Caminhao).filter(Caminhao.id == caminhao.id).first()
            original_caminhao = Caminhao(
                id               = BDcaminhao.id,
                modelo           = BDcaminhao.modelo,
                capacidade_carga = BDcaminhao.capacidade_carga,
                localizacao      = BDcaminhao.localizacao,
                status           = BDcaminhao.status,
                motorista        = BDcaminhao.motorista
            )

            BDcaminhao.modelo           = caminhao.modelo
            BDcaminhao.capacidade_carga = caminhao.capacidade_carga
            BDcaminhao.localizacao      = caminhao.localizacao
            BDcaminhao.status           = caminhao.status
            BDcaminhao.motorista        = caminhao.motorista

            session.commit()
            session.refresh(BDcaminhao)
            return {
                "status": "SUCESS",
                "original": original_caminhao,
                "data": BDcaminhao
            }
        except Exception as e:
            print(f"Erro ao atualizar o banco: {str(e)}")
            session.rollback()
        finally:
            session.close()


def processa_clientes(tipo, dados):
    cliente = Cliente(**json.loads(dados))
    if tipo == "post":
        return inserir_no_banco(cliente)
    elif tipo == "put":
        session = Session()
        try:
            BDcliente = session.query(Cliente).filter(Cliente.id == cliente.id).first()
            original_cliente = Cliente(
                id          = BDcliente.id,
                nome        = BDcliente.nome,
                telefone    = BDcliente.telefone,
                cpf         = BDcliente.cpf,
                cep         = BDcliente.cep,
                numero      = BDcliente.numero,
                complemento = BDcliente.complemento
            )
            BDcliente.nome        = cliente.nome,
            BDcliente.telefone    = cliente.telefone,
            BDcliente.cpf         = cliente.cpf,
            BDcliente.cep         = cliente.cep,
            BDcliente.numero      = cliente.numero,
            BDcliente.complemento = cliente.complemento

            session.commit()
            session.refresh(BDcliente)
            return {
                "status": "SUCESS",
                "original": original_cliente,
                "data": BDcliente
            }
        except Exception as e:
            print(f"Erro ao atualizar o banco: {str(e)}")
            session.rollback()
        finally:
            session.close()

def processa_pedidos(tipo, dados):
    pedido = Pedido(**json.loads(dados))
    if tipo == "post":
        return inserir_no_banco(pedido)
    elif tipo == "put":
        session = Session()
        try:
            BDpedido = session.query(Pedido).filter(Pedido.id == pedido.id).first()
            original_pedido = Pedido(
                id          = BDpedido.id,
                quantidade  = BDpedido.quantidade,
                status      = BDpedido.status,
                cliente_id  = BDpedido.cliente_id,
                item_id     = BDpedido.item_id,
                caminhao_id = BDpedido.caminhao_id
            )
            BDpedido.quantidade   = pedido.quantidade,
            BDpedido.status       = pedido.status,
            BDpedido.cliente_id   = pedido.cliente_id,
            BDpedido.item_id      = pedido.item_id,
            BDpedido.caminhao_id  = pedido.caminhao_id

            session.commit()
            session.refresh(BDpedido)
            return {
                "status": "SUCESS",
                "original": original_pedido,
                "data": BDpedido
            }
        except Exception as e:
            print(f"Erro ao atualizar o banco: {str(e)}")
            session.rollback()
        finally:
            session.close()

def inserir_no_banco(objeto):
    session = Session()
    try:
        del(objeto.id)
        session.add(objeto)
        session.commit()
        return {
            "status": "SUCESS",
            "data": objeto
        }
    except Exception as e:
        print(f"Erro ao inserir no banco: {str(e)}")
        session.rollback()
    finally:
        session.close()

async def subscriber():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('10.99.236.228', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='transportadora_queue')

    channel.basic_consume(queue='transportadora_queue',
                          on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


def app():
    TIME_INTERVAL_IN_SEC = 5

    async def crawl_websites():
        while True:
            try:
                await subscriber()
                await asyncio.sleep(TIME_INTERVAL_IN_SEC)
            except Exception as e:
                pass

    loop = asyncio.get_event_loop()
    task = loop.create_task(crawl_websites())
    loop.run_until_complete(task)
