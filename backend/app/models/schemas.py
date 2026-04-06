from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime , timezone

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    symptoms: str
    # Bir kullanıcının birden fazla geçmiş tavsiyesi olabilir
    recommendations: List["Recommendation"] = Relationship(back_populates="user")

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
    
    # Department -> Doctor ilişkisi (Bir departmanda çok doktor olur)
    doctors: List["Doctor"] = Relationship(back_populates="department")

class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str  # Dr., Uzm. Dr. vb.
    first_name: str
    last_name: str
    experience: int
    
    # Doctor -> Department ilişkisi
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    department: Optional[Department] = Relationship(back_populates="doctors")
    
    # Rezervasyonlar için ilişki (İlerisi için)
    reservations: List["Reservation"] = Relationship(back_populates="doctor")

class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    appointment_time: datetime = Field(index=True)
    doctor_id: int = Field(foreign_key="doctor.id")
    doctor: Doctor = Relationship(back_populates="reservations")