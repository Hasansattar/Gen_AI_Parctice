# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends ,HTTPException
from sqlmodel import Session ,select
from typing import Annotated ,AsyncGenerator
from app.db_engine import create_db_and_tables, engine
from app.models.todo_model import Todo, TodoCreate, TodoUpdate
from app.consumers.todo_consumer  import consume_messages_add ,consume_messages_update , consume_messages_list_todos, consume_message_get_todo,consume_message_delete_todo
from app.producers.todo_producer  import get_kafka_producer
from app import todo_pb2
from aiokafka import AIOKafkaProducer
import asyncio



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables.")
    # loop.run_until_complete(consume_messages('todos', 'broker:19092'))
    task0 = asyncio.create_task(consume_messages_add('todos_add', 'broker:19092'))
    task1 = asyncio.create_task(consume_messages_update('todos_updates', 'broker:19092'))
    task2 = asyncio.create_task(consume_messages_list_todos('todos_list', 'broker:19092'))
    task3 = asyncio.create_task(consume_message_get_todo('todos_get', 'broker:19092'))
    task4 = asyncio.create_task(consume_message_delete_todo('todos_delete', 'broker:19092'))
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

 # ============================ADD TODOS  - START===========================
 # ============================ADD TODOS  - START===========================



@app.post("/todos/", response_model=Todo)
async def add_todo(todo: TodoCreate, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]) -> Todo:
    # todo_dict = {field: getattr(todo, field) for field in todo.dict()}
    # todo_json = json.dumps(todo_dict).encode("utf-8")
    # print("todoJSON:", todo_json)
    # Produce message
    # await producer.send_and_wait("todos", todo_json)
    

    todo_protbuf = todo_pb2.TodoCreate(id=todo.id, title=todo.title, description=todo.description, completed=todo.completed)
    print(f"Todo Protobuf: {todo_protbuf}")
    # Serialize the message to a byte string
    serialized_todo = todo_protbuf.SerializeToString()
    print(f"Serialized data: {serialized_todo}")
    # Produce message
    await producer.send_and_wait("todos_add", serialized_todo)

    # session.add(todo)
    # session.commit()
    # session.refresh(todo)
    return todo


 # ============================ADD TODOS  - END===========================
 # ============================ADD TODOS  - END===========================



# ============================LIST TODOS - START===========================
# ============================LIST TODOS - START===========================


# @app.get("/todos/", response_model=list[Todo])
# def list_todos(session: Annotated[Session, Depends(get_session)]):
#     todos = session.exec(select(TodoCreate)).all()
#     return todos

@app.get("/todos/", response_model=list[Todo])
async def list_todos(session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]) -> list[Todo]:
    todos = session.exec(select(TodoCreate)).all()

    # Prepare message to send to Kafka
    todo_list_message = todo_pb2.TodoList()
    for todo in todos:
        todo_protobuf = todo_list_message.todos.add()  # Add each todo to the protobuf list
        todo_protobuf.id = todo.id
        todo_protobuf.title = todo.title
        todo_protobuf.description = todo.description
        todo_protobuf.completed = todo.completed

    serialized_todo_list = todo_list_message.SerializeToString()
    
    # Produce message to Kafka
    await producer.send_and_wait("todos_list", serialized_todo_list)

    return todos


# ============================LIST TODOS - END===========================
# ============================LIST TODOS - END===========================



 # ============================GET SINGLE TODOS - START===========================
 # ============================GET SINGLE TODOS - START=========================== 


# @app.get("/todos/{todo_id}", response_model=Todo)
# async def get_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):
#     return session.get(TodoCreate, todo_id)
    
    
@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]) -> Todo:
    todo = session.get(TodoCreate, todo_id)
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Prepare message to send to Kafka
    todo_protobuf = todo_pb2.TodoCreate(id=todo.id, title=todo.title, description=todo.description, completed=todo.completed)
    serialized_todo = todo_protobuf.SerializeToString()
    
    # Produce message to Kafka
    await producer.send_and_wait("todos_get", serialized_todo)

    return todo    

 # ============================GET SINGLE TODOS - END===========================
 # ============================GET SINGLE TODOS - END=========================== 
    
 # ============================DELETE TODOS - START===========================
 # ============================DELETE TODOS - START=========================== 
    
# @app.delete("/todos/{todo_id}", response_model=dict)
# async def delete_todo_item(todo_id: int, session: Annotated[Session, Depends(get_session)]):
#      db_todo = session.get(TodoCreate, todo_id)
#      if db_todo:
#         session.delete(db_todo)
#         session.commit()
#         return {"message": "Todo deleted"}
#      return {"message": "Todo not found"}


 
 
@app.delete("/todos/{todo_id}", response_model=dict)
async def delete_todo_item(todo_id: int, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]) -> dict:
    db_todo = session.get(TodoCreate, todo_id)
    if db_todo:
        session.delete(db_todo)
        session.commit()

        # Prepare delete message for Kafka
        todo_delete_message = todo_pb2.TodoDelete(id=todo_id)
        serialized_todo_delete = todo_delete_message.SerializeToString()

        # Produce message to Kafka
        await producer.send_and_wait("todos_delete", serialized_todo_delete)

        return {"message": "Todo deleted"}
    
    raise HTTPException(status_code=404, detail="Todo not found")
 
 
 # ============================DELETE TODOS - END===========================
 # ============================DELETE TODOS - END===========================
 
 
 # ============================LIST TODOS UPDATE - START===========================
 # ============================LIST TODOS UPDATE- START===========================


@app.put("/todos/{todo_id}", response_model=TodoUpdate)
async def update_todo_item(todo_id: int, todo_update: TodoUpdate, session: Annotated[Session, Depends(get_session)],  producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]): 
    # db_todo = session.get(TodoCreate, todo_id)
    # if db_todo:
    #     for key, value in todo_update.dict(exclude_unset=True).items():
    #         setattr(db_todo, key, value)
    #     session.add(db_todo)
    #     session.commit()
    #     session.refresh(db_todo)
    #     return db_todo
    # return None
    # Deserialize the protobuf message
    
    
    
    # Create a TodoUpdate protobuf message
 try: 
    todo_protobuf = todo_pb2.TodoUpdate(id=todo_id)
    
    if todo_update.title:
        todo_protobuf.title = todo_update.title
    if todo_update.description:
        todo_protobuf.description = todo_update.description
    todo_protobuf.completed = todo_update.completed

    # Serialize the protobuf message
    serialized_todo = todo_protobuf.SerializeToString()

    # Produce the message to Kafka topic for updating
    await producer.send_and_wait("todos_updates", serialized_todo)

    return todo_update

 except Exception as e:
        return {"error": f"Failed to produce message: {str(e)}"}
 
 # ============================LIST TODOS UPDATE - END===========================
 # ============================LIST TODOS UPDATE - END===========================

