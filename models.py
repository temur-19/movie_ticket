
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey


from database import Base



class User(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    name:Mapped[str] = mapped_column(String(length=100))
    lastname:Mapped[str] = mapped_column(String(length=100))
    email:Mapped[str] = mapped_column(String(),unique=True)
    hashed_password:Mapped[str] = mapped_column(String(length=200))
    tickets:Mapped['Ticket'] = relationship(back_populates='user')



class Ticket(Base):
    __tablename__ = 'tickets'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_name: Mapped[str] = mapped_column(String(length=100))
    customer_name: Mapped[str] = mapped_column(String(length=100))
    seat_number: Mapped[int] = mapped_column(Integer)
    is_vip: Mapped[bool] = mapped_column(Boolean, default=False)
    price: Mapped[float] = mapped_column(Float)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    user:Mapped['User']  = relationship(back_populates='tickets')
