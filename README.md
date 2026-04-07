# Health AI - Hospital Department Assistant

An intelligent AI-powered application that analyzes patient symptoms and recommends the appropriate hospital department, along with available doctors in that department.

## Features

- 🏥 **Smart Department Recommendation** - Uses AI to analyze patient symptoms and suggest the correct hospital department
- 👨‍⚕️ **Doctor Listing** - Returns available doctors in the recommended department
- 🤖 **AI-Powered Analysis** - Leverages Ollama for local, private symptom analysis
- ⚡ **Fast API** - Built with FastAPI for high performance and easy deployment
- 📱 **Simple Interface** - Accept natural language symptom descriptions like "I have a headache"

## Tech Stack

- **FastAPI** - Modern web framework for building APIs
- **SQLModel** - SQL ORM/query builder with type hints
- **PostgreSQL** - Relational database (via psycopg2)
- **Ollama** - Local LLM engine for AI-powered analysis
- **Pandas & NumPy** - Data processing and numerical computations
- **Python 3.8+** - Core programming language
- **Uvicorn** - ASGI server for running FastAPI applications
- **Docker & Docker Compose** - Containerization and orchestration

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- Ollama (download from [ollama.ai](https://ollama.ai))
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd health-ai
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

5. **Ensure Ollama is running:**
   - Start the Ollama service (it typically runs on `http://localhost:11434`)
   - Make sure you have an LLM model downloaded (e.g., `ollama pull qwen2.5:7b-instruct-q4_K_M`)

## Usage

### Starting the Application

Navigate to the backend directory and run the FastAPI development server:

```bash
cd backend
fastapi dev app/main.py
```

The API will be available at `http://localhost:8000`

## Docker Deployment

### Using Docker Compose

The project includes a `docker-compose.yml` file for easy deployment with all dependencies.

```bash
docker-compose up
```

The API will be available at `http://localhost:8000`

### Building Docker Image

```bash
docker build -t health-ai:latest backend/
```

### Running with Docker

```bash
docker run -p 8000:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 health-ai:latest
```

**Environment Variables:**
- `OLLAMA_HOST` - URL to Ollama service (default: http://localhost:11434)

#### POST `/analyze`

Analyzes patient symptoms and recommends the appropriate department with available doctors.

**Request:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "I have a headache and dizziness"}'
```

**Request Body:**
```json
{
  "symptoms": "string - Description of patient symptoms"
}
```

**Response:**
```json
{
  "department": "Pediatric Surgery",
  "importance": 10,
  "reason": "The symptoms of difficulty breathing and a continuous fever in a child require immediate attention to rule out serious conditions such as infections or obstructions.",
  "suggested_doctors": [
    {
      "id": 8,
      "title": "Specialist Dr.",
      "first_name": "Jaclyn",
      "last_name": "Danielot",
      "experience": 8
    },
    {
      "id": 9,
      "title": "Asst. Prof.",
      "first_name": "Aaron",
      "last_name": "Race",
      "experience": 17
    },
    {
      "id": 10,
      "title": "Assoc. Prof.",
      "first_name": "Correna",
      "last_name": "Aldersey",
      "experience": 18
    }
  ]
}
```

**Response Fields:**
- `department` (string) - Recommended hospital department
- `importance` (string) - Severity level of the condition (low/medium/high)
- `reason` (string) - Explanation for the recommendation
- `suggested_doctors` (array) - List of available doctors in the department

## Project Structure

```
health-ai/
├── README.md
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # Main FastAPI application
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       └── analyze.py
│   │   └── services/
│   │       ├── __init__.py
│   │       └── ai_service.py # AI integration service
│   └── data/
│       └── hospital-data.json # Hospital departments and doctors database
```
├── .venv/                 # Virtual environment (gitignored)
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## API Endpoints

### POST `/analyze`
Analyzes patient symptoms and returns department recommendation with available doctors.

**Request Body:**
```json
{
  "symptom": "I have a headache"
}
```

**Response:**
```json
{
  "symptom": "string",
  "department": "string",
  "confidence": "float",
  "doctors": [
    {
      "id": "int",
      "name": "string",
      "specialty": "string"
    }
  ]
}
```

## Data Format

The `hospital-data.json` file contains department and doctor information:

```json
{
  "departments": [
    {
      "id": 1,
      "name": "Neurology",
      "keywords": ["headache", "migraine", "brain", "dizziness"],
      "doctors": [
        {"id": 1, "name": "Dr. Smith", "specialty": "Headache Specialist"},
        {"id": 2, "name": "Dr. Johnson", "specialty": "Neurologist"}
      ]
    }
  ]
}
```

## Future Improvements

- [ ] Add multilingual support for symptom analysis
- [ ] Implement confidence scoring based on symptom severity
- [ ] Create a web UI for better user experience
- [ ] Add appointment booking integration
- [ ] Implement user history and personalized recommendations
- [ ] Add emergency alert system for critical symptoms
- [ ] Integrate with hospital management systems
- [ ] Add logging and monitoring
- [ ] Deployment configurations (Docker, cloud platforms)

## Development Notes

- Ensure Ollama is running before starting the application
- For production deployment, consider using a production ASGI server like Gunicorn
- Keep the `hospital-data.json` file updated with current department and doctor information
- Monitor AI model responses for accuracy and fine-tune prompts as needed

## Contributing

Feel free to submit issues and pull requests to improve the Health AI application.

## License

This project is open source and available under the MIT License.

---

**Last Updated:** April 2026