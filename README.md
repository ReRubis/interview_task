# zypl_interview.

*Для запуска*: 
```sh
docker-compose up -d --build
uvicorn --app-dir app main:app --reload
```

*Миграции*:

```sh
alembic revision --autogenerate -m "<message>"
alembic upgrade head
```

*Login to DB inside the docker container*:
```sh
psql -h localhost -d postgres -U myuser -W
select count(*) from pg_stat_activity;

\l  list databases
\c zypl;
\dt list tables
```