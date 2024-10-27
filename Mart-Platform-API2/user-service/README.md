
# Important Links related to user-service:


- https://fastapi.tiangolo.com/tutorial/response-model/#add-an-output-model
- https://fastapi.tiangolo.com/tutorial/response-model/#annotate-a-response-subclass
- https://fastapi.tiangolo.com/tutorial/request-forms/
- https://fastapi.tiangolo.com/tutorial/request-form-models/#check-the-docs
- https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/#add-dependencies-to-the-path-operation-decorator
- https://fastapi.tiangolo.com/tutorial/security/first-steps/#how-it-looks
- https://fastapi.tiangolo.com/tutorial/security/get-current-user/#create-a-user-model
- https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#scope
- https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords



# FastAPI User and Event Management API

## Overview
This API provides endpoints for managing users, user profiles, and events in a FastAPI application. It includes user authentication and allows the creation, retrieval, updating, and deletion of users and events.

## Features
- User Management
- User Profile Management
- Event Management
- User Authentication

## API Structure

### 1. Root Endpoint
- **GET** `/`
  - **Description:** Welcome message.

### 2. User Management
- **POST** `/users/`
  - **Description:** Create a new user.
  
- **GET** `/users/`
  - **Description:** List all users.
  
- **GET** `/users/{user_id}`
  - **Description:** Get a user by ID.
  
- **PUT** `/users/{user_id}`
  - **Description:** Update user information.

### 3. User Profile Management
- **POST** `/profiles/`
  - **Description:** Create a user profile.
  
- **GET** `/profiles/`
  - **Description:** List all user profiles.
  
- **GET** `/profiles/{profile_id}`
  - **Description:** Get a profile by ID.
  
- **PUT** `/profiles/{profile_id}`
  - **Description:** Update a user profile.

### 4. Event Management
- **POST** `/events/`
  - **Description:** Create a new event.
  
- **GET** `/events/`
  - **Description:** List all events.
  
- **GET** `/events/{event_id}`
  - **Description:** Get an event by ID.
  
- **PUT** `/events/{event_id}`
  - **Description:** Update an event.

### 5. User Authentication
- **POST** `/login/`
  - **Description:** Authenticate a user and return a JWT token.
  
- **POST** `/reset-password/`
  - **Description:** Request a password reset.

## Technologies Used
- FastAPI
- Pydantic
- SQLAlchemy (or any ORM you are using)
- JWT (for authentication)
- (Add any other technologies or libraries used)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo



# Prototype Methods

##### 1- we have already proto compiler into running container.
##### 2- go inside the container : `docker exec -it container-name /bin/bash`
##### 3- go to `todo.proto` file
##### 4- Run this command check version: ``protoc --version``
##### 5- Run this command for compile the file: (1)  `protoc --python_out=. user.proto`

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




