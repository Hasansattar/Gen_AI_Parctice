from aiokafka import AIOKafkaConsumer
from app.models.product_model import CategoryCreate, CategoryUpdate
from sqlmodel import Session
from app.db_engine import engine
from app import category_pb2  # Assuming you have a protobuf for Category


def get_session():
    with Session(engine) as session:
        yield session

# ===========================CONSUMER ADD CATEGORY - START ====================
async def consume_messages_add_category(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="category-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            new_category = category_pb2.CategoryCreate()
            new_category.ParseFromString(message.value)
            print(f"Consumer Deserialized Category: {new_category}")

            # Add category to DB
            with next(get_session()) as session:
                category = CategoryCreate(
                    id=new_category.id,
                    name=new_category.name,
                    description=new_category.description,
                )
                session.add(category)
                session.commit()
                session.refresh(category)
                print(f"Category added: {category}")

    finally:
        await consumer.stop()
# ===========================CONSUMER ADD CATEGORY - END ====================


# ===========================CONSUMER UPDATE CATEGORY - START ====================
async def consume_messages_update_category(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="category-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            category_update = category_pb2.CategoryUpdate()
            category_update.ParseFromString(message.value)
            print(f"Consumer Deserialized Category Update: {category_update}")

            # Update the category in the database
            with next(get_session()) as session:
                db_category = session.get(CategoryCreate, category_update.id)
                if db_category:
                    if category_update.name:
                        db_category.name = category_update.name
                    if category_update.description:
                        db_category.description = category_update.description
                    
                    session.add(db_category)
                    session.commit()
                    session.refresh(db_category)
                    print(f"Category updated: {db_category}")
                else:
                    print(f"Category with ID {category_update.id} not found.")

    finally:
        await consumer.stop()
# ===========================CONSUMER UPDATE CATEGORY - END ====================


# ===========================CONSUMER DELETE CATEGORY - START ====================
async def consume_message_delete_category(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="category-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            category_delete = category_pb2.CategoryDelete()
            category_delete.ParseFromString(message.value)
            print(f"Consumer Deserialized Category Delete: {category_delete}")

            # Delete the category from the database
            with next(get_session()) as session:
                db_category = session.get(CategoryCreate, category_delete.id)
                if db_category:
                    session.delete(db_category)
                    session.commit()
                    print(f"Category deleted: {db_category.id}")
                else:
                    print(f"Category with ID {category_delete.id} not found.")

    finally:
        await consumer.stop()
# ===========================CONSUMER DELETE CATEGORY - END ====================


# ===========================CONSUMER LIST CATEGORIES - START ====================
async def consume_messages_list_categories(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="category-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic {message.topic}")

            # Deserialize the message
            category_list = category_pb2.CategoryList()
            category_list.ParseFromString(message.value)
            print(f"Consumer Deserialized Category List: {category_list}")

            # Process each category in the list
            for category_protobuf in category_list.categories:
                print(f"Processing Category: {category_protobuf}")

                # Example: add each category to the database if needed
                with next(get_session()) as session:
                    category = CategoryCreate(
                        id=category_protobuf.id,
                        name=category_protobuf.name,
                        description=category_protobuf.description,
                    )
                    session.add(category)
                    session.commit()
                    session.refresh(category)
                    print(f"Category added: {category}")

    finally:
        await consumer.stop()
# ===========================CONSUMER LIST CATEGORIES - END ====================



# ===========================CONSUMER GET CATEGORY - START ====================
async def consume_message_get_category(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="category-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic {message.topic}")

            # Deserialize the message
            category_protobuf = category_pb2.CategoryCreate()
            category_protobuf.ParseFromString(message.value)
            print(f"Consumer Deserialized Category: {category_protobuf}")

            # Here you can process the category item
            print(f"Category Fetched: ID={category_protobuf.id}, Name={category_protobuf.name}, Description={category_protobuf.description}")

    finally:
        await consumer.stop()

# ===========================CONSUMER GET CATEGORY - END ====================


