# AI Candidate Selection and Resume Ranking

An AI-powered recruitment screening tool that analyzes a job description, evaluates candidate resumes against the extracted criteria, and ranks candidates by overall fit.

## Features

- Upload a job description as PDF or DOCX
- Upload multiple candidate resumes as PDF or DOCX
- Extract structured hiring criteria from the job description
- Score candidates against must-have skills, nice-to-have skills, experience, education, and responsibilities
- Generate strengths, weaknesses, confidence scores, justifications, and category scores
- Rank candidates from strongest to weakest match
- Run locally with Python or Docker

## Tech Stack

- Python 3.11
- FastAPI
- Streamlit
- LangChain
- Ollama
- Pydantic
- PyMuPDF
- docx2txt
- Docker / Docker Compose

## Project Structure

```text
.
├── backend/
│   ├── main.py
│   ├── pipeline.py
│   ├── llm_service.py
│   ├── document_loader.py
│   ├── models.py
│   ├── config.py
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
├── docker-compose.yml
├── start_backend.bat
├── start_frontend.bat
└── README.md
```

Requirements
Install:
  - Python 3.11+
  - Ollama
  - Docker Desktop, optional

Pull the default model:
  - ollama pull llama3.1
** Make sure Ollama is running before starting the backend.

Running Locally
  - Backend
```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Backend URL:
    http://localhost:8000

  - Frontend
  Open a second terminal:
```
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```
Frontend URL:
    http://localhost:8501

Running With Docker
```
Before using Docker Compose, rename:
  backend/Dockerfile.txt -> backend/Dockerfile
  frontend/Dockerfile.txt -> frontend/Dockerfile
Then run:
  docker compose up --build
```
Services:
    Backend: http://localhost:8000
    Frontend: http://localhost:8501

The Docker setup expects Ollama to run on the host at:
    http://host.docker.internal:11434


API Endpoints
POST /analyze_jd_file
    - Uploads a PDF or DOCX job description and returns structured hiring criteria.
POST /evaluate_files
    - Uploads candidate resumes and evaluates them against criteria.
POST /rank
    - Ranks candidate evaluations by overall_score.
POST /pipeline
    - Runs the full pipeline from raw job description text and resume text.

Supported File Types
  - PDF
  - DOCX
    
Notes
    - Results depend on the selected Ollama model.
    - Candidate scores should support, not replace, human hiring decisions.
    - For production, add authentication, persistent storage, audit logs, stricter CORS, and stronger file security checks.

MIT License

  Copyright (c) 2026 CK
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
  
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.    
