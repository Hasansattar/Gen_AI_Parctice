from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta
from sqlmodel import Session, select
from typing import Annotated, AsyncGenerator, List
from app.db_engine import create_db_and_tables, engine
from app.models.user_model import UserCreate, UserUpdate ,User , UserProfile,UserEvent , UserLoginRequest,UserLoginResponse ,PasswordResetRequest
from app.consumers.user_consumer import (
    consume_messages_add_user,
    consume_messages_update_user,
    consume_messages_list_users,
    consume_message_get_user,
)


from app.consumers.profile_consumer import(
  consume_messages_add_user_profile,
  consume_messages_list_user_profile,
  consume_messages_get_user_profile,
  consume_messages_update_user_profile
)


from app.consumers.event_consumer import (
  consume_messages_add_user_event,
  consume_messages_get_user_event
)

from app.consumers.login_logout_consumer import (
  consume_messages_user_login,
  consume_messages_password_reset
  
  
)


from app.consumers.login_secret_fn import(
  generate_access_token,
  generate_refresh_token,
  hash_password,
  verify_password,
  generate_reset_token
)


from app.producers.user_producer import get_kafka_producer
from app import user_pb2
from aiokafka import AIOKafkaProducer
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables.")
    
    #  User defined
    task1 = asyncio.create_task(
        consume_messages_add_user("users_add", "broker:19092")
    )
    task2 = asyncio.create_task(
        consume_messages_update_user("users_update", "broker:19092")
    )
    task3 = asyncio.create_task(
        consume_messages_list_users("users_list", "broker:19092")
    )
    task4 = asyncio.create_task(
        consume_message_get_user("users_get", "broker:19092")
    )
    
    # User profile defined

    task5 = asyncio.create_task(
        consume_messages_add_user_profile("profiles_add", "broker:19092")
    )
    
    task6 = asyncio.create_task(
        consume_messages_list_user_profile("profiles_list", "broker:19092")
    )
    
    task7 = asyncio.create_task(
        consume_messages_get_user_profile("profiles_get", "broker:19092")
    )
 
    task8 = asyncio.create_task(
        consume_messages_update_user_profile("profiles_update", "broker:19092")
    )
   
   
   # User Events
   
    task9 = asyncio.create_task(
        consume_messages_add_user_event("events_add", "broker:19092")
    )
    
    task10 = asyncio.create_task(
        consume_messages_get_user_event("events_get", "broker:19092")
    )
    
    
    # Login Consumer
    
    task11 = asyncio.create_task(
        consume_messages_user_login("user_login", "broker:19092")
    )
    
    task12 = asyncio.create_task(
          consume_messages_password_reset("password_reset_topic", "broker:19092")
    )
    
   
   

    create_db_and_tables()
    yield

app = FastAPI(
    lifespan=lifespan,
    title="User Service API",
    version="0.1.0",
)

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def read_root():
    return {"Hello": "Welcome to User Service"}

# ============================ USER APIs ===========================
# ============================ USER APIs ===========================
# ============================ USER APIs ===========================

