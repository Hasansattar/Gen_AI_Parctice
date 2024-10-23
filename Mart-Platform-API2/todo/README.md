This code is a full-stack FastAPI app with Kafka integration, SQLModel for the database, and Protocol Buffers for serialization, allowing you to produce and consume todos with Kafka and manage them in a PostgreSQL database.


### 1. Imports

```python
from contextlib import asynccontextmanager
from typing import Union, Optional, Annotated
from app import settings
from sqlmodel import Field, Session, SQLModel, create_engine, select, Sequence
from fastapi import FastAPI, Depends
from typing import AsyncGenerator
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json
from app import todo_pb2

```
**Standard Python libraries:**

- **`contextlib.asynccontextmanager`**: Manages asynchronous context, useful for lifespan events in FastAPI.
- **`typing`**: Provides type hints for more readable and maintainable code.
- **`asyncio`**: Handles asynchronous operations, which are important for non-blocking I/O, such as Kafka messaging.
- **`json`**: Used for JSON serialization and deserialization.

**FastAPI:**

- **`FastAPI`**: Main framework for building the API.
- **`Depends`**: A way to define dependencies in FastAPI.

**SQLModel:**

- **`SQLModel`**: A SQL ORM library that simplifies working with SQL databases in Python.
- **`Field`**: Used to define table columns.
- **`Session`**: Represents a database session.
- **`create_engine`**: Creates a database engine for SQL connections.
- **`select`**: Used for querying the database.

**Kafka:**
- **`IOKafkaProducer`**, **`AIOKafkaConsumer`**: Async Kafka client libraries used for producing and consuming messages.

**Protocol Buffers (Protobuf):**

- **`todo_pb2`**: A file generated by the protobuf compiler, defining the schema for **``Todo``** messages used for serialization.

### 2. Todo Model

```python
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(index=True)

```
**Todo class:** Defines a database table using SQLModel
- **`id`**: Optional primary key for the ``Todo`` entry.
- **`content`**: The main content of the todo item, which is indexed for faster queries.


### 3. Database Setup

```python
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)

```

- **`Database Connection String`**: This replaces the default ``postgresql`` scheme with ``postgresql+psycopg`` (required for using the ``psycopg3`` driver).
- **`create_engine`**: Creates a connection to the database, with ``pool_recycle=300`` ensuring connections are recycled every 5 minutes.



### 4. Create Database Tables

```python
def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

```

- **``create_db_and_tables``**: A utility function that creates the database tables based on the SQLModel definitions (``Todo`` table in this case).




### 5. Kafka Consumer

```python
async def consume_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-group",
    )
    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message: {message.value.decode()} on topic {message.topic}")

            new_todo = todo_pb2.Todo()
            new_todo.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_todo}")

            with next(get_session()) as session:
                todo = Todo(id=new_todo.id, content=new_todo.content)
                session.add(todo)
                session.commit()
                session.refresh(todo)
    finally:
        await consumer.stop()

```
**consume_messages**: Consumes messages from Kafka

- Uses the ``AIOKafkaConsumer`` class to consume messages from a Kafka topic.
- **`message.value.decode()`**: Deserializes the message (from Protobuf).
- **`Deserialization`**: Converts Kafka message bytes into a Protobuf Todo object using ParseFromString().
- Stores the ``Todo`` in the database using SQLModel.


### 6. FastAPI Lifespan

```python
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables.")
    task = asyncio.create_task(consume_messages('todos2', 'broker:19092'))
    create_db_and_tables()
    yield

```
**lifespan**: FastAPI's lifespan event runs tasks at the startup and cleanup phases of the application.

- Starts consuming messages from Kafka in a background task (``consume_messages``).
- Creates database tables by calling ``create_db_and_tables``.




### 7. Initialize FastAPI App

```python
app = FastAPI(
    lifespan=lifespan,
    title="Hello World API with DB",
    version="0.0.1",
)

```
- **`FastAPI instance`**: Configures FastAPI with custom lifespan management, a title, and versioning.



### 8. Database Session Dependency

```python
def get_session():
    with Session(engine) as session:
        yield session

```
- **`get_session`**: Provides a database session to be used in FastAPI routes.



### 9. Basic Route

```python
@app.get("/")
def read_root():
    return {"Hello": "PanaCloud"}

```

- **`Root Route`**: A simple API endpoint that returns a greeting.




### 10. Kafka Producer Dependency

```python
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

```

- **`get_kafka_producer`**: Creates a Kafka producer, starts it, yields it to the caller, and stops it after use.




### 11. Create Todo Endpoint

```python
@app.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]) -> Todo:
    todo_protbuf = todo_pb2.Todo(id=todo.id, content=todo.content)
    serialized_todo = todo_protbuf.SerializeToString()
    await producer.send_and_wait("todos2", serialized_todo)
    return todo

```
**`create_todo`**

- Takes in a ``Todo`` object, database session, and Kafka producer as dependencies.
- Converts the ``Todo`` into a Protobuf message (``SerializeToString``).
- Sends the serialized ``Todo`` to a Kafka topic.



### 12. Read Todos Endpoint

```python
@app.get("/todos/", response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)]):
    todos = session.exec(select(Todo)).all()
    return todos

```

**`read_todos`**
- Fetches all todos from the database using a SQL query (``select(Todo)``).
- Returns the list of todos as the response.


# Summary 
The provided code is a FastAPI application that integrates Kafka messaging, PostgreSQL using SQLModel, and Protocol Buffers (Protobuf) for efficient serialization. It defines a Todo model to represent todo items stored in the database. During application startup, it creates the necessary database tables and starts a Kafka consumer that listens for messages on a specified topic. Messages are deserialized from Protobuf and stored in the database. The app includes a POST endpoint to create new todo items, which are serialized into Protobuf format and sent to a Kafka topic, as well as a GET endpoint to retrieve all todos from the database. The use of asynchronous Kafka producers and consumers ensures non-blocking communication between the API, the database, and the messaging system.






### Browser
http://localhost:8003/docs



