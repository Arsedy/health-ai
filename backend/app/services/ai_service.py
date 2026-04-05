import json
from pydantic import BaseModel
import httpx
from pathlib import Path
import os

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "hospital-data.json"

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434") # Use environment variable or default to localhost
OLLAMA_API_URL = f"{OLLAMA_BASE_URL}/api/generate"


#AI model request function
async  def ollama_request(prompt: str):
    payload = {
        'model': 'qwen2.5:7b-instruct-q4_K_M',
        'prompt': prompt,
        'stream': False,
        'format': 'json',
        'options': {'temperature': 0}
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()
            
            full_response = response.json()
            raw_content = full_response.get('response', '{}')
           
            if isinstance(raw_content, str):
                return json.loads(raw_content)
            return raw_content
            
        except httpx.ConnectError:
            return {"error": f"Failed to connect to Ollama at : {OLLAMA_API_URL}"}
        except Exception as e:
            return {"error": str(e)}
    

async def analyze_symptom(symptoms: str):
    valid_departments = [
        "Cardiology", "Pediatric Allergy", "Pediatric Surgery", 
        "Anesthesiology", "Neurosurgery", "Nutrition and Dietetics", 
        "Oral and Dental Health", "General Surgery", 
        "Pediatric Endocrinology", "Urology", "Dermatology", "Neurology"
    ]
    
    prompt = f"""
    You are a medical triage assistant. Your ONLY job is to map symptoms to one of the specific departments listed below.
    
    ALLOWED DEPARTMENTS:
    {", ".join(valid_departments)}

    STRICT RULES:
    1. You MUST choose a department ONLY from the ALLOWED DEPARTMENTS list above.
    2. Do NOT create new department names.
    3. If you are unsure or the department is not in the list, default to "General Surgery".
    4. Return a JSON object with "Department" and "Importance" (1-10) keys.

    Patient symptoms: {symptoms}
    """

    return await ollama_request(prompt)


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
    symptom_analysis = await analyze_symptom(symptoms)
    print(f"AI Raw response: {symptom_analysis}")

    if not symptom_analysis or "error" in symptom_analysis:
        return {
            "department": "Unknown",
            "importance": 0,
            "reason": symptoms,
            "suggested_doctors": [],
            "status_message": "The model failed to analyze the symptoms. Please try again later.",
            "error": symptom_analysis
        }

    try:
        department = symptom_analysis.get("Department")
        importance = symptom_analysis.get("Importance")
    except AttributeError:
        return {"error": "Failed to parse department or importance from AI response."}

    doctors = list_of_doctors(department)

    return {
        "department": department,
        "importance": importance,
        "reason": symptoms,
        "suggested_doctors": doctors
        }
    

