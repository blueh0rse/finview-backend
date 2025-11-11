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

> See `Makefile` for the complete list!

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL

## Changelog

### v1.0.0

- Implement CRUD operations for Transaction.
- Display the total portfolio value (net invested amount).
- Show the portfolio allocation by asset (quantity × unit price, with percentage of total).
