# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import Annotated, AsyncGenerator,List
from app.db_engine import create_db_and_tables, engine
from app.models.order_model import (
    Order,
    OrderCreate,
    OrderUpdate,
    OrderItem,
    OrderItemCreate,
    OrderItemUpdate,
    Payment,
    PaymentCreate,
    PaymentUpdate,
    OrderStatusHistory,
    OrderStatusHistoryCreate
    
)

from app.consumers.order_consumer import (
    consume_messages_add_order,
    consume_messages_update_order,
    consume_messages_list_orders,
    consume_message_get_order,
    # consume_message_delete_order,
)

from app.consumers.order_item_consumer import (
    consume_messages_add_order_item,
    consume_messages_update_order_item,
    consume_messages_list_order_items,
    consume_message_get_order_item,
    # consume_message_delete_order_item,
)


from app.consumers.payment_consumer import (
    consume_messages_add_payment,
    consume_messages_get_payment,
    consume_messages_list_payment

)


from app.consumers.order_status_history_consumer import (
     consume_messages_add_order_history_status, 
     consume_messages_get_list_order_history_status
    
)   





from app.producers.order_producer import get_kafka_producer
from app import order_pb2
# , order_item_pb2
from aiokafka import AIOKafkaProducer
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables.")
    # Start consumers for order
    task0 = asyncio.create_task(
        consume_messages_add_order("orders_add", "broker:19092")
    )
    task1 = asyncio.create_task(
        consume_messages_update_order("orders_update", "broker:19092")
    )
    task2 = asyncio.create_task(
        consume_messages_list_orders("orders_list", "broker:19092")
    )
    task3 = asyncio.create_task(
        consume_message_get_order("orders_get", "broker:19092")
    )
    # task4 = asyncio.create_task(
    #     consume_message_delete_order("orders_delete", "broker:19092")
    # )

    # # Start consumers for order items
    task5 = asyncio.create_task(
        consume_messages_add_order_item("order_items_add", "broker:19092")
    )
    task6 = asyncio.create_task(
        consume_messages_update_order_item("order_items_update", "broker:19092")
    )
    task7 = asyncio.create_task(
        consume_messages_list_order_items("order_items_list", "broker:19092")
    )
    task8 = asyncio.create_task(
        consume_message_get_order_item("order_items_get", "broker:19092")
    )
    # task9 = asyncio.create_task(
    #     consume_message_delete_order_item("order_items_delete", "broker:19092")
    # )
    
     # # Start consumers for payment requests
    task10 = asyncio.create_task(
    consume_messages_add_payment("payments_add", "broker:19092")
     )
    
    task11 = asyncio.create_task(
    consume_messages_get_payment("payments_get", "broker:19092")
     )
    task12 = asyncio.create_task(
    consume_messages_list_payment("payments_list", "broker:19092")
     )
    
    task13 = asyncio.create_task(
    consume_messages_add_order_history_status("history_order_add", "broker:19092")
     )
    task14 = asyncio.create_task(
    consume_messages_get_list_order_history_status("history_order_history_list", "broker:19092")
     )
    
    create_db_and_tables()
    yield

app = FastAPI(
    lifespan=lifespan,
    title="Order Service API",
    version="0.1.0",
)

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def read_root():
    return {"Hello": "Welcome to Order Service"}

# ============================ ORDER APIs ===========================
# ============================ ORDER APIs ===========================
# ============================ ORDER APIs ===========================


