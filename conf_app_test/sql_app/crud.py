from datetime import date
from http.client import HTTPException
from turtle import end_fill
from xml.dom.pulldom import END_ELEMENT
from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException
from sqlalchemy import and_, or_
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

'''
Query Document
https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying

# Userテーブルのnameカラムをすべて取得
users = session.query(User).all()
# カラムを絞って取得
users = session.query(User.name, User.email).all()

# 完全一致
users = session.query(User).\
    filter(User.name=="name").\
    all()

# In
names = ['taro', 'jiro', 'ichiro']
brothers = session.query(User).\
    filter(User.name.in_(names)).\
    all()

# order by
from sqlalchemy import desc
users = session.query(User).\
    order_by(desc(User.created_at)).\
    all()

# distinct
from sqlalchemy import distinct
user_name = session.query(distinct(User.name)).\
    all()

# JOIN
user_name = session.query(User, UserSocial).\
    join(UserSocial, User.id==UserSocial.user_id).\
    all()

# LEFT JOIN
user_name = session.query(User, UserSocial).\
    outerjoin(UserSocial, User.id==UserSocial.user_id).\
    all()

# union 
tag_genre = session.query(Tag).\
    union(session.query(Genre)).\
    all()


'''

def get_organizations(db: Session, limit: int = 100, q_name: str = None):
    model = models.Organization
    q_list = [] 
    if q_name:
        q_name = model.name.like(f"%{q_name}%")
        q_list.append(q_name)

    q_all = and_(*q_list)
    queryset = db.query(model).filter(q_all).all()
    return queryset

def create_organization(db: Session, data: schemas.OrganizationCreate):
    model = models.Organization
    new_record = model(
        name = data.name,
        high_org = data.high_org,
        active = data.active
    )
    print("#######", new_record, "########")
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def create_employee(db: Session, data: schemas.EmployeeCreate):
    model = models.Employee
    new_record = model(
        employee_id = data.employee_id,
        name = data.name,
        organization = data.organization,
        email = data.email,
        active = data.active
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def create_theme(db: Session, data: schemas.ThemeCreate):
    model = models.Theme
    new_record = model(
        name = data.name,
        active = data.active
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def create_kwcategory(db: Session, data: schemas.KwCategoryCreate):
    model = models.KwCategory
    new_record = model(
        name = data.name,
        active = data.active
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def create_keyword(db: Session, data: schemas.KeyWordCreate):
    model = models.KeyWord
    new_record = model(
        name = data.name,
        category = data.category,
        active = data.active
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def create_meeting(db: Session, data: schemas.MeetingCreate):
    model = models.Meeting
    new_record = model(
        name = data.name,
        description = data.description,
        members = data.members,
        responsible_person = data.responsible_person,
        host_org = data.host_org,
        periodic = data.periodic,
        active = data.active
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


def create_ics(db: Session, data: schemas.ICSCreate):
    model = models.ICS
    new_record = model(
        name = data.name,
        active = data.active
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def create_schedule(db: Session, data: schemas.ScheduleCreate):
    model = models.Schedule
    new_record = model(
        meeting = data.meeting,
        date = data.date,
        start_time = data.start_time,
        end_time = data.end_time,
        facilitator = data.facilitator,
        members = data.members,
        link = data.link,
        ics = data.ics,
        active = data.active
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def create_entry(db: Session, data: schemas.EntryCreate):
    model = models.Entry
    new_record = model(
        schedule = data.schedule,
        purpose = data.purpose,
        theme = data.theme,
        title = data.title,
        keywords = data.keywords,
        presentor = data.presentor,
        time = data.time,
        material_link = data.material_link,
        material_fixed = data.material_fixed,
        active = data.active
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record
# # ユーザー一覧取得
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()
#     # offset: 最初の方のデータを除外する場合に設定（0の場合除外無しなので無くて良い）
#     # limit: 件数の上限

# # 会議室一覧取得
# def get_rooms(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Room).offset(skip).limit(limit).all()

# # 予約一覧取得
# def get_bookings(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Booking).offset(skip).limit(limit).all()


# # ユーザー登録
# def create_user(db: Session, user: schemas.User):
#     db_user = models.User(username=user.username)  # DBインスタンス作成
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# # 会議室登録
# def create_room(db: Session, room: schemas.Room):
#     db_room = models.Room(room_name=room.room_name, capacity=room.capacity)  # DBインスタンス作成
#     db.add(db_room)
#     db.commit()
#     db.refresh(db_room)
#     return db_room

# # 予約登録
# def create_booking(db: Session, booking: schemas.Booking):
#     db_booked = db.query(models.Booking).\
#         filter(models.Booking.room_id == booking.room_id).\
#         filter(models.Booking.end_datetime > booking.start_datetime).\
#         filter(models.Booking.start_datetime < booking.end_datetime).\
#         all()
    
#     if len(db_booked) == 0:  # 重複なしの場合予約可能
#         db_booking = models.Booking(
#             user_id = booking.user_id,
#             room_id = booking.room_id,
#             booked_num = booking.booked_num,
#             start_datetime = booking.start_datetime,
#             end_datetime = booking.end_datetime
#         )  # DBインスタンス作成
#         db.add(db_booking)
#         db.commit()
#         db.refresh(db_booking)
#         return db_booking

#     else:
#         raise HTTPException(status_code=404, detail="予約重複")
#         # apiは404をレスポンスとして返すため、app側では404に対する処理を記述