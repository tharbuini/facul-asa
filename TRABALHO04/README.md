<!-- @format -->

## Projeto de Arquitetura de Software Aplicada: Transportadora

Execute o docker-compose para iniciar os containers do banco, gerenciador do banco e o rabbitmq

```
docker-compose up -d
```

Navegue até o diretório app/src/

```
cd app/src/
```

Execute o publisher

```
uvicorn publisher:app --host localhost --port 8000 --reload
```

Em outro terminal execute o subscriber

```
uvicorn subscriber:app --host localhost --port 8001 --reload
```
