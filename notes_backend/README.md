# Notes Backend (FastAPI)

Simple Notes API with in-memory storage (MVP) exposing CRUD endpoints.

- Framework: FastAPI
- Port: 3001
- CORS: allows http://localhost:3000 (frontend)

## Install

Python 3.10+

```
pip install -r requirements.txt
```

## Run

```
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

Then open:
- API docs: http://localhost:3001/docs
- OpenAPI JSON: http://localhost:3001/openapi.json

## Endpoints

- GET /            -> Health
- GET /notes       -> List notes
- GET /notes/{id}  -> Get one
- POST /notes      -> Create
- PUT /notes/{id}  -> Update
- DELETE /notes/{id} -> Delete

Note model:
```
{
  "id": number,
  "title": string,
  "content": string,
  "updated_at": ISO datetime
}
```

## Environment

For this MVP, no env variables are required. Provided for future expansion:

```
# .env.example
# BACKEND_PORT=3001
# CORS_ALLOW_ORIGINS=http://localhost:3000
```
