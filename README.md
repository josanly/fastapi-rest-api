# REST API build with FastAPI

Small project to develop REST API using [FastAPI](https://fastapi.tiangolo.com/).

## Development 

### Generate secret key (random)

```bash
$ openssl rand -hex 32
```



## Docker Compose (dev and testing only) 

Stack:

* FastAPI app
* Postgres server
* Mongodb server
* Traefik proxy

Access Swagger UI of FastAPI app: http://fastapi.localhost:8000/docs

Access Traefik dashboard: http://fastapi.localhost:8081/dashboard/#/

For further details refer to: [this blog](https://testdriven.io/blog/fastapi-docker-traefik/#production-dockerfile).

### Setup Mongodb

Create User:

```bash
# inside mongodb container 
$ docker compose exec mongodb /bin/sh

root@d6c8bd94bb9c:/#  mongosh -u admin -p admin --authenticationDatabase admin
test> db.createUser({user: 'restapp', pwd: 'restapppassword', roles: [{role: 'readWrite', db: 'docdb', }, ],});
test > use docdb
docdb> 
```