from aiokafka import AIOKafkaConsumer
from app.models.order_model import OrderCreate, OrderUpdate
from sqlmodel import Session
from app.db_engine import engine
from app import order_pb2


def get_session():
    with Session(engine) as session:
        yield session


# ===========================CONSUMER ADD ORDER - START ====================
async def consume_messages_add_order(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="orders-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            new_order = order_pb2.OrderCreate()
            new_order.ParseFromString(message.value)
            print(f"Consumer Deserialized Order: {new_order}")

            # Add order to DB
            with next(get_session()) as session:
                order = OrderCreate(
                    id=new_order.id,
                    user_id=new_order.user_id,
                    status=new_order.status,
                    total_amount=new_order.total_amount,
                    payment_status=new_order.payment_status,
                    shipping_address=new_order.shipping_address,
                    order_date=new_order.order_date,
                )
                session.add(order)
                session.commit()
                session.refresh(order)
                print(f"Order added: {order}")

    finally:
        await consumer.stop()

# ===========================CONSUMER ADD ORDER - END ====================


# ===========================CONSUMER UPDATE ORDER - START ====================
async def consume_messages_update_order(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="orders-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            order_update = order_pb2.OrderUpdate()
            order_update.ParseFromString(message.value)
            print(f"Consumer Deserialized Order Update: {order_update}")

            # Update the order in the database
            with next(get_session()) as session:
                db_order = session.get(OrderCreate, order_update.id)
                if db_order:
                    if order_update.status:
                        db_order.status = order_update.status
                    if order_update.payment_status:
                        db_order.payment_status = order_update.payment_status
                    db_order.shipping_address = order_update.shipping_address

                    session.add(db_order)
                    session.commit()
                    session.refresh(db_order)
                    print(f"Order updated: {db_order}")
                else:
                    print(f"Order with ID {order_update.id} not found.")

    finally:
        await consumer.stop()

# ===========================CONSUMER UPDATE ORDER - END ====================


# ===========================CONSUMER LIST ORDERS - START ====================
async def consume_messages_list_orders(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="orders-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic {message.topic}")

            # Deserialize the message
            order_list = order_pb2.OrderList()
            order_list.ParseFromString(message.value)
            print(f"Consumer Deserialized Order List: {order_list}")

            # Process each order in the list
            for order_protobuf in order_list.orders:
                print(f"Processing Order: {order_protobuf}")

            
                    

    finally:
        await consumer.stop()

# ===========================CONSUMER LIST ORDERS - END ====================


# ===========================CONSUMER GET ORDER - START ====================
async def consume_message_get_order(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="orders-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            order_protobuf = order_pb2.OrderCreate()
            order_protobuf.ParseFromString(message.value)
            print(f"Consumer Deserialized Order: {order_protobuf}")

            # Here you can process the order item
            print(f"Order Fetched: ID={order_protobuf.id}, Customer_ID={order_protobuf.user_id}, Product_ID={order_protobuf.product_id}, Quantity={order_protobuf.payment_status}, Total_Price={order_protobuf.total_amount},Shipping_Address={order_protobuf.shipping_address},Order_Date={order_protobuf.order_date}")

    finally:
        await consumer.stop()

# ===========================CONSUMER GET ORDER - END ====================


# ===========================CONSUMER DELETE ORDER - START ====================
# async def consume_message_delete_order(topic, bootstrap_servers):
#     consumer = AIOKafkaConsumer(
#         topic,
#         bootstrap_servers=bootstrap_servers,
#         group_id="orders-group",
#     )

#     await consumer.start()
#     try:
#         async for message in consumer:
#             print(f"Received message on topic: {message.topic}")

#             # Deserialize the message
#             order_delete = order_pb2.OrderDelete()
#             print(f"Order Delete: {order_delete}")
            
#             order_delete.ParseFromString(message.value)
#             print(f"Consumer Deserialized Order Delete: {order_delete}")

#             # Delete the order from the database
#             with next(get_session()) as session:
#                 db_order = session.get(OrderCreate, order_delete.id)
#                 if db_order:
#                     session.delete(db_order)
#                     session.commit()
#                     print(f"Order deleted: {db_order.id}")
#                 else:
#                     print(f"Order with ID {order_delete.id} not found.")

#     finally:
#         await consumer.stop()

# ===========================CONSUMER DELETE ORDER - END ====================
