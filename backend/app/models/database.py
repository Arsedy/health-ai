from sqlmodel import SQLModel, create_engine, Session , select
import os
from app.models.schemas import Department, Doctor
import json

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session







#---- Database seeding function ----
def seed_data(engine):  
    with Session(engine) as session:
        statement = select(Department)
        results = session.exec(statement).first()
        
        if not results:
            print("Database is empty. Seeding data...")
            # Get the correct path to the JSON file relative to this module
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            json_path = os.path.join(current_dir, "data", "hospital-data.json")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            for dept_data in data["departments"]:
                db_dept = Department(name=dept_data["name"])
                session.add(db_dept)
                session.flush() 
                
                for doc_data in dept_data["doctors"]:
                    db_doctor = Doctor(
                        id=doc_data["id"],
                        title=doc_data["title"],
                        first_name=doc_data["first_name"],
                        last_name=doc_data["last_name"],
                        experience=doc_data["experience"],
                        department_id=db_dept.id
                    )
                    session.add(db_doctor)
            session.commit()
            print("Data successfully loaded!")