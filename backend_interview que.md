# Backend Interview Questions & Detailed Explanations

This guide explains 30 fundamental backend interview questions in a clear, beginner-friendly manner. Each answer uses analogies, simple terms, and real-world examples to make complex concepts easy to understand.

---

## 📋 Table of Contents
1. [Monolithic vs. Microservices](#1-monolithic-vs-microservices)
2. [Synchronous vs. Asynchronous Processing](#2-synchronous-vs-asynchronous-processing)
3. [RESTful APIs vs. GraphQL](#3-restful-apis-vs-graphql)
4. [Event-Driven Architecture](#4-event-driven-architecture)
5. [Handling Background Jobs](#5-handling-background-jobs)
6. [SQL vs. NoSQL Databases](#6-sql-vs-nosql-databases)
7. [Database Indexing & Performance](#7-database-indexing--performance)
8. [ACID Properties](#8-acid-properties)
9. [Preventing Deadlocks](#9-preventing-deadlocks)
10. [Database Replication](#10-database-replication)
11. [Caching Strategies](#11-caching-strategies)
12. [Redis vs. Memcached](#12-redis-vs-memcached)
13. [Optimizing Database Queries](#13-optimizing-database-queries)
14. [Rate Limiting & Security](#14-rate-limiting--security)
15. [Scaling to Millions of Requests](#15-scaling-to-millions-of-requests)
16. [OAuth vs. JWT vs. Sessions](#16-oauth-vs-jwt-vs-sessions)
17. [Preventing SQL Injection](#17-preventing-sql-injection)
18. [CORS (Cross-Origin Resource Sharing)](#18-cors-cross-origin-resource-sharing)
19. [Common Security Vulnerabilities](#19-common-security-vulnerabilities)
20. [Secure Password Storage](#20-secure-password-storage)
21. [Designing a URL Shortener](#21-designing-a-url-shortener)
22. [Designing a Message Queue](#22-designing-a-message-queue)
23. [Load Balancing](#23-load-balancing)
24. [Distributed File Storage](#24-distributed-file-storage)
25. [Eventual vs. Strong Consistency](#25-eventual-vs-strong-consistency)
26. [Unit, Integration, & E2E Testing](#26-unit-integration--e2e-testing)
27. [Debugging Memory Leaks](#27-debugging-memory-leaks)
28. [Logging & Monitoring](#28-logging--monitoring)
29. [Failed Transactions in Distributed Systems](#29-failed-transactions-in-distributed-systems)
30. [Idempotency in APIs](#30-idempotency-in-apis)

---

### 1. Monolithic vs. Microservices
* **Analogy**: 
  * **Monolith**: A Swiss Army Knife. It has a knife, scissors, corkscrew, and screwdriver all attached to a single handle. It's compact and easy to carry, but if the scissors break, you might have to send the whole tool in for repair.
  * **Microservices**: A dedicated toolbox. You have a separate hammer, a separate screwdriver, and a separate pair of pliers. If your hammer breaks, your screwdriver still works perfectly, and you only replace the hammer.
* **Monolith**: 
  * The entire backend application (user authentication, payment processing, database connection, database queries) is written, built, and deployed as **one single codebase**.
  * **Pros**: Simple to build, test, and deploy early on.
  * **Cons**: As the app grows, the codebase becomes massive and slow to build. If a bug crashes the payment module, the *entire* website goes offline.
* **Microservices**:
  * The application is split into small, self-contained programs (services) that each handle *one* job (e.g., Auth Service, Payment Service, Order Service). They communicate with each other over the network (using HTTP requests or message queues).
  * **Pros**: If the payment service goes down, users can still browse products. Teams can work on separate services independently and deploy them whenever they want.
  * **Cons**: Much harder to set up, secure, and debug because messages are constantly traveling across the network.

---

### 2. Synchronous vs. Asynchronous Processing
* **Analogy**:
  * **Synchronous**: Ordering food at a fast-food counter. You place your order, stand there waiting, and the cashier cannot help the next customer until you receive your food and leave.
  * **Asynchronous**: Ordering food, receiving a buzzing pager, and sitting down. The cashier can immediately take the next person's order. When your food is ready, the pager buzzes, and you collect it.
* **Synchronous**:
  * Tasks are executed sequentially (one after the other). The system waits for Task A to finish completely before moving to Task B.
  * **Use Case**: Getting a user's name from a database. It takes milliseconds, and you need the name to display the profile page, so waiting makes sense.
* **Asynchronous**:
  * A task is started, but instead of waiting for it to finish, the system immediately moves to the next task. The slow task runs in the background and notifies the system when it's done.
  * **Use Case**: Sending a welcome email after registration. Sending emails can take 2–3 seconds. Instead of making the user wait, you start the email send task asynchronously, immediately return "Welcome!" to the browser, and let the email send in the background.

---

### 3. RESTful APIs vs. GraphQL
* **REST (Representational State Transfer)**:
  * Uses standard HTTP methods (like `GET` to read, `POST` to create, `PUT` to update, and `DELETE` to remove data).
  * Data is split into clean folders called **endpoints** (e.g., `/users` gives you a list of users, `/users/1` gives you user #1).
  * **The Problem**: If you only want a user's username, a `GET /users/1` request might still return their phone number, home address, and bio (this is called **Over-fetching**). If you want their posts too, you might have to make a second request to `/users/1/posts` (this is called **Under-fetching**).
* **GraphQL**:
  * A query language created by Facebook that exposes **one single endpoint** (usually `/graphql`).
  * The client sends a request describing *exactly* what fields they want.
  * **Example Query**:
    ```graphql
    {
      user(id: 1) {
        username
        posts {
          title
        }
      }
    }
    ```
  * The server returns *only* the username and post titles in a single round-trip.
  * **Comparison Summary**: Use REST for simpler, standard projects. Use GraphQL when you have complex data structures and want mobile or web clients to minimize data usage.

---

### 4. Event-Driven Architecture
* **Concept**: An architectural design where services communicate by reacting to "events" (messages stating that something has happened, e.g., `"OrderPlaced"` or `"UserSignedUp"`).
* **The Flow**:
  1. A service does something and publishes an event to an **Event Broker** (like Kafka or RabbitMQ).
  2. Other services "subscribe" (listen) to that broker. When the event arrives, they automatically trigger their own tasks.
* **Real-World Example (E-commerce Checkout)**:
  * The **Checkout Service** processes a payment and publishes an event: `"OrderPaid"`.
  * The **Inventory Service** hears `"OrderPaid"` and automatically decrements the stock.
  * **Email Service** hears `"OrderPaid"` and sends the receipt email.
  * **Shipping Service** hears `"OrderPaid"` and prints a shipping label.
* **Why it's great**: The Checkout Service doesn't need to know that the Email or Shipping services even exist. If the Shipping Service crashes, the user can still buy things; the Shipping Service will simply process the `"OrderPaid"` events later when it wakes back up.

---

### 5. How to Handle Background Jobs
* **The Problem**: Web servers are designed to respond to users quickly (within 200 milliseconds). If a user requests a heavy task—like resizing 100 images or generating a 50-page PDF report—running it inside the web request will freeze the application or cause a timeout.
* **The Solution (Background Job Queue)**:
  1. **User Request**: The user clicks "Export PDF".
  2. **Enqueue**: The backend server creates a small task packet (e.g., `{"task": "generate_pdf", "userId": 42}`) and pushes it into a **Message Queue** (like Redis or RabbitMQ).
  3. **Immediate Response**: The server tells the user, "We are working on it! We'll email you or update this page when it's done."
  4. **The Workers**: A separate program running in the background (called a **Worker** or **Consumer**) listens to the queue, pulls the task, and spends the next 30 seconds generating the PDF.
* **Popular Tools**: Celery (Python), BullMQ/Sidekiq (NodeJS/Ruby), Hangfire (.NET).

---

### 6. SQL vs. NoSQL Databases
* **SQL (Relational Databases)**:
  * Data is organized into strict **tables** with columns and rows, like Excel spreadsheets.
  * Uses **SQL** (Structured Query Language) to query data.
  * Relationships between tables are strictly enforced (e.g., a post table has a `user_id` pointing to the user table).
  * **When to use**: When your data structure is stable and you need highly reliable transactions (e.g., banking systems, accounting, checkout systems).
  * **Examples**: PostgreSQL, MySQL, SQLite.
* **NoSQL (Non-Relational Databases)**:
  * Data can be stored in many ways: documents (JSON files), key-value pairs, column collections, or graphs.
  * Schema-less: You can save different fields for different items in the same collection.
  * Highly scalable across multiple servers (horizontal scaling).
  * **When to use**: When your data structures change rapidly, or you are handling unstructured data (e.g., user chats, real-time gaming profiles, IoT logs).
  * **Examples**: MongoDB (Documents), Redis (Key-Value), Neo4j (Graphs).

---

### 7. Database Indexing & Performance
* **Analogy**: Think of a physical textbook. If you want to find where "indexes" are mentioned:
  * **Without an Index**: You must flip through the book page-by-page from start to finish. This is called a **Table Scan**.
  * **With an Index**: You flip to the index at the very back, find "indexes" under "I", see it says "pages 45 and 92", and jump straight there.
* **What is an Index?**: 
  * A special lookup table created by the database engine on specific columns (like `email` or `created_at`). It organizes the data in a sorted structure (typically a **B-Tree**) so the database can search it in logarithmic time ($O(\log N)$) instead of linear time ($O(N)$).
* **The Impact**:
  * **Reads (`SELECT`)**: Extremely fast.
  * **Writes (`INSERT`, `UPDATE`, `DELETE`)**: Slower. Why? Every time you add or update data, the database has to update both the main table *and* rebuild parts of the sorted index.
  * **Rule of Thumb**: Only index columns that you use frequently in `WHERE`, `JOIN`, or `ORDER BY` clauses. Do not index columns with highly repetitive data (like boolean flags `true`/`false`).

---

### 8. ACID Properties in Databases
ACID is a checklist of guarantees that ensures database transactions (a bundle of database operations) are safe and reliable, even if the server crashes or loses power.

* **Atomicity (All-or-Nothing)**: 
  * If a transaction has three steps (e.g., 1. Deduct $10 from Account A, 2. Add $10 to Account B, 3. Log the transfer), all three must succeed. If step 3 fails, steps 1 and 2 are rolled back as if nothing ever happened.
* **Consistency**:
  * The transaction must move the database from one valid state to another. For example, if a table has a rule that "balance cannot be negative," any transaction that would make a balance -$5 is rejected.
* **Isolation**:
  * If two users execute transactions at the exact same time, the database runs them in a way that they don't interfere with each other. User B's transaction won't see half-completed changes made by User A.
* **Durability**:
  * Once a transaction is "Committed" (successful), the changes are written to non-volatile storage (the hard drive). Even if the server crashes or the power goes out a millisecond later, the data is safe.

---

### 9. Preventing Deadlocks in Relational Databases
* **What is a Deadlock?**: 
  * Imagine User A locks Row 1 and needs to update Row 2. At the same time, User B locks Row 2 and needs to update Row 1. Both users are frozen forever, waiting for the other to release their lock.
* **Prevention Techniques**:
  1. **Acquire Locks in a Consistent Order**: Always update tables/rows in the exact same order in your code (e.g., always update `users` first, then `profiles`).
  2. **Keep Transactions Short**: Get in, execute your queries, and commit. Never make slow network calls (like calling a payment API) inside a database transaction.
  3. **Use Lower Isolation Levels**: If your app can tolerate it, use isolation levels that lock less data (like `Read Committed` instead of `Serializable`).
  4. **Set Lock Timeouts**: Tell the database: "If I cannot acquire this lock in 3 seconds, fail the transaction and let me retry."

---

### 10. Database Replication
* **Concept**: Copying data in real-time from one database server (called the **Primary** or **Leader**) to one or more other servers (called **Replicas** or **Followers**).
* **Why it's useful**:
  * **High Availability / Disaster Recovery**: If your primary database crashes, you can promote a replica to be the new primary, preventing downtime.
  * **Read Scaling**: In most apps, users read data (views posts) 90% of the time and write data (creates posts) 10% of the time. You can send all writes to the Primary and split all read traffic among multiple Replicas.
  * **Geography**: You can place replicas closer to your users globally to reduce network latency.

---

### 11. Caching & Caching Strategies
* **Concept**: Storing copy-cat versions of slow-to-retrieve data in a super-fast storage area (usually RAM, using tools like Redis) so future requests are answered instantly.
* **Strategies**:
  * **Cache-Aside (Lazy Loading)**:
    1. The app checks the cache.
    2. *Cache Hit*: Data found! Return it immediately.
    3. *Cache Miss*: Data not found. Query the slow database, save the result in the cache for next time, and return it.
  * **Write-Through**:
    * When writing data, the app updates the cache and the database at the exact same time. The cache is always up-to-date, but writes are slightly slower.
  * **Write-Behind (Write-Back)**:
    * The app writes updates only to the cache. The cache later writes to the database in batches. Extremely fast, but if the cache server crashes before saving to disk, you lose data.
* **Cache Eviction (LRU)**: Cache memory is limited. When it's full, the system uses **Least Recently Used (LRU)** to delete the data that hasn't been accessed in the longest time.

---

### 12. Redis vs. Memcached
Both are in-memory, key-value stores used primarily for caching, but they have distinct differences:

| Feature | Redis | Memcached |
| :--- | :--- | :--- |
| **Data Types** | Supports Strings, Lists, Hashes, Sets, and Sorted Sets. | Supports only simple Strings. |
| **Persistence** | Can save data to disk (survives server restarts). | Purely in-memory (loses all data on restart). |
| **Architecture** | Single-threaded (handles concurrency using event loops). | Multi-threaded (great for utilizing multi-core CPUs). |
| **Features** | Includes Pub/Sub, transactions, and script execution. | Simple, straightforward, fast cache. |

* **Winner**: Use **Redis** for 95% of modern projects due to its rich features. Use **Memcached** if you have a simple key-value cache and value size is large.

---

### 13. Optimizing Database Queries
If your website is loading slowly, the database is often the bottleneck. Optimize it using these steps:

1. **Only SELECT what you need**: Avoid `SELECT *`. Instead, write `SELECT id, username`. This saves network bandwidth and memory.
2. **Add Indexes**: Use indexes on columns inside `WHERE` filters, `JOIN` conditions, and `ORDER BY` sorting.
3. **Use pagination**: Never load all records at once. Use `LIMIT 20 OFFSET 0` to load data page-by-page.
4. **Use EXPLAIN**: Write `EXPLAIN` before your SQL query (e.g., `EXPLAIN SELECT ...`). The database will print its execution plan, showing you if it scanned the entire table or used an index.
5. **N+1 Query Avoidance**: If loading 10 posts and their authors, don't run 1 query to get the posts, and then 10 separate queries to get each author. Use a `JOIN` to get them all in a single query.

---

### 14. Rate Limiting & API Security
* **Concept**: Restricting the number of requests a client can make to your server within a certain window (e.g., "max 60 requests per minute").
* **Why it helps**:
  * **Prevents Denial of Service (DoS)**: Stops a malicious bot from hammering your server with millions of requests, which would crash the application.
  * **Protects Login Screens**: Stops hackers from using brute-force programs to test thousands of passwords per second.
  * **Saves Money**: If your API calls paid services (like sending an SMS or using AI), rate limiting stops users from generating huge bills.
* **Algorithms**:
  * *Token Bucket*: Users get a bucket filled with tokens. Every request costs a token. The bucket refuels slowly over time.
  * *Fixed Window*: You get 100 requests every fixed hour (e.g., 12:00 to 1:00).

---

### 15. Scaling a Backend to Millions of Requests
Scaling means designing your system to handle massive growth. We do this by avoiding "Single Points of Failure":

1. **Horizontal Scaling (Scaling Out)**: Instead of buying a bigger server (Vertical Scaling), run multiple small servers side-by-side.
2. **Load Balancer**: Place a load balancer in front of your servers. It takes incoming traffic and distributes it evenly among your app servers.
3. **Stateless Servers**: Ensure app servers do not store user sessions locally. Store sessions in Redis or use JWTs, so any server can handle any request.
4. **Database Read/Write Splitting & Sharding**:
   * Send database writes to a primary database and reads to replicas.
   * **Sharding**: Break large tables into smaller pieces (shards) across different servers (e.g., Users A-M on Server 1, Users N-Z on Server 2).
5. **CDN (Content Delivery Network)**: Cache static files (images, JS, CSS) on servers globally so users load them locally, avoiding your backend.

---

### 16. OAuth vs. JWT vs. Session-Based Authentication
These are methods for identifying who a user is when they make requests:

* **Session-Based (Stateful)**:
  * **How**: The user logs in. The server saves a session ID in its database/memory and sends it to the browser as a cookie. The browser sends this cookie back with every request.
  * **Pros**: Easy to revoke. If a user logs out, you delete the session ID from your database.
  * **Cons**: Hard to scale. If you have 10 servers, they all need access to the same session database.
* **JWT (JSON Web Token - Stateless)**:
  * **How**: The user logs in. The server creates a token containing user data (e.g., `userId: 42`) and signs it using a secret key. The token is sent to the client. The client sends it in the `Authorization` header. The server verifies the token signature mathematically without querying any database.
  * **Pros**: Super fast and highly scalable.
  * **Cons**: Hard to revoke. Once a JWT is issued, it is valid until it expires.
* **OAuth**:
  * **How**: An authorization protocol, not a login system. It allows a third-party app to access data on another site on your behalf without knowing your password (e.g., "Log in with Google" or "Authorize Spotify to access your Discord").

---

### 17. How to Prevent SQL Injection Attacks
* **What is SQL Injection?**: 
  * An attack where a hacker inputs SQL commands into input forms (like search boxes) to trick the database.
  * *Vulnerable code*: 
    ```javascript
    const query = "SELECT * FROM users WHERE email = '" + userInput + "'";
    ```
    If the user enters `' OR '1'='1`, the query becomes `SELECT * FROM users WHERE email = '' OR '1'='1'`. This returns *every* user in the database, bypassing login!
* **Prevention**:
  * **Use Prepared Statements / Parameterized Queries**:
    ```javascript
    const query = "SELECT * FROM users WHERE email = ?";
    ```
    Placeholders (`?`) tell the database engine: "Treat this input strictly as a string literal, not executable code." Even if the input contains SQL commands, they are treated as plain text and cannot run.
  * **Use ORMs**: Tools like Prisma or Hibernate automatically parameterize queries.

---

### 18. CORS (Cross-Origin Resource Sharing)
* **The Problem (Same-Origin Policy)**: 
  * For security, web browsers block scripts running on `websiteA.com` from making requests to `api.websiteB.com` unless `websiteB.com` explicitly permits it. This prevents malicious sites from fetching your personal data from other tabs.
* **What is CORS?**: 
  * A system of HTTP headers that tells browsers: "I trust requests coming from these specific domains."
* **How it works (Preflight)**:
  * For complex requests, the browser sends an automatic `OPTIONS` request (a preflight request) to the server.
  * The server responds with headers like:
    `Access-Control-Allow-Origin: https://myfrontend.com`
  * If the browser sees that the originating site is approved, it sends the actual request. If not, the browser blocks it and throws a CORS error.

---

### 19. Common Security Vulnerabilities & Mitigations
* **XSS (Cross-Site Scripting)**:
  * *Vulnerability*: Attackers inject malicious JavaScript into your site, which runs in other users' browsers (e.g., in a comment section).
  * *Mitigation*: Sanitize and escape all user input before displaying it in HTML. Use a Content Security Policy (CSP) header.
* **CSRF (Cross-Site Request Forgery)**:
  * *Vulnerability*: A malicious website tricks a logged-in user's browser into sending a request to your API (e.g., transferring money) using their cookies.
  * *Mitigation*: Use unique, one-time CSRF tokens on forms, and set cookie properties to `SameSite=Strict` or `Lax`.
* **Broken Object-Level Authorization (BOLA)**:
  * *Vulnerability*: Changing the ID in a URL (like `/api/invoice/100` to `/api/invoice/101`) to view another user's invoice.
  * *Mitigation*: Always check if the currently logged-in user owns the requested resource before returning it.

---

### 20. Secure Password Storage
* **Rule 1: NEVER store passwords in plain text.** If your database is breached, all accounts are compromised.
* **Rule 2: Do NOT use fast hashing algorithms (MD5, SHA-256).** They are designed to run in microseconds. Hackers can use graphics cards (GPUs) to guess billions of hashes per second.
* **The Secure Way**:
  * Use **Adaptive, Slow KDFs** (Key Derivation Functions) like **Bcrypt**, **Argon2id**, or **PBKDF2**. These are intentionally slow to prevent brute-force attacks.
  * **Always use a Salt**: A salt is a random string generated for each user. You attach the salt to the password before hashing: `hash(password + salt)`. 
  * *Why Salting Matters*: If two users use the password `Password123`, they will have completely different hashes. This prevents attackers from using pre-calculated lists of password hashes (Rainbow Tables) to crack them.

---

### 21. Designing a URL Shortener (e.g., Bitly)
* **Goal**: Take a long URL (e.g., `https://amazon.com/item/12345/ref=abc`) and turn it into a short code (e.g., `https://bit.ly/aB9x2`).
* **Core Components**:
  1. **Short Code Generator**: Convert database auto-increment IDs to **Base62** strings (using characters `a-z`, `A-Z`, `0-9`). A 6-character code generates $62^6 \approx 56.8$ billion unique short links.
  2. **Database Schema**: A simple table mapping:
     `short_code (Primary Key) -> long_url -> created_at`
  3. **Redirection (The API)**:
     * When a user visits `/aB9x2`, the backend does a database lookup.
     * It returns an HTTP status code **301 (Moved Permanently)** or **302 (Found)** with a `Location` header pointing to the long URL.
  4. **Performance**: Since 99% of requests are reads (redirections), cache the mappings in Redis.

---

### 22. Designing a Message Queue System
* **Core Concepts**:
  * **Producer**: The app component that creates a message (e.g., "Email this user").
  * **Broker / Queue**: The database/buffer that stores messages in order (FIFO - First In, First Out) on disk or in memory.
  * **Consumer / Worker**: The component that reads messages from the queue and processes them.
* **Important Design Factors**:
  * **Acknowledgments (Ack)**: The queue should not delete a message immediately. It waits for the consumer to send an "Ack" (success). If the consumer crashes before sending the Ack, the queue places the message back in line for another consumer.
  * **Dead Letter Queue (DLQ)**: If a message fails to process multiple times (e.g., bad data), move it to a DLQ so it doesn't block the queue forever (Head-of-line blocking).

---

### 23. Load Balancing
* **Concept**: A load balancer is a reverse proxy that sits in front of your servers and routes incoming client traffic to prevent any single server from becoming overwhelmed.
* **Algorithms**:
  * **Round Robin**: Sends the first request to Server 1, the second to Server 2, and so on.
  * **Least Connections**: Sends traffic to the server currently handling the fewest active requests.
  * **IP Hash**: Determines which server gets the request based on the client's IP address (ensures a user stays on the same server).
* **Types**:
  * **Layer 4 (Transport)**: Routes traffic based on TCP/UDP data (IP addresses and ports). It is fast but cannot inspect HTTP data.
  * **Layer 7 (Application)**: Routes traffic based on HTTP content (URLs, cookies, headers). It allows smart routing (e.g., sending `/videos` to a video-optimized server).

---

### 24. Designing a Distributed File Storage System
* **The Problem**: A single server runs out of disk space quickly. How do you store petabytes of user uploads (images/videos) reliably?
* **Core Components**:
  1. **Metadata Server (Master Node)**: A database that keeps track of files (e.g., "File `cat.jpg` is split into Chunks A, B, and C, which are stored on Server 5, 9, and 12").
  2. **Data Nodes (Chunk Servers)**: Simple servers that store raw binary chunks of files (usually 64MB chunks).
  3. **Replication**: Write each chunk to at least 3 separate Data Nodes in different physical racks. If Server 5 catches fire, the file is safely recovered from Server 9 or 12.
* **Examples**: Google File System (GFS), Amazon S3.

---

### 25. Eventual Consistency vs. Strong Consistency
In a distributed database (where data is copied across multiple servers), keeping data synchronized takes time.

* **Strong Consistency**:
  * When you update data, the write is not complete until *every single node* is updated.
  * **Pros**: Anyone reading from any node will see the absolute latest data immediately.
  * **Cons**: High latency. If one database node is slow or offline, the write fails.
  * **Use Case**: Bank account balances.
* **Eventual Consistency**:
  * When you update data, it writes to one node and returns success. The data then replicates to other nodes in the background.
  * **Pros**: High speed and availability.
  * **Cons**: For a few seconds, User A might see the updated post while User B sees the old one. Eventually, all nodes synchronize.
  * **Use Case**: Social media likes, comment threads.

---

### 26. Unit, Integration, & E2E Testing
* **Unit Tests**:
  * **What**: Testing a single, isolated function in your code (e.g., `calculateTax(price)`).
  * **Speed**: Extremely fast (milliseconds).
  * **Mocking**: You replace external resources (like database calls or APIs) with fake data (mocks) so you are testing *only* the function logic.
* **Integration Tests**:
  * **What**: Testing how multiple components work together (e.g., testing if your `registerUser` function successfully writes to a test database and sends an event).
  * **Speed**: Slower (seconds).
* **End-to-End (E2E) Tests**:
  * **What**: Simulates a real user action. A script opens a browser, clicks the registration button, fills in details, submits, and checks if the welcome screen loads.
  * **Speed**: Very slow and fragile, but validates that the entire system works.

---

### 27. Debugging Memory Leaks
* **What is a Memory Leak?**: 
  * Occurs when your code allocates RAM memory (e.g., creating arrays or objects) but fails to clean it up when it is no longer needed. The RAM usage rises continuously until the server runs out of memory and crashes.
* **How to Debug**:
  1. **Monitor**: Look at memory graphs (APM tools). If you see a "sawtooth" pattern (memory goes up, drops slightly, but overall trends upward), you have a leak.
  2. **Heap Snapshots**: Take a memory snapshot of your running application using a debugger (e.g., Chrome DevTools for NodeJS). Let the app run some tasks, then take a second snapshot.
  3. **Compare**: Compare the snapshots to see which objects grew in number and were not cleared by the Garbage Collector.
  4. **Common Culprits**: Forgotten event listeners, global variables, and open database connections.

---

### 28. Logging & Monitoring
* **Logging (The Past)**:
  * Records events that happened inside the app.
  * **Best Practice**: Use **Structured Logging** (JSON format) instead of plain text, so log aggregation tools can parse and query them.
  * **Levels**: `DEBUG` (diagnostic details), `INFO` (normal events), `WARN` (something unexpected but not a failure), `ERROR` (crashes/failures).
  * **Tools**: Winston, ELK Stack (Elasticsearch, Logstash, Kibana).
* **Monitoring (The Present)**:
  * Tracks the health of your system in real-time.
  * **Metrics**: CPU usage, RAM, HTTP Response Times, and Error Rates.
  * **Tools**: Prometheus (gathers metrics) + Grafana (displays beautiful graphs).
* **Tracing (The Journey)**:
  * Tracking a single request as it jumps across multiple microservices using a unique ID (Trace ID).

---

### 29. Failed Transactions in Distributed Systems
* **The Problem**: In microservices, a transaction might span multiple databases (e.g., payment database and inventory database). If the payment succeeds but inventory updates fail, you cannot run standard SQL rollback because they are on different servers.
* **The Solution (The Saga Pattern)**:
  * A design pattern where a distributed transaction is split into a series of local transactions.
  * If a step fails, the Saga orchestrator triggers **Compensating Transactions** (rollback commands) in reverse order.
  * *Example*:
    1. **Order Service**: Reserve stock (Success).
    2. **Payment Service**: Charge credit card (Fail).
    3. **Order Service (Compensating)**: Release the reserved stock to undo step 1.

---

### 30. Idempotency in APIs
* **Concept**: An API endpoint is **idempotent** if making the same request multiple times has the exact same effect as making it once.
* **Why it matters**:
  * Imagine you are paying for an item. The request is sent, but your internet drops before you get a confirmation. You click "Pay" again. Without idempotency, you get charged twice.
* **How to Implement**:
  1. The client generates a unique ID (e.g., `Idempotency-Key: uuid-123-abc`) and sends it in the request header.
  2. The backend receives the request and checks Redis/Database: "Have we seen `uuid-123-abc`?"
  3. **If Yes**: Do not run the payment again. Return the cached response from the first payment.
  4. **If No**: Run the payment, save the response with the key `uuid-123-abc`, and return the response.
