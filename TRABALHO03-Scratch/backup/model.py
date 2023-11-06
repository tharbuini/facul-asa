from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import relationship
from local_settings import postgresql as settings

def get_engine(user, passwd, host, port, db):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine

engine = get_engine(settings['pguser'],
                    settings['pgpasswd'],
                    settings['pghost'],
                    settings['pgport'],
                    settings['pgdb'])

def get_engine_from_settings():
    keys = ['pguser', 'pgpasswd', 'pghost', 'pgport', 'pgdb']
    if not all(key in keys for key in settings.keys()):
        raise Exception('Bad config file')

    return get_engine(settings['pguser'],
                      settings['pgpasswd'],
                      settings['pghost'],
                      settings['pgport'],
                      settings['pgdb'])

engine  = get_engine_from_settings()
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

class CursoAluno(Base):
    __tablename__  = 'cursoaluno'        
    idAluno     = Column(Integer, ForeignKey('aluno.id'), primary_key=True)
    idCurso     = Column(Integer, ForeignKey('curso.id'), primary_key=True)        
    curso       = relationship(Curso)
    aluno       = relationship(Aluno)

class CursoProfessor(Base):
    __tablename__  = 'cursoprofessor'
    idProfessor = Column(Integer, ForeignKey('professor.id'), primary_key=True)
    idCurso     = Column(Integer, ForeignKey('curso.id'), primary_key=True)        
    curso       = relationship(Curso)
    professor   = relationship(Professor)

Base.metadata.create_all(engine)

