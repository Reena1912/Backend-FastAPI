# Concept: Non-blocking I/O & The Event Loop

In traditional backend frameworks (like Django or Flask), each incoming request is assigned to a thread. If a request queries a database that takes 2 seconds to respond, that thread is completely frozen (blocked) waiting for the data. To handle 1000 concurrent requests, you need 1000 threads, which consumes massive amounts of RAM and CPU.

FastAPI is built on **Starlette** and uses Python's **AsyncIO** engine to implement **Asynchronous Concurrency (Non-blocking I/O)**.

---

## 1. The Event Loop & The Waiter Analogy

Think of the server as a restaurant with one waiter (the Event Loop):

*   **Synchronous (Blocking):** The waiter takes Order 1 to the kitchen, stands at the window, and waits 15 minutes for the chef to cook it. During this time, customers at Tables 2, 3, and 4 cannot order or get water.
*   **Asynchronous (Non-blocking):** The waiter takes Order 1 to the kitchen. The chef starts cooking it. The waiter immediately leaves the kitchen to take orders from Tables 2, 3, and 4. When Order 1 is ready, the kitchen calls the waiter, and the waiter serves it.

In asynchronous code, the server can handle thousands of clients concurrently on a **single thread**, because it never wastes time waiting for network calls, database queries, or file reads to resolve.

---

## 2. The `async` and `await` Keywords

*   **`async def`:** Declares a function as a **Coroutine**. Calling this function does not run the code; it returns a coroutine object that is ready to be run.
*   **`await`:** Can *only* be used inside an `async def` function. It tells the Event Loop: "This operation will take some time (like a network call). I yield control back to you. Go work on other requests, and resume this function once this operation completes."

```python
import asyncio

async def fetch_data():
    # Simulate a 2-second database query. 
    # asyncio.sleep is non-blocking, yielding control back to the loop.
    await asyncio.sleep(2) 
    return {"data": "success"}
```

---

## 3. When to use `async def` vs. normal `def` in FastAPI

One of the most important concepts in FastAPI is knowing when to write `async def` vs. normal `def`.

### The golden rules:
1.  **Use `async def`** if you are calling libraries that support `async/await` (e.g., using `httpx` for API requests, `asyncpg` for PostgreSQL, or `motor` for MongoDB).
2.  **Use `async def`** if you have zero blocking operations (only simple calculations/returns).
3.  **Use normal `def`** if you are calling blocking, synchronous libraries (like standard SQLAlchemy, `requests` for APIs, or `time.sleep`).
    *   *Why?* If you write `async def` but then run a blocking operation like `time.sleep(2)` inside it, **you block the entire event loop**, freezing the whole server for everyone.
    *   If you write normal `def`, FastAPI is smart: it automatically runs that function in a background **Thread Pool** so it doesn't block the main event loop.
