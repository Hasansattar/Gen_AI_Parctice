# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import Annotated, AsyncGenerator
from app.db_engine import create_db_and_tables, engine
from app.models.product_model import (
    Product,
    ProductCreate,
    ProductUpdate,
    Category,
    CategoryCreate,
    CategoryUpdate,
    ImageCreate,
    Image,
    ImageUpdate,
)

from app.consumers.product_consumer import (
    consume_messages_add_product,
    consume_messages_update_product,
    consume_messages_list_products,
    consume_message_get_product,
    consume_message_delete_product,
)
from app.consumers.category_consumer import (
    consume_messages_add_category,
    consume_messages_update_category,
    consume_messages_list_categories,
    consume_message_get_category,
    consume_message_delete_category,
)
from app.consumers.image_consumer import (
    consume_messages_add_image,
    consume_messages_list_image,
    consume_messages_get_image,
    consume_messages_delete_image,
    consume_messages_update_image
   
)

from app.producers.product_producer import get_kafka_producer
from app import product_pb2, category_pb2 , image_pb2
from aiokafka import AIOKafkaProducer
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables.")
    # Start consumers for product
    task0 = asyncio.create_task(
        consume_messages_add_product("products_add", "broker:19092")
    )
    task1 = asyncio.create_task(
        consume_messages_update_product("products_update", "broker:19092")
    )
    task2 = asyncio.create_task(
        consume_messages_list_products("products_list", "broker:19092")
    )
    task3 = asyncio.create_task(
        consume_message_get_product("products_get", "broker:19092")
    )
    task4 = asyncio.create_task(
        consume_message_delete_product("products_delete", "broker:19092")
    )

    # Start category consumers
    task5 = asyncio.create_task(
        consume_messages_add_category("categories_add", "broker:19092")
    )
    task6 = asyncio.create_task(
        consume_messages_update_category("categories_update", "broker:19092")
    )
    task7 = asyncio.create_task(
        consume_messages_list_categories("categories_list", "broker:19092")
    )
    task8 = asyncio.create_task(
        consume_message_get_category("categories_get", "broker:19092")
    )
    task9 = asyncio.create_task(
        consume_message_delete_category("categories_delete", "broker:19092")
    )
    
    
    task10 = asyncio.create_task(
        consume_messages_add_image("images_add", "broker:19092")
    )
    
    task11 = asyncio.create_task(
        consume_messages_list_image("images_list", "broker:19092")
    )
    task12 = asyncio.create_task(
        consume_messages_get_image("images_get", "broker:19092")
    )
    
    task13 = asyncio.create_task(
        consume_messages_delete_image("images_delete", "broker:19092")
    )
    task14 = asyncio.create_task(
        consume_messages_update_image("images_update", "broker:19092")
    )
    create_db_and_tables()
    yield
    
    # await asyncio.sleep(5)  # Adjust the sleep time as needed to capture relevant task output
    # result = await asyncio.gather(task0)
    # print(f"Taskresult: {result}")

app = FastAPI(
    lifespan=lifespan,
    title="Product Service API",
    version="0.1.0",
)


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def read_root():
    return {"Hello": "Welcome to Product Service"}

# ============================ PRODUCT APIs ===========================
# ============================ PRODUCT APIs ===========================
# ============================ PRODUCT APIs ===========================


