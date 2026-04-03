from fastapi import FastAPI
import json
import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"
app = FastAPI()

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
    You are a medical assistant. Return a JSON object with the key "Guess".
    Departments: Cardiology, Pediatric Allergy, Pediatric Surgery, Anesthesiology, Neurosurgery, Nutrition and Dietetics, Oral and Dental Health, General Surgery.
    
    Patient symptoms: {symptoms}
    
    Return ONLY the JSON.
    Example output: {{"Guess": "Cardiology"}}
    """
    return ollama_request(prompt)


def list_of_doctors(department: str) -> list: 
    with open("data/hospital-data.json", "r") as f:
        data = json.load(f)
    departments = data.get("departments", [])
    for dept in departments:
        if dept.get("name").lower() == department.lower():
            return dept.get("doctors", [])
    return []

#@app.post("/")
#async def patient_info(prompt: str):
#    #taking the symptoms from the user and sending it to the function that will decide the department.
#    guess = decide_department(prompt)
#    department = guess.get("Guess")

guess = decide_department("I cant masturbate.")
print(guess)

try:
    guess_dict = json.loads(guess)
except json.JSONDecodeError:
    print("Failed to parse the response as JSON.")

print(list_of_doctors(guess_dict.get("Guess")))