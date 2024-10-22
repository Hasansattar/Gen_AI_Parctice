# app/main.py
from fastapi import FastAPI, Depends
from sqlmodel import Session ,select
from typing import Annotated ,AsyncGenerator
from app.db_engine import create_db_and_tables, engine
from app.models.todo_model import Todo
#  , TodoCreate, TodoUpdate
# from app.crud.todo_crud import create_todo, get_all_todos, get_todo_by_id, update_todo, delete_todo
from fastapi import FastAPI, Depends
import asyncio
from contextlib import asynccontextmanager
from app.consumers.todo_consumer  import consume_messages 
from app.producers.todo_producer  import get_kafka_producer
from app import todo_pb2

from aiokafka import AIOKafkaProducer
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     create_db_and_tables()
#     yield
    
# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
#     print("Creating tables.")
#     # loop.run_until_complete(consume_messages('todos', 'broker:19092'))
#     task = asyncio.create_task(consume_todo_messages('todos3', 'broker:19092'))
#     create_db_and_tables()
#     yield    
    

# app = FastAPI(lifespan=lifespan)


# # Add a dependency for database session
# def get_session() -> Session:
#     with Session(engine) as session:
#         yield session
        
        
# @app.get("/")
# def read_root():
#     return {"Hello": "PanaCloud Todo 2"}


# @app.post("/todos/", response_model=Todo)
# async def add_todo(todo: TodoCreate, session: Annotated[Session, Depends(get_session)]):
#     return create_todo(todo, session)

# @app.get("/todos/", response_model=list[Todo])
# async def list_todos(session: Annotated[Session, Depends(get_session)]):
#     return get_all_todos(session)

# @app.get("/todos/{todo_id}", response_model=Todo)
# async def get_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):
#     todo = get_todo_by_id(todo_id, session)
#     if todo:
#         return todo
#     raise HTTPException(status_code=404, detail="Todo not found")

# @app.put("/todos/{todo_id}", response_model=Todo)
# async def update_todo_item(todo_id: int, todo_update: TodoUpdate, session: Annotated[Session, Depends(get_session)]):
#     updated_todo = update_todo(todo_id, todo_update, session)
#     if updated_todo:
#         return updated_todo
#     raise HTTPException(status_code=404, detail="Todo not found")

# @app.delete("/todos/{todo_id}", response_model=dict)
# async def delete_todo_item(todo_id: int, session: Annotated[Session, Depends(get_session)]):
#     return delete_todo(todo_id, session)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables.")
    # loop.run_until_complete(consume_messages('todos', 'broker:19092'))
    task = asyncio.create_task(consume_messages('todos2', 'broker:19092'))
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Hello World API with DB",
    version="0.0.1",
     
)

def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def read_root():
    return {"Hello": "PanaCloud Todo 2"}

# Kafka Producer as a dependency        



@app.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]) -> Todo:
    # todo_dict = {field: getattr(todo, field) for field in todo.dict()}
    # todo_json = json.dumps(todo_dict).encode("utf-8")
    # print("todoJSON:", todo_json)
    # Produce message
    # await producer.send_and_wait("todos", todo_json)

    todo_protbuf = todo_pb2.Todo(id=todo.id, content=todo.content)
    print(f"Todo Protobuf: {todo_protbuf}")
    # Serialize the message to a byte string
    serialized_todo = todo_protbuf.SerializeToString()
    print(f"Serialized data: {serialized_todo}")
    # Produce message
    await producer.send_and_wait("todos2", serialized_todo)

    # session.add(todo)
    # session.commit()
    # session.refresh(todo)
    return todo


@app.get("/todos/", response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)]):
    todos = session.exec(select(Todo)).all()
    return todos