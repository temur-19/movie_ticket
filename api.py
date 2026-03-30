from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from schemas import TicketCreate, TicketOut
from database import Base, get_db, engine
from models import Ticket



Base.metadata.create_all(bind=engine)
api_router = APIRouter(prefix='/api/tickets')


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