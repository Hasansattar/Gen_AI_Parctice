This FastAPI application manages products, categories, and images through REST API endpoints, integrating with Kafka for real-time message handling and Protobuf for serialization. Here’s a step-by-step breakdown


### Folder structure


```python
product-service/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── product_model.py
│   ├── db_engine.py
│   ├── settings.py
│   └── consumers/
│   │   ├── __init__.py
│   │   └── category_consumer.py
│   │   └── product_consumer.py
│   └── producers/
│   │   ├── __init__.py
│   │   └── product_producer.py
│   ├── product_pb2.py
│   ├── category_pb2.py
│   ├── image_pb2.py
└── pyproject.toml

```

# app/main.py

### Imports

- **Libraries**: Imports `FastAPI`, `Depends`, `HTTPException` from fastapi, and `Session` and `select` from sqlmodel for database interaction.
- **Type Hints**: `Annotated`, `AsyncGenerator` are used for defining dependencies and asynchronous generators.
- **Database Setup**: `create_db_and_tables` and `engine` from `app.db_engine` initialize the database and create tables.
- **Model Imports**: Imports `Product`, `Category`, and `Image` classes and their CRUD models (`ProductCreate`, `CategoryCreate`, `ImageCreate`, etc.) from `app.models.product_model`.
- **Kafka Consumers**: Imports consumer functions for handling messages related to `Product`, `Category`, and `Image` from app.consumers.product_consumer, category_consumer, and image_consumer.
- **Protobuf Models**: Imports protobuf schema for data serialization from `product_pb2`, `category_pb2`, and `image_pb2`.
- **Kafka Producer**: Imports Kafka producer dependencies for handling event messaging with Kafka.

### Application Setup
#### 1. Lifespan Event:

- This `@asynccontextmanager` function sets up tasks that consume messages from Kafka topics.
- Each task (`task0`, `task1`, etc.) calls a consumer function that subscribes to a Kafka topic, such as consume_messages_add_product(`"products_add"`, `"broker:19092"`) which listens for new product addition messages.
- `create_db_and_tables()` ensures database tables are initialized before the application yields control to API operations.


#### 2. FastAPI Instance:

- The `app` instance of FastAPI initializes the main application, with a lifespan event.
- Metadata (title and version) is added.



#### 3. Session Dependency:
- `get_session()` creates and yields a SQLAlchemy session connected to the database via `engine`.


### Routes and Endpoints

#### 1. Root Endpoint `(@app.get("/"))`
- Returns a welcome message when the base URL is accessed.


**Product Endpoints**

#### 2. Add Product `(@app.post("/products/"))`:

- Accepts a `ProductCreate` model, serializes it into a protobuf format, and sends it to the `products_add` Kafka topic for processing.
- Uses `AIOKafkaProducer` to send messages, asynchronously ensuring that product data is processed.



#### 3. List Products `(@app.get("/products/"))`:

- Fetches products from the database.
- Iterates through each product, converting it to protobuf format, serializes it, and sends to Kafka's `products_list` topic.


#### 4. Get Product by ID `(@app.get("/products/{product_id}"))`:


- Fetches a single product by `product_id`.
- If the product exists, it serializes and sends the product information to Kafka for further processing or distribution.
- Raises a 404 error if the product doesn’t exist


#### 5. Delete Product `(@app.delete("/products/{product_id}"))`:


- Deletes a product if it exists by sending a delete message to the `products_delete` topic in Kafka.
- Returns a success message or raises a 404 error if the product is not found.



#### 6. Update Product `(@app.put("/products/{product_id}"))`:

- Accepts `ProductUpdate` data for partially updating a product's information.
- Updates only the provided fields, serializes the data to protobuf format, and sends it to the `products_update` Kafka topic.
- Returns an error message if the Kafka producer fails.


### Category Endpoints


#### 7. Add Category `(@app.post("/categories/"))`:
- Creates a new category by sending the serialized category data to `categories_add` Kafka topic.

#### 8. List Categories `(@app.get("/categories/"))`:

- Retrieves all categories, serializes them, and publishes them on `categories_list` topic for consumption.

#### 9. Get Category by ID `(@app.get("/categories/{category_id}"))`:

- Retrieves a category by `category_id`, serializes the data, and sends it to `categories_get` Kafka topic.


#### 10. Delete Category `(@app.delete("/categories/{category_id}"))`:

- Deletes a category, if it exists, and sends a delete message to `categories_delete` Kafka topic.
- Returns an error if the category is not found.



#### 11. Update Category `(@app.put("/categories/{category_id}"))`:

- Partially updates the specified category fields and sends updated data to `categories_update` Kafka topic.

### Image Endpoints



#### 12. Add Image `(@app.post("/images/"))`:
- Adds a new image for a product, serializing it to protobuf and sending it to `images_add` Kafka topic.

#### 13. List Images `(@app.get("/images/"))`:
- Retrieves and lists all images associated with products, publishing them to `images_list`.


### Asynchronous Handling

- The entire application leverages asynchronous handling with FastAPI and Kafka's `AIOKafkaProducer` for non-blocking communication.
- Each route that interacts with Kafka uses the `await` keyword, indicating asynchronous message production or data fetching, enhancing the app’s responsiveness and handling of multiple concurrent requests

# Summary
This application:

