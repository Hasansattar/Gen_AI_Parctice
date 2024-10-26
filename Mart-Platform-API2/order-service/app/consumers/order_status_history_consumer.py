from aiokafka import AIOKafkaConsumer
from app.models.order_model import OrderStatusHistory,OrderStatusHistoryCreate
from sqlmodel import Session
from app.db_engine import engine
from app import order_pb2


def get_session():
    with Session(engine) as session:
        yield session
        
        
        # ===========================CONSUMER ADD ORDER HISTORY - START ====================
async def consume_messages_add_order_history_status(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="orders-history-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            new_order_history = order_pb2.OrderStatusHistoryCreate()
            new_order_history.ParseFromString(message.value)
            print(f"Consumer Deserialized Order: {new_order_history}")

            # Add order to DB
            with next(get_session()) as session:
                order_history = OrderStatusHistoryCreate(
                    id=new_order_history.id,
                    order_id=new_order_history.order_id,
                    status=new_order_history.status,
                    timestamp=new_order_history.timestamp,
              
                )
                session.add(order_history)
                session.commit()
                session.refresh(order_history)
                print(f"Order History added: {order_history}")

    finally:
        await consumer.stop()

# ===========================CONSUMER ADD ORDER HISTORY - END ====================




        # ===========================CONSUMER ADD ORDER HISTORY - START ====================
async def consume_messages_get_list_order_history_status(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="orders-history-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            new_order_history = order_pb2.OrderStatusHistory()
            new_order_history.ParseFromString(message.value)
            print(f"Consumer Deserialized Order: {new_order_history}")

            

    finally:
        await consumer.stop()

# ===========================CONSUMER ADD ORDER HISTORY - END ====================
