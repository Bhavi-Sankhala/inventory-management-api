# Inventory Management API

Backend-only Inventory Management API built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy ORM**.  
The project follows a **schema-first design** and exposes clean CRUD APIs with automatic Swagger documentation.

---

## Features

- Product inventory management
- CRUD APIs (Create, Read, Update, Delete)
- Schema-first PostgreSQL design
- SQLAlchemy used only for ORM mapping and queries
- Swagger UI for API testing
- No authentication, no frontend, no migrations

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Pydantic
- Uvicorn

---

## Architecture Highlights

- Tables are created manually in PostgreSQL (schema-first)
- SQLAlchemy models map to existing tables
- Thin APIs: one endpoint per CRUD action
- Stateless REST APIs

---

## API Endpoints

| Method | Endpoint | Description |
|------|--------|------------|
| GET | `/products` | Get all products |
| POST | `/products` | Create a product |
| GET | `/products/{id}` | Get product by ID |
| PUT | `/products/{id}` | Update product |
| DELETE | `/products/{id}` | Delete product |

---

## Swagger Documentation

Swagger UI is available at:
http://127.0.0.1:8000/docs


---

## Project Structure

API/
├── app/
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ └── crud.py
├── requirements.txt
└── README.md


---

## Setup & Run

### Prerequisites
- Python 3.10+
- PostgreSQL

### Steps

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

## Notes

- Database tables are created manually in PostgreSQL (schema-first approach)
- No authentication or authorization is implemented
- Designed to demonstrate clean and minimal backend architecture

---

## Future Enhancements

- Stock in / stock out tracking
- Product categories
- Pagination and filtering
- Authentication and role-based access control

