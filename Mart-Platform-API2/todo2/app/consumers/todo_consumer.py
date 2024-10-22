# app/consumers/todo_consumer.py
from aiokafka import AIOKafkaConsumer
from app.models.todo_model import Todo
from sqlmodel import Session
from app.db_engine import engine
from app import todo_pb2



def get_session():
    with Session(engine) as session:
        yield session



async def consume_messages(topic, bootstrap_servers):
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

            new_todo = todo_pb2.Todo()
            new_todo.ParseFromString(message.value)
            print(f"\n\n Consumer Deserialized data: {new_todo}")

            # # Add todo to DB
            with next(get_session()) as session:
                todo = Todo(id=new_todo.id, content=new_todo.content)
                session.add(todo)
                session.commit()
                session.refresh(todo)

            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()

