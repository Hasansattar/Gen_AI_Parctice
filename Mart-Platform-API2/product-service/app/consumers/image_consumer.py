# app/consumers/image_consumer.py
from aiokafka import AIOKafkaConsumer
from app.models.product_model import ImageCreate, ImageUpdate
from sqlmodel import Session
from app.db_engine import engine
from app import image_pb2

def get_session():
    with Session(engine) as session:
        yield session


# ===========================CONSUMER ADD IMAGE PRODUCT - START ====================
async def consume_messages_add_image(topic: str, broker: str):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers=broker,group_id="image-group")
    await consumer.start()
    try:
        async for msg in consumer:
            # Deserialize and handle the incoming message
            print(f"Received message on topic: {msg.topic}")
            
                        # Deserialize the message
            image_product = image_pb2.ImageCreate()
            image_product.ParseFromString(msg.value)
            print(f"Consumer Deserialized Image Added Product: {image_product}")
            
             # Add category to DB
            with next(get_session()) as session:
                image = ImageCreate(
                    id=image_product.id,
                    image_url=image_product.image_url,
                    product_id=image_product.product_id,
    
                )
                session.add(image)
                session.commit()
                session.refresh(image)
                print(f"Image added: {image}")
            
    finally:
        await consumer.stop()
        
        
        
# ===========================CONSUMER ADD IMAGE PRODUCT - END ====================


# ===========================CONSUMER LIST IMAGE PRODUCT - START ====================
async def consume_messages_list_image(topic: str, broker: str):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers=broker,group_id="image-group")
    await consumer.start()
    try:
        async for msg in consumer:
            # Deserialize and handle the incoming message
            print(f"Received message on topic: {msg.topic}")
            
                        # Deserialize the message
            image_list = image_pb2.ImageList()
            image_list.ParseFromString(msg.value)
            print(f"Consumer Deserialized Image List: {image_list}")
            
        
            print(f"Image added")
            
    finally:
        await consumer.stop()
        
        
        
# ===========================CONSUMER LIST IMAGE PRODUCT - END ====================
               
               
               
               
               
# ===========================CONSUMER GET IMAGE PRODUCT - START ====================
async def consume_messages_get_image(topic: str, broker: str):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers=broker,group_id="image-group")
    await consumer.start()
    try:
        async for msg in consumer:
            # Deserialize and handle the incoming message
            print(f"Received message on topic: {msg.topic}")
            
                        # Deserialize the message
            image_list = image_pb2.Image()
            image_list.ParseFromString(msg.value)
            print(f"Consumer Deserialized Image List: {image_list}")
            
            
           
            
           
            print(f"Image Received: {image_list}")
            
    finally:
        await consumer.stop()
        
        
        
# ===========================CONSUMER GET IMAGE PRODUCT - END ====================
               
   
 # ===========================CONSUMER IMAGE DELETE ====================
async def consume_messages_delete_image(topic: str, broker: str):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers=broker)
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message on topic: {msg.topic}")
            
            # Deserialize the message
            image_delete = image_pb2.ImageDelete()
            image_delete.ParseFromString(msg.value)
            print(f"Consumer Deserialized Image Delete: {image_delete}")
            
            # Delete image from DB
            with next(get_session()) as session:
                db_image = session.get(ImageCreate, image_delete.id)
                if db_image:
                    session.delete(db_image)
                    session.commit()
                    print(f"Image deleted: {db_image}")
    finally:
        await consumer.stop()               
        
        
 # ===========================CONSUMER IMAGE UPDATE ====================
async def consume_messages_update_image(topic: str, broker: str):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers=broker)
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received message on topic: {msg.topic}")
            
            # Deserialize the message
            image_update = image_pb2.ImageUpdate()
            image_update.ParseFromString(msg.value)
            print(f"Consumer Deserialized Image Update: {image_update}")
            
            # Update image in DB
            with next(get_session()) as session:
                db_image = session.get(ImageCreate, image_update.id)
                if db_image:
                    if image_update.image_url:
                        db_image.image_url = image_update.image_url
                    if image_update.product_id:
                        db_image.product_id = image_update.product_id
                        
                    session.commit()
                    print(f"Image updated: {db_image}")
    finally:
        await consumer.stop()       