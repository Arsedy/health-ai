import json
from pydantic import BaseModel
import requests
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "hospital-data.json"

OLLAMA_API_URL = "http://localhost:11434/api/generate"


#AI model request function
def ollama_request(prompt: str):
    payload = {
    'model': 'qwen2.5:7b-instruct-q4_K_M',
    'prompt': prompt,
    'stream' : False,
    'format' : 'json',
    'options': {
        'temperature': 0
        }
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    return response.json().get('response')

def decide_department(symptoms: str):
    prompt = f"""
    You are a medical assistant. Return a JSON object with the key "Department".
    Departments:Cardiology
                Pediatric Allergy
                Pediatric Surgery
                Anesthesiology
                Neurosurgery
                Nutrition and Dietetics
                Oral and Dental Health
                General Surgery
                Pediatric Endocrinology
                Urology
                Dermatology
                Neurology

    Return ONLY the JSON.
    Example output: {{"Department": "Cardiology"}}
    Example output if the symptoms are not clear: {{"Department": "General Surgery"}}

    Patient symptoms: {symptoms}
    """
    return ollama_request(prompt)


def list_of_doctors(department: str) -> list: 
    with open(DATA_DIR, "r") as f:
        data = json.load(f)
    departments = data.get("departments", [])
    for dept in departments:
        if dept.get("name").lower() == department.lower():
            return dept.get("doctors", [])
    return []

class Message(BaseModel):
    prompt: str


async def doctor_recommendation(symptoms: str) -> list:
    department = await decide_department(symptoms)
    print(f"AI recommended department log : {department}")
    try:
        department = json.loads(department).get("Department")
    except json.JSONDecodeError:
        return {"error": "Failed to parse department from AI response."}

    doctors = list_of_doctors(department)

    result ={
        "department": department,
        "reason": symptoms,
        "suggested_doctors": doctors
        }
    
    return result
