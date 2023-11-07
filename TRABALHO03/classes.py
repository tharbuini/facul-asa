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

class Request_Curso_Aluno(BaseModel):
    id_aluno:   int
    id_curso:   int

class Request_Curso_Professor(BaseModel):
    id_professor:   int
    id_curso:   int