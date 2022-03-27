import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


class OrganizationCreate(BaseModel):
    name: str = Field(max_length=50)
    high_org: Optional[int]  # another Organization
    active: bool = Field(default=True)

class Organization(OrganizationCreate):
    pk: int

    class Config:
        orm_mode = True

class EmployeeCreate(BaseModel):
    employee_id: str = Field(max_length=50)
    name: str = Field(max_length=50)
    organization: int  # Organization
    email: str
    active: bool = Field(default=True)

class Employee(EmployeeCreate):
    pk: int

    class Config:
        orm_mode = True

class ThemeCreate(BaseModel):
    name: str = Field(max_length=50)
    active: bool = Field(default=True)

class Theme(ThemeCreate):
    pk: int

    class Config:
        orm_mode = True

class KwCategoryCreate(BaseModel):
    name: str = Field(max_length=50)
    active: bool = Field(default=True)

class KwCategory(KwCategoryCreate):
    pk: int

    class Config:
        orm_mode = True

class KeyWordCreate(BaseModel):
    name: str = Field(max_length=50)
    category: Optional[int]  # KwCategory
    active: bool = Field(default=True)

class KeyWord(KeyWordCreate):
    pk: int

    class Config:
        orm_mode = True

class MeetingCreate(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=300)
    members: List[int]  # Employee
    responsible_person: int  # Emmployee
    host_org: int  # Organization
    periodic: bool
    active: bool = Field(default=True)

class Meeting(MeetingCreate):
    pk: int

    class Config:
        orm_mode = True

class ICSCreate(BaseModel):
    name: str = Field(max_length=50)
    # pid: int
    active: bool = Field(default=True)

class ICS(ICSCreate):
    pk: int
    pid: str
    class Config:
        orm_mode = True


class ScheduleCreate(BaseModel):
    meeting: int  # Meeting
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time
    facilitator: int  # Employee
    members: List[int]  # Employee
    link: str
    ics: Optional[int]  # ICS
    active: bool

class Schedule(ScheduleCreate):
    pk: int

    class Config:
        orm_mode = True

class EntryCreate(BaseModel):
    schedule: int  # Schedule
    purpose: str
    theme: int  # Theme
    title: str
    keywords: List[int]  # KeyWord
    presentor: int  # Employee
    time: int
    material_link: str
    material_fixed: bool
    active: bool

class Entry(EntryCreate):
    pk: int

    class Config:
        orm_mode = True
