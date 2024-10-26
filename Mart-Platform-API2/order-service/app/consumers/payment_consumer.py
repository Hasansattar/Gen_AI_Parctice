from aiokafka import AIOKafkaConsumer
from app.models.order_model import PaymentCreate, PaymentUpdate ,Payment
from sqlmodel import Session
from app.db_engine import engine
from app import order_pb2


def get_session():
    with Session(engine) as session:
        yield session


# ===========================Consumer Payment add==============

async def consume_messages_add_payment(topic: str, bootstrap_servers: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="payment_group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            print(f"Consumed message: {message.value}")
            # Deserialize and process payment message
            
            
              # Deserialize the message
            new_payment = order_pb2.PaymentCreate()
            new_payment.ParseFromString(message.value)
            print(f"Consumer Deserialized Payment: {new_payment}")
            
            
            # Add Payment to DB
            with next(get_session()) as session:
                payement = PaymentCreate(
                    id=new_payment.id,
                    amount=new_payment.amount,
                    payment_method=new_payment.payment_method,
                    status=new_payment.status,
                    transaction_id=new_payment.transaction_id,
                    order_id=new_payment.order_id,
                )
                session.add(payement)
                session.commit()
                session.refresh(payement)
                print(f"Payment added: {payement}")
    finally:
        await consumer.stop()





# ===========================Consumer Payment get ==============


async def consume_messages_get_payment(topic: str, bootstrap_servers: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="payment_group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            print(f"Consumed message: {message.value}")
            # Deserialize and process payment message
            
            
              # Deserialize the message
            new_payment = order_pb2.Payment()
            new_payment.ParseFromString(message.value)
            print(f"Consumer Deserialized Payment: {new_payment}")
            
            
           
    finally:
        await consumer.stop()




# ===========================Consumer Payment List ==============


async def consume_messages_list_payment(topic: str, bootstrap_servers: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="payment_group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            print(f"Consumed message: {message.value}")
            # Deserialize and process payment message
            
            
              # Deserialize the message
            new_payment = order_pb2.Payment()
            new_payment.ParseFromString(message.value)
            print(f"Consumer Deserialized Payment: {new_payment}")
            
            
           
    finally:
        await consumer.stop()

