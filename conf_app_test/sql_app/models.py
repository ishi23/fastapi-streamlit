# from enum import unique
# from xmlrpc.client import Boolean
# # from pyparsing import nullDebugAction
# from enum import unique
# from unicodedata import name
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Date, Time
from database import Base

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

class Organization(Base):
    __tablename__ = "organizations"
    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    high_org = Column(Integer, ForeignKey("organizations.pk"), index=True, nullable=True)
    active = Column(Boolean, index=True)

class Employee(Base):
    __tablename__ = "employees"
    pk = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    organization = Column(String, ForeignKey("organizations.pk"))
    email = Column(String, unique=True)
    active = Column(Boolean, index=True)

class Theme(Base):
    __tablename__ = "themes"
    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    active = Column(Boolean, index=True)

class KwCategory(Base):
    __tablename__ = "kwcategories"
    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)    
    active = Column(Boolean, index=True)

class KeyWord(Base):
    __tablename__ = "keywords"
    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(Integer, ForeignKey("kwcategories.pk"), index=True)
    active = Column(Boolean, index=True)

class Meeting(Base):
    __tablename__ = "meetings"
    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    members = Column(Integer, ForeignKey("employees.pk"), index=True)
    responsible_person = Column(Integer, ForeignKey("employees.pk"), index=True)
    host_org = Column(Integer, ForeignKey("organizations.pk"), index=True)
    periodic = Column(Boolean, index=True) 
    active = Column(Boolean, index=True)
    
class ICS(Base):
    __tablename__ = "icss"
    pk = Column(Integer, primary_key=True, index=True)
    pid = Column(String, unique=True, index=True)
    filepath = Column(String)
    active = Column(Boolean, index=True)

class Schedule(Base):
    __tablename__ = "schedules"
    pk = Column(Integer, primary_key=True, index=True)
    meeting = Column(Integer, ForeignKey("meetings.pk"), index=True)
    date = Column(Date, index=True)
    start_time = Column(Time)
    end_time = Column(Time)
    facilitator = Column(Integer, ForeignKey("employees.pk"), index=True)
    members = Column(Integer, ForeignKey("employees.pk"), index=True)
    link = Column(String)
    ics = Column(Integer, ForeignKey("icss.pk"), nullable=True)
    active = Column(Boolean, index=True)
    

class Entry(Base):
    __tablename__ = "entries"
    pk = Column(Integer, primary_key=True, index=True)
    schedule = Column(Integer, ForeignKey("schedules.pk"), index=True)
    purpose = Column(String, index=False)
    theme = Column(Integer, ForeignKey("themes.pk"), index=True)
    title = Column(String, index=True)
    keywords = Column(Integer, ForeignKey("keywords.pk"), index=True)
    presentor = Column(Integer, ForeignKey("employees.pk"), index=True)
    time = Column(Integer)
    material_link = Column(String)
    material_fixed = Column(Boolean)
    active = Column(Boolean, index=True)

