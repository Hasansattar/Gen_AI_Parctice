from aiokafka import AIOKafkaConsumer
from app.models.user_model import UserCreate, UserUpdate
from sqlmodel import Session
from app.db_engine import engine
from app import user_pb2

def get_session():
    with Session(engine) as session:
        yield session

# ===========================CONSUMER ADD USER - START ====================
async def consume_messages_add_user(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="users-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            new_user = user_pb2.UserCreate()
            new_user.ParseFromString(message.value)
            print(f"Consumer Deserialized User: {new_user}")

            # Add user to DB
            with next(get_session()) as session:
                user = UserCreate(
                    id=new_user.id,
                    username=new_user.username,
                    email=new_user.email,
                    password_hash=new_user.password_hash,
                    phone=new_user.phone,
                    is_active=new_user.is_active,
                    is_verified=new_user.is_verified,
                    role=new_user.role,
                    created_at=new_user.created_at,
                    updated_at=new_user.updated_at,
                 )
                print(f"Before User added: {user}")
                
                
                session.add(user)
                session.commit()
                session.refresh(user)
                print(f"User added: {user}")

    finally:
        await consumer.stop()
# ===========================CONSUMER ADD USER - END ====================

# ===========================CONSUMER UPDATE USER - START ====================
async def consume_messages_update_user(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="users-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            user_update = user_pb2.UserUpdate()
            user_update.ParseFromString(message.value)
            print(f"Consumer Deserialized User Update: {user_update}")

            # Update user in DB
            with next(get_session()) as session:
                db_user = session.get(UserCreate, user_update.id)
                if db_user:
                    if user_update.phone:
                        db_user.phone = user_update.phone
                    if user_update.password_hash:
                        db_user.password_hash = user_update.password_hash
                    if user_update.updated_at:
                        db_user.updated_at = user_update.updated_at
                    

                    session.add(db_user)
                    session.commit()
                    session.refresh(db_user)
                    print(f"User updated: {db_user}")
                else:
                    print(f"User with ID {user_update.id} not found.")
    finally:
        await consumer.stop()
# ===========================CONSUMER UPDATE USER - END ====================

# ===========================CONSUMER GET USER - START ====================
async def consume_message_get_user(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="users-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            user_protobuf = user_pb2.UserCreate()
            user_protobuf.ParseFromString(message.value)
            print(f"Consumer Deserialized User: {user_protobuf}")

            # Fetch user information
            print(f"User Fetched: ID={user_protobuf.id}, Name={user_protobuf.name}, Email={user_protobuf.email}, Address={user_protobuf.address}, Phone={user_protobuf.phone}")

    finally:
        await consumer.stop()
        
# ===========================CONSUMER LIST USERS - START ====================
async def consume_messages_list_users(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="users-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            user_list = user_pb2.UserList()
            user_list.ParseFromString(message.value)
            print(f"Consumer Deserialized User List: {user_list}")

        

    finally:
        await consumer.stop()
# ===========================CONSUMER LIST USERS - END ====================
# ===========================CONSUMER GET USER - END ====================

# # ===========================CONSUMER DELETE USER - START ====================
# async def consume_message_delete_user(topic, bootstrap_servers):
#     consumer = AIOKafkaConsumer(
#         topic,
#         bootstrap_servers=bootstrap_servers,
#         group_id="users-group",
#     )

#     await consumer.start()
#     try:
#         async for message in consumer:
#             print(f"Received message on topic: {message.topic}")

#             # Deserialize the message
#             user_delete = user_pb2.UserDelete()
#             user_delete.ParseFromString(message.value)
#             print(f"Consumer Deserialized User Delete: {user_delete}")

#             # Delete user from DB
#             with next(get_session()) as session:
#                 db_user = session.get(UserCreate, user_delete.id)
#                 if db_user:
#                     session.delete(db_user)
#                     session.commit()
#                     print(f"User deleted: {db_user.id}")
#                 else:
#                     print(f"User with ID {user_delete.id} not found.")

#     finally:
#         await consumer.stop()
# # ===========================CONSUMER DELETE USER - END ====================
