from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from schemas import TicketCreate, TicketOut, UserCreate, UserOut, Token
from database import Base, get_db, engine
from models import Ticket   
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
import security
from models import User
from sqlalchemy.orm import Session


Base.metadata.create_all(bind=engine)
api_router = APIRouter(prefix='/api/tickets')



from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token yaroqsiz yoki muddati tugagan"
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = db.scalar(select(User).where(User.id == int(user_id)))
    if user is None:
        raise credentials_exception
    return user


@api_router.post('/users', response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == user_in.email))
    if user:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

    user_dict = user_in.model_dump()
    hashed_password = security.get_password_hash(user_dict.pop("password"))
    
    user = User(**user_dict, hashed_password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@api_router.post('/users/login', response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == form.username))
    if not user:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud emas")

    if not security.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="email yoki parol noto'g'ri")

    access_token = security.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@api_router.get('/users/me', response_model=UserOut)
def get_current_user_profile(current_user: UserOut = Depends(get_current_user)):
    return current_user

@api_router.post('/', response_model=TicketOut)
def create_ticket(ticket_in: TicketCreate, db = Depends(get_db)):
    stmt = select(Ticket).where(Ticket.movie_name == ticket_in.movie_name,
                                Ticket.seat_number == ticket_in.seat_number)
    existing_ticket = db.scalar(stmt)
    if existing_ticket:
        raise HTTPException(status_code=404, detail="Bu bilet allaqachon sotilgan.")

    price = 80000.00 if ticket_in.is_vip else 40000.00

    ticket = Ticket(
        **ticket_in.model_dump(),
        price=price
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket






@api_router.get('/', response_model=List[TicketOut])
def get_tickets(db = Depends(get_db)):
    stmt = select(Ticket)
    tickets = db.scalars(stmt).all()
    return tickets