# ============================ ADD USER ===========================
@app.post("/users/", response_model=UserCreate)
async def add_user(
    user: UserCreate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> UserCreate:
    user_protobuf = user_pb2.UserCreate(
        id=user.id,
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password_hash),  
        phone=user.phone,
        is_active=user.is_active,
        is_verified=user.is_verified,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
    print(f"user_protobuf==>: {user_protobuf}")
    serialized_user = user_protobuf.SerializeToString()
    await producer.send_and_wait("users_add", serialized_user)
    print(f"user add==>: {user}")
    return user

# ============================ LIST USERS ===========================
@app.get("/users/", response_model=List[User])
async def list_users(
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> List[User]:
    users = session.exec(select(UserCreate)).all()
    
    user_list_message = user_pb2.UserList()
    for user in users:
        user_protobuf = user_list_message.users.add()
        user_protobuf.id = user.id
        user_protobuf.username = user.username
        user_protobuf.email = user.email
        user_protobuf.phone = user.phone
        user_protobuf.is_active = user.is_active
        user_protobuf.is_verified = user.is_verified
        user_protobuf.role = user.role
        user_protobuf.created_at = user.created_at.isoformat()
        
    serialized_user_list = user_list_message.SerializeToString()
    await producer.send_and_wait("users_list", serialized_user_list)
    return users

# ============================ GET SINGLE USER ===========================
@app.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
) -> User:
    user = session.get(UserCreate, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_protobuf = user_pb2.User(
        id=user.id,
        username=user.username,
        email=user.email,
        phone=user.phone,
        is_active=user.is_active,
        is_verified=user.is_verified,
        role=user.role,
        created_at=user.created_at.isoformat(),
    )
    serialized_user = user_protobuf.SerializeToString()
    await producer.send_and_wait("users_get", serialized_user)
    
    return user

# ============================ UPDATE USER ===========================
@app.put("/users/{user_id}", response_model=UserUpdate)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
) -> UserUpdate:
    db_user = session.get(UserCreate, user_id)
    print(f"user ===> {db_user} ")
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_protobuf = user_pb2.UserUpdate(id=user_id)
    if user_update.password_hash:
        user_protobuf.password_hash = hash_password(user_update.password_hash)   
    if user_update.phone:
        user_protobuf.phone = user_update.phone
    if user_update.updated_at:
        user_protobuf.updated_at = user_update.updated_at.isoformat()
    
    print(f"user_protobuf ===> {user_protobuf} ")
    
    serialized_user = user_protobuf.SerializeToString()
    await producer.send_and_wait("users_update", serialized_user)

    return user_update



# ============================ USER PROFILE APIs ===========================
# ============================ USER PROFILE APIs ===========================
# ============================ USER PROFILE APIs ===========================



# ============================ ADD USER PROFILE ===========================
@app.post("/profiles/", response_model=UserProfile)
async def add_user_profile(
    profile: UserProfile,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
) -> UserProfile:


    # Prepare protobuf message for Kafka
    profile_protobuf = user_pb2.UserProfile(
        id=profile.id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        address=profile.address,
        avatar_url=profile.avatar_url,
        date_of_birth=profile.date_of_birth,
        user_id=profile.user_id,
    )
    serialized_profile = profile_protobuf.SerializeToString()
    await producer.send_and_wait("profiles_add", serialized_profile)

    return profile



# ============================ LIST USER PROFILES ===========================

@app.get("/profiles/", response_model=List[UserProfile])
async def list_user_profiles(
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
) -> List[UserProfile]:
    profiles = session.exec(select(UserProfile)).all()
    
    # Prepare and send list of profiles as protobuf message
    profile_list_message = user_pb2.UserProfileList()
    for profile in profiles:
        profile_protobuf = profile_list_message.profiles.add()
        profile_protobuf.id = profile.id
        profile_protobuf.first_name = profile.first_name
        profile_protobuf.last_name = profile.last_name
        profile_protobuf.address = profile.address
        profile_protobuf.avatar_url = profile.avatar_url
        profile_protobuf.date_of_birth = profile.date_of_birth.isoformat() if profile.date_of_birth else None
        profile_protobuf.user_id = profile.user_id

    serialized_profile_list = profile_list_message.SerializeToString()
    await producer.send_and_wait("profiles_list", serialized_profile_list)
    
    return profiles
  
  
  
  
  # ============================ GET SINGLE USER PROFILE ===========================
@app.get("/profiles/{profile_id}", response_model=UserProfile)
async def get_user_profile(
    profile_id: int,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
) -> UserProfile:
    profile = session.get(UserProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Prepare and send protobuf message
    profile_protobuf = user_pb2.UserProfile(
        id=profile.id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        address=profile.address,
        avatar_url=profile.avatar_url,
        date_of_birth=profile.date_of_birth.isoformat() if profile.date_of_birth else None,
        user_id=profile.user_id,
    )
    serialized_profile = profile_protobuf.SerializeToString()
    await producer.send_and_wait("profiles_get", serialized_profile)
    
    return profile
  
  
  
  # ============================ UPDATE USER PROFILE ===========================
@app.put("/profiles/{profile_id}", response_model=UserProfile)
async def update_user_profile(
    profile_id: int,
    profile_update: UserProfile,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
) -> UserProfile:
    db_profile = session.get(UserProfile, profile_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")


    # Prepare and send protobuf message
    profile_protobuf = user_pb2.UserProfile(
        id=db_profile.id,
        first_name=db_profile.first_name,
        last_name=db_profile.last_name,
        address=db_profile.address,
        avatar_url=db_profile.avatar_url,
        date_of_birth=db_profile.date_of_birth.isoformat() if db_profile.date_of_birth else None,
        user_id=db_profile.user_id,
    )
    serialized_profile = profile_protobuf.SerializeToString()
    await producer.send_and_wait("profiles_update", serialized_profile)

    return db_profile
  
  
  
  
  
  
  # ============================ USER EVENT APIs ===========================
  # ============================ USER EVENT APIs ===========================
  # ============================ USER EVENT APIs ===========================
  
  
  
  # ============================ ADD USER EVENT ===========================
@app.post("/events/", response_model=UserEvent)
async def add_user_event(
    event: UserEvent,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
) -> UserEvent:
     
    print(f"Before event post ==>: {event}")
   # Map the `event_type` to corresponding protobuf enum integer
    event_type_mapping = {
        "CREATED": user_pb2.UserEvent.EventType.CREATED,
        "UPDATED": user_pb2.UserEvent.EventType.UPDATED,
        "DELETED": user_pb2.UserEvent.EventType.DELETED,
        "VERIFIED": user_pb2.UserEvent.EventType.VERIFIED
    }
    
    user_pb2.UserEvent.EventType.VERIFIED
    
    if event.event_type not in event_type_mapping:
        raise HTTPException(status_code=400, detail="Invalid event type")
    
    event_type_enum = event_type_mapping[event.event_type]
    
  
    # Prepare protobuf message for Kafka
    event_protobuf = user_pb2.UserEvent(
        id=event.id,
        event_type= event_type_enum,
        event_payload=event.event_payload,
        timestamp=event.timestamp,   # timestamp=event.timestamp.isoformat(),  
        user_id=event.user_id,
    )
    
    print(f"event post ==>: {event_protobuf}")
    serialized_event = event_protobuf.SerializeToString()
    await producer.send_and_wait("events_add", serialized_event)

    return event
  
  
  
  
  # ============================ GET SINGLE USER EVENT ===========================
@app.get("/events/{event_id}", response_model=UserEvent)
async def get_user_event(
    event_id: int,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
) -> UserEvent:
    event = session.get(UserEvent, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Prepare and send protobuf message
    event_protobuf = user_pb2.UserEvent(
        id=event.id,
        event_type=event.event_type,
        event_payload=event.event_payload,
        timestamp=event.timestamp.isoformat(),
        user_id=event.user_id,
    )
    serialized_event = event_protobuf.SerializeToString()
    await producer.send_and_wait("events_get", serialized_event)

    return event
  
  
  
  
  
  
  # ============================ USER LOGIN - RESET APIs ===========================
  # ============================ USER LOGIN - RESET APIs ===========================
  # ============================ USER LOGIN - RESET APIs ===========================
  
  
  
  # ==========================LOGIN USER =====================
  
@app.post("/login/", response_model=UserLoginResponse)
async def login_user(
    login_request: UserLoginRequest,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
) -> UserLoginResponse:
  
    # Fetch user from the database
  user = session.exec(select(UserCreate).where(UserCreate.username == login_request.username)).first()
  
  print(f"login user name: {user}")
  
   # Check if user exists and password is valid
  if not user or not verify_password(login_request.password, user.password_hash):  # Assume a function that verifies the password
        raise HTTPException(status_code=401, detail="Invalid username or password")
   
  print(f"chek access token:===>{generate_access_token(user.id)}")    
  login_response = user_pb2.UserLoginResponse(
        user_id=user.id,
        access_token=generate_access_token(user.id),  # Assume a function that generates an access token
        refresh_token=generate_refresh_token(user.id)  # Assume a function that generates a refresh token
    )
   
   # Send event to Kafka
  login_event = user_pb2.UserEvent(
        user_id=user.id,
        event_type=user_pb2.UserEvent.EventType.VERIFIED,
        event_payload=f"User {user.username} logged in",
        timestamp= datetime.utcnow().isoformat()
    )      
  
  
  print(f"login_event:===>{login_event}")  

  serialized_login_event = login_event.SerializeToString()
  await producer.send_and_wait("user_login", serialized_login_event)
  return login_response
 
 
 
#  =============================PASSWORD RESET===============================
 
@app.post("/password/reset/", response_model=PasswordResetRequest)
async def get_login(
    reset_request: PasswordResetRequest,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
) -> PasswordResetRequest:
  
   
    # Fetch user from the database
  user = session.exec(select(UserCreate).where(UserCreate.username == reset_request.username)).first()
  
  print(f"login user name: {user}")
  
   # Check if user exists and password is valid
  if not user or not verify_password(reset_request.oldpassword, user.password_hash):  # Assume a function that verifies the password
        raise HTTPException(status_code=401, detail="Invalid username or password")
   
  
  new_hashed_password = hash_password(reset_request.newpassword)
    
  
  reset_protobuf = user_pb2.UserUpdate(id=user.id)
  if reset_request.oldpassword:
        reset_protobuf.password_hash = new_hashed_password

  print(f"Reset Password ===>: {reset_protobuf}")  
  serialized_reset_request = reset_protobuf.SerializeToString()
    
    # Send serialized message to Kafka
  await producer.send_and_wait("password_reset_topic", serialized_reset_request)

  return reset_request
  
  