- Uses FastAPI for REST API structure.
- SQLModel for data handling.
- Kafka for asynchronous event messaging to manage products, categories, and images.
- Protobuf serialization for efficient data handling across Kafka

# Prototype Methods

##### 1- we have already proto compiler into running container.
##### 2- go inside the container : `docker exec -it container-name /bin/bash`
##### 3- go to `todo.proto` file
##### 4- Run this command check version: ``protoc --version``
##### 5- Run this command for compile the file: (1)  `protoc --python_out=. product.proto` (2)  `protoc --python_out=. category.proto` (3) `protoc --python_out=. image.proto`

# Commmands

### Run Docker containers
**1. docker compose down**
**2. docker compose up -d**
**3. docker compose up --build -d**
**4. docker compose logs service-name**
**5. docker exec -it container-name /bin/bash**

### 1. Check the Container Logs
Use the following command to check the logs of the services running on ports that don't show the website:


```bash
docker-compose logs service_name

```
For example:
```bash
docker-compose logs todo-service
docker-compose logs api

```
This will help identify if there's an error in the service startup or if the application is throwing an error.


## Here is a sample query to join both data product model data and Category model data

### Sample PostgreSQL Query
Assuming you have the following tables based on your model:
- **Table**: `productcreate`
- - `id` (Primary Key)
- - `name`
- - `description`
- - `price`
- - `stock_quantity`
- - `category_id` (Foreign Key referencing categorycreate.id)

- **Table**: `categorycreate`
- - `id` (Primary Key)
- - `name`
- - `description`


## SQL Query Example 1.


```sql
SELECT
    p.*,
    c.id AS category_id,
    c.name AS category_name,
    c.description AS category_description
FROM
    productcreate p
LEFT JOIN
    categorycreate c ON p.category_id = c.id;
```
#### Explanation of the Query
**SELECT Statement**:
- `p.*`: Selects all columns from the productcreate table (aliased as p).
- `c.id AS category_id:` Retrieves the category ID and aliases it.
- `c.name AS category_name:` Retrieves the category name.
- `c.description AS category_description`: Retrieves the category description.

**FROM Clause**:
- `productcreate p`: Specifies the productcreate table as the main table to query from, using p as an alias.

**LEFT JOIN Clause**:

- Joins the `categorycreate` table (aliased as c) with the `productcreate` table on the condition that `p.category_id` matches `c.id`.
- A `LEFT JOIN` ensures that all products are included, even if they do not have a corresponding category


## SQL Query Example 2.


```sql
SELECT
    p.*,                                         -- Select all columns from the `productcreate` table
    c.id AS category_id,                        -- Select the `id` from the `categorycreate` table as `category_id`
    c.name AS category_name,                     -- Select the `name` from the `categorycreate` table as `category_name`
    c.description AS category_description,       -- Select the `description` from the `categorycreate` table as `category_description`
    i.id AS image_id,                           -- Select the `id` from the `imagecreate` table as `image_id`
    i.image_url AS image_url                    -- Select the `image_url` from the `imagecreate` table
FROM
    productcreate p
LEFT JOIN
    categorycreate c ON p.category_id = c.id    -- Join `productcreate` and `categorycreate` on matching category IDs
LEFT JOIN
    imagecreate i ON p.id = i.product_id        -- Join `productcreate` and `imagecreate` on matching product IDs

```
## SQL Query Example 3.
Show the all products and their categories and product images
```sql
SELECT
    p.*,                                         -- Select all columns from the `productcreate` table
    c.id AS category_id,                        -- Select the `id` from the `categorycreate` table as `category_id`
    c.name AS category_name,                     -- Select the `name` from the `categorycreate` table as `category_name`
    c.description AS category_description,       -- Select the `description` from the `categorycreate` table as `category_description`
    i.id AS image_id,                           -- Select the `id` from the `imagecreate` table as `image_id`
    i.image_url AS image_url,                    -- Select the `image_url` from the `imagecreate` table
    i.product_id AS product_id 
FROM
    productcreate p
LEFT JOIN
    categorycreate c ON p.category_id = c.id    -- Join `productcreate` and `categorycreate` on matching category IDs
LEFT JOIN
    imagecreate i ON p.id = i.product_id        -- Join `productcreate` and `imagecreate` on matching product IDs

```

## SQL Query Example 4.
Only show those products where product IDs of the product and image product IDs of the product will be same


```sql
SELECT
    p.*,                                         -- Select all columns from the `productcreate` table
    c.id AS category_id,                        -- Select the `id` from the `categorycreate` table as `category_id`
    c.name AS category_name,                     -- Select the `name` from the `categorycreate` table as `category_name`
    c.description AS category_description,       -- Select the `description` from the `categorycreate` table as `category_description`
    i.id AS image_id,                           -- Select the `id` from the `imagecreate` table as `image_id`
    i.image_url AS image_url,                    -- Select the `image_url` from the `imagecreate` table
    i.product_id AS image_product_id             -- Select the `product_id` from the `imagecreate` table as `image_product_id`
FROM
    productcreate p
LEFT JOIN
    categorycreate c ON p.category_id = c.id    -- Join `productcreate` and `categorycreate` on matching category IDs
LEFT JOIN
    imagecreate i ON p.id = i.product_id        -- Join `productcreate` and `imagecreate` on matching product IDs
WHERE
    p.id = product_id OR i.image_url = image_url  -- Filter based on product ID or image URL

```