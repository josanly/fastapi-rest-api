# REST API build with FastAPI

## Generate secret key (random)

```bash
$ openssl rand -hex 32
```

```bash
# inside mongodb container 
$ docker compose exec mongodb /bin/sh

root@d6c8bd94bb9c:/#  mongosh -u admin -p admin --authenticationDatabase admin
test> db.createUser({user: 'restapp', pwd: 'restapppassword', roles: [{role: 'readWrite', db: 'docdb', }, ],});
test > use docdb
docdb> 
```
