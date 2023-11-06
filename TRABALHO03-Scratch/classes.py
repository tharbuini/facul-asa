from pydantic import BaseModel

class Request_Aluno(BaseModel):
    id:         int
    nome:       str
    email:      str
    cpf:        str
    endereco:   str

class Request_Professor(BaseModel):
    id:         int
    nome:       str
    email:      str
    cpf:        str
    endereco:   str

class Request_Curso(BaseModel):
    id:         int
    descricao:  str

class Request_Aluno_Curso(BaseModel):
    id_aluno:   int
    nome:       str
    email:      str
    cpf:        str
    endereco:   str
    id_curso:   int
    descricao:  str