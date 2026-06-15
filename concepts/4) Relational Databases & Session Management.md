# Concept: Relational Databases & Session Management

Every real-world backend application needs to store data permanently (persistence). If the server crashes or restarts, state stored in-memory (in global lists or dicts) is lost.

In this module, we explore how to link a database, write to it, read from it, and manage connection lifecycles safely.

---

## 1. What is an ORM (Object-Relational Mapper)?

A relational database (like PostgreSQL or SQLite) stores data in flat **Tables** consisting of **Rows** and **Columns**.
Python is an **Object-Oriented Language** utilizing **Classes** and **Instances**.

An **ORM** (such as SQLAlchemy or SQLModel) acts as a translator:
*   An ORM class maps to a Database Table.
*   An object instance maps to a Row.
*   Object attributes map to Columns.

```python
# Python Class definition
class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)

# Translates to SQL:
# CREATE TABLE users (id INTEGER PRIMARY KEY, username VARCHAR);
```

---

## 2. Managing the Database Session

A database session represents a single unit of work (a transaction) with the database.

### The Session Lifecycle:
1.  **Request Begins:** The client hits an endpoint.
2.  **Session Created:** FastAPI invokes dependency injection to obtain a database session (`SessionLocal()`).
3.  **Execute Operations:** Read user data, change field values, add new rows.
4.  **Transaction Commit:** If everything succeeds, save all changes permanent to disk (`db.commit()`).
5.  **Transaction Rollback:** If any error occurs during execution, cancel all uncommitted database changes to avoid corrupting state (`db.rollback()`).
6.  **Close Session:** Release the database connection back to the connection pool so other requests can reuse it (`db.close()`).

---

## 3. Why SQLite?

For learning, we use **SQLite**.
*   It is serverless: the database is stored in a single, local file (e.g., `test.db`).
*   It requires no external daemon to run (unlike PostgreSQL or MySQL).
*   SQLAlchemy treats it exactly like PostgreSQL, meaning the code you write here works similarly on enterprise databases with minor configuration swaps.
