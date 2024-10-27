from aiokafka import AIOKafkaConsumer
from app.models.user_model import UserProfile
from sqlmodel import Session
from app.db_engine import engine
from app import user_pb2

def get_session():
    with Session(engine) as session:
        yield session

# ===========================CONSUMER USER PROFILE ADD - START ====================
async def consume_messages_add_user_profile(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="users-profile-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            new_user_profile = user_pb2.UserProfile()
            new_user_profile.ParseFromString(message.value)
            print(f"Consumer Deserialized User Profile: {new_user_profile}")

            # Add user to DB
            with next(get_session()) as session:
                user = UserProfile(
                    id=new_user_profile.id,
                    first_name=new_user_profile.first_name,
                    last_name=new_user_profile.last_name,
                    address=new_user_profile.address,
                    avatar_url=new_user_profile.avatar_url,
                    date_of_birth=new_user_profile.date_of_birth,
                    user_id=new_user_profile.user_id,
                 )
                print(f"Before User Profile added: {user}")
                
                
                session.add(user)
                session.commit()
                session.refresh(user)
                print(f"User Profile added: {user}")

    finally:
        await consumer.stop()
# ===========================CONSUMER USER PROFILE ADD - END ====================



# ===========================CONSUMER USER PROFILE LIST - START ====================
async def consume_messages_list_user_profile(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="users-profile-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            new_user_profile_list = user_pb2.UserProfileList()
            new_user_profile_list.ParseFromString(message.value)
            print(f"Consumer Deserialized User Profile List: {new_user_profile_list}")

            
          

    finally:
        await consumer.stop()
# ===========================CONSUMER AUSER PROFILE LIST - END ====================





# ===========================CONSUMER USER PROFILE GET - START ====================
async def consume_messages_get_user_profile(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="users-profile-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            new_user_profile_get = user_pb2.UserProfile()
            new_user_profile_get.ParseFromString(message.value)
            print(f"Consumer Deserialized User Profile Get: {new_user_profile_get}")

            
          

    finally:
        await consumer.stop()
# ===========================CONSUMER AUSER PROFILE GET - END ====================



# ===========================CONSUMER USER PROFILE UPDATE - START ====================
async def consume_messages_update_user_profile(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="users-profile-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic: {message.topic}")

            # Deserialize the message
            new_user_profile = user_pb2.UserProfile()
            new_user_profile.ParseFromString(message.value)
            print(f"Consumer Deserialized User Profile: {new_user_profile}")

            # Add user to DB
            with next(get_session()) as session:
                user = UserProfile(
                    id=new_user_profile.id,
                    first_name=new_user_profile.first_name,
                    last_name=new_user_profile.last_name,
                    address=new_user_profile.address,
                    avatar_url=new_user_profile.avatar_url,
                    date_of_birth=new_user_profile.date_of_birth,
                    user_id=new_user_profile.user_id,
                 )
                print(f"Before User Profile updated: {user}")
                
                
                session.add(user)
                session.commit()
                session.refresh(user)
                print(f"User Profile updated: {user}")

    finally:
        await consumer.stop()
# ===========================CONSUMER USER PROFILE UPDATE - END ====================
