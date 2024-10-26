from aiokafka import AIOKafkaConsumer
from app.models.order_model import OrderItemCreate, OrderItemUpdate
from sqlmodel import Session
from app.db_engine import engine
from app import order_pb2


def get_session():
    with Session(engine) as session:
        yield session


# ===========================CONSUMER ADD ORDER ITEM - START ====================
async def consume_messages_add_order_item(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="order-items-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            new_order_item = order_pb2.OrderItemCreate()
            new_order_item.ParseFromString(message.value)
            print(f"Consumer Deserialized Order Item: {new_order_item}")

            # Add order item to DB
            with next(get_session()) as session:
                order_item = OrderItemCreate(
                    id=new_order_item.id,
                    order_id=new_order_item.order_id,
                    product_id=new_order_item.product_id,
                    quantity=new_order_item.quantity,
                    price_per_unit=new_order_item.price_per_unit,
                    total_price=new_order_item.total_price,
                )
                print(f"After Deserialized Order Item: {order_item}")
                session.add(order_item)
                session.commit()
                session.refresh(order_item)
                print(f"Order item added: {order_item}")

    finally:
        await consumer.stop()

# ===========================CONSUMER ADD ORDER ITEM - END ====================


# ===========================CONSUMER UPDATE ORDER ITEM - START ====================
async def consume_messages_update_order_item(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="order-items-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            order_item_update = order_pb2.OrderItemUpdate()
            order_item_update.ParseFromString(message.value)
            print(f"Consumer Deserialized Order Item Update: {order_item_update}")

            # Update the order item in the database
            with next(get_session()) as session:
                db_order_item = session.get(OrderItemCreate, order_item_update.id)
                
                if db_order_item:
                    if order_item_update.quantity:
                        db_order_item.quantity = order_item_update.quantity
                    if order_item_update.price_per_unit:
                        db_order_item.price_per_unit = order_item_update.price_per_unit
                    if order_item_update.total_price:
                        db_order_item.total_price = order_item_update.total_price
                    
                    session.add(db_order_item)
                    session.commit()
                    session.refresh(db_order_item)
                    print(f"Order item updated: {db_order_item}")
                else:
                    print(f"Order item with ID {order_item_update.id} not found.")

    finally:
        await consumer.stop()

# ===========================CONSUMER UPDATE ORDER ITEM - END ====================


# ===========================CONSUMER LIST ORDER ITEMS - START ====================
async def consume_messages_list_order_items(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="order-items-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            order_item_list = order_pb2.OrderItemList()
            order_item_list.ParseFromString(message.value)
            print(f"Consumer Deserialized Order Item List: {order_item_list}")

            # Process each order item in the list
            for order_item_protobuf in order_item_list.items:
             print(f"Processing Order Item: {order_item_protobuf}")

                
    finally:
        await consumer.stop()

# # ===========================CONSUMER LIST ORDER ITEMS - END ====================


# ===========================CONSUMER GET ORDER ITEM - START ====================
async def consume_message_get_order_item(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="order-items-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic {message.topic}")

            # Deserialize the message
            order_item_protobuf = order_pb2.OrderItem()
            order_item_protobuf.ParseFromString(message.value)
            print(f"Consumer Deserialized Order Item: {order_item_protobuf}")

            
    finally:
        await consumer.stop()

# ===========================CONSUMER GET ORDER ITEM - END ====================


# # ===========================CONSUMER DELETE ORDER ITEM - START ====================
# async def consume_message_delete_order_item(topic, bootstrap_servers):
#     consumer = AIOKafkaConsumer(
#         topic,
#         bootstrap_servers=bootstrap_servers,
#         group_id="order-items-group",
#     )

#     await consumer.start()
#     try:
#         async for message in consumer:
#             print(f"Received message on topic {message.topic}")

#             # Deserialize the message
#             order_item_delete = order_item_pb2.OrderItemDelete()
#             order_item_delete.ParseFromString(message.value)
#             print(f"Consumer Deserialized Order Item Delete: {order_item_delete}")

#             # Delete the order item from the database
#             with next(get_session()) as session:
#                 db_order_item = session.get(OrderItemCreate, order_item_delete.id)
#                 if db_order_item:
#                     session.delete(db_order_item)
#                     session.commit()
#                     print(f"Order item deleted: {db_order_item.id}")
#                 else:
#                     print(f"Order item with ID {order_item_delete.id} not found.")

#     finally:
#         await consumer.stop()

# # ===========================CONSUMER DELETE ORDER ITEM - END ====================
