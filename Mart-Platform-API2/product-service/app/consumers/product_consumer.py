from aiokafka import AIOKafkaConsumer
from app.models.product_model import ProductCreate, ProductUpdate
from sqlmodel import Session
from app.db_engine import engine
from app import product_pb2


def get_session():
    with Session(engine) as session:
        yield session


# ===========================CONSUMER ADD PRODUCT - START ====================
async def consume_messages_add_product(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="productss-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            new_product = product_pb2.ProductCreate()
            new_product.ParseFromString(message.value)
            print(f"Consumer Deserialized Product: {new_product}")

            # Add product to DB
            with next(get_session()) as session:
                product = ProductCreate(
                    id=new_product.id,
                    name=new_product.name,
                    description=new_product.description,
                    price=new_product.price,
                    category_id=new_product.category_id,
                    stock_quantity=new_product.stock_quantity,
                    image_id=new_product.image_id
                )
                session.add(product)
                session.commit()
                session.refresh(product)
                print(f"Product added: {product}")

    finally:
        await consumer.stop()

# ===========================CONSUMER ADD PRODUCT - END ====================


# ===========================CONSUMER UPDATE PRODUCT - START ====================
async def consume_messages_update_product(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="product-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            product_update = product_pb2.ProductUpdate()
            product_update.ParseFromString(message.value)
            print(f"Consumer Deserialized Product Update: {product_update}")

            # Update the product in the database
            with next(get_session()) as session:
                db_product = session.get(ProductCreate, product_update.id)
                if db_product:
                    if product_update.name:
                        db_product.name = product_update.name
                    if product_update.description:
                        db_product.description = product_update.description
                    db_product.price = product_update.price
                    db_product.stock_quantity = product_update.stock_quantity
                    db_product.category_id = product_update.category_id
                    db_product.image_id = product_update.image_id
                    
                    session.add(db_product)
                    session.commit()
                    session.refresh(db_product)
                    print(f"Product updated: {db_product}")
                else:
                    print(f"Product with ID {product_update.id} not found.")

    finally:
        await consumer.stop()

# ===========================CONSUMER UPDATE PRODUCT - END ====================


# ===========================CONSUMER LIST PRODUCTS - START ====================
async def consume_messages_list_products(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="product-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic {message.topic}")

            # Deserialize the message
            product_list = product_pb2.ProductList()
            product_list.ParseFromString(message.value)
            print(f"Consumer Deserialized Product List: {product_list}")

            # Process each product in the list
            for product_protobuf in product_list.products:
                print(f"Processing Product: {product_protobuf}")

                # Example: add each product to the database if needed
                with next(get_session()) as session:
                    product = ProductCreate(
                        id=product_protobuf.id,
                        name=product_protobuf.name,
                        description=product_protobuf.description,
                        price=product_protobuf.price,
                        category_id=product_protobuf.category_id,
                        stock_quantity=product_protobuf.stock_quantity,
                        image_id=product_protobuf.image_id
                    )
                    session.add(product)
                    session.commit()
                    session.refresh(product)
                    print(f"Product added: {product}")

    finally:
        await consumer.stop()

# ===========================CONSUMER LIST PRODUCTS - END ====================


# ===========================CONSUMER GET PRODUCT - START ====================
async def consume_message_get_product(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="product-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic {message.topic}")

            # Deserialize the message
            product_protobuf = product_pb2.ProductCreate()
            product_protobuf.ParseFromString(message.value)
            print(f"Consumer Deserialized Product: {product_protobuf}")

            # Here you can process the product item
            print(f"Product Fetched: ID={product_protobuf.id}, Name={product_protobuf.name}, Description={product_protobuf.description}, Price={product_protobuf.price}, Stock_Quantity={product_protobuf.stock_quantity}")

    finally:
        await consumer.stop()

# ===========================CONSUMER GET PRODUCT - END ====================


# ===========================CONSUMER DELETE PRODUCT - START ====================
async def consume_message_delete_product(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="product-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            product_delete = product_pb2.ProductDelete()
            product_delete.ParseFromString(message.value)
            print(f"Consumer Deserialized Product Delete: {product_delete}")

            # Delete the product from the database
            with next(get_session()) as session:
                db_product = session.get(ProductCreate, product_delete.id)
                if db_product:
                    session.delete(db_product)
                    session.commit()
                    print(f"Product deleted: {db_product.id}")
                else:
                    print(f"Product with ID {product_delete.id} not found.")

    finally:
        await consumer.stop()

# ===========================CONSUMER DELETE PRODUCT - END ====================



