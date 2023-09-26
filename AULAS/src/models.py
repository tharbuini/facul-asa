from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import relationship

# definindo a URL para conexão no banco
url = URL.create(
    drivername='postgresql+psycopg2',
    username='postgres',
    password='banco',
    host='localhost',
    database='postgres',
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


class Professor(Base):
    __tablename__ = 'professor'
    id          = Column(Integer, primary_key=True)
    nome        = Column(String, nullable=True)
    email       = Column(String)
    cpf         = Column(String, nullable=True)
    endereco    = Column(String, nullable=True)


class Curso(Base):
    __tablename__   = 'curso'
    id              = Column(Integer, primary_key=True)
    descricao       = Column(String, nullable=True)
    professor_id    = Column(Integer, ForeignKey('professor.id'))
    professor       = relationship(Professor)

class CursoAluno(Base):
    __tablename__  = 'cursoaluno'
    idCurso     = Column(Integer, ForeignKey('curso.id'), primary_key=True)
    idAluno     = Column(Integer, ForeignKey('aluno.id'), primary_key=True)
    curso       = relationship(Curso)
    aluno       = relationship(Aluno)


Base.metadata.create_all(engine)


#docker run --name postgreSQL_SERVER -e POSTGRES_PASSWORD=banco -e POSTGRES_USER=postgres -p 5432:5432 
# -v /home/marciocunha/util/postgresData:/var/lib/postgresql/data -d postgres:14

