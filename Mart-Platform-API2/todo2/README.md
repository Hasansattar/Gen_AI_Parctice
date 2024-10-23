CRUD implementation for a simple Todo application using FastAPI, Postgres db ,SQLModel, and Kafka. The example will include all the necessary components, such as models, routes, and Kafka integration.


# Folder structure
```python
todo_app/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── db_engine.py
│   ├── settings.py
│   ├── todo_pb2.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── todo_model.py
│   └── consumers/
│       ├── __init__.py
│       └── todo_consumer.py
│   └── producers/
│       ├── __init__.py
│       └── todo_producer.py
├── pyproject.toml

```

# app/main.py

### 1. Imports

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from typing import Annotated, AsyncGenerator
from app.db_engine import create_db_and_tables, engine
from app.models.todo_model import Todo, TodoCreate, TodoUpdate
from app.consumers.todo_consumer import consume_messages
from app.producers.todo_producer import get_kafka_producer
from app import todo_pb2
from aiokafka import AIOKafkaProducer
import asyncio
```
- **contextlib, FastAPI, and SQLModel**: These are necessary for managing asynchronous contexts, web APIs, and database operations.
- **typing.Annotated**: It’s used to annotate dependencies like database sessions and Kafka producers.
- **todo_consumer and todo_producer**: These are custom modules for consuming and producing Kafka messages.
- **todo_pb2**: Protobuf serialization for the Todo model.
- **asyncio**: Used to run asynchronous Kafka message consumption.




### 2. Lifespan Manager

```python
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables.")
    task = asyncio.create_task(consume_messages('todos2', 'broker:19092'))
    create_db_and_tables()
    yield

```
- This function defines an **asynchronous lifespan manager** for the FastAPI app.
- - It **creates database tables** by ``calling create_db_and_tables()``.
- - It **starts a Kafka consumer** by asynchronously running ``consume_messages()`` to listen for messages on the todos2 topic.

- The yield pauses the function, allowing the FastAPI app to run, and everything before yield happens during app startup.
 

### 3. FastAPI App Initialization

```python
app = FastAPI(
    lifespan=lifespan,
    title="Hello World API with DB",
    version="0.0.1",
)


```
- **lifespan**: This FastAPI app uses the lifespan context, making sure that the database is initialized and Kafka consumers are running.
- **title and version**: The metadata for the API.





### 4. Database Session Management

```python
def get_session():
    with Session(engine) as session:
        yield session

```

- This function provides a database session using the SQLModel Session with the engine. It's used by FastAPI's dependency injection system to manage database connections per request.




### 5. Basic Route

```python
@app.get("/")
def read_root():
    return {"Hello": "PanaCloud Todo 2"}

```
- A **simple route** that returns a welcome message. It demonstrates how the FastAPI framework handles basic routes.

### 6. Add Todo (POST)

```python
@app.post("/todos/", response_model=Todo)
async def add_todo(todo: TodoCreate, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]) -> Todo:
    todo_protbuf = todo_pb2.TodoCreate(id=todo.id, title=todo.title, description=todo.description, completed=todo.completed)
    print(f"Todo Protobuf: {todo_protbuf}")
    serialized_todo = todo_protbuf.SerializeToString()
    await producer.send_and_wait("todos2", serialized_todo)

    return todo


```
- `/todos/` **(POST)**: This is an endpoint to **add a new "todo" item**

- -It receives a ``TodoCreate`` object (validated request body), a database session, and a Kafka producer (injected by ``Depends``).
- -It **serializes** the TodoCreate object using **Protocol Buffers** (``todo_pb2.TodoCreate``) and sends the serialized data to the Kafka topic (``todos2``).
- -The **message is produced asynchronously** using ``producer.send_and_wait()``.
- -Finally, it returns the ``todo`` object



### 7. List Todos (GET)

```python
@app.get("/todos/", response_model=list[Todo])
def list_todos(session: Annotated[Session, Depends(get_session)]):
    todos = session.exec(select(TodoCreate)).all()
    return todos

```
``/todos/`` **(GET)**: Fetches all the "todo" items from the database.
- **SQLModel's** ``select`` **query** is used to retrieve all ``TodoCreate`` items.
- It returns the list of todos as the response.



### 8. Get Todo by ID (GET)

```python
@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):
    return session.get(TodoCreate, todo_id)


```
``/todos/{todo_id}`` **(GET)**: Fetches a **specific "todo" item** by its ID.
- It uses the session to query for a ``TodoCreate`` item using the ``session.get()`` method.

### 9. Delete Todo (DELETE)

```python
@app.delete("/todos/{todo_id}", response_model=dict)
async def delete_todo_item(todo_id: int, session: Annotated[Session, Depends(get_session)]):
    db_todo = session.get(TodoCreate, todo_id)
    if db_todo:
        session.delete(db_todo)
        session.commit()
        return {"message": "Todo deleted"}
    return {"message": "Todo not found"}

