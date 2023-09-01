from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

# definindo a URL para conexão no banco
url = URL.create(
    drivername='postgresql+psycopg2',
    username='postgres',
    password='banco',
    host='localhost',
    database='faculdade',
    port=5432
)

#url = "postgresql+psycopg2://postgres:banco@localhost/postgres"

# nesse ponto são instanciados os objetos para conexão com o banco
engine  = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Aluno(Base):
    __tablename__ = 'aluno'

    id          = Column(Integer, primary_key=True)
    nome        = Column(String, nullable=True)
    email       = Column(String)
    cpf         = Column(String, nullable=True)
    endereco    = Column(String, nullable=True)



Base.metadata.create_all(engine)



