# app/consumers/todo_consumer.py
from aiokafka import AIOKafkaConsumer
from app.models.todo_model import TodoCreate
from sqlmodel import Session
from app.db_engine import engine
from app import todo_pb2



def get_session():
    with Session(engine) as session:
        yield session


# ===========================CONSUMER ADD TODOS - START ====================
# ===========================CONSUMER ADD TODOS - START ====================



async def consume_messages_add(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-group",
    )

    # Start the consumer.
    await consumer.start()
    try:
            
        # Continuously listen for messages.
        async for message in consumer:
            print(f"Received message: {
                  message.value.decode()} on topic {message.topic}")

            new_todo = todo_pb2.TodoCreate()
            new_todo.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_todo}")

            # # Add todo to DB
            with next(get_session()) as session:
                todo = TodoCreate(id=new_todo.id, title=new_todo.title,description=new_todo.description,completed=new_todo.completed)
                session.add(todo)
                session.commit()
                session.refresh(todo)

            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()


# ===========================CONSUMER ADD TODOS - END ====================
# ===========================CONSUMER ADD TODOS - END ====================


# ===========================CONSUMER UPDATE TODOS - START ====================
# ===========================CONSUMER UPDATE TODOS - START ====================


async def consume_messages_update(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-group",
    )

    await consumer.start()
    try:
        
        async for message in consumer:
            print(f"Received message: {message.value.decode()} on topic {message.topic}")

            # Deserialize the message
            todo_update = todo_pb2.TodoUpdate()
            todo_update.ParseFromString(message.value)
            
            print(f"\n\n Consumer Deserialized Update data: {todo_update}")

            # Update the Todo in the database
            with next(get_session()) as session:
                db_todo = session.get(TodoCreate, todo_update.id)
                if db_todo:
                    if todo_update.title:
                        db_todo.title = todo_update.title
                    if todo_update.description:
                        db_todo.description = todo_update.description
                    db_todo.completed = todo_update.completed

                    session.add(db_todo)
                    session.commit()
                    session.refresh(db_todo)
                    print(f"Todo updated: {db_todo}")
                else:
                    print(f"Todo with ID {todo_update.id} not found.")

    finally:
        await consumer.stop()
        
        
     
  
# ===========================CONSUMER UPDATE TODOS - END ====================
# ===========================CONSUMER UPDATE TODOS - END ====================
      
      
# ===========================CONSUMER LIST TODOS - START ====================
# ===========================CONSUMER LIST TODOS - START ====================
      
    

async def consume_messages_list_todos(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic {message.topic}")

            # Deserialize the message
            todo_list = todo_pb2.TodoList()
            todo_list.ParseFromString(message.value)

            print(f"Consumer Deserialized Todo List: {todo_list}")

            # Process each todo in the list
            for todo_protobuf in todo_list.todos:
                print(f"Processing Todo: {todo_protobuf}")

                # Example: add each todo to the database if needed
                with next(get_session()) as session:
                    todo = TodoCreate(id=todo_protobuf.id, title=todo_protobuf.title, description=todo_protobuf.description, completed=todo_protobuf.completed)
                    session.add(todo)
                    session.commit()
                    session.refresh(todo)
                    print(f"Todo added: {todo}")

    finally:
        await consumer.stop()
        
       
       
# ===========================CONSUMER LIST TODOS - END ====================
# ===========================CONSUMER LIST TODOS - END ====================
       
       
        

# ===========================CONSUMER GET TODOS - START ====================
# ===========================CONSUMER GET TODOS - START ====================
        
        
async def consume_message_get_todo(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic {message.topic}")

            # Deserialize the message
            todo_protobuf = todo_pb2.TodoCreate()
            todo_protobuf.ParseFromString(message.value)

            print(f"Consumer Deserialized Todo: {todo_protobuf}")

            # Here you can process the todo item (e.g., log it, update something, etc.)
            print(f"Todo Fetched: ID={todo_protobuf.id}, Title={todo_protobuf.title}, Description={todo_protobuf.description}, Completed={todo_protobuf.completed}")

    finally:
        await consumer.stop()
        
  
  
# ===========================CONSUMER GET TODOS - END ====================
# ===========================CONSUMER GET TODOS - END ====================
     
  
  
# ===========================CONSUMER DELETE TODOS - START ====================
# ===========================CONSUMER DELETE TODOS - START ====================
     
  
        
async def consume_message_delete_todo(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic {message.topic}")

            # Deserialize the message
            todo_delete = todo_pb2.TodoDelete()
            todo_delete.ParseFromString(message.value)

            print(f"Consumer Deserialized Todo Delete: {todo_delete}")

            # Delete the todo from the database
            with next(get_session()) as session:
                db_todo = session.get(TodoCreate, todo_delete.id)
                if db_todo:
                    session.delete(db_todo)
                    session.commit()
                    print(f"Todo deleted: {db_todo.id}")
                else:
                    print(f"Todo with ID {todo_delete.id} not found.")

    finally:
        await consumer.stop()
  
# ===========================CONSUMER DELETE TODOS - END ====================
# ===========================CONSUMER DELETE TODOS - END ====================
           