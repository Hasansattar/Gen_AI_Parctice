# https://fastapi.tiangolo.com/tutorial/response-model/#add-an-output-model
# https://fastapi.tiangolo.com/tutorial/response-model/#annotate-a-response-subclass


# https://fastapi.tiangolo.com/tutorial/request-forms/
# https://fastapi.tiangolo.com/tutorial/request-form-models/#check-the-docs
# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/#add-dependencies-to-the-path-operation-decorator
# https://fastapi.tiangolo.com/tutorial/security/first-steps/#how-it-looks
# https://fastapi.tiangolo.com/tutorial/security/get-current-user/#create-a-user-model
# https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#scope
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords

from sqlmodel import SQLModel, Field, EmailStr


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str



# ===============================================================

class UserIn(SQLModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None
    
    
    
class UserOut(SQLModel):
    username: str
    email: EmailStr
    full_name: str | None = None   
    
    
    
    
    