# Concept: Data Type Safety, Validation & Serialization

In backend engineering, you must treat **all client input as untrusted**. A client can send missing fields, incorrect data types (like text where a price should be), or malicious payloads designed to crash your app or database.

In FastAPI, **Pydantic** is the library responsible for resolving this problem. It does two main things:
1.  **Data Validation (Deserialization / Parsing):** Inspects incoming data payloads, checks them against your types, coerces values if possible (e.g. converting a string `"12.50"` to a float `12.5`), and throws clear errors if validation fails.
2.  **Data Serialization (Filtering):** Transforms Python objects (like SQLAlchemy database rows) back into JSON strings, filtering out sensitive columns (like passwords) before sending the data to the client.

---

## 1. What is a Pydantic Model?

A Pydantic model is a class that inherits from `pydantic.BaseModel`. It defines the "shape" of your data using Python type annotations.

```python
from pydantic import BaseModel, EmailStr, Field

class CreateUserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr  # Automatically validates email formatting!
    age: int = Field(gt=0, lt=150)  # Must be between 0 and 150
```

If a client sends this:
```json
{
  "username": "jk",
  "email": "invalid-email",
  "age": -5
}
```
Pydantic intercepts this request *before* your endpoint function runs, halts execution, and returns a detailed `422 Unprocessable Entity` status code indicating precisely what failed.

---

## 2. Inbound vs. Outbound Schemas (DTOs)

A critical backend pattern is separating **Inbound** schemas (what the client sends) from **Outbound** schemas (what the server returns). This pattern is often called **Data Transfer Objects (DTOs)**.

```
       [ Client Request Payload ]
                   │
                   ▼
       [ Inbound Schema (UserCreate) ] 
       - requires username, password, email.
                   │
                   ▼
         ( Business Logic / DB )
                   │
                   ▼
       [ Outbound Schema (UserResponse) ]
       - returns id, username, email, created_at.
       - NEVER returns the hashed password!
                   │
                   ▼
       [ Client Response Payload ]
```

---

## 3. Nested Schemas

Real-world datasets are rarely flat. Pydantic handles nested JSON structures cleanly by letting models contain lists or other models.

```python
class Item(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    order_id: int
    items: list[Item]  # Lists of other Pydantic models!
```

---

## 4. Query & Path Parameter Validations

FastAPI also lets you apply validation rules directly to query and path parameters using `Query` and `Path` classes from `fastapi`.

*   `q: str | None = Query(default=None, min_length=3)` (Requires queries to be at least 3 characters if provided).
*   `item_id: int = Path(gt=0)` (Ensures the URL path parameter is a positive integer).
