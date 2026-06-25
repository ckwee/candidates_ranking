import logging
from typing import List, Dict

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import CriteriaSchema, EvaluationSchema, PipelineRequest, PipelineResponse
from document_loader import load_document_secure
from pipeline import analyze_jd, evaluate_candidates, rank_candidates

logging.basicConfig(level="INFO")
logger = logging.getLogger("backend")

app = FastAPI(title="AI Resume Screener Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze_jd_file", response_model=CriteriaSchema)
async def analyze_jd_file(jd_file: UploadFile = File(...)):
    text = load_document_secure(jd_file)
    return analyze_jd(text)

@app.post("/evaluate_files", response_model=List[EvaluationSchema])
async def evaluate_files(
    criteria: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    try:
        criteria_obj = CriteriaSchema.model_validate_json(criteria)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid criteria JSON: {e}")

    resume_texts = {}
    for f in resumes:
        text = load_document_secure(f)
        name = f.filename.rsplit(".", 1)[0]
        resume_texts[name] = text

    return evaluate_candidates(criteria_obj, resume_texts)

@app.post("/rank", response_model=List[EvaluationSchema])
async def rank_endpoint(evals: List[EvaluationSchema]):
    return rank_candidates(evals)

@app.post("/pipeline", response_model=PipelineResponse)
async def pipeline_endpoint(req: PipelineRequest):
    criteria = analyze_jd(req.job_description)
    evaluations = evaluate_candidates(criteria, req.resumes)
    ranking = rank_candidates(evaluations)
    return PipelineResponse(criteria=criteria, evaluations=evaluations, ranking=ranking)
