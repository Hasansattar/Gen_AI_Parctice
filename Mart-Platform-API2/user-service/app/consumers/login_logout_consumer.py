from aiokafka import AIOKafkaConsumer
from app.models.user_model import UserCreate
from sqlmodel import Session
from app.db_engine import engine
from app import user_pb2

def get_session():
    with Session(engine) as session:
        yield session
        
        
        
# =========================== CONSUMER USER LOGIN - START ====================
async def consume_messages_user_login(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="login-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received login message on topic: {message.topic}")
            login_request = user_pb2.UserEvent()
            login_request.ParseFromString(message.value)
            print(f"Consumer Login Request: {login_request}")

            # # Perform login operation (check username and password hash)
            # with next(get_session()) as session:
            #     db_user = session.query(UserCreate).filter(
            #         UserCreate.username == login_request.username).first()
            #     if db_user and db_user.password_hash == login_request.password:
            #         print("Login successful")
            #     else:
            #         print("Login failed")

    finally:
        await consumer.stop()
# =========================== CONSUMER USER LOGIN - END ====================        



# =========================== CONSUMER PASSWORD RESET - START ====================
async def consume_messages_password_reset(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="login-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received password reset message on topic: {message.topic}")
            password_reset_request = user_pb2.UserUpdate()
            password_reset_request.ParseFromString(message.value)
            print(f"Consumer Password Reset Request: {password_reset_request}")

            # Handle password reset by sending reset token or updating password
            # (This example assumes an external mechanism will send email with the reset token)
            # Implement token generation and reset logic here
             # Update user in DB
            with next(get_session()) as session:
                db_user = session.get(UserCreate, password_reset_request.id)
                if db_user:
                   
                    if password_reset_request.password_hash:
                        db_user.password_hash = password_reset_request.password_hash
                
                    

                    session.add(db_user)
                    session.commit()
                    session.refresh(db_user)
                    print(f"User updated: {db_user}")
            print("Password reset token sent")

    finally:
        await consumer.stop()
# =========================== CONSUMER PASSWORD RESET - END ====================