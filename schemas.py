from pydantic import BaseModel, Field,EmailStr


class TicketCreate(BaseModel):
    movie_name: str = Field(max_length=200)
    seat_number: int = Field(ge=1, le=50)
    customer_name: str = Field(max_length=100)
    is_vip: bool = False


class TicketOut(BaseModel):
    id: int = Field(ge=1)
    movie_name: str = Field(max_length=200)
    seat_number: int = Field(ge=1, le=50)
    customer_name: str = Field(max_length=100)
    is_vip: bool = False
    price: float = Field(default=0)


class UserBase(BaseModel):
    id:int = Field(ge=1)
    name:str = Field(max_length=100)
    lastname:str = Field(max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password:str = Field(min_length=6)

class UserOut(UserBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str