```

``/todos/{todo_id}`` **(DELETE)**: Deletes a "todo" item by its ID.
- It retrieves the item by ``todo_id``, deletes it if it exists, and commits the transaction.
- Returns a success or failure message.



### 10. Update Todo (PUT)

```python
@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo_item(todo_id: int, todo_update: TodoUpdate, session: Annotated[Session, Depends(get_session)]): 
    db_todo = session.get(TodoCreate, todo_id)
    if db_todo:
        for key, value in todo_update.dict(exclude_unset=True).items():
            setattr(db_todo, key, value)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo
    return None

```

``/todos/{todo_id}`` **(PUT)**: Updates an existing "todo" item.
- Retrieves the "todo" item by ID, updates only the provided fields using the ``todo_update`` object, - and saves the changes to the database.

- If the item is not found, it returns ``None``.



# app/db_engine.py
### 1. Imports

```python
from sqlmodel import SQLModel, create_engine
from app import settings
import time
from sqlalchemy.exc import OperationalError

```

- SQLModel and create_engine are imported from the sqlmodel library, which is used for defining and interacting with SQL databases using Python data classes.
- settings is imported from the app module, which presumably contains configuration details like the database URL.
- time is a standard Python module used for time-related functions, particularly for adding delays in execution.
- OperationalError is imported from sqlalchemy.exc to handle exceptions related to database operations.

### 2. Creating the Database Engine

```python

connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)


engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)


def create_db_and_tables() -> None:
    # SQLModel.metadata.create_all(engine)
    max_retries = 5
    retry_wait = 5  # seconds

    for attempt in range(max_retries):
        try:
            SQLModel.metadata.create_all(engine)
            print("Database connected and tables created.")
            break
        except OperationalError as e:
            print(f"Database connection failed. Attempt {attempt + 1} of {max_retries}. Retrying in {retry_wait} seconds...")
            time.sleep(retry_wait)
    else:
        print("Could not connect to the database after several attempts.")


```

the app/db_engine.py script is responsible for establishing a connection to a PostgreSQL database using SQLModel and creating the necessary tables. It imports required modules, including SQLModel for database interaction, and OperationalError for handling connection-related exceptions. The connection string is constructed from a URL specified in the application's settings, replacing "postgresql" with "postgresql+psycopg" to utilize the psycopg driver. An SQLAlchemy engine is created with this connection string, configuring a connection pool that recycles idle connections after 300 seconds. The create_db_and_tables function attempts to connect to the database and create tables defined in the SQLModel classes. It incorporates a retry mechanism, allowing up to five attempts to establish the connection, with a 5-second wait between attempts. If the table creation is successful, a confirmation message is printed; otherwise, an error message indicates the number of attempts made. If all attempts fail, a final message is printed stating that the connection could not be established. This structure ensures that the application can handle transient database connection issues effectively during startup.


# app/producers/todo_producer.py

### 1. Import the AIOKafkaProducer:

```python
from aiokafka import AIOKafkaProducer

```
This line imports the ``AIOKafkaProducer`` class from the ``aiokafka`` library, which is an asynchronous Kafka client designed to work with Python's ``asyncio`` module. This allows for non-blocking operations when interacting with Kafka.


### 2. Define the get_kafka_producer function:
```python
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
```

- This line defines an asynchronous generator function named ``get_kafka_producer``. The ``async`` keyword indicates that this function will contain asynchronous operations.

- Here, an instance of ``AIOKafkaProducer`` is created, connecting it to a Kafka broker specified by the ``bootstrap_servers`` parameter. In this case, the broker is located at ``broker:19092``. This is the entry point for the Kafka cluster.
- The ``start()`` method is called on the ``producer`` instance, which initializes the connection to the Kafka broker. The ``await`` keyword is used here to wait for the operation to complete asynchronously.
- The ``yield`` statement allows the function to return the ``producer`` instance to the caller while maintaining its state. This is useful for dependency injection, allowing other parts of the application to use the Kafka producer within an asynchronous context.
- The ``finally`` block ensures that the ``stop()`` method is called on the producer when it is no longer needed (e.g., when exiting the context). This safely closes the connection to the Kafka broker and releases any resources held by the producer.




# app/consumers/todo_consumer.py

### 1. Imports:

```python
from aiokafka import AIOKafkaConsumer
from app.models.todo_model import TodoCreate
from sqlmodel import Session
from app.db_engine import engine
from app import todo_pb2

