from pathlib import Path
import json
from sqlmodel import Session, select
from app.models.database import engine
from app.models.schemas import Department, Doctor

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "hospital-data.json"


def list_doctors_by_department(department_name: str) -> list[dict]:
    with Session(engine) as session:
        statement = select(Department).where(Department.name.ilike(department_name))
        department = session.exec(statement).first()
        if not department:
            return []

        statement = select(Doctor).where(Doctor.department_id == department.id)
        doctors = session.exec(statement).all()

        return [
            {
                "id": doctor.id,
                "title": doctor.title,
                "first_name": doctor.first_name,
                "last_name": doctor.last_name,
                "experience": doctor.experience,
                "department_id": doctor.department_id,
            }
            for doctor in doctors
        ]


def seed_database_if_empty() -> None:
    with Session(engine) as session:
        if session.exec(select(Department)).first():
            return

        if not DATA_FILE.exists():
            raise FileNotFoundError(f"Hospital data file not found: {DATA_FILE}")

        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        for dept_data in data.get("departments", []):
            db_dept = Department(name=dept_data["name"])
            session.add(db_dept)
            session.flush()

            for doc_data in dept_data.get("doctors", []):
                db_doctor = Doctor(
                    id=doc_data.get("id"),
                    title=doc_data.get("title"),
                    first_name=doc_data.get("first_name"),
                    last_name=doc_data.get("last_name"),
                    experience=doc_data.get("experience"),
                    department_id=db_dept.id,
                )
                session.add(db_doctor)

        session.commit()
