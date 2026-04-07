from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime , timezone

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    symptoms: str
    recommendations: List["Recommendation"] = Relationship(back_populates="user")
    reservations: List["Reservation"] = Relationship(back_populates="patient")

class Recommendation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    department: str
    importance: int
    reason: str
    
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="recommendations")
    
    suggested_doctors_json: Optional[str] = Field(default=None) 

class Department(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    
    doctors: List["Doctor"] = Relationship(back_populates="department")

class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str  # Dr., Uzm. Dr. vb.
    first_name: str
    last_name: str
    experience: int
    
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    department: Optional[Department] = Relationship(back_populates="doctors")
    
    reservations: List["Reservation"] = Relationship(back_populates="doctor")

class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="user.id")
    patient: Optional[User] = Relationship(back_populates="reservations")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    appointment_time: datetime = Field(index=True)
    doctor_id: int = Field(foreign_key="doctor.id")
    doctor: Optional[Doctor] = Relationship(back_populates="reservations")