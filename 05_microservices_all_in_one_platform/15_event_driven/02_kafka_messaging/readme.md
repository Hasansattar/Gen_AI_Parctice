#### it will make new images, if the previous images already exists  
   docker compose up -d --build
#### it will only down broker service, other services will remain running
   docker compose down broker
   OR 
   docker compose down api1

#### it will only broker service will up, other services will remain running
   docker compose up broker

#### it will only show broker service logs, other services will remain running
   docker compose logs broker



#### it will only show api1 container service logs live , -f means follow or live
   docker compose logs api1 -f   
   



# 02_kafka_messaging

### AIOKafkaProducer

AIOKafkaProducer is a high-level, asynchronous message producer.

Example of AIOKafkaProducer usage:

```
from aiokafka import AIOKafkaProducer

# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("my_topic", b"Super message")
    finally:
        await producer.stop()
```

### AIOKafkaConsumer
AIOKafkaConsumer is a high-level, asynchronous message consumer. It interacts with the assigned Kafka Group Coordinator node to allow multiple consumers to load balance consumption of topics (requires kafka >= 0.9.0.0).

Example of AIOKafkaConsumer usage:

```
from aiokafka import AIOKafkaConsumer
import asyncio

async def consume_messages():
    consumer = AIOKafkaConsumer(
        'my_topic', 'my_other_topic',
        bootstrap_servers='localhost:9092',
        group_id="my-group")
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

asyncio.create_task(consume_messages())
```

https://github.com/aio-libs/aiokafka