```

- **AIOKafkaConsumer**: An asynchronous Kafka consumer class for consuming messages.
- **TodoCreate**: A model representing a Todo item, which is likely defined elsewhere in the application.
- **Session**: A session management class from SQLModel to interact with the database.
- **engine**: The database engine created in db_engine.py, used to connect to the database.
- **todo_pb2**: A generated protocol buffer module, used for serializing and deserializing messages.

### 2. Session Management:

```python
def get_session():
    with Session(engine) as session:
        yield session

```
- This function creates a new database session using the ``engine``. It uses a context manager (``with`` statement) to ensure that the session is properly closed after use. The ``yield`` keyword allows it to be used as a generator, providing a session object to the caller.


### 3. Message Consumption:
```python
async def consume_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-group",
    )

```

- **consume_messages**: An asynchronous function that consumes messages from a specified Kafka topic.
- **AIOKafkaConsumer**: Initializes the Kafka consumer with the specified topic and bootstrap_servers. The group_id parameter allows Kafka to manage message offsets for consumers in the same group.


### 4. Starting the Consumer:
```python
await consumer.start()
try:
    async for message in consumer:
        print(f"Received message: {message.value.decode()} on topic {message.topic}")

```

- ``await consumer.start()``: Starts the Kafka consumer asynchronously.
- ``async for message in consumer``: Continuously listens for incoming messages. For each message received, it decodes and prints the message value and the topic from which it was received.



### 5. Deserializing the Message:


```python
new_todo = todo_pb2.TodoCreate()
new_todo.ParseFromString(message.value)
print(f"\n\n Consumer Deserialized data: {new_todo}")

```

- ``todo_pb2.TodoCreate()``: Creates a new instance of the TodoCreate protocol buffer message.
- ``ParseFromString``: Deserializes the message data from a byte string into the new_todo object.
The deserialized data is printed for debugging.

### 6. Adding to the Database:

```python
with next(get_session()) as session:
    todo = TodoCreate(id=new_todo.id, title=new_todo.title, description=new_todo.description, completed=new_todo.completed)
    session.add(todo)
    session.commit()
    session.refresh(todo)

```


- A new session is created to interact with the database.
- A new ``TodoCreate`` instance is created with the data from ``new_todo``.
- The new Todo item is added to the session and committed to the database, ensuring it is saved. The ``session.refresh(todo)`` call updates the ``todo`` instance with any changes made by the database (such as auto-generated fields).



### Closing the Consumer:

```python
finally:
    await consumer.stop()

```
- The ``finally`` block ensures that the consumer is stopped gracefully, releasing any resources it may be holding.


# app/models/todo_model.py

### 1. Imports:


```python
from sqlmodel import SQLModel, Field
from typing import Optional

```

- **SQLModel**: A class that serves as the base for defining SQLAlchemy models with Pydantic-like features.
- **Field**: A function that allows you to define the properties of model fields, including validation and constraints.
- **Optional**: A type hint that indicates a field can be of a specified type or None.



### 2. Base Class for Todo:

```python
class TodoBase(SQLModel):
    title: str = Field(..., max_length=100)
    description: str = Field(default=None, max_length=255)
    completed: bool = Field(default=False)

```

**TodoBase**: This is a base model class that defines common fields for the Todo items.

- **title**: A required field (indicated by ``...``) with a maximum length of 100 characters.
- **description**: An optional field with a default value of ``None`` and a maximum length of 255 characters.
- **completed**: A boolean field that defaults to ``False``, indicating whether the Todo item has been completed.


### 3. Todo Creation Model:

```python
class TodoCreate(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

```

 **TodoCreate**: This model is used for creating new Todo items and is marked as a database table (**table=True**).
- **id**: An optional integer field that serves as the primary key. It defaults to None and is automatically generated by the database when a new record is created.



### 4. Todo Model:

```python
class Todo(TodoBase):
    id: Optional[int] = Field(default=None, primary_key=True)

```


**Todo**: This model represents a Todo item in the database.
- Inherits from ``TodoBase``, meaning it has all the fields defined there.
- Includes an ``id`` field that serves as the primary key, similar to ``TodoCreate``.


### 5. Todo Update Model:

```python
class TodoUpdate(TodoBase):
    pass

```
- **TodoUpdate**: This model is used for updating existing Todo items. It inherits from TodoBase, meaning it will have all the fields defined there but does not add any new fields or change existing ones.






# Prototype Methods

1- we have already proto compiler into running container.
2- go inside the container : docker exec -it <container-name> /bin/bash
3- go to todo.proto file
4- Run this command check version: ``protoc --version``
4- Run this command for compile the file: `protoc --python_out=. todo.proto`



### Browser
http://localhost:8003/docs




# Commmands


### 1. Check the Container Logs
Use the following command to check the logs of the services running on ports that don't show the website:


```bash
docker-compose logs <service_name>

```
For example:
```bash
docker-compose logs todo-service
docker-compose logs api

```
This will help identify if there's an error in the service startup or if the application is throwing an error.
