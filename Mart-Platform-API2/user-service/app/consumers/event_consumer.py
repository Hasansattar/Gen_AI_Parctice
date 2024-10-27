from aiokafka import AIOKafkaConsumer
from app.models.user_model import UserEvent
from sqlmodel import Session
from app.db_engine import engine
from app import user_pb2

def get_session():
    with Session(engine) as session:
        yield session

# ===========================CONSUMER USER EVENT ADD - START ====================
async def consume_messages_add_user_event(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="users-event-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            new_user_event = user_pb2.UserEvent()
            new_user_event.ParseFromString(message.value)
            print(f"Consumer Deserialized User Event: {new_user_event}")

            # Add user to DB
            with next(get_session()) as session:
             event = UserEvent(
                    id=new_user_event.id,
                    event_type=new_user_event.event_type,
                    event_payload=new_user_event.event_payload,
                    timestamp=new_user_event.timestamp,
                    user_id=new_user_event.user_id,
                 )
                # print(f"Before User Event added: {event}")
                
                
             session.add(event)
             session.commit()
             session.refresh(event)
             print(f"User Event added: {event}")

    finally:
        await consumer.stop()
# ===========================CONSUMER USER EVENT ADD - END ====================




# ===========================CONSUMER USER EVENT GET - START ====================
async def consume_messages_get_user_event(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="users-event-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            new_user_event = user_pb2.UserEvent()
            new_user_event.ParseFromString(message.value)
            print(f"Consumer Deserialized User Event: {new_user_event}")

          

    finally:
        await consumer.stop()
# ===========================CONSUMER USER EVENT GET - END ====================
