from pydantic import BaseModel

class Request_Aluno(BaseModel):
    id:         int
    nome:       str
    email:      str
    cpf:        str
    endereco:   str
