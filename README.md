# FINVIEW

A Finary-like web application.

## Start

Dev locally

```sh
make db
make api
```

Build everything

```sh
make run
```

## Commands

```sh
make run            -> start API and DB containers
make clean          -> clean API and DB containers

make api            -> start dev API server
make db             -> start DB container

make check          -> lint code with ruff
make lint           -> lint and fix errors with ruff
make format         -> format code with ruff
```

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