# ============================ ADD PRODUCT ===========================
@app.post("/products/", response_model=Product)
async def add_product(
    product: ProductCreate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> Product:
    product_protobuf = product_pb2.ProductCreate(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity,
        category_id=product.category_id,
        image_id=product.image_id,
    )
    serialized_product = product_protobuf.SerializeToString()
    await producer.send_and_wait("products_add", serialized_product)
    print(f"Product: {product}")
    return product


# ============================ LIST PRODUCTS ===========================
@app.get("/products/", response_model=list[Product])
async def list_products(
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> list[Product]:
    products = session.exec(select(ProductCreate)).all()
    print(f"Product list: {products}")

    product_list_message = product_pb2.ProductList()
    for product in products:
        product_protobuf = product_list_message.products.add()
        product_protobuf.id = product.id
        product_protobuf.name = product.name
        product_protobuf.description = product.description
        product_protobuf.price = product.price
        product_protobuf.stock_quantity = product.stock_quantity
        product_protobuf.category_id = product.category_id
        product_protobuf.image_id = product.image_id
        

    serialized_product_list = product_list_message.SerializeToString()
    await producer.send_and_wait("products_list", serialized_product_list)

    return products


# ============================ GET SINGLE PRODUCT ===========================
@app.get("/products/{product_id}", response_model=Product)
async def get_product(
    product_id: int,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> Product:
    product = session.get(ProductCreate, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_protobuf = product_pb2.ProductCreate(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity,
        category_id=product.category_id,
        image_id=product.image_id,
        
    )
    serialized_product = product_protobuf.SerializeToString()
    await producer.send_and_wait("products_get", serialized_product)

    return product


# ============================ DELETE PRODUCT ===========================
@app.delete("/products/{product_id}", response_model=dict)
async def delete_product(
    product_id: int,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> dict:
    db_product = session.get(ProductCreate, product_id)
    if db_product:

        product_delete_message = product_pb2.ProductDelete(id=product_id)
        serialized_product_delete = product_delete_message.SerializeToString()
        await producer.send_and_wait("products_delete", serialized_product_delete)

        return {"message": "Product deleted"}

    raise HTTPException(status_code=404, detail="Product not found")


# ============================ UPDATE PRODUCT ===========================
@app.put("/products/{product_id}", response_model=ProductUpdate)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> ProductUpdate:
    try:
        product_protobuf = product_pb2.ProductUpdate(id=product_id)

        if product_update.name:
            product_protobuf.name = product_update.name
        if product_update.description:
            product_protobuf.description = product_update.description
        if product_update.price is not None:
            product_protobuf.price = product_update.price
        if product_update.stock_quantity is not None:
            product_protobuf.stock_quantity = product_update.stock_quantity
        if product_update.category_id is not None:
            product_protobuf.category_id = product_update.category_id
        if product_update.image_id is not None:
            product_protobuf.image_id = product_update.image_id    

        serialized_product = product_protobuf.SerializeToString()
        await producer.send_and_wait("products_update", serialized_product)

        return product_update

    except Exception as e:
        return {"error": f"Failed to produce message: {str(e)}"}


# ============================ CATEGORY APIs ===========================
# ============================ CATEGORY APIs ===========================
# ============================ CATEGORY APIs ===========================


# ============================ ADD CATEGORY ===========================
@app.post("/categories/", response_model=Category)
async def add_category(
    category: CategoryCreate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> Category:
    category_protobuf = category_pb2.CategoryCreate(
        id=category.id, name=category.name, description=category.description
    )
    serialized_category = category_protobuf.SerializeToString()
    await producer.send_and_wait("categories_add", serialized_category)
    return category


# ============================ LIST CATEGORIES ===========================
@app.get("/categories/", response_model=list[Category])
async def list_categories(
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> list[Category]:
    categories = session.exec(
        select(CategoryCreate)
    ).all()  # Adjusted to use the correct Category model

    print(f"categories==>: {categories}")
    category_list_message = category_pb2.CategoryList()
    for category in categories:
        category_protobuf = category_list_message.categories.add()
        category_protobuf.id = category.id
        category_protobuf.name = category.name
        category_protobuf.description = category.description

    serialized_category_list = category_list_message.SerializeToString()
    await producer.send_and_wait("categories_list", serialized_category_list)

    return categories


# ============================ GET SINGLE CATEGORY ===========================
@app.get("/categories/{category_id}", response_model=Category)
async def get_category(
    category_id: int,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> Category:
    category = session.get(CategoryCreate, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category_protobuf = category_pb2.Category(
        id=category.id, name=category.name, description=category.description
    )
    serialized_category = category_protobuf.SerializeToString()
    await producer.send_and_wait("categories_get", serialized_category)

    return category


# ============================ DELETE CATEGORY ===========================
@app.delete("/categories/{category_id}", response_model=dict)
async def delete_category(
    category_id: int,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> dict:
    db_category = session.get(CategoryCreate, category_id)
    if db_category:
        category_delete_message = category_pb2.CategoryDelete(id=category_id)
        serialized_category_delete = category_delete_message.SerializeToString()
        await producer.send_and_wait("categories_delete", serialized_category_delete)

        return {"message": "Category deleted"}

    raise HTTPException(status_code=404, detail="Category not found")


# ============================ UPDATE CATEGORY ===========================
@app.put("/categories/{category_id}", response_model=CategoryUpdate)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> CategoryUpdate:
    try:
        category_protobuf = category_pb2.CategoryUpdate(id=category_id)

        if category_update.name:
            category_protobuf.name = category_update.name
        if category_update.description:
            category_protobuf.description = category_update.description

        serialized_category = category_protobuf.SerializeToString()
        await producer.send_and_wait("categories_update", serialized_category)

        return category_update

    except Exception as e:
        return {"error": f"Failed to produce message: {str(e)}"}



# ============================ PRODUCT IMAGES ===========================
# ============================ PRODUCT IMAGES ===========================
# ============================ PRODUCT IMAGES ===========================
# ============================ ADD IMAGE ===========================
@app.post("/images/", response_model=Image)
async def add_image(
    image: ImageCreate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> Image:
    image_protobuf = image_pb2.ImageCreate(
        id=image.id,
        image_url=image.image_url,
        product_id=image.product_id,
    )
    serialized_image = image_protobuf.SerializeToString()
    await producer.send_and_wait("images_add", serialized_image)
    return image



# ============================ LIST IMAGES ===========================
@app.get("/images/", response_model=list[Image])
async def list_images(
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> list[Image]:
    images = session.exec(select(ImageCreate)).all()
    print(f"Images list==>: {images}")
    
    
    # Create a list to store the formatted images
    formatted_images = []

    for con_image in images:
        # Ensure image.image_url is a string, not a list of characters
        if isinstance(con_image.image_url, list):
            image_url_str = ''.join(con_image.image_url)  # Join list to form a string
        else:
            image_url_str = con_image.image_url  # Already a string
        
        # Print for debugging
        print(f"Formatted image_url==>: {image_url_str}")
        
        # Append the formatted image to the list
        formatted_images.append({
            "id": con_image.id,
            "image_url": [image_url_str],  # Wrap the string in a list
            "product_id": con_image.product_id
        })
    
    image_list_message = image_pb2.ImageList()
    print(f" Before image_list_message list==>: {[image_list_message]}")   
    for image in formatted_images:
        image_protobuf = image_list_message.images.add()
        image_protobuf.id = image["id"]
        image_protobuf.product_id = image["product_id"]
        image_protobuf.image_url.extend(image["image_url"])  # Extend with lis
        # image_protobuf.image_url.extend(image.image_url) 
        
           
    serialized_image_list = image_list_message.SerializeToString()
    await producer.send_and_wait("images_list", serialized_image_list)
    
    
    return formatted_images  # Return the formatted list of images





# ============================ GET SINGLE IMAGE ===========================
@app.get("/images/{image_id}", response_model=Image)
async def get_image(
    image_id: int,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> Image:
    image = session.get(ImageCreate, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    # print(f" before sending event===>:{image}")
    
    # Ensure image.image_url is a string, not a list of characters
    if isinstance(image.image_url, list):
        image_url_str = ''.join(image.image_url)  # Join list to form a string
    else:
        image_url_str = image.image_url  # Already a string
    
    print(f" NEW sending image_url_str ===>:{image_url_str}")
    
    
    image_protobuf = image_pb2.Image(
        id=image.id,
        image_url=[image_url_str],
        product_id=image.product_id,
    )
    print(f" After sending  ===>:{image_protobuf}")
    
    serialized_image = image_protobuf.SerializeToString()
    print(f" serialized_image  ===>:{serialized_image}")
    
    await producer.send_and_wait("images_get", serialized_image)

    return image_protobuf


# ============================ DELETE IMAGE ===========================
@app.delete("/images/{image_id}", response_model=dict)
async def delete_image(
    image_id: int,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> dict:
    db_image = session.get(ImageCreate, image_id)
    if db_image:

        image_delete_message = image_pb2.ImageDelete(id=image_id)
        serialized_image_delete = image_delete_message.SerializeToString()
        await producer.send_and_wait("images_delete", serialized_image_delete)

        return {"message": "Image deleted"}

    raise HTTPException(status_code=404, detail="Image not found")





# ============================ UPDATE IMAGE ===========================
@app.put("/images/{image_id}", response_model=ImageUpdate)
async def update_image(
    image_id: int,
    image_update: ImageUpdate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> ImageUpdate:
    try:
        image_protobuf = image_pb2.ImageUpdate(id=image_id)

        if image_update.image_url:
            image_protobuf.image_url = image_update.image_url
        if image_update.product_id:
            image_protobuf.product_id = image_update.product_id    
    

        serialized_image = image_protobuf.SerializeToString()
        await producer.send_and_wait("images_update", serialized_image)

        return image_update

    except Exception as e:
        return {"error": f"Failed to produce message: {str(e)}"}