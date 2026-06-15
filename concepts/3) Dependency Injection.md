# Concept: Dependency Injection (DI)

**Dependency Injection** is a software design pattern where an object or function receives other resources (dependencies) it needs, rather than creating them itself.

In FastAPI, the Dependency Injection engine is extremely powerful and centered around `Depends()`.

---

## 1. The Core Problem: Tightly Coupled Code

Imagine we have a function to get items from a database:

```python
# POOR PRACTICE (Hardcoded Dependency)
def read_items():
    db = DatabaseConnection("postgresql://user:pass@host/db") # Created inside!
    return db.query_all_items()
```

If you want to run unit tests, this function *always* tries to connect to the production PostgreSQL instance. You can't swap the database connection for a mock connection without modifying the function's internal code.

---

## 2. The Solution: Injected Dependencies

Instead of creating the resource inside the function, we ask FastAPI to inject it:

```python
# GOOD PRACTICE (Injected Dependency)
def get_db():
    db = DatabaseConnection("postgresql://...")
    try:
        yield db
    finally:
        db.close() # Ensures connection closes when request completes!

@app.get("/items")
def read_items(db = Depends(get_db)):
    return db.query_all_items()
```

---

## 3. Why Use Dependency Injection?

1.  **Code Reuse:** Share utilities (like database sessions, configurations, or authentication validators) across multiple routes easily.
2.  **Resource Lifecycle Management:** With `yield`, FastAPI handles the cleanup of resources. It runs the setup part, gives the resource to the endpoint, waits for the endpoint to return the response, and then runs the cleanup part (e.g. closing database sessions or network sockets) automatically.
3.  **Testability (Dependency Overrides):** During testing, you can instruct FastAPI to replace a real dependency (like `get_db`) with a mock dependency (like `get_test_db`) without modifying a single line of endpoint code.
4.  **Sub-dependencies:** Dependencies can depend on *other* dependencies, creating a dependency tree. FastAPI resolves the entire tree automatically.

---

## 4. How FastAPI Resolves Dependencies

1.  A request arrives at `@app.get("/items")`.
2.  FastAPI sees `db = Depends(get_db)` in the function signature.
3.  FastAPI runs `get_db()`.
4.  If `get_db()` uses `yield`, FastAPI executes up to the `yield` statement.
5.  FastAPI passes the yielded database session into the `read_items` function as the `db` variable.
6.  The `read_items` function processes the request and returns a response.
7.  FastAPI goes back to `get_db()` and runs the cleanup code (after the `yield` statement) to close the session.
