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


#### Model creation

- **1. Order**: Manages general order details, with status and payment status fields to track the lifecycle.
- **2. OrderItem**: Each item in the order, linked to a product and with details like quantity and per-unit price.
- **3. Payment**: Manages payment status and transaction details, linked to the order.
- **4. OrderStatusHistory**: Tracks each change in order status over time, useful for audits and tracking order lifecycle.
********************************************

# Order Service

The Order Service handles the complete lifecycle of customer orders, including order creation, item management, payment processing, and status tracking. This service enables efficient management of orders and tracks each stage, from initiation to completion.

## Table of Contents
- [Service Structure](#service-structure)
- [Models Overview](#models-overview)
- [Workflow Sequence](#workflow-sequence)
- [Database Table Details](#database-table-details)
- [Endpoints](#endpoints)

## Service Structure

The Order Service consists of several models representing different stages and components of an order. These models help manage order information, including items, payments, and historical status changes.

## Models Overview

### 1. **OrderBase**
   - Defines the base properties of an order, including `user_id`, `status`, `total_amount`, `payment_status`, `shipping_address`, and `order_date`.
   - Used as a foundation for the `OrderCreate` and `Order` models.

### 2. **OrderCreate**
   - Represents the database model for creating and persisting new orders.
   - Includes a one-to-many relationship with `OrderItemCreate`.

### 3. **Order**
   - Read model for retrieving order details along with associated items.
   - Links to `OrderItem` to retrieve a list of items within an order.

### 4. **OrderItemBase**
   - Defines the base properties of an order item, including `product_id`, `quantity`, `price_per_unit`, and `total_price`.

### 5. **OrderItemCreate**
   - Database model for creating order items.
   - Associated with an order through `order_id`.

### 6. **PaymentBase**
   - Provides the base attributes for payment information, such as `amount`, `payment_method`, `status`, and `transaction_id`.

### 7. **PaymentCreate**
   - Model for creating a payment record linked to an order.
   - Includes a foreign key, `order_id`, to associate payments with orders.

### 8. **OrderStatusHistoryBase**
   - Base model for recording order status changes with attributes `status` and `timestamp`.

### 9. **OrderStatusHistoryCreate**
   - Model to persist the order status history linked to the `order_id` for tracking status changes over time.

## Workflow Sequence

The following sequence describes the typical initiation order and processing flow for each service in the Order Service:

### 1. **Order Creation (`OrderCreate`)**
   - **Initiate**: An order is created with basic details, such as `user_id`, `shipping_address`, and `total_amount`.
   - **Initial Status**: Orders start with a **pending** status.
   - **Database Table**: `OrderCreate`

### 2. **Order Item Creation (`OrderItemCreate`)**
   - **Initiate**: Once an order is created, items can be added using `OrderItemCreate`.
   - **Details Added**: Each item includes `product_id`, `quantity`, `price_per_unit`, and `total_price`.
   - **Database Table**: `OrderItemCreate`

### 3. **Payment Creation (`PaymentCreate`)**
   - **Initiate**: After order and items are confirmed, a payment entry is created.
   - **Initial Status**: Payments are initially marked as **pending**.
   - **Database Table**: `PaymentCreate`

### 4. **Order Status History (`OrderStatusHistoryCreate`)**
   - **Initiate**: Throughout the order lifecycle, updates to `status` are logged here.
   - **Details Recorded**: Records each status change and the associated timestamp.
   - **Database Table**: `OrderStatusHistoryCreate`

## Database Table Details

Each model represents a database table in SQLModel. Below is a summary of each table’s purpose and key fields:

| Table                  | Description                                     | Key Fields                                              |
|------------------------|-------------------------------------------------|---------------------------------------------------------|
| **OrderCreate**        | Stores order details and initial state          | `user_id`, `status`, `total_amount`, `order_date`       |
| **OrderItemCreate**    | Stores individual items within an order         | `product_id`, `quantity`, `price_per_unit`, `order_id`  |
| **PaymentCreate**      | Manages payment entries linked to orders        | `amount`, `payment_method`, `status`, `transaction_id`  |
| **OrderStatusHistoryCreate** | Tracks order status changes over time | `status`, `timestamp`, `order_id`                       |

## Endpoints

### 1. **Create Order**
   - **Endpoint**: `/orders/create`
   - **Method**: `POST`
   - **Description**: Initiates a new order and sets initial status to **pending**.

### 2. **Add Item to Order**
   - **Endpoint**: `/orders/{order_id}/items/add`
   - **Method**: `POST`
   - **Description**: Adds an item to an existing order, requiring `product_id`, `quantity`, and `price_per_unit`.

### 3. **Process Payment**
   - **Endpoint**: `/orders/{order_id}/payment`
   - **Method**: `POST`
   - **Description**: Processes a payment for an order. Sets initial payment status to **pending**.

### 4. **Update Order Status**
   - **Endpoint**: `/orders/{order_id}/status`
   - **Method**: `PATCH`
   - **Description**: Updates the order status and logs the change in `OrderStatusHistory`.

## Additional Information

- **SQLModel** is used to define the data models with constraints on fields such as required values, string lengths, and defaults for fields like `status` and `payment_status`.
- **Relationships** are used to link `Order`, `OrderItem`, and `Payment` models, enabling efficient retrieval of associated data.
  
This structure ensures clear tracking of each order and its components, facilitating efficient order management.

---


***************************************************




# Prototype Methods

##### 1- we have already proto compiler into running container.
##### 2- go inside the container : `docker exec -it container-name /bin/bash`
##### 3- go to `todo.proto` file
##### 4- Run this command check version: ``protoc --version``
##### 5- Run this command for compile the file: (1)  `protoc --python_out=. order.proto`

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




