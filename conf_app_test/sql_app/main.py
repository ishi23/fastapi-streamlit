from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal, engine
import models, schemas, crud


# データベース作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
Organization
Employee
Theme
KwCategory
KeyWord
Meeting
ICS
Schedule
Entry

'''


@app.get("/")
async def index():
    return {"message": "Success"}

@app.get("/organizations", response_model=List[schemas.Organization])
async def read_users(
    limit: int = 100, 
    db: Session = Depends(get_db),
    q_name: str = None
    ):
    users = crud.get_organizations(db=db, limit=limit, q_name=q_name)
    return users

# @app.get("/rooms", response_model=List[schemas.Room])
# async def read_rooms(skip: int =0, limit: int = 100, db: Session = Depends(get_db)):
#     rooms = crud.get_rooms(db=db, skip=skip, limit=limit)
#     return rooms

# @app.get("/bookings", response_model=List[schemas.Booking])
# async def read_bookings(skip: int =0, limit: int = 100, db: Session = Depends(get_db)):
#     bookings = crud.get_bookings(db=db, skip=skip, limit=limit)
#     return bookings

@app.post("/organizations", response_model=schemas.Organization)
async def create_organization(data: schemas.OrganizationCreate, db: Session = Depends(get_db)):
    organization = crud.create_organization(db=db, data=data)
    return organization

@app.post("/employees", response_model=schemas.Employee)
async def create_employee(data: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    employee = crud.create_employee(db=db, data=data)
    return employee

@app.post("/themes", response_model=schemas.Theme)
async def create_theme(data: schemas.ThemeCreate, db: Session = Depends(get_db)):
    theme = crud.create_theme(db=db, data=data)
    return theme

@app.post("/kwcategories", response_model=schemas.KwCategory)
async def create_kwcategory(data: schemas.KwCategoryCreate, db: Session = Depends(get_db)):
    kwcategory = crud.create_kwcategory(db=db, data=data)
    return kwcategory

@app.post("/keywords", response_model=schemas.KeyWord)
async def create_keyword(data: schemas.KeyWordCreate, db: Session = Depends(get_db)):
    keyword = crud.create_keyword(db=db, data=data)
    return keyword

@app.post("/meetings", response_model=schemas.Meeting)
async def create_meeting(data: schemas.MeetingCreate, db: Session = Depends(get_db)):
    meeting = crud.create_meeting(db=db, data=data)
    return meeting

@app.post("/icss", response_model=schemas.ICS)
async def create_ics(data: schemas.ICSCreate, db: Session = Depends(get_db)):
    ics = crud.create_ics(db=db, data=data)
    return ics

@app.post("/schedules", response_model=schemas.Schedule)
async def create_schedule(data: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    schedule = crud.create_schedule(db=db, data=data)
    return schedule

@app.post("/entries", response_model=schemas.Entry)
async def create_entry(data: schemas.EntryCreate, db: Session = Depends(get_db)):
    entry = crud.create_entry(db=db, data=data)
    return entry

# @app.post("/users", response_model=schemas.User)
# async def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     user = crud.create_user(db=db, user=user)
#     return user

# @app.post("/rooms", response_model=schemas.Room)
# async def create_rooms(room: schemas.RoomCreate, db: Session = Depends(get_db)):
#     room = crud.create_room(db=db, room=room)
#     return room

# @app.post("/bookings", response_model=schemas.Booking)
# async def create_bookings(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
#     booking = crud.create_booking(db=db, booking=booking)
#     return booking