# ============================ ADD ORDER ===========================
@app.post("/orders/", response_model=Order)
async def add_order(
    order: OrderCreate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> Order:
    print(f"Before order creation: {order}")
    order_protobuf = order_pb2.OrderCreate(
        id=order.id,
        user_id=order.user_id,
        status=order.status,
        total_amount=order.total_amount,
        payment_status=order.payment_status,
        shipping_address=order.shipping_address,
        order_date=order.order_date,
    )
    serialized_order = order_protobuf.SerializeToString()
    await producer.send_and_wait("orders_add", serialized_order)
    print(f"After order creation: {order}")
    return order

# ============================ LIST ORDERS ===========================
@app.get("/orders/", response_model=list[Order])
async def list_orders(
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> list[Order]:
    orders = session.exec(select(OrderCreate)).all()
    print(f"Orders list==>: {orders}")
    
    order_list_message = order_pb2.OrderList()
    for order in orders:
        order_protobuf = order_list_message.orders.add()
        order_protobuf.id = order.id
        order_protobuf.user_id = order.user_id
        order_protobuf.status = order.status
        order_protobuf.total_amount = order.total_amount
        order_protobuf.payment_status = order.payment_status
        order_protobuf.shipping_address = order.shipping_address
        order_protobuf.order_date = order.order_date.isoformat() 
        

    serialized_order_list = order_list_message.SerializeToString()
    await producer.send_and_wait("orders_list", serialized_order_list)
    return orders

# ============================ GET SINGLE ORDER ===========================
@app.get("/orders/{order_id}", response_model=Order)
async def get_order(
    order_id: int,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
) -> Order:
    order = session.get(OrderCreate, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    print(f"Before Order get==>: {order}")
    order_protobuf = order_pb2.Order(
        id=order.id,
        user_id=order.user_id,
        status=order.status,
        total_amount=order.total_amount,
        payment_status=order.payment_status,
        shipping_address=order.shipping_address,
        order_date=order.order_date.isoformat(),
        
    )
    print(f"After Order get==>: {order}")
    serialized_product = order_protobuf.SerializeToString()
    await producer.send_and_wait("orders_get", serialized_product)
    
    return order

# # ============================ DELETE ORDER ===========================
# @app.delete("/orders/{order_id}", response_model=dict)
# async def delete_order(
#     order_id: int,
#     session: Annotated[Session, Depends(get_session)],
#     producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
# ) -> dict:
#     db_order = session.get(OrderCreate, order_id)
    
#     print(f"Before Delete Order==>: {db_order}")
    
#     if db_order:
#         order_delete_message = order_pb2.OrderDelete(id= order_id)
#         print(f"order_delete_message==>: {order_delete_message}")
#         serialized_order_delete = order_delete_message.SerializeToString()
#         print(f"serialized_order_delete Order==>: {serialized_order_delete}")
#         await producer.send_and_wait("orders_delete", serialized_order_delete)

#         return {"message": "Order deleted"}
#     raise HTTPException(status_code=404, detail="Order not found")


#  ============================ UPDATE ORDER ===========================
@app.put("/orders/{order_id}", response_model=OrderUpdate)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
) -> OrderUpdate:
    db_order = session.get(OrderCreate, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
     
    order_protobuf = order_pb2.OrderUpdate(id=order_id)
    
    if order_update.status:
        order_protobuf.status = order_update.status
    if order_update.payment_status:
        order_protobuf.payment_status = order_update.payment_status
    if order_update.shipping_address:
        order_protobuf.shipping_address = order_update.shipping_address
    
    serialized_product = order_protobuf.SerializeToString()
    await producer.send_and_wait("orders_update", serialized_product)

    
    return order_update

# ======================================================



# ============================ ORDER ITEM APIs ===========================
# ============================ ORDER ITEM APIs ===========================
# ============================ ORDER ITEM APIs ===========================



# ============================ ADD ORDER ITEM ===========================
@app.post("/order-items/", response_model=OrderItem)
async def add_order_item(
    order_item: OrderItemCreate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> OrderItem:
    order_item_protobuf = order_pb2.OrderItemCreate(
        id=order_item.id,
        order_id=order_item.order_id,
        product_id=order_item.product_id,
        quantity=order_item.quantity,
        price_per_unit=order_item.price_per_unit,
        total_price=order_item.total_price,
    )
    serialized_order_item = order_item_protobuf.SerializeToString()
    await producer.send_and_wait("order_items_add", serialized_order_item)
    return order_item

# # ============================ LIST ORDER ITEMS ===========================
@app.get("/order-items/", response_model=list[OrderItem])
async def list_order_items(
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> list[OrderItem]:
    order_items = session.exec(select(OrderItemCreate)).all()
    print(f"Orders Items list==>: {order_items}")
    
    order_item_list_message = order_pb2.OrderItemList()
    for orderitem in order_items:
        order_item_protobuf = order_item_list_message.ordersitem.add()
        
        order_item_protobuf.id = orderitem.id
        order_item_protobuf.order_id = orderitem.order_id
        order_item_protobuf.product_id = orderitem.product_id
        order_item_protobuf.quantity = orderitem.quantity
        order_item_protobuf.price_per_unit = orderitem.price_per_unit
        order_item_protobuf.total_price = orderitem.total_price
    
    serialized_order_item_list = order_item_list_message.SerializeToString()
    await producer.send_and_wait("order_items_list", serialized_order_item_list)
    
    return order_items

# # ============================ GET SINGLE ORDER ITEM ===========================
@app.get("/order-items/{order_item_id}", response_model=OrderItem)
async def get_order_item(
    order_item_id: int,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
) -> OrderItem:
    order_item = session.get(OrderItemCreate, order_item_id)
    if not order_item:
        raise HTTPException(status_code=404, detail="Order Item not found")
   
   
    print(f"Before Order Item==>: {order_item}")
    order_item_protobuf = order_pb2.OrderItem(
        id=order_item.id,
        order_id=order_item.order_id,
        product_id=order_item.product_id,
        quantity=order_item.quantity,
        price_per_unit=order_item.price_per_unit,
        total_price=order_item.total_price
        
    )

    serialized_product = order_item_protobuf.SerializeToString()
    await producer.send_and_wait("order_items_get", serialized_product)
   
   
    return order_item

# # ============================ DELETE ORDER ITEM ===========================
# @app.delete("/order-items/{order_item_id}", response_model=dict)
# async def delete_order_item(
#     order_item_id: int,
#     session: Annotated[Session, Depends(get_session)],
# ) -> dict:
#     db_order_item = session.get(OrderItem, order_item_id)
#     if db_order_item:
#         session.delete(db_order_item)
#         return {"message": "Order Item deleted"}
#     raise HTTPException(status_code=404, detail="Order Item not found")

# ============================ UPDATE ORDER ITEM ===========================
@app.put("/order-items/{order_item_id}", response_model=OrderItemUpdate)
async def update_order_item(
    order_item_id: int,
    order_item_update: OrderItemUpdate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
) -> OrderItemUpdate:
    db_order_item = session.get(OrderItemCreate, order_item_id)
    if not db_order_item:
        raise HTTPException(status_code=404, detail="Order Item not found")

    order_item_protobuf = order_pb2.OrderItemUpdate(id=order_item_id)


    if order_item_update.quantity is not None:
        order_item_protobuf.quantity = order_item_update.quantity
    if order_item_update.price_per_unit is not None:
        order_item_protobuf.price_per_unit = order_item_update.price_per_unit
    if order_item_update.total_price is not None:
        order_item_protobuf.total_price = order_item_update.total_price    
  
    serialized_product = order_item_protobuf.SerializeToString()
    await producer.send_and_wait("order_items_update", serialized_product)

 
    return order_item_update







# ============================ PAYEMENT APIs ===========================
# ============================ PAYEMENT APIs ===========================
# ============================ PAYEMENT APIs ===========================


# ============================ ADD PAYMENT ===========================
@app.post("/payments/", response_model=Payment)
async def add_payment(
    payment: PaymentCreate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> Payment:
    payment_protobuf = order_pb2.PaymentCreate(
        id=payment.id,
        order_id=payment.order_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status=payment.status,
        transaction_id=payment.transaction_id
    )
    serialized_payment = payment_protobuf.SerializeToString()
    await producer.send_and_wait("payments_add", serialized_payment)
    return payment



# ============================ GET PAYMENT ===========================
@app.get("/payments/{payment_id}", response_model=Payment)
async def get_payment(
    payment_id: int,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> Payment:
    payment = session.get(PaymentCreate, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
  
    payment_protobuf = order_pb2.Payment(
        id=payment.id,
        order_id=payment.order_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status=payment.status,
        transaction_id=payment.transaction_id
        
    )

    serialized_payment = payment_protobuf.SerializeToString()
    await producer.send_and_wait("payments_get", serialized_payment)
  
    return payment






# ============================ GET PAYMENT LIST ===========================
@app.get("/payments/", response_model=List[Payment])
async def get_payment_list(
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> Payment:
    payment_list =session.exec(select(PaymentCreate)).all()
    print(f"list of payment==>{payment_list}")
    payemnt_list_message = order_pb2.PaymentList()
    for payment in payment_list:
        payemnt_protobuf = payemnt_list_message.payments.add()
        
        payemnt_protobuf.id = payment.id
        payemnt_protobuf.order_id = payment.order_id
        payemnt_protobuf.amount = payment.amount
        payemnt_protobuf.payment_method = payment.payment_method
        payemnt_protobuf.status = payment.status
        payemnt_protobuf.transaction_id = payment.transaction_id
    

    serialized_payment_list = payemnt_list_message.SerializeToString()
    await producer.send_and_wait("payments_list", serialized_payment_list)
  
    return payment_list






# ============================ ORDER HISTORY STATUS APIs ===========================
# ============================ ORDER HISTORY STATUSAPIs ===========================
# ============================ ORDER HISTORY STATUSAPIs ===========================







# API to get the status history of a specific order
@app.post("/orders/history", response_model=OrderStatusHistory)
async def add_order_status_history(
    order_history: OrderStatusHistoryCreate,
    session: Annotated[Session, Depends(get_session)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
    
) -> OrderStatusHistory:
    
    
    history_order_protobuf = order_pb2.OrderStatusHistoryCreate(
        id=order_history.id,
        order_id=order_history.order_id,
        status=order_history.status,
        timestamp=order_history.timestamp,
    )
     
    serialized_history_order = history_order_protobuf.SerializeToString()
    await producer.send_and_wait("history_order_add", serialized_history_order)
    
    return order_history;
    




# API to get the status history of a specific order
@app.get("/orders/{order_id}/history", response_model=List[OrderStatusHistory])
async def get_order_status_history(
       order_id: int,
       session: Annotated[Session, Depends(get_session)],
       producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
) -> List[OrderStatusHistory]:
    # Query OrderStatusHistory records based on order_id
    order_history = session.exec(
        select(OrderStatusHistoryCreate).where(OrderStatusHistoryCreate.order_id == order_id)
    ).all()

    if not order_history:
        raise HTTPException(status_code=404, detail="Order history not found")


    response_history_order = order_pb2.OrderStatusHistoryList()
    for record in order_history:
        history_record = response_history_order.histroy.add()
    
        history_record.id = record.id
        history_record.order_id = record.order_id
        history_record.status = record.status
        history_record.timestamp = record.timestamp.isoformat()  # Ensure timestamp is a string

    print(f"After ====> {response_history_order}")
    serialized_history_list = response_history_order.SerializeToString()
    await producer.send_and_wait("history_order_history_list", serialized_history_list)
  
    return order_history