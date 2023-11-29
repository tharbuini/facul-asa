from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.engine.url import URL

# BANCO ========================================================
# Configuração da URL do PostgreSQL
db_url = URL.create(
    drivername='postgresql+psycopg2',
    username='admin',
    password='admin',
    host='localhost',
    database='postgres',
    port=5432
)

# Configuração da conexão com o PostgreSQL
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Item(Base):
    __tablename__ = 'itens'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    peso = Column(Float)

class Caminhao(Base):
    __tablename__ = 'caminhoes'
    id = Column(Integer, primary_key=True)
    modelo = Column(String, nullable=False)
    capacidade_carga = Column(Float, nullable=False)
    localizacao = Column(String, nullable=False)  # Informação de localização do caminhão
    status = Column(String, nullable=False)  # Status do caminhão
    motorista = Column(String, nullable=False)

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    complemento = Column(String, nullable=False)

class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True)
    quantidade = Column(Integer)
    status = Column(String, nullable=False)  # Status do pedido
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    cliente = relationship("Cliente")
    item_id = Column(Integer, ForeignKey('itens.id'))
    item = relationship("Item")
    caminhao_id = Column(Integer, ForeignKey('caminhoes.id'))
    caminhao = relationship("Caminhao")

# Crie as tabelas no banco de dados
Base.metadata.create_all